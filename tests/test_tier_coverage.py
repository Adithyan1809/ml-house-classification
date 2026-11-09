import pytest
from src.predict import HouseClassifierPredictor

def test_all_four_market_tiers_reachable():
    engine = HouseClassifierPredictor()

    test_cases = [
        ("Affordable / Starter", {
            "bedrooms": 3, "bathrooms": 1.0, "sqft_living": 1150, "sqft_lot": 5500,
            "floors": 1.0, "waterfront": 0, "view": 0, "condition": 3, "grade": 6,
            "sqft_above": 1150, "sqft_basement": 0, "yr_built": 1978, "yr_renovated": 0,
            "zipcode": 98003, "lat": 47.3100, "long": -122.3120, "sqft_living15": 1200, "sqft_lot15": 5500
        }),
        ("Mid-Range / Core Family", {
            "bedrooms": 3, "bathrooms": 2.0, "sqft_living": 1750, "sqft_lot": 7200,
            "floors": 1.0, "waterfront": 0, "view": 0, "condition": 3, "grade": 7,
            "sqft_above": 1750, "sqft_basement": 0, "yr_built": 1988, "yr_renovated": 0,
            "zipcode": 98058, "lat": 47.4560, "long": -122.1480, "sqft_living15": 1750, "sqft_lot15": 7200
        }),
        ("Upper-Mid / Executive", {
            "bedrooms": 4, "bathrooms": 2.5, "sqft_living": 2350, "sqft_lot": 7500,
            "floors": 2.0, "waterfront": 0, "view": 0, "condition": 3, "grade": 8,
            "sqft_above": 2350, "sqft_basement": 0, "yr_built": 1995, "yr_renovated": 0,
            "zipcode": 98052, "lat": 47.6740, "long": -122.1215, "sqft_living15": 2350, "sqft_lot15": 7500
        }),
        ("Luxury / Elite Estate", {
            "bedrooms": 5, "bathrooms": 4.0, "sqft_living": 4200, "sqft_lot": 14000,
            "floors": 2.0, "waterfront": 1, "view": 3, "condition": 4, "grade": 11,
            "sqft_above": 3200, "sqft_basement": 1000, "yr_built": 2012, "yr_renovated": 0,
            "zipcode": 98004, "lat": 47.6200, "long": -122.2150, "sqft_living15": 3800, "sqft_lot15": 12000
        })
    ]

    for expected_tier, payload in test_cases:
        res = engine.predict_single(payload)
        assert res["predicted_tier"] == expected_tier, (
            f"Expected {expected_tier}, but got {res['predicted_tier']} with confidence {res['confidence']}"
        )
