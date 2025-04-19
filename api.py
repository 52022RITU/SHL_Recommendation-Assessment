# FASTAPI BACKEND
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recommender import SHLRecommender

app = FastAPI(title="SHL Assessment Recommender API")
recommender = SHLRecommender()

class Query(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(query_data: Query):
    try:
        recommendations = recommender.get_recommendations(query_data.query)
        return {"recommended_assessments": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

















