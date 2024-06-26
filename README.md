# Resume_Parser_using_Claude


# Resume Parser API

This project provides an API to upload resumes in PDF format, parse them using Huggingface's transformers, and extract relevant information such as name, email, phone number, skills, experiences, education, certificates, and languages.

## Features

- Upload resumes in PDF format.
- Extracts and parses resume content using Huggingface transformers.
- Retrieves key information such as personal details, skills, experiences, education, and more.
- Provides endpoints for both file upload and URL-based resume fetching.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Huggingface Transformers
- Apache Tika
- Requests
- Jinja2Templates

## Installation

1. Clone the repository:

```bash
git clone https://github.com/roopdawg/Resume_Parser_using_Claude.git
cd Resume_Parser_using_Claude

```
2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
 pip install -r requirements.txt
```


4. Set up Apache Tika:
Download the Apache Tika server JAR file and place it in the APACHE_tika_server directory. Set the environment variables:
```bash
export TIKA_SERVER_JAR="APACHE_tika_server/tika-server.jar"
export TIKA_PATH="APACHE_tika_server/"
```


## Usage

Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

Access the endpoints:
- Home Page: http://localhost:8080/home/
- Airex Page: http://localhost:8080/airex/

### Endpoints

Upload Resume
- URL: /upload_resume
- Method: POST
- Params:
  pdf: PDF file of the resume.
  resume_service_url: URL of the resume PDF file.
- Response: JSON containing extracted information.

Example using curl:
```bash
curl -X POST "http://localhost:8080/upload_resume" -F "pdf=@path/to/resume.pdf"
```

Example with URL:

```bash
curl -X POST "http://localhost:8080/upload_resume" -F "resume_service_url=http://example.com/resume.pdf"
```

## Project Structure
- main.py: Main application file containing API endpoints.
- requirements.txt: List of Python packages required for the project.
- APACHE_tika_server/: Directory containing Apache Tika server JAR file.
Code Overview

The main.py file contains the following key components:
Imports: Required libraries and modules.
FastAPI App: Initializes the FastAPI application.
Endpoints:
- index: Serves the home page.
- upload_resume: Handles resume uploads and URL-based fetching.
Utility Functions:
- tika_function: Extracts text from PDF using Apache Tika.
- huggingface_parser: Parses the extracted text using Huggingface transformers.

## Planned Enhancements
- working on integrating Claude's API for more nuanced and contextual entity extraction
- Improve the error handling for various edge cases
- Extend the parser to handle additional entities and customizations as needed


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.




