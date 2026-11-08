"""
Model Training and Comparison Pipeline
Trains Baseline Logistic Regression, Random Forest, and XGBoost.
Evaluates metrics, saves artifacts, confusion matrices, and selects the best model.
"""

import os
import json
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from sklearn.model_selection import cross_val_score

from src.data_loader import get_train_test_data, TARGET_TIERS
from src.feature_engineering import HouseFeatureTransformer

def train_and_evaluate():
    print("=== Step 1: Loading & Splitting Data ===")
    X_train, X_test, y_train, y_test, full_df = get_train_test_data()
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    print("\n=== Step 2: Feature Engineering & Preprocessing ===")
    transformer = HouseFeatureTransformer()
    X_train_scaled = transformer.fit_transform(X_train)
    X_test_scaled = transformer.transform(X_test)
    print(f"Features created ({len(transformer.feature_names_)}): {transformer.feature_names_}")

    models = {
        "Logistic Regression (Baseline)": LogisticRegression(
            max_iter=1000, multi_class="multinomial", random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150, max_depth=16, min_samples_split=4, n_jobs=-1, random_state=42
        ),
        "XGBoost": XGBClassifier(
            n_estimators=180, max_depth=6, learning_rate=0.08,
            subsample=0.85, colsample_bytree=0.85, eval_metric="mlogloss",
            random_state=42, n_jobs=-1
        )
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model = None

    print("\n=== Step 3: Model Training & Evaluation ===")
    for name, model in models.items():
        print(f"\n--> Training {name}...")
        start_train = time.time()
        model.fit(X_train_scaled, y_train)
        train_time = time.time() - start_train

        # Cross Validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="f1_macro", n_jobs=-1)
        cv_mean = float(np.mean(cv_scores))

        # Prediction & Latency
        start_inf = time.time()
        y_pred = model.predict(X_test_scaled)
        inference_latency_ms = ((time.time() - start_inf) / len(X_test)) * 1000

        acc = float(accuracy_score(y_test, y_pred))
        prec_macro = float(precision_score(y_test, y_pred, average="macro"))
        rec_macro = float(recall_score(y_test, y_pred, average="macro"))
        f1_macro = float(f1_score(y_test, y_pred, average="macro"))
        f1_weighted = float(f1_score(y_test, y_pred, average="weighted"))
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": round(acc, 4),
            "precision_macro": round(prec_macro, 4),
            "recall_macro": round(rec_macro, 4),
            "f1_macro": round(f1_macro, 4),
            "f1_weighted": round(f1_weighted, 4),
            "cv_f1_macro_mean": round(cv_mean, 4),
            "train_time_sec": round(train_time, 3),
            "latency_ms_per_sample": round(inference_latency_ms, 4),
            "confusion_matrix": cm,
        }

        print(f"    Accuracy: {acc:.4f} | Macro F1: {f1_macro:.4f} | 5-Fold CV: {cv_mean:.4f}")

        if f1_macro > best_f1:
            best_f1 = f1_macro
            best_model_name = name
            best_model = model

    print(f"\n==========================================")
    print(f" BEST PERFORMING MODEL: {best_model_name} (Macro F1 = {best_f1:.4f})")
    print(f"==========================================")

    # Save artifacts in models/
    os.makedirs("models", exist_ok=True)
    
    # Save best model and transformer
    joblib.dump(best_model, "models/best_model.pkl")
    joblib.dump(transformer, "models/transformer.pkl")
    
    # Extract feature importances if tree-based
    feature_importances = {}
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
        feature_importances = {
            feat: round(float(imp), 4)
            for feat, imp in sorted(zip(transformer.feature_names_, importances), key=lambda x: x[1], reverse=True)
        }

    summary = {
        "best_model_name": best_model_name,
        "best_metrics": results[best_model_name],
        "all_models": results,
        "feature_importances": feature_importances,
        "target_tiers": TARGET_TIERS,
        "num_train_samples": len(X_train),
        "num_test_samples": len(X_test),
        "feature_names": transformer.feature_names_
    }

    with open("models/metrics.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open("models/feature_names.json", "w") as f:
        json.dump(transformer.feature_names_, f, indent=2)

    with open("models/class_labels.json", "w") as f:
        json.dump(TARGET_TIERS, f, indent=2)

    print(" Artifacts successfully saved to models/")
    return summary

if __name__ == "__main__":
    train_and_evaluate()
