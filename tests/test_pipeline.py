"""
Unit & Integration Tests for House Classification Pipeline
"""

import pytest
import numpy as np
import pandas as pd
from src.data_loader import load_and_clean_data, get_train_test_data, TARGET_TIERS
from src.feature_engineering import HouseFeatureTransformer
from src.predict import HouseClassifierPredictor

def test_data_loader_structure():
    X_train, X_test, y_train, y_test, df = get_train_test_data()
    assert len(X_train) > 10000
    assert len(X_test) > 2000
    assert len(y_train) == len(X_train)
    assert set(y_train.unique()) == {0, 1, 2, 3}

def test_feature_transformer():
    X_train, X_test, y_train, y_test, _ = get_train_test_data()
    transformer = HouseFeatureTransformer()
    X_train_scaled = transformer.fit_transform(X_train)
    X_test_scaled = transformer.transform(X_test)

    assert X_train_scaled.shape[1] == len(transformer.feature_names_)
    assert X_test_scaled.shape[1] == len(transformer.feature_names_)
    assert not np.isnan(X_train_scaled).any()
    assert not np.isnan(X_test_scaled).any()

def test_inference_predictor():
    predictor = HouseClassifierPredictor()
    sample = {
        'bedrooms': 3, 'bathrooms': 2.0, 'sqft_living': 1900, 'sqft_lot': 6000,
        'floors': 1.0, 'waterfront': 0, 'view': 0, 'condition': 3, 'grade': 7,
        'sqft_above': 1900, 'sqft_basement': 0, 'yr_built': 1990, 'yr_renovated': 0,
        'zipcode': 98058, 'lat': 47.4560, 'long': -122.1480,
        'sqft_living15': 1850, 'sqft_lot15': 5900
    }
    res = predictor.predict_single(sample)
    assert "predicted_class" in res
    assert res["predicted_class"] in [0, 1, 2, 3]
    assert res["predicted_tier"] in TARGET_TIERS
    assert 0.0 <= res["confidence"] <= 1.0
    assert len(res["class_probabilities"]) == 4

def test_batch_prediction():
    predictor = HouseClassifierPredictor()
    sample_df = pd.DataFrame([{
        'bedrooms': 3, 'bathrooms': 2.0, 'sqft_living': 1900, 'sqft_lot': 6000,
        'floors': 1.0, 'waterfront': 0, 'view': 0, 'condition': 3, 'grade': 7,
        'sqft_above': 1900, 'sqft_basement': 0, 'yr_built': 1990, 'yr_renovated': 0,
        'zipcode': 98058, 'lat': 47.4560, 'long': -122.1480,
        'sqft_living15': 1850, 'sqft_lot15': 5900
    }])
    result_df = predictor.predict_batch(sample_df)
    assert "predicted_tier" in result_df.columns
    assert "confidence" in result_df.columns
