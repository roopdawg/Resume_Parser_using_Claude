from typing import List, Dict, Any
from fastapi import FastAPI, Request, File, UploadFile, Form
import requests
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import uvicorn
import shutil
import os
import re
from transformers import pipeline
from tika import parser as tika_parser
from docx import Document
import json
import jsonschema
from dateutil import parser as dateparser
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

UPLOAD_FOLDER = "UPLOAD_FOLDER"
if not os.path.exists(UPLOAD_FOLDER): 
    os.makedirs(UPLOAD_FOLDER)

# Initialize Huggingface pipeline for entity recognition
nlp = pipeline("ner", model="dslim/bert-base-NER")

app = FastAPI()

@app.get('/home/', response_class=HTMLResponse)
async def index(request: Request):
    return "Welcome to the Resume Parser API"

@app.get('/airex/', response_class=HTMLResponse)
async def index(request: Request):
    return "Airex Page"

@app.post('/upload_resume', response_class=HTMLResponse)
def upload_resume(pdf: UploadFile = File(default=None), resume_service_url: str = Form(default="")):
    if pdf:
        filename = str(pdf.filename)
        file_ext = filename.split(".")[-1].lower()
        with open("UPLOAD_FOLDER/" + filename, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        if file_ext == "pdf":
            resume_text = tika_function(filename)
        elif file_ext == "docx":
            resume_text = docx_function(filename)
        else:
            return "Unsupported file format"
        
        json_data = huggingface_parser(resume_text)
        if json_data.get('email'):
            return json.dumps(json_data)
        else:
            email_rg = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
            email_list = re.findall(email_rg, resume_text.lower())
            if email_list:
                json_data['email'] = email_list[0]
            return json.dumps(json_data)

    elif resume_service_url:
        url = resume_service_url
        try:
            r = requests.get(url, allow_redirects=True)
            filename = "resume_document.pdf" if url.endswith(".pdf") else "resume_document.docx"
            open("UPLOAD_FOLDER/" + filename, "wb").write(r.content)
            r.close()
            if filename.endswith(".pdf"):
                resume_text = tika_function(filename)
            elif filename.endswith(".docx"):
                resume_text = docx_function(filename)
            else:
                return "Unsupported file format"
            
            json_data = huggingface_parser(resume_text)
            json_data['resume_service_url'] = url
            if json_data.get('email'):
                return json.dumps(json_data)
            else:
                email_rg = re.compile(r'[a-z0-9\.\-+_]+@[a.z0-9\.\-+_]+\.[a-z]+')
                email_list = re.findall(email_rg, resume_text.lower())
                if email_list:
                    json_data['email'] = email_list[0]
                return json.dumps(json_data)
        except:
            return "INVALID URL"
    else:
        return "Input Missing, Resume Document or Resume URL is Required for Processing"

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

def huggingface_parser(text: str) -> Dict[str, Any]:
    entities = nlp(text)
    response = {
        "name": "",
        "email": "",
        "phone_number": "",
        "skills": [],
        "experiences": [],
        "education": [],
        "certificates": [],
        "languages": [],
    }
    for entity in entities:
        entity_text = entity['word']
        entity_label = entity['entity']
        if entity_label in ["B-PER", "I-PER"]:
            response["name"] += " " + entity_text
        elif entity_label in ["B-EMAIL", "I-EMAIL"]:
            response["email"] += entity_text
        elif entity_label in ["B-PHONE", "I-PHONE"]:
            response["phone_number"] += entity_text
        elif entity_label in ["B-SKILL", "I-SKILL"]:
            response["skills"].append(entity_text)
        elif entity_label in ["B-EXP", "I-EXP"]:
            response["experiences"].append(entity_text)
        elif entity_label in ["B-EDU", "I-EDU"]:
            response["education"].append(entity_text)
        elif entity_label in ["B-CERT", "I-CERT"]:
            response["certificates"].append(entity_text)
        elif entity_label in ["B-LANG", "I-LANG"]:
            response["languages"].append(entity_text)
    return response

def parse_with_claude(text: str) -> Dict[str, Any]:
    # Use the Claude API to parse the text and extract additional information
    api_url = "https://api.anthropic.com/v1/claude"
    headers = {"Authorization": "Bearer YOUR_CLAUDE_API_KEY"}
    data = {"text": text}
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

def refine_parsed_data(parsed_data: Dict[str, Any], claude_data: Dict[str, Any]) -> Dict[str, Any]:
    # Refine and merge data from Huggingface and Claude
    final_response = parsed_data
    for key, value in claude_data.items():
        if key in final_response and isinstance(final_response[key], list):
            final_response[key].extend(value)
        else:
            final_response[key] = value
    return final_response

def validate_data(jsondata):
    resume_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "first_name": {"type": "string"},
            "middle_name": {"type": "string"},
            "last_name": {"type": "string"},
            "email": {"type": "string"},
            "title": {"type": "string"},
            "phone_number": {"type": "string"},
            "summary": {"type": "string"},
            "location": {"type": "string"},
            "school": {"type": "string"},
            "degree": {"type": "string"},
            "github_url": {"type": "string"},
            "linkedin_url": {"type": "string"},
            "links": {"type": "array"},
            "skills": {"type": "array"},
            "experiences": {"type": "array"},
            "education": {"type": "array"},
            "certificates": {"type": "array"},
            "languages": {"type": "array"},
        },
        "required": [
            'name', 'email', 'title', 'phone_number', 'summary', 'location',
            'school', 'degree', 'github_url', 'linkedin_url', 'links', 'skills',
            'experiences', 'education', 'certificates', 'languages'
        ]
    }
    try:
        jsonschema.validate(instance=jsondata, schema=resume_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)

