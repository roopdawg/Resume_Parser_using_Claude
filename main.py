from typing import List, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form
import requests
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import shutil
import os
import re
from tika import parser as tika_parser
from docx import Document
import json
import jsonschema
import logging
from transformers import AutoModel, AutoTokenizer
import torch
import faiss
import pinecone

app = FastAPI()

# Ensure the UPLOAD_FOLDER directory exists
UPLOAD_FOLDER = "UPLOAD_FOLDER"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FAISS index
dimension = 768  # Example dimension, should match your embedding model output
index = faiss.IndexFlatL2(dimension)

# Initialize Pinecone
pinecone.init(api_key="YOUR_PINECONE_API_KEY")
index_name = "resume-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=dimension)
pinecone_index = pinecone.Index(index_name)

# Initialize embedding model
class Embedder:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state[:, 0, :]
        return embeddings.numpy()

embedder = Embedder()

@app.post('/upload_resume', response_class=HTMLResponse)
def upload_resume(pdf: UploadFile = File(default=None), resume_service_url: str = Form(default="")):
    try:
        if pdf:
            filename = str(pdf.filename)
            file_ext = filename.split(".")[-1].lower()
            with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as buffer:
                shutil.copyfileobj(pdf.file, buffer)
            
            if file_ext == "pdf":
                resume_text = tika_function(filename)
            elif file_ext == "docx":
                resume_text = docx_function(filename)
            else:
                return "Unsupported file format"
            
            # Index resume in FAISS and Pinecone
            index_resume(filename, resume_text)
            return JSONResponse(content={"message": "Resume uploaded and indexed successfully."})

        elif resume_service_url:
            url = resume_service_url
            try:
                r = requests.get(url, allow_redirects=True)
                filename = "resume_document.pdf" if url.endswith(".pdf") else "resume_document.docx"
                with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as buffer:
                    buffer.write(r.content)
                r.close()
                
                if filename.endswith(".pdf"):
                    resume_text = tika_function(filename)
                elif filename.endswith(".docx"):
                    resume_text = docx_function(filename)
                else:
                    return "Unsupported file format"
                
                # Index resume in FAISS and Pinecone
                index_resume(filename, resume_text)
                return JSONResponse(content={"message": "Resume uploaded and indexed successfully."})
            except:
                return "INVALID URL"
        else:
            return "Input Missing, Resume Document or Resume URL is Required for Processing"
    except Exception as e:
        logging.error(f"Error processing resume: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

def tika_function(pdf_filename):
    if pdf_filename:
        parsed_doc = tika_parser.from_file('UPLOAD_FOLDER/' + str(pdf_filename))
        try:
            text = parsed_doc['content'].strip('\n')
            return text
        except:
            return 'No Valid file Selected!'

def docx_function(docx_filename):
    if docx_filename:
        doc = Document('UPLOAD_FOLDER/' + str(docx_filename))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

def index_resume(resume_id, resume_text):
    vector = embedder.embed(resume_text)
    faiss.normalize_L2(vector)
    index.add(vector)
    pinecone_index.upsert([(resume_id, vector.tolist())])

def search_resumes(query, top_k=5):
    query_vector = embedder.embed(query)
    faiss.normalize_L2(query_vector)
    D, I = index.search(query_vector, top_k)
    return I

def re_rank_with_claude(resumes, query):
    context = query + "\n\n" + "\n\n".join(resumes)
    return parse_with_claude(context)

def parse_with_claude(text):
    api_url = "https://api.anthropic.com/v1/claude"
    headers = {"Authorization": "Bearer YOUR_CLAUDE_API_KEY"}
    data = {"text": text}
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

@app.post('/search_resumes', response_class=JSONResponse)
def search_and_rank(query: str, top_k: int = 5):
    try:
        initial_results = search_resumes(query, top_k)
        resumes = [tika_function(f'resume_{i}.pdf') for i in initial_results]
        final_ranking = re_rank_with_claude(resumes, query)
        return JSONResponse(content=final_ranking)
    except Exception as e:
        logging.error(f"Error searching resumes: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
