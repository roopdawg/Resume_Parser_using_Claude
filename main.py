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

app = FastAPI()

# Ensure the UPLOAD_FOLDER directory exists
UPLOAD_FOLDER = "UPLOAD_FOLDER"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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
            
            # Use Claude for parsing
            claude_data = parse_with_claude(resume_text)
            return JSONResponse(content=claude_data)

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
                
                # Use Claude for parsing
                claude_data = parse_with_claude(resume_text)
                return JSONResponse(content=claude_data)
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

def parse_with_claude(text: str) -> Dict[str, Any]:
    # Use the Claude API to parse the text and extract additional information
    api_url = "https://api.anthropic.com/v1/claude"
    headers = {"Authorization": f"Bearer {os.getenv('CLAUDE_API_KEY')}"}
    data = {"text": text}
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
