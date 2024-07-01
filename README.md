# Resume Parser and Matcher

This project is a resume parsing and matching system using FastAPI, Apache Tika, and Claude. The system allows for uploading resumes in PDF or DOCX format, parsing their content, and storing them in a vector database for efficient retrieval and matching.

## Features

- **Resume Upload**: Supports PDF and DOCX resume uploads.
- **Parsing with Claude**: Utilizes the Claude API for extracting structured data from resumes.
- **Vector Storage with Pinecone**: Stores resume vectors for efficient similarity search.
- **Query Matching**: Retrieves top matching resumes based on job descriptions or candidate queries.

## Prerequisites

- Python 3.9 or higher
- FastAPI
- Uvicorn
- Apache Tika
- Pinecone
- Requests
- Docx
- JSONSchema

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Resume_Parser_and_Matcher.git
   cd Resume_Parser_and_Matcher
   ```


2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

# once you create the environment and activate it, you don't need to create it again 



3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:

Create a .env file in the project root directory with the following content:
CLAUDE_API_KEY=your_claude_api_key
PINECONE_API_KEY=your_pinecone_api_key


5. **Ensure Tika Server is Running:
Download the Tika server jar from the Apache Tika website and run it:
java -jar tika-server-1.24.jar


6. **un the FastAPI Application**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```

#Usage

Uploading Resumes
Endpoint: /upload_resume
Method: POST
Parameters:
pdf: Upload a PDF or DOCX file.
resume_service_url: (Optional) URL to a resume document.
Querying Resumes
Endpoint: /query_resumes
Method: POST
Parameters:
query: The job description or candidate query text.
Example
Upload a Resume:

```bash
curl -X POST "http://localhost:8080/upload_resume" -F "pdf=@/path/to/your/resume.pdf"
```

Query Resumes:

```bash
curl -X POST "http://localhost:8080/query_resumes" -H "Content-Type: application/json" -d '{"query": "Looking for a software engineer with experience in Python and machine learning"}'
```

# Code Structure
main.py: Contains the FastAPI application and endpoints.
requirements.txt: Lists all the required Python packages.
UPLOAD_FOLDER/: Directory where uploaded resumes are stored.

## Choosing a Vector Database
Pinecone vs. FAISS vs. Chroma DB
###Pinecone:
Fully managed, scalable, and optimized for high-performance vector search.
Best for cloud-based applications where scalability and ease of use are crucial.

###FAISS:
Open-source library optimized for efficient similarity search.
Best for local deployments or when you need full control over the infrastructure.

###Chroma DB:
An open-source database focusing on vector embeddings and retrieval.
Suitable for projects that prefer open-source solutions and need a specialized vector database.

###Storing Private Data in a Vector Database
Data is encrypted both in transit and at rest.
Access controls are in place to restrict unauthorized access.
