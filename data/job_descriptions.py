import os
import requests
import json

# URL of the FastAPI server
api_url = "http://localhost:8080/upload_JD"

# Directory containing the resume PDF files
# text Roopa to get this test resume directory shared to you and replace it with your downloaded directory path
resume_dir = "/Users/sreeroopasom/Documents/JDBank"

# Loop through each file in the job description directory
for filename in os.listdir(jd_dir):
    if filename.endswith(".pdf"):
        file_path = os.path.join(jd_dir, filename)
        with open(file_path, "rb") as file:
            files = {"pdf": file}
            response = requests.post(api_url, files=files)
            if response.status_code == 200:
                print(f"Results for {filename}:")
                print(json.dumps(response.json(), indent=4))
            else:
                print(f"Failed to process {filename}: {response.status_code}")
