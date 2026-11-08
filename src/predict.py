"""
Inference Engine for House Classification
Loads trained model and transformer pipeline for single and batch predictions.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")
TRANSFORMER_PATH = os.path.join(MODELS_DIR, "transformer.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")

class HouseClassifierPredictor:
    def __init__(self, model_path: str = MODEL_PATH, transformer_path: str = TRANSFORMER_PATH):
        if not os.path.exists(model_path) or not os.path.exists(transformer_path):
            raise FileNotFoundError(f"Model or Transformer artifact missing in {MODELS_DIR}. Run training first.")

        self.model = joblib.load(model_path)
        self.transformer = joblib.load(transformer_path)

        with open(METRICS_PATH, "r") as f:
            self.metadata = json.load(f)

        self.target_tiers = self.metadata["target_tiers"]

    def predict_single(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts raw dictionary of property features and returns predicted tier,
        probabilities, and price guidance.
        """
        df = pd.DataFrame([property_data])
        X_scaled = self.transformer.transform(df)

        pred_class = int(self.model.predict(X_scaled)[0])
        probabilities = self.model.predict_proba(X_scaled)[0].tolist()

        tier_name = self.target_tiers[pred_class]
        
        # Price benchmarks corresponding to classes
        price_ranges = {
            "Affordable / Starter": "Under $325,000",
            "Mid-Range / Core Family": "$325,000 - $500,000",
            "Upper-Mid / Executive": "$500,000 - $750,000",
            "Luxury / Elite Estate": "$750,000 and above"
        }

        prob_breakdown = {
            self.target_tiers[i]: round(float(prob), 4)
            for i, prob in enumerate(probabilities)
        }

        return {
            "predicted_class": pred_class,
            "predicted_tier": tier_name,
            "confidence": round(float(probabilities[pred_class]), 4),
            "estimated_price_range": price_ranges[tier_name],
            "class_probabilities": prob_breakdown
        }

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Accepts dataframe of properties and appends prediction columns.
        """
        X_scaled = self.transformer.transform(df)
        preds = self.model.predict(X_scaled)
        probas = self.model.predict_proba(X_scaled)

        result_df = df.copy()
        result_df["predicted_class"] = preds
        result_df["predicted_tier"] = [self.target_tiers[p] for p in preds]
        result_df["confidence"] = [round(float(probas[i][p]), 4) for i, p in enumerate(preds)]
        return result_df
