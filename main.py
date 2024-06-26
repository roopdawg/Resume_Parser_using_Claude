from typing import List, Dict, Any
from fastapi import FastAPI, Request, File, UploadFile, Form
import requests
from fastapi.responses import HTMLResponse
import uvicorn
import shutil
import os
from transformers import pipeline
from tika import parser

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
        with open("UPLOAD_FOLDER/" + filename, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        resume_text = tika_function(filename)
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
            filename = "resume_document.pdf"
            open("UPLOAD_FOLDER/" + filename, "wb").write(r.content)
            r.close()
            resume_text = tika_function(filename)
            json_data = huggingface_parser(resume_text)
            json_data['resume_service_url'] = url
            if json_data.get('email'):
                return json.dumps(json_data)
            else:
                email_rg = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
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
        parsed_doc = parser.from_file('UPLOAD_FOLDER/' + str(pdf_filename), service="text")
        try:
            text = parsed_doc['content'].strip('\n')
            return text
        except:
            return 'No Valid file Selected!'

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
        if entity_label == "B-PER" or entity_label == "I-PER":
            response["name"] += " " + entity_text
        elif entity_label == "B-EMAIL" or entity_label == "I-EMAIL":
            response["email"] += entity_text
        elif entity_label == "B-PHONE" or entity_label == "I-PHONE":
            response["phone_number"] += entity_text
        elif entity_label == "B-SKILL" or entity_label == "I-SKILL":
            response["skills"].append(entity_text)
        elif entity_label == "B-EXP" or entity_label == "I-EXP":
            response["experiences"].append(entity_text)
        elif entity_label == "B-EDU" or entity_label == "I-EDU":
            response["education"].append(entity_text)
        elif entity_label == "B-CERT" or entity_label == "I-CERT":
            response["certificates"].append(entity_text)
        elif entity_label == "B-LANG" or entity_label == "I-LANG":
            response["languages"].append(entity_text)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
