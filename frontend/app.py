"""
Premium Real Estate Market Tier Classification Frontend
Built with Streamlit & Powered by XGBoost / Scikit-Learn
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict import HouseClassifierPredictor, METRICS_PATH

# 1. Page Configuration
st.set_page_config(
    page_title="EstateClassify AI • House Market Tier Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Load Model Engine & Metadata
@st.cache_resource
def load_engine():
    return HouseClassifierPredictor()

@st.cache_data
def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return {}

try:
    engine = load_engine()
    metrics = load_metrics()
except Exception as e:
    st.error(f"Error loading model artifacts: {e}. Please ensure models are trained.")
    st.stop()

# Preset Locations in King County, Washington
LOCATION_PRESETS = {
    "Medina / Bellevue Luxury Gold Coast (98004)": {"lat": 47.6200, "long": -122.2150, "zipcode": 98004},
    "Mercer Island Lakefront (98040)": {"lat": 47.5707, "long": -122.2220, "zipcode": 98040},
    "Redmond Innovation Corridor (98052)": {"lat": 47.6740, "long": -122.1215, "zipcode": 98052},
    "Seattle Capitol Hill / Downtown (98102)": {"lat": 47.6320, "long": -122.3210, "zipcode": 98102},
    "Kirkland Waterfront / Highlands (98033)": {"lat": 47.6815, "long": -122.2087, "zipcode": 98033},
    "Renton Family Suburban (98058)": {"lat": 47.4560, "long": -122.1480, "zipcode": 98058},
    "Federal Way Starter Community (98003)": {"lat": 47.3100, "long": -122.3120, "zipcode": 98003},
    "Custom GPS Coordinates": {"lat": 47.5500, "long": -122.2000, "zipcode": 98115}
}

# Sidebar Navigation & Overview
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <span style="font-size:2.2rem;">🏰</span>
            <div>
                <h2 style="margin:0; font-size:1.3rem; font-weight:800; letter-spacing:-0.03em;">EstateClassify AI</h2>
                <p style="margin:0; font-size:0.75rem; color:#94a3b8;">Real Estate Market Tier Engine</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="status-pill">
            <div class="status-pill-dot"></div>
            Model: XGBoost • AWS Deployed
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Quick Benchmark")
    best_m = metrics.get("best_metrics", {})
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Test Accuracy", f"{best_m.get('accuracy', 0)*100:.1f}%")
        st.metric("Macro F1", f"{best_m.get('f1_macro', 0)*100:.1f}%")
    with col_sb2:
        st.metric("5-Fold CV", f"{best_m.get('cv_f1_macro_mean', 0)*100:.1f}%")
        st.metric("Latency", f"{best_m.get('latency_ms_per_sample', 0):.2f} ms")

    st.markdown("---")
    st.markdown("### 📍 Location Presets")
    selected_preset_name = st.selectbox("Choose Area", list(LOCATION_PRESETS.keys()))
    selected_preset = LOCATION_PRESETS[selected_preset_name]

# Main App Navigation Tabs
tab_predict, tab_analytics, tab_batch, tab_arch = st.tabs([
    "🏡 Property Classifier",
    "📊 Model Analytics & Explainability",
    "📁 Batch Portfolio Valuation",
    "☁️ Cloud & API Specs"
])

# ==========================================
# TAB 1: PROPERTY CLASSIFIER
# ==========================================
with tab_predict:
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.03em;">
                Predict Property Market Tier
            </h1>
            <p style="color: #94a3b8; font-size: 1.05rem; margin: 0;">
                Input architectural specifications and geographic coordinates to determine market classification, valuation bracket, and risk profile.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("property_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 📐 Layout & Dimensions")
            bedrooms = st.slider("Bedrooms", min_value=1, max_value=11, value=4, step=1)
            bathrooms = st.slider("Bathrooms", min_value=1.0, max_value=8.0, value=2.75, step=0.25)
            sqft_living = st.number_input("Living Area (sqft)", min_value=300, max_value=15000, value=2850, step=50)
            sqft_lot = st.number_input("Lot Size (sqft)", min_value=500, max_value=500000, value=7500, step=250)
            floors = st.selectbox("Number of Floors", [1.0, 1.5, 2.0, 2.5, 3.0, 3.5], index=2)

        with col2:
            st.markdown("#### 💎 Architecture & Quality")
            grade = st.slider(
                "Construction & Design Grade (1-13)",
                min_value=1, max_value=13, value=9,
                help="1-3: Poor, 7: Average, 10: High, 11-13: Mansion/Custom Architecture"
            )
            condition = st.slider(
                "Overall Condition (1-5)",
                min_value=1, max_value=5, value=4,
                help="1: Poor, 3: Average, 5: Pristine/Immaculate"
            )
            waterfront = st.selectbox("Waterfront Property?", [0, 1], format_func=lambda x: "Yes (Direct Shoreline)" if x == 1 else "No")
            view = st.slider("View Quality Score (0-4)", min_value=0, max_value=4, value=1, help="0: None, 4: Panoramic Mountain/Water View")
            sqft_basement = st.number_input("Basement Area (sqft)", min_value=0, max_value=5000, value=400, step=50)

        with col3:
            st.markdown("#### 📍 Location & History")
            lat = st.number_input("Latitude", value=float(selected_preset["lat"]), format="%.4f")
            long = st.number_input("Longitude", value=float(selected_preset["long"]), format="%.4f")
            zipcode = st.number_input("ZIP Code", value=int(selected_preset["zipcode"]), step=1)
            yr_built = st.number_input("Year Built", min_value=1900, max_value=2026, value=2008, step=1)
            yr_renovated = st.number_input("Year Renovated (0 if none)", min_value=0, max_value=2026, value=0, step=1)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("⚡ Classify Property Tier", use_container_width=True)

    # Process Prediction
    sqft_above = sqft_living - sqft_basement
    if sqft_above < 200:
        sqft_above = 200

    prop_payload = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "grade": grade,
        "sqft_above": sqft_above,
        "sqft_basement": sqft_basement,
        "yr_built": yr_built,
        "yr_renovated": yr_renovated,
        "zipcode": zipcode,
        "lat": lat,
        "long": long,
        "sqft_living15": sqft_living,
        "sqft_lot15": sqft_lot
    }

    result = engine.predict_single(prop_payload)
    pred_tier = result["predicted_tier"]
    confidence = result["confidence"]
    price_range = result["estimated_price_range"]
    prob_dict = result["class_probabilities"]

    # Tier CSS class assignment
    tier_styles = {
        "Affordable / Starter": "tier-affordable",
        "Mid-Range / Core Family": "tier-mid-range",
        "Upper-Mid / Executive": "tier-upper-mid",
        "Luxury / Elite Estate": "tier-luxury"
    }
    applied_style = tier_styles.get(pred_tier, "tier-upper-mid")

    st.markdown("---")
    st.markdown("### 🏆 Classification Result")

    res_col1, res_col2 = st.columns([1.2, 1])

    with res_col1:
        st.markdown(f"""
            <div class="glass-card">
                <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">
                    Model Predicted Market Segment
                </span>
                <div style="margin: 12px 0;">
                    <span class="tier-badge {applied_style}">{pred_tier}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
                    <div>
                        <div class="metric-highlight">{confidence * 100:.1f}%</div>
                        <div class="metric-label">Model Confidence</div>
                    </div>
                    <div>
                        <div class="metric-highlight" style="font-size: 1.8rem; color:#38bdf8;">{price_range}</div>
                        <div class="metric-label">Estimated Valuation Bracket</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Probabilities Bar Chart
        prob_df = pd.DataFrame({
            "Market Tier": list(prob_dict.keys()),
            "Probability (%)": [v * 100 for v in prob_dict.values()]
        })

        chart = alt.Chart(prob_df).mark_bar(cornerRadius=6).encode(
            x=alt.X("Probability (%):Q", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("Market Tier:N", sort=None, title=None),
            color=alt.Color(
                "Probability (%):Q",
                scale=alt.Scale(scheme="viridis"),
                legend=None
            ),
            tooltip=["Market Tier", alt.Tooltip("Probability (%):Q", format=".1f")]
        ).properties(height=180)

        st.altair_chart(chart, use_container_width=True)

    with res_col2:
        st.markdown("#### 🗺️ Geographic Location Preview")
        map_data = pd.DataFrame({
            "lat": [lat],
            "lon": [long]
        })
        st.map(map_data, zoom=11)

        st.markdown(f"""
            <div style="font-size: 0.85rem; color: #94a3b8; background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); margin-top:10px;">
                <strong>📍 Coordinates:</strong> {lat:.4f}° N, {long:.4f}° W<br>
                <strong>🏷️ ZIP Code:</strong> {zipcode} (King County, Washington)<br>
                <strong>📐 Space Ratio:</strong> {sqft_living / (bedrooms + 0.5):.0f} sqft/bedroom
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: MODEL ANALYTICS & EXPLAINABILITY
# ==========================================
with tab_analytics:
    st.markdown("### 🔬 Comparative Model Evaluation & Explainability")
    st.markdown("Rigorous benchmark evaluation following machine learning engineering best practices.")

    all_models = metrics.get("all_models", {})
    if all_models:
        comp_data = []
        for name, m in all_models.items():
            comp_data.append({
                "Model": name,
                "Accuracy": f"{m['accuracy']*100:.2f}%",
                "Macro F1": f"{m['f1_macro']*100:.2f}%",
                "Weighted F1": f"{m['f1_weighted']*100:.2f}%",
                "Precision": f"{m['precision_macro']*100:.2f}%",
                "Recall": f"{m['recall_macro']*100:.2f}%",
                "5-Fold CV F1": f"{m['cv_f1_macro_mean']*100:.2f}%",
                "Latency (ms)": f"{m['latency_ms_per_sample']:.3f}"
            })
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True)

    st.markdown("---")
    col_feat, col_cm = st.columns(2)

    with col_feat:
        st.markdown("#### 🌟 Top Feature Importances")
        feat_imp = metrics.get("feature_importances", {})
        if feat_imp:
            top_features = list(feat_imp.items())[:10]
            top_df = pd.DataFrame(top_features, columns=["Feature", "Relative Importance"]).sort_values("Relative Importance", ascending=True)

            fig, ax = plt.subplots(figsize=(6, 4.5))
            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#0f172a')
            
            bars = ax.barh(top_df["Feature"], top_df["Relative Importance"], color='#6366f1')
            ax.tick_params(colors='#94a3b8')
            for spine in ax.spines.values():
                spine.set_color('#334155')
            ax.set_xlabel("Importance Score", color='#94a3b8')
            st.pyplot(fig)

    with col_cm:
        st.markdown("#### 🎯 Best Model Confusion Matrix")
        best_cm = best_m.get("confusion_matrix")
        if best_cm:
            cm_arr = np.array(best_cm)
            fig_cm, ax_cm = plt.subplots(figsize=(6, 4.5))
            fig_cm.patch.set_facecolor('#0f172a')
            ax_cm.set_facecolor('#0f172a')

            labels = ["Starter", "Mid", "Upper", "Luxury"]
            sns.heatmap(
                cm_arr, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels,
                cbar=False, ax=ax_cm
            )
            ax_cm.tick_params(colors='#94a3b8')
            ax_cm.set_xlabel("Predicted Tier", color='#94a3b8')
            ax_cm.set_ylabel("Actual Tier", color='#94a3b8')
            for spine in ax_cm.spines.values():
                spine.set_color('#334155')
            st.pyplot(fig_cm)

# ==========================================
# TAB 3: BATCH PORTFOLIO VALUATION
# ==========================================
with tab_batch:
    st.markdown("### 📁 Batch Portfolio Valuation & CSV Ingestion")
    st.markdown("Upload a portfolio of houses to classify multiple properties simultaneously.")

    # Generate sample download
    sample_df = pd.DataFrame([
        {
            "bedrooms": 3, "bathrooms": 2.0, "sqft_living": 1800, "sqft_lot": 5000,
            "floors": 1.0, "waterfront": 0, "view": 0, "condition": 3, "grade": 7,
            "sqft_above": 1800, "sqft_basement": 0, "yr_built": 1985, "yr_renovated": 0,
            "zipcode": 98058, "lat": 47.4560, "long": -122.1480, "sqft_living15": 1750, "sqft_lot15": 5200
        },
        {
            "bedrooms": 5, "bathrooms": 4.5, "sqft_living": 4800, "sqft_lot": 15000,
            "floors": 2.0, "waterfront": 1, "view": 3, "condition": 5, "grade": 11,
            "sqft_above": 3800, "sqft_basement": 1000, "yr_built": 2012, "yr_renovated": 0,
            "zipcode": 98004, "lat": 47.6200, "long": -122.2150, "sqft_living15": 4200, "sqft_lot15": 14000
        }
    ])

    st.download_button(
        "📥 Download Sample CSV Template",
        data=sample_df.to_csv(index=False),
        file_name="sample_houses_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.write(f"Loaded {len(batch_df)} properties for batch classification:")
            classified_df = engine.predict_batch(batch_df)
            st.dataframe(classified_df.head(20), use_container_width=True)

            csv_data = classified_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Classified Portfolio Results",
                data=csv_data,
                file_name="classified_portfolio_results.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error processing batch CSV: {e}")

# ==========================================
# TAB 4: CLOUD & API SPECS
# ==========================================
with tab_arch:
    st.markdown("### ☁️ AWS Cloud Architecture & REST API")
    st.markdown("""
        This machine learning system is engineered for zero-downtime, scalable cloud production.
    """)

    st.markdown("""
    ```mermaid
    graph LR
        User([Client / App]) -->|HTTP / 8501| Streamlit[Streamlit UI]
        User -->|REST API / 8000| FastAPI[FastAPI Microservice]
        FastAPI --> XGBoost[XGBoost Classifier]
        Streamlit --> XGBoost
        XGBoost --> Pipeline[Feature Transformer Engine]
        Docker[(Docker Container)] -.-> Streamlit
        Docker -.-> FastAPI
        AWS[AWS EC2 / App Runner] ==> Docker
    ```
    """)

    st.markdown("""
    #### 🚀 Production Highlights
    - **Dataset**: Kaggle King County Real Estate (21,613 properties, 27 engineered features)
    - **Model**: Tuned XGBoost Ensemble Classifier (Macro F1 = 0.8122, Accuracy = 80.42%)
    - **Frameworks**: Scikit-Learn 1.6, XGBoost 3.4, FastAPI, Streamlit, Boto3
    - **Deployment Target**: AWS EC2 / Docker Container
    - **CI/CD**: GitHub Actions Automated Testing & Deployment
    """)
