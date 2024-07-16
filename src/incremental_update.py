import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from data_preprocessing import preprocess_text

# Load the existing model
pipeline = joblib.load('model/initial_model.joblib')

# Function to update model incrementally
def update_model(new_texts, new_labels):
    pipeline.named_steps['sgdclassifier'].partial_fit(
        pipeline.named_steps['tfidfvectorizer'].transform(new_texts), 
        new_labels, 
        classes=np.unique(new_labels)
    )
    joblib.dump(pipeline, 'model/updated_model.joblib')

# Example new data
new_texts = ["Example new resume text"]
new_labels = [1]  # Corresponding label

# Update the model with new data
update_model(new_texts, new_labels)
