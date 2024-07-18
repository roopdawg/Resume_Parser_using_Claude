# AI Recruiter

## Overview

The AI Recruiter project leverages state-of-the-art Natural Language Processing (NLP) techniques to match resumes to job descriptions. The system uses a combination of BM25 for initial candidate retrieval, FAISS for semantic similarity, and Anthropic's Claude for interacting with the user (user query in natural language) and showing the criteria that the candidate does/doesn't match on. The model is fine-tuned iteratively with recruiter feedback to continuously improve its performance.

## Methodology

### Initial Candidate Retrieval

1. **BM25 Retrieval**: 
   - Uses BM25 algorithm to rank candidates based on the textual relevance of resumes to the job description.
   - Provides an initial set of candidate matches.

2. **FAISS Retrieval**:
   - Generates embeddings for resumes and job descriptions + notes using a pre-trained BERT model.
   - Uses FAISS (Facebook AI Similarity Search) to perform vector-based similarity search, refining the initial BM25 results.

### Feature Extraction

- **Anthropic's Claude**:
  - Interacts with the user to obtain the ideal candidate query in natural language + job description upload
  - Provides a comprehensive understanding of each candidate's qualifications.
  - TODO:  Enhances candidate profiles by extracting detailed features such as skills, job titles, experience, education, and specific requirements from the job description uploaded

### Fine-Tuning with Feedback

- **Recruiter Feedback**:
  - Collects real-time feedback from recruiters on the quality of matches.
  - Fine-tunes the model periodically with the collected feedback to adapt to changing hiring criteria and preferences.

## Setup

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Resume_Parser_and_Matcher.git
   cd Resume_Parser_and_Matcher
   ```

2. **Create a Virtual Environment**:
   ```bash
    python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

# once you create the environment and activate it, you don't need to create it again 


3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

##API Endpoints

/match
Method: POST
Description: Retrieve top matching resumes based on a job query.
Request Body:

```json

{
  "query": "Senior Software Engineer with Python experience"
}
```
Response:
```json
Copy code
{
  "matches": ["Resume 1", "Resume 2", ...]
}
``` 
##/extract_features
Method: POST
Description: Extract features from a given text using Claude.
Request Body:
```json
{
  "text": "Resume text here",
  "context_type": "resume"
}
```
Response:
```json
{
  "Skills": [...],
  "Job Titles": [...],
  "Experience": [...],
  "Education": [...],
  "Specific Requirements": [...]
}
```


##Fine-Tuning - To fine-tune the model with recruiter feedback:
Prepare the training data with recruiter feedback.
Run the fine-tuning script:
```bash
python finetuning.py
```
The fine-tuned model and tokenizer will be saved in the ./fine_tuned_model directory.



##Docker

Build the Docker image:
```bash
docker build -t ai-recruiter . 
```
Run the Docker container:
```bash
docker run -p 8000:8000 ai-recruiter
```


##Contributing
If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.
