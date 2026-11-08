"""
Feature Engineering and Transformation Pipeline
Adheres to strict ordering: fit on training data only, transform test/live data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, List

REFERENCE_YEAR = 2026

class HouseFeatureTransformer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names_: List[str] = []
        self.is_fitted = False

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates domain-specific real estate features.
        """
        df = df.copy()

        # Age and renovation features
        df["house_age"] = REFERENCE_YEAR - df["yr_built"]
        df["is_renovated"] = (df["yr_renovated"] > 0).astype(int)
        df["years_since_renovation"] = np.where(
            df["yr_renovated"] > 0,
            REFERENCE_YEAR - df["yr_renovated"],
            df["house_age"]
        )

        # Ratios & space utilization
        df["sqft_living_per_bed"] = df["sqft_living"] / (df["bedrooms"] + 0.5)
        df["bath_to_bed_ratio"] = df["bathrooms"] / (df["bedrooms"] + 0.5)
        df["living_to_lot_ratio"] = df["sqft_living"] / (df["sqft_lot"] + 1.0)
        df["has_basement"] = (df["sqft_basement"] > 0).astype(int)
        df["basement_ratio"] = df["sqft_basement"] / (df["sqft_living"] + 1.0)

        # Neighborhood comparison metrics
        df["living_vs_neighbors"] = df["sqft_living"] / (df["sqft_living15"] + 1.0)
        df["lot_vs_neighbors"] = df["sqft_lot"] / (df["sqft_lot15"] + 1.0)

        # Luxury & Quality Score
        df["luxury_score"] = (
            df["waterfront"] * 4.0 +
            df["view"] * 2.0 +
            (df["grade"] >= 10).astype(int) * 3.0 +
            (df["condition"] >= 4).astype(int) * 1.0
        )

        # Drop original raw year and temporary columns that shouldn't go directly to scaling
        drop_cols = ["yr_built", "yr_renovated"]
        df = df.drop(columns=[col for col in drop_cols if col in df.columns])

        return df

    def fit(self, X: pd.DataFrame):
        """
        Fit scaler strictly on training engineered features.
        """
        X_engineered = self.engineer_features(X)
        self.feature_names_ = list(X_engineered.columns)
        self.scaler.fit(X_engineered[self.feature_names_])
        self.is_fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform engineered features using fitted scaler.
        """
        if not self.is_fitted:
            raise RuntimeError("Transformer must be fitted before transforming data.")
        X_engineered = self.engineer_features(X)
        return self.scaler.transform(X_engineered[self.feature_names_])

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.fit(X).transform(X)
