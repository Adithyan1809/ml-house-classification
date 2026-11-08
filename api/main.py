"""
FastAPI REST API for Real Estate Market Tier Classification
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import pandas as pd
import json
import os

from src.predict import HouseClassifierPredictor, METRICS_PATH

app = FastAPI(
    title="House Market Tier Classification API",
    description="Machine Learning Service predicting real estate market tiers and valuation segments.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = None

def get_predictor():
    global predictor
    if predictor is None:
        predictor = HouseClassifierPredictor()
    return predictor

class HouseFeatures(BaseModel):
    bedrooms: int = Field(..., ge=1, le=20, example=4)
    bathrooms: float = Field(..., ge=0.5, le=15.0, example=2.5)
    sqft_living: int = Field(..., ge=200, le=20000, example=2500)
    sqft_lot: int = Field(..., ge=200, le=1000000, example=7500)
    floors: float = Field(..., ge=1.0, le=4.0, example=2.0)
    waterfront: int = Field(0, ge=0, le=1, example=0)
    view: int = Field(0, ge=0, le=4, example=1)
    condition: int = Field(3, ge=1, le=5, example=4)
    grade: int = Field(7, ge=1, le=13, example=8)
    sqft_above: int = Field(..., ge=200, le=15000, example=2000)
    sqft_basement: int = Field(0, ge=0, le=10000, example=500)
    yr_built: int = Field(..., ge=1900, le=2026, example=1995)
    yr_renovated: int = Field(0, ge=0, le=2026, example=0)
    zipcode: int = Field(..., example=98052)
    lat: float = Field(..., example=47.65)
    long: float = Field(..., example=-122.12)
    sqft_living15: int = Field(..., ge=200, le=20000, example=2400)
    sqft_lot15: int = Field(..., ge=200, le=1000000, example=7200)

class PredictionResponse(BaseModel):
    predicted_class: int
    predicted_tier: str
    confidence: float
    estimated_price_range: str
    class_probabilities: Dict[str, float]

@app.get("/")
def root():
    return {
        "service": "House Market Tier Classification API",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}

@app.get("/model/metrics")
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="Metrics artifact not found")
    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)
    return metrics

@app.post("/predict", response_model=PredictionResponse)
def predict(features: HouseFeatures):
    try:
        engine = get_predictor()
        res = engine.predict_single(features.model_dump())
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-batch")
def predict_batch(properties: List[HouseFeatures]):
    try:
        engine = get_predictor()
        df = pd.DataFrame([p.model_dump() for p in properties])
        result_df = engine.predict_batch(df)
        return result_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
