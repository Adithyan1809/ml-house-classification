# 🏰 EstateClassify AI: Real Estate Market Tier Classification

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-XGBoost%20%7C%20Scikit--Learn-orange.svg)](https://xgboost.readthedocs.io/)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit%20Dark%20Glassmorphism-red.svg)](https://streamlit.io/)
[![Cloud](https://img.shields.io/badge/Cloud-AWS%20EC2%20%26%20Docker-FF9900.svg)](https://aws.amazon.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green.svg)](https://github.com/)

An end-to-end Machine Learning production system that classifies residential properties into market valuation segments and economic tiers using the Kaggle King County Real Estate dataset. Features automated feature engineering, multi-model evaluation, a modern glassmorphic Streamlit UI, a FastAPI microservice, Docker containerization, and AWS deployment automation.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Dataset & Target Formulation](#-dataset--target-formulation)
3. [Architecture & Pipeline](#-architecture--pipeline)
4. [Machine Learning Experiments & Benchmarks](#-machine-learning-experiments--benchmarks)
5. [Frontend & User Experience](#-frontend--user-experience)
6. [API Specifications](#-api-specifications)
7. [Local Setup & Execution](#-local-setup--execution)
8. [Docker Containerization](#-docker-containerization)
9. [AWS Cloud Deployment](#-aws-cloud-deployment)
10. [Automated CI/CD Pipeline](#-automated-cicd-pipeline)

---

## 🎯 Project Overview

In residential real estate and mortgage analytics, predicting continuous price often misses categorical strategic decisions such as portfolio grouping, risk stratification, and buyer segment matching.

**EstateClassify AI** classifies houses into four distinct market segments:
- **Affordable / Starter**: Entry-level starter homes (< $325,000)
- **Mid-Range / Core Family**: Standard suburban single-family homes ($325,000 – $500,000)
- **Upper-Mid / Executive**: High-end properties in desirable neighborhoods ($500,000 – $750,000)
- **Luxury / Elite Estate**: Premier luxury estates, waterfronts, and architectural masterpieces (≥ $750,000)

---

## 📊 Dataset & Target Formulation

- **Source**: Kaggle King County House Sales (`harlfoxem/housesalesprediction`)
- **Volume**: 21,613 property records
- **Geographic Scope**: King County, Washington (Seattle, Bellevue, Redmond, Kirkland, Mercer Island, etc.)
- **Raw Features**: `bedrooms`, `bathrooms`, `sqft_living`, `sqft_lot`, `floors`, `waterfront`, `view`, `condition`, `grade`, `sqft_above`, `sqft_basement`, `yr_built`, `yr_renovated`, `zipcode`, `lat`, `long`, `sqft_living15`, `sqft_lot15`.

### Feature Engineering
Following strict ML discipline (fit on train, transform on test/live):
1. **Property Age & History**: `house_age` ($2026 - \text{yr\_built}$), `is_renovated`, `years_since_renovation`.
2. **Spatial Utilization**: `sqft_living_per_bed`, `bath_to_bed_ratio`, `living_to_lot_ratio`, `has_basement`, `basement_ratio`.
3. **Neighborhood Comparison**: `living_vs_neighbors` ($\text{sqft\_living} / \text{sqft\_living15}$), `lot_vs_neighbors`.
4. **Luxury Index**: Composite scoring factoring waterfront access, panoramic view ratings, construction grade ($1-13$), and property condition.

---

## 🔬 Machine Learning Experiments & Benchmarks

Three models were trained and rigorously cross-validated using 5-Fold Stratified CV on 17,277 training records and evaluated on an independent test set of 4,320 records:

| Model | Test Accuracy | Macro F1 | Weighted F1 | 5-Fold CV F1 | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Logistic Regression (Baseline)** | 68.38% | 0.6944 | 0.6846 | 0.6829 | 0.001 ms/sample |
| **Random Forest Classifier (150 trees)** | 79.10% | 0.7991 | 0.7915 | 0.7791 | 0.015 ms/sample |
| **XGBoost Classifier (Tuned)** 🏆 | **80.42%** | **0.8122** | **0.8050** | **0.7957** | **0.007 ms/sample** |

### Top Predictive Features
1. `grade` (King County Construction & Design Quality Grade)
2. `lat` (Latitude coordinate / Neighborhood desirability)
3. `sqft_living` (Total interior living area)
4. `luxury_score` (Engineered composite amenity indicator)
5. `living_vs_neighbors` (Scale relative to immediate 15 neighbors)

---

## 🎨 Frontend & User Experience

Built with Streamlit featuring a customized Glassmorphic Dark UI:
- **Tab 1: Property Classifier**: Interactive sliders, King County location presets (Bellevue, Seattle Downtown, Redmond, Mercer Island), dynamic probability breakdown, and live map view.
- **Tab 2: Model Analytics & Explainability**: Interactive confusion matrix heatmaps, feature importance charts, and model benchmark tables.
- **Tab 3: Batch Portfolio Valuation**: Ingestion of multi-property CSV portfolios with instant downloadable classification reports.
- **Tab 4: Cloud & API Specs**: Real-time architectural documentation and microservice status.

---

## 🚀 Local Setup & Execution

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/adithyan18092005/ml-house-classification.git
cd ml-house-classification

# Create & activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Kaggle Dataset & Train Models
```bash
kaggle datasets download -d harlfoxem/housesalesprediction --unzip -p data
python -m src.train
```

### 3. Launch Frontend Application
```bash
streamlit run frontend/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 4. Launch FastAPI Microservice
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 5. Run Automated Tests
```bash
pytest tests/ -v
```

---

## 🐳 Docker Containerization

### Build Image:
```bash
docker build -t estate-classify:latest -f deploy/Dockerfile .
```

### Run Container:
```bash
docker run -p 8501:8501 estate-classify:latest
```

---

## ☁️ AWS Cloud Deployment

An automated deployment script using `boto3` is provided in `deploy/deploy_aws.py`.

### Automated AWS EC2 Provisioning
```bash
python deploy/deploy_aws.py
```
The script automatically:
1. Validates AWS credentials and VPC settings.
2. Creates or reuses a security group (`estate-classify-web-sg`) with open ports `80` and `8501`.
3. Discovers the latest Amazon Linux / Ubuntu AMI in `us-east-1`.
4. Provisions a Free Tier `t2.micro` or `t3.small` instance with a cloud-init script that installs dependencies, sets up systemd service, and launches the application.
5. Outputs the public IPv4 web address: `http://<EC2-PUBLIC-IP>:8501`.

---

## 🔄 Automated CI/CD Pipeline

The `.github/workflows/ci_cd.yml` workflow triggers on push to `main`:
1. Checks out code.
2. Installs dependencies from `requirements.txt`.
3. Runs the test suite via `pytest`.
4. Builds and validates the Docker container.
