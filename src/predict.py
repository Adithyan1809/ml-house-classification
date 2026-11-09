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

    def explain_prediction(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates Tree SHAP feature contributions for explainability.
        """
        df = pd.DataFrame([property_data])
        X_scaled = self.transformer.transform(df)
        pred_class = int(self.model.predict(X_scaled)[0])

        friendly_names = {
            "grade": "Construction Quality Grade",
            "lat": "Geographic Latitude (Neighborhood Desirability)",
            "long": "Longitude Coordinate",
            "sqft_living": "Interior Living Area (sqft)",
            "sqft_living_per_bed": "Space Density (sqft per Bedroom)",
            "luxury_score": "Luxury Score (Waterfront + View + High Grade)",
            "waterfront": "Waterfront Shoreline Access",
            "view": "Panoramic View Rating",
            "condition": "Overall Property Condition",
            "house_age": "Property Age",
            "bathrooms": "Bathroom Count",
            "bedrooms": "Bedroom Count",
            "zipcode": "Postal ZIP Code",
            "sqft_lot": "Lot Parcel Size",
            "sqft_above": "Above-Ground Living Area",
            "living_vs_neighbors": "Size Relative to Immediate Neighbors"
        }

        try:
            if hasattr(self.model, "get_booster"):
                import xgboost as xgb
                booster = self.model.get_booster()
                dmatrix = xgb.DMatrix(X_scaled, feature_names=self.transformer.feature_names_)
                contribs = booster.predict(dmatrix, pred_contribs=True)

                # Factors pulling down from Luxury tier (class 3)
                lux_c_vals = contribs[0, 3, :-1]
                lux_draggers = []
                for name, val in zip(self.transformer.feature_names_, lux_c_vals):
                    if val < -0.10:
                        lux_draggers.append({
                            "feature": friendly_names.get(name, name),
                            "raw_name": name,
                            "impact": round(float(val), 3)
                        })
                lux_draggers = sorted(lux_draggers, key=lambda x: x["impact"])[:4]

                # Top positive factors for predicted class
                pred_c_vals = contribs[0, pred_class, :-1]
                top_pos = []
                for name, val in zip(self.transformer.feature_names_, pred_c_vals):
                    if val > 0.05:
                        top_pos.append({
                            "feature": friendly_names.get(name, name),
                            "raw_name": name,
                            "impact": round(float(val), 3)
                        })
                top_pos = sorted(top_pos, key=lambda x: x["impact"], reverse=True)[:3]

                return {
                    "top_drivers": top_pos,
                    "luxury_draggers": lux_draggers
                }
        except Exception:
            pass

        return {"top_drivers": [], "luxury_draggers": []}

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
