import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
from data_preprocessing import preprocess_text, load_and_preprocess_data

# Load and preprocess data
data = load_and_preprocess_data('data/resumes.csv')
texts = data['cleaned_text'].tolist()
labels = data['label'].tolist()  # Assuming 'label' is a column in your dataset

# Create a text classification pipeline with TF-IDF and SGDClassifier
pipeline = make_pipeline(TfidfVectorizer(), SGDClassifier(loss='log'))

# Fit the initial model
pipeline.fit(texts, labels)

# Save the trained model
import joblib
joblib.dump(pipeline, 'model/initial_model.joblib')
