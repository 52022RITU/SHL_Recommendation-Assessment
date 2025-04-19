# RECOMMENDATION LOGIC
# recommender.py (updated)
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import os

class SHLRecommender:
    def __init__(self):
        self.embeddings = np.load("data/assessment_embeddings.npy", allow_pickle=True)
        self.assessments = pd.read_csv("data/processed_assessments.csv")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Use environment variable

    def get_recommendations(self, query, max_results=10):
        query_embedding = self.model.encode([query])[0]
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )  # Fixed parenthesis
        
        top_indices = np.argsort(similarities)[::-1][:max_results]
        top_assessments = self.assessments.iloc[top_indices]
        
        assessment_list = top_assessments['description'].tolist()
        context = "\n".join(assessment_list)
        
        prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""
            Given the following query: {query}
            And these potential assessments:
            {context}
            Rank these assessments by relevance to the query and explain why they are relevant.
            """
        )
        refined_response = self.llm(prompt.format(query=query, context=context))
        
        results = []
        for _, row in top_assessments.iterrows():
            results.append({
                "url": row['url'],
                "adaptive_support": "Yes" if row['adaptive_support'] == 1 else "No",
                "description": row['description'],
                "duration": row['duration'],
                "remote_support": "Yes" if row['remote_support'] == 1 else "No",
                "test_type": row['test_type'].split(',')
            })
        return results
