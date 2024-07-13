from flask import Flask, request, jsonify
from data_preprocessing import preprocess_text, load_and_preprocess_data
from bm25_retrieval import bm25_retrieval
from faiss_retrieval import FAISSRetrieval
from feature_extraction import extract_features_with_claude

app = Flask(__name__)

# Load and preprocess resumes and job descriptions
resumes = load_and_preprocess_data('data/resumes.csv')['cleaned_text'].tolist()
job_descriptions = load_and_preprocess_data('data/job_descriptions.csv')['cleaned_text'].tolist()

faiss_retrieval = FAISSRetrieval()
faiss_index, _ = faiss_retrieval.build_index(resumes)

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    query = preprocess_text(data.get('query', ''))

    # BM25 Retrieval
    bm25_indices, bm25_scores = bm25_retrieval(query, resumes)

    # FAISS Retrieval
    faiss_indices, faiss_distances = faiss_retrieval.search(query, faiss_index)

    # Combine BM25 and FAISS results
    combined_results = set(bm25_indices).union(set(faiss_indices))
    combined_scores = {idx: (bm25_scores[idx] if idx in bm25_indices else 0) + (1/faiss_distances[idx] if idx in faiss_indices else 0) for idx in combined_results}

    sorted_results = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)
    top_matches = [resumes[idx] for idx, _ in sorted_results[:10]]

    return jsonify(top_matches)

@app.route('/extract_features', methods=['POST'])
def extract_features():
    data = request.json
    text = data.get('text', '')
    context_type = data.get('context_type', 'resume')
    features = extract_features_with_claude(text, context_type)
    return jsonify(features)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

