"""
Data Loader & Preprocessing for House Classification
King County Housing Dataset (Kaggle)
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

TARGET_TIERS = [
    "Affordable / Starter",
    "Mid-Range / Core Family",
    "Upper-Mid / Executive",
    "Luxury / Elite Estate"
]

def load_and_clean_data(csv_path: str = "data/kc_house_data.csv") -> pd.DataFrame:
    """
    Load data, clean known anomalies, and create target classification labels.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # 1. Handle known data anomalies:
    # Row with 33 bedrooms for 1620 sqft is a known typo (should be 3)
    df.loc[df["bedrooms"] == 33, "bedrooms"] = 3
    
    # Filter out records with 0 bedrooms or 0 bathrooms if unreasonable (< 0.1% of records)
    df = df[(df["bedrooms"] > 0) & (df["bathrooms"] > 0)].copy()

    # 2. Assign Classification Target: Market Tier
    # Tier 0: < $325,000
    # Tier 1: $325,000 - $500,000
    # Tier 2: $500,000 - $750,000
    # Tier 3: >= $750,000
    bins = [0, 325000, 500000, 750000, np.inf]
    df["target_class"] = pd.cut(
        df["price"],
        bins=bins,
        labels=[0, 1, 2, 3],
        right=False
    ).astype(int)
    
    df["target_label"] = df["target_class"].map(lambda x: TARGET_TIERS[x])
    
    return df

def get_train_test_data(csv_path: str = "data/kc_house_data.csv", test_size: float = 0.2, random_state: int = 42):
    """
    Split data strictly BEFORE preprocessing to avoid data leakage.
    """
    df = load_and_clean_data(csv_path)
    
    # Raw feature columns
    feature_cols = [
        "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
        "waterfront", "view", "condition", "grade", "sqft_above",
        "sqft_basement", "yr_built", "yr_renovated", "zipcode",
        "lat", "long", "sqft_living15", "sqft_lot15"
    ]
    
    X = df[feature_cols]
    y = df["target_class"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, df
