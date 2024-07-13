from rank_bm25 import BM25Okapi
import numpy as np

def bm25_retrieval(query, documents, top_n=10):
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    top_n_indices = np.argsort(scores)[-top_n:]
    return top_n_indices, scores[top_n_indices]

