import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Create sample data if the CSV doesn't exist
if not os.path.exists('data/processed_assessments.csv'):
    print("Creating sample assessment data...")
    sample_data = [
        {'name': 'SHL Verify G+', 'description': 'Cognitive ability test for graduate and professional roles', 'url': 'https://www.shl.com/verify-g-plus', 'duration': 45, 'remote_support': 'Yes', 'adaptive_support': 'Yes', 'test_type': 'Cognitive'},
        {'name': 'OPQ32 Personality', 'description': 'Comprehensive personality assessment for all levels', 'url': 'https://www.shl.com/opq32', 'duration': 30, 'remote_support': 'Yes', 'adaptive_support': 'No', 'test_type': 'Personality'},
        {'name': 'SHL Verify Numerical', 'description': 'Tests ability to analyze numerical data', 'url': 'https://www.shl.com/verify-numerical', 'duration': 25, 'remote_support': 'Yes', 'adaptive_support': 'Yes', 'test_type': 'Cognitive'},
        {'name': 'SHL Verify Verbal', 'description': 'Tests ability to analyze written information', 'url': 'https://www.shl.com/verify-verbal', 'duration': 20, 'remote_support': 'Yes', 'adaptive_support': 'Yes', 'test_type': 'Cognitive'},
        {'name': 'SHL Verify Coding', 'description': 'Technical assessment for programming skills', 'url': 'https://www.shl.com/verify-coding', 'duration': 40, 'remote_support': 'Yes', 'adaptive_support': 'No', 'test_type': 'Technical'},
    ]
    df = pd.DataFrame(sample_data)
    df.to_csv('data/processed_assessments.csv', index=False)
    print("Sample data created successfully!")
else:
    print("Using existing processed_assessments.csv file")

# Load the processed assessments
df = pd.read_csv('data/processed_assessments.csv')
print(f"Loaded {len(df)} assessments")

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully")

# Generate embeddings from the description column
# Combine name and description for better context
texts = df['name'] + ": " + df['description'].astype(str)
embeddings = model.encode(texts, show_progress_bar=True)

# Save the embeddings
np.save('data/assessment_embeddings.npy', embeddings)
print(f"Embeddings shape: {embeddings.shape}")  # Should be (num_assessments, 384)
print("Embeddings saved successfully to data/assessment_embeddings.npy")
