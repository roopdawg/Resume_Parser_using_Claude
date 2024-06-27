import os
import requests
import json

# URL of the FastAPI server
api_url = "http://localhost:8080/upload_resume"

# Directory containing the resume PDF files
resume_dir = "/Users/sreeroopasom/Documents/ResumeBank"

# Loop through each file in the resume directory
for filename in os.listdir(resume_dir):
    if filename.endswith(".pdf"):
        file_path = os.path.join(resume_dir, filename)
        with open(file_path, "rb") as file:
            files = {"pdf": file}
            response = requests.post(api_url, files=files)
            if response.status_code == 200:
                print(f"Results for {filename}:")
                print(json.dumps(response.json(), indent=4))
            else:
                print(f"Failed to process {filename}: {response.status_code}")
