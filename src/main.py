from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from data_preprocessing import preprocess_text, load_and_preprocess_data
from bm25_retrieval import bm25_retrieval
from faiss_retrieval import FAISSRetrieval
from feature_extraction import extract_features_with_claude
import uvicorn

app = FastAPI()

class MatchRequest(BaseModel):
    query: str

class FeatureRequest(BaseModel):
    text: str
    context_type: str = 'resume'

# Load and preprocess resumes and job descriptions
resumes = load_and_preprocess_data('data/resumes.csv')['cleaned_text'].tolist()
job_descriptions = load_and_preprocess_data('data/job_descriptions.csv')['cleaned_text'].tolist()

faiss_retrieval = FAISSRetrieval()
faiss_index, _ = faiss_retrieval.build_index(resumes)

@app.post("/match")
async def match(request: MatchRequest):
    query = preprocess_text(request.query)

    # BM25 Retrieval
    bm25_indices, bm25_scores = bm25_retrieval(query, resumes)

    # FAISS Retrieval
    faiss_indices, faiss_distances = faiss_retrieval.search(query, faiss_index)

    # Combine BM25 and FAISS results
    combined_results = set(bm25_indices).union(set(faiss_indices))
    combined_scores = {idx: (bm25_scores[idx] if idx in bm25_indices else 0) + (1/faiss_distances[idx] if idx in faiss_indices else 0) for idx in combined_results}

    sorted_results = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)
    top_matches = [resumes[idx] for idx, _ in sorted_results[:10]]

    return {"matches": top_matches}

@app.post("/extract_features")
async def extract_features(request: FeatureRequest):
    features = extract_features_with_claude(request.text, request.context_type)
    return features

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
