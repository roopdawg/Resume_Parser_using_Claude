import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel

class FAISSRetrieval:
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def text_to_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()

    def build_index(self, documents):
        embeddings = np.array([self.text_to_embedding(doc) for doc in documents])
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        return index, embeddings

    def search(self, query, index, top_n=10):
        query_embedding = self.text_to_embedding(query)
        distances, indices = index.search(query_embedding, top_n)
        return indices[0], distances[0]
