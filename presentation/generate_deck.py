"""
Generates an Executive College-Level 16:9 Presentation (.pptx)
for the EstateClassify AI Machine Learning Project.
"""

import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_pptx: str = "presentation/EstateClassify_AI_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_BG = RGBColor(15, 23, 42)        # #0F172A Dark Slate
    C_CARD = RGBColor(30, 41, 59)      # #1E293B Slate Box
    C_CARD_BORDER = RGBColor(51, 65, 85) # #334155
    C_INDIGO = RGBColor(99, 102, 241)  # #6366F1 Accent
    C_CYAN = RGBColor(6, 182, 212)     # #06B6D4 Highlight
    C_GOLD = RGBColor(245, 158, 11)    # #F59E0B Luxury Gold
    C_TEXT = RGBColor(248, 250, 252)   # #F8FAFC White Text
    C_MUTED = RGBColor(148, 163, 184)  # #94A3B8 Gray Text

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="ESTATECLASSIFY AI • COLLEGE ML PRESENTATION"):
        # Category Pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative accent card
    accent = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.8))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_CARD
    accent.line.color.rgb = C_CARD_BORDER

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11), Inches(2.2))
    tf = tbox.text_frame
    p0 = tf.paragraphs[0]
    p0.text = "ESTATECLASSIFY AI"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN

    p1 = tf.add_paragraph()
    p1.text = "End-to-End Real Estate Market Tier Classification"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT

    p2 = tf.add_paragraph()
    p2.text = "Production Machine Learning Engineering, Kaggle King County Dataset, XGBoost Ensemble & AWS EC2 Cloud Deployment"
    p2.font.size = Pt(15)
    p2.font.color.rgb = C_MUTED

    # Highlights footer boxes
    boxes = [
        ("🏆 Best Model", "XGBoost (80.42% Acc, 0.81 F1)"),
        ("⚡ Tech Stack", "Scikit-Learn, FastAPI, Streamlit"),
        ("☁️ Cloud Host", "AWS EC2 • Live on Port 80 & 8501"),
        ("🐙 Open Source", "GitHub CI/CD Automation")
    ]
    for i, (b_title, b_sub) in enumerate(boxes):
        bx = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2 + i * 2.75), Inches(4.3), Inches(2.6), Inches(1.5))
        bx.fill.solid()
        bx.fill.fore_color.rgb = RGBColor(15, 23, 42)
        bx.line.color.rgb = C_CARD_BORDER
        btf = bx.text_frame
        btf.margin_top = Inches(0.2)
        bp0 = btf.paragraphs[0]
        bp0.text = b_title
        bp0.font.size = Pt(12)
        bp0.font.bold = True
        bp0.font.color.rgb = C_INDIGO
        bp1 = btf.add_paragraph()
        bp1.text = b_sub
        bp1.font.size = Pt(10)
        bp1.font.color.rgb = C_TEXT

    s1.notes_slide.notes_text_frame.text = (
        "Speaker Notes: Welcome professors and colleagues. Today I am presenting EstateClassify AI, "
        "an end-to-end production Machine Learning engineering project that classifies residential properties into "
        "market valuation tiers using the Kaggle King County dataset, tuned XGBoost ensembles, and live AWS cloud infrastructure."
    )

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Strategic Motivation", "Phase 1: Project Formulation")

    col_w = Inches(3.64)
    cards_s2 = [
        ("Traditional Regression Limitations", [
            "Continuous dollar outputs ($542,109) obscure business decisions.",
            "High variance in real estate valuation models ($50k-$100k RMSE).",
            "Fails to categorize risk stratification for mortgage underwriters.",
            "Doesn't align with homebuyer search tiers & portfolio budgeting."
        ], C_CARD),
        ("The Classification Paradigm", [
            "Segments properties into 4 strategic economic tiers.",
            "Delivers calibrated class probability distributions.",
            "Provides clear confidence bounds and risk categorization.",
            "Optimizes mortgage portfolio clustering & capital allocation."
        ], C_CARD),
        ("Target Market Tiers", [
            "Affordable / Starter: Entry-level homes (< $325k)",
            "Mid-Range / Core Family: Suburban homes ($325k - $500k)",
            "Upper-Mid / Executive: High-demand areas ($500k - $750k)",
            "Luxury / Elite Estate: Waterfronts & custom estates (>= $750k)"
        ], C_CARD)
    ]
    for i, (title, points, color) in enumerate(cards_s2):
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.0), Inches(1.8), col_w, Inches(4.8))
        c.fill.solid()
        c.fill.fore_color.rgb = color
        c.line.color.rgb = C_CARD_BORDER
        ctf = c.text_frame
        ctf.margin_left = Inches(0.25)
        ctf.margin_right = Inches(0.25)
        ctf.margin_top = Inches(0.3)
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        for pt in points:
            p_sub = ctf.add_paragraph()
            p_sub.text = "• " + pt
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = C_TEXT
            p_sub.space_before = Pt(8)

    s2.notes_slide.notes_text_frame.text = (
        "Speaker Notes: Most housing ML projects attempt continuous price regression, which often suffers from high RMSE "
        "and fails to answer strategic grouping questions. Real estate funds, appraisers, and mortgage banks need categorical "
        "tier classification to bucket risk and match buyers. We formulated a 4-tier market classification spanning starter homes to luxury estates."
    )

    # ==========================================
    # SLIDE 3: DATASET ARCHITECTURE & EDA
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Kaggle Dataset Architecture & Data Quality", "Phase 2: Exploratory Data Analysis")

    left_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = C_CARD
    left_box.line.color.rgb = C_CARD_BORDER
    ltf = left_box.text_frame
    ltf.margin_left = Inches(0.3)
    ltf.margin_top = Inches(0.3)
    p = ltf.paragraphs[0]
    p.text = "Dataset Schema & Dimensions"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    items_l = [
        "Source: Kaggle House Sales in King County, USA",
        "Volume: 21,613 transaction records (Seattle metro area)",
        "Raw Attributes: 21 columns including structural & geospatial specs",
        "Target Balance: 4 stratified tiers (25%, 33%, 24%, 18%)",
        "Zero initial nulls across core numerical measurements"
    ]
    for it in items_l:
        p_sub = ltf.add_paragraph()
        p_sub.text = "✓ " + it
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = C_TEXT
        p_sub.space_before = Pt(10)

    right_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    right_box.fill.solid()
    right_box.fill.fore_color.rgb = C_CARD
    right_box.line.color.rgb = C_CARD_BORDER
    rtf = right_box.text_frame
    rtf.margin_left = Inches(0.3)
    rtf.margin_top = Inches(0.3)
    p = rtf.paragraphs[0]
    p.text = "Data Cleaning & Anomaly Correction"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    items_r = [
        "Bedrooms Typo Fix: Corrected known outlier row with 33 bedrooms for 1,620 sqft (input error for 3 bedrooms).",
        "Structural Sanity: Filtered non-viable records with 0 bedrooms or 0 bathrooms (< 0.1%).",
        "Strict Preprocessing Ordering: Train/test split (80/20 stratified) executed BEFORE any scaler or transformation.",
        "Zero Data Leakage: StandardScalers and transformers fitted solely on training partition."
    ]
    for it in items_r:
        p_sub = rtf.add_paragraph()
        p_sub.text = "• " + it
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = C_TEXT
        p_sub.space_before = Pt(10)

    s3.notes_slide.notes_text_frame.text = (
        "Speaker Notes: We sourced the gold-standard King County dataset from Kaggle. Data hygiene was critical: "
        "we addressed known recording typos such as the 33-bedroom 1620-sqft house. Crucially, following ML best practices, "
        "we stratified and split the 21,613 records into train and test sets BEFORE applying any transformations to eliminate data leakage."
    )

    # ==========================================
    # SLIDE 4: FEATURE ENGINEERING
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Domain-Driven Feature Engineering (27 Features)", "Phase 3: Representation Engineering")

    col_w4 = Inches(2.7)
    cards_s4 = [
        ("⏳ Age & History", [
            "house_age = 2026 - yr_built",
            "is_renovated = (yr_renovated > 0)",
            "years_since_renovation: effective chronological depreciation",
            "Captures modern construction premiums"
        ]),
        ("📐 Spatial Utilization", [
            "sqft_living_per_bed: space per occupant",
            "bath_to_bed_ratio: luxury layout proxy",
            "living_to_lot_ratio: density indicator",
            "has_basement & basement_ratio"
        ]),
        ("🏘️ Neighborhood Scale", [
            "living_vs_neighbors: living area / sqft_living15",
            "lot_vs_neighbors: lot / sqft_lot15",
            "Captures whether home is under/overbuilt for street",
            "Strong local valuation signals"
        ]),
        ("💎 Composite Luxury Score", [
            "waterfront * 4.0",
            "+ view * 2.0 (panoramic score)",
            "+ (grade >= 10) * 3.0 (custom arch)",
            "+ (condition >= 4) * 1.0",
            "Highly predictive of Tier 3 luxury"
        ])
    ]
    for i, (title, points) in enumerate(cards_s4):
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(1.8), col_w4, Inches(4.8))
        c.fill.solid()
        c.fill.fore_color.rgb = C_CARD
        c.line.color.rgb = C_CARD_BORDER
        ctf = c.text_frame
        ctf.margin_left = Inches(0.2)
        ctf.margin_top = Inches(0.3)
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_INDIGO
        for pt in points:
            p_sub = ctf.add_paragraph()
            p_sub.text = "• " + pt
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_TEXT
            p_sub.space_before = Pt(8)

    s4.notes_slide.notes_text_frame.text = (
        "Speaker Notes: Raw features alone do not reflect real estate market mechanics. We engineered 27 domain-specific features "
        "spanning building age, spatial density, neighborhood relative scale, and a composite Luxury Index. "
        "Notice living_vs_neighbors: a 3,000 sqft home surrounded by 1,500 sqft homes behaves very differently in the market."
    )

    # ==========================================
    # SLIDE 5: MODEL COMPARISON & BENCHMARKS
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Comparative Model Architecture & Benchmarking", "Phase 4: Empirical Evaluation")

    # Table of Results
    rows, cols = 4, 6
    table_shape = s5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.3))
    table = table_shape.table

    headers = ["Model Candidate", "Test Accuracy", "Macro F1", "Weighted F1", "5-Fold CV F1", "Latency / Sample"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_INDIGO
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_TEXT

    data = [
        ["Logistic Regression (Baseline)", "68.38%", "0.6944", "0.6846", "0.6829", "0.001 ms"],
        ["Random Forest (150 trees)", "79.10%", "0.7991", "0.7915", "0.7791", "0.015 ms"],
        ["XGBoost Classifier (Tuned) 🏆", "80.42%", "0.8122", "0.8050", "0.7957", "0.007 ms"]
    ]
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 41, 59) if i < 2 else RGBColor(40, 55, 80)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(12)
            p.font.bold = (i == 2)
            p.font.color.rgb = C_CYAN if (i == 2 and j == 0) else C_TEXT

    # Lower analysis cards
    ac1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.4), Inches(5.7), Inches(2.2))
    ac1.fill.solid()
    ac1.fill.fore_color.rgb = C_CARD
    ac1.line.color.rgb = C_CARD_BORDER
    actf1 = ac1.text_frame
    actf1.margin_left = Inches(0.25)
    actf1.margin_top = Inches(0.2)
    p = actf1.paragraphs[0]
    p.text = "🎯 Why XGBoost Won the Benchmark"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    for t in [
        "Surpassed linear baseline by +12.04% Accuracy and +0.1178 Macro F1.",
        "Superior handling of non-linear geographic spatial thresholds (lat/long).",
        "Regularized loss prevents overfitting (L1/L2 shrinkage on leaf weights)."
    ]:
        ps = actf1.add_paragraph()
        ps.text = "• " + t
        ps.font.size = Pt(11)
        ps.font.color.rgb = C_TEXT

    ac2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.2))
    ac2.fill.solid()
    ac2.fill.fore_color.rgb = C_CARD
    ac2.line.color.rgb = C_CARD_BORDER
    actf2 = ac2.text_frame
    actf2.margin_left = Inches(0.25)
    actf2.margin_top = Inches(0.2)
    p = actf2.paragraphs[0]
    p.text = "⚡ Operational & Latency Viability"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    for t in [
        "Inference Speed: 0.007 milliseconds per property (140,000 predictions/sec).",
        "Compact Model Size: 1.4 MB on disk; ideal for microservice deployment.",
        "Calibrated Probabilities: Softmax outputs provide granular confidence scores."
    ]:
        ps = actf2.add_paragraph()
        ps.text = "• " + t
        ps.font.size = Pt(11)
        ps.font.color.rgb = C_TEXT

    s5.notes_slide.notes_text_frame.text = (
        "Speaker Notes: Following model comparison best practices, we benchmarked Logistic Regression as a baseline, "
        "Random Forest as a bagging ensemble, and XGBoost as gradient boosting. XGBoost demonstrated clear superiority, achieving "
        "80.42% accuracy and 0.8122 Macro F1. Furthermore, its 7-microsecond latency makes it production-ready for live real estate traffic."
    )

    # ==========================================
    # SLIDE 6: EXPLAINABILITY & CONFUSION MATRIX
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Model Explainability & Error Diagnostics", "Phase 5: Interpretability & Validation")

    box_feat = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    box_feat.fill.solid()
    box_feat.fill.fore_color.rgb = C_CARD
    box_feat.line.color.rgb = C_CARD_BORDER
    ftf = box_feat.text_frame
    ftf.margin_left = Inches(0.25)
    ftf.margin_top = Inches(0.25)
    p = ftf.paragraphs[0]
    p.text = "Top Driving Features (SHAP / Gini Importance)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    drivers = [
        ("1. Construction Grade (1-13)", "Primary determinant of structural valuation."),
        ("2. Latitude Coordinate", "Neighborhood premium: Mercer Island/Bellevue vs suburbs."),
        ("3. Interior Living Area (sqft)", "Pure floorplan volume scaling."),
        ("4. Luxury Composite Score", "Waterfront access and panoramic mountain/lake view."),
        ("5. Living vs. Neighbors", "Scale relative to immediate community houses.")
    ]
    for d_name, d_desc in drivers:
        ps = ftf.add_paragraph()
        ps.text = f"{d_name}: {d_desc}"
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT
        ps.space_before = Pt(8)

    box_cm = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    box_cm.fill.solid()
    box_cm.fill.fore_color.rgb = C_CARD
    box_cm.line.color.rgb = C_CARD_BORDER
    ctf_cm = box_cm.text_frame
    ctf_cm.margin_left = Inches(0.25)
    ctf_cm.margin_top = Inches(0.25)
    p = ctf_cm.paragraphs[0]
    p.text = "Confusion Matrix & Error Analysis"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    insights_cm = [
        "Starter Homes (Tier 0): 919 Correct out of 1095 (84.0% sensitivity).",
        "Mid-Range Homes (Tier 1): 1,088 Correct out of 1,384 (78.6% sensitivity).",
        "Upper-Mid Homes (Tier 2): 845 Correct out of 1,108 (76.3% sensitivity).",
        "Luxury Estates (Tier 3): 622 Correct out of 733 (84.9% sensitivity).",
        "Zero Catastrophic Misses: 0 Tier 0 homes were misclassified as Tier 3 luxury, and 0 Tier 3 homes were classified as Tier 0."
    ]
    for ins in insights_cm:
        ps = ctf_cm.add_paragraph()
        ps.text = "✓ " + ins
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT
        ps.space_before = Pt(8)

    s6.notes_slide.notes_text_frame.text = (
        "Speaker Notes: Transparency and error analysis are vital. Feature importance reveals that construction grade "
        "and latitude (neighborhood prestige) dominate valuation over bedroom count. Looking at our confusion matrix, errors only "
        "occur between immediately adjacent tiers (e.g. Mid-Range vs Upper-Mid). There were zero catastrophic tier leaps, proving strong model stability."
    )

    # ==========================================
    # SLIDE 7: END-TO-END SYSTEM ARCHITECTURE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "End-to-End System & Cloud Architecture", "Phase 6: Engineering Architecture")

    steps = [
        ("1. Data Ingestion", "Kaggle King County Dataset\nAutomated ingestion & cleaning\n21,613 records"),
        ("2. Feature Transformer", "HouseFeatureTransformer\nStrict train-only fitting\n27 domain engineered metrics"),
        ("3. Model Core", "Tuned XGBoost Ensemble\nJoblib serialization\nCalibrated Softmax outputs"),
        ("4. Dual Serving", "FastAPI Microservice (Port 8000)\nStreamlit Glassmorphic UI (Port 8501)\nDocker Multi-Stage Container")
    ]
    for i, (st_title, st_body) in enumerate(steps):
        bx = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(1.8), Inches(2.7), Inches(3.2))
        bx.fill.solid()
        bx.fill.fore_color.rgb = C_CARD
        bx.line.color.rgb = C_INDIGO if i == 2 else C_CARD_BORDER
        btf = bx.text_frame
        btf.margin_left = Inches(0.2)
        btf.margin_top = Inches(0.3)
        p = btf.paragraphs[0]
        p.text = st_title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p_sub = btf.add_paragraph()
        p_sub.text = st_body
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = C_TEXT
        p_sub.space_before = Pt(8)

    # Cloud banner across bottom
    bot = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.3))
    bot.fill.solid()
    bot.fill.fore_color.rgb = RGBColor(20, 30, 48)
    bot.line.color.rgb = C_CYAN
    bttf = bot.text_frame
    bttf.margin_left = Inches(0.3)
    bttf.margin_top = Inches(0.15)
    p = bttf.paragraphs[0]
    p.text = "☁️ Continuous Integration & Cloud Deployment Pipeline"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p2 = bttf.add_paragraph()
    p2.text = "GitHub Actions CI/CD (Pytest test suite & Docker container build)  ➜  AWS S3 Presigned Deployment  ➜  AWS EC2 Ubuntu Host"
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT

    s7.notes_slide.notes_text_frame.text = (
        "Speaker Notes: This slide highlights our production software engineering architecture. Rather than leaving the model in a notebook, "
        "we engineered a modular pipeline: a scikit-learn transformer, serialized XGBoost core, FastAPI REST service, and Streamlit frontend, "
        "orchestrated with Docker and GitHub Actions CI/CD."
    )

    # ==========================================
    # SLIDE 8: AWS CLOUD DEPLOYMENT & LIVE APP
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Live AWS Cloud Deployment & Production Telemetry", "Phase 7: Cloud Deployment")

    l_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    l_card.fill.solid()
    l_card.fill.fore_color.rgb = C_CARD
    l_card.line.color.rgb = C_CARD_BORDER
    ltf = l_card.text_frame
    ltf.margin_left = Inches(0.3)
    ltf.margin_top = Inches(0.3)
    p = ltf.paragraphs[0]
    p.text = "AWS EC2 Infrastructure Details"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    specs = [
        ("Cloud Provider", "Amazon Web Services (AWS)"),
        ("Region", "us-east-1 (N. Virginia)"),
        ("Instance Type", "t3.small (2 vCPU, 2GB RAM + 2GB Swap)"),
        ("Operating System", "Ubuntu 22.04 LTS (Jammy)"),
        ("Security Group", "estate-classify-web-sg (Inbound 80, 8501, 22)"),
        ("Process Daemon", "systemd service (estateclassify.service)"),
        ("Port Forwarding", "iptables PREROUTING redirect (Port 80 -> 8501)")
    ]
    for k, v in specs:
        ps = ltf.add_paragraph()
        ps.text = f"• {k}: {v}"
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT
        ps.space_before = Pt(6)

    r_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = C_CARD
    r_card.line.color.rgb = C_CARD_BORDER
    rtf = r_card.text_frame
    rtf.margin_left = Inches(0.3)
    rtf.margin_top = Inches(0.3)
    p = rtf.paragraphs[0]
    p.text = "Live Endpoints & User Experience"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    url_items = [
        "🌐 Live Production URL: http://100.62.105.206 (Port 80)",
        "⚡ Streamlit Endpoint: http://100.62.105.206:8501",
        "🐙 GitHub Repository: https://github.com/Adithyan1809/ml-house-classification",
        "✨ Key UI Features:",
        "   - King County Presets (Bellevue, Redmond, Seattle)",
        "   - Real-time probability breakdown bar charts",
        "   - Interactive coordinate mapping with GPS pins",
        "   - Batch CSV file ingestion and valuation export"
    ]
    for it in url_items:
        ps = rtf.add_paragraph()
        ps.text = it
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT
        ps.space_before = Pt(6)

    s8.notes_slide.notes_text_frame.text = (
        "Speaker Notes: A project is only complete when it serves real users. We automated the deployment to AWS EC2 using Boto3, "
        "cloud-init, and systemd. The application is running live at http://100.62.105.206 on standard port 80. "
        "Evaluators and clients can open it on their phones or laptops right now and test property classifications."
    )

    # ==========================================
    # SLIDE 9: CONCLUSION & FUTURE HORIZONS
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Summary of Achievements & Future Horizons", "Phase 8: Project Conclusion")

    c1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_CARD
    c1.line.color.rgb = C_CARD_BORDER
    c1tf = c1.text_frame
    c1tf.margin_left = Inches(0.3)
    c1tf.margin_top = Inches(0.3)
    p = c1tf.paragraphs[0]
    p.text = "Key Project Achievements"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    achs = [
        "Resolved real-world housing segmentation using 4 calibrated market tiers.",
        "80.42% accuracy and 0.8122 Macro F1 achieved with XGBoost ensemble.",
        "Engineered 27 domain-specific features without data leakage.",
        "Beautiful glassmorphic dark-mode web application built with Streamlit.",
        "100% test coverage with automated pytest suite and GitHub Actions CI/CD.",
        "Zero-downtime AWS EC2 cloud deployment on public IP with systemd daemon."
    ]
    for a in achs:
        ps = c1tf.add_paragraph()
        ps.text = "✔ " + a
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT
        ps.space_before = Pt(8)

    c2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_CARD
    c2.line.color.rgb = C_CARD_BORDER
    c2tf = c2.text_frame
    c2tf.margin_left = Inches(0.3)
    c2tf.margin_top = Inches(0.3)
    p = c2tf.paragraphs[0]
    p.text = "Future Research Horizons"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    horizons = [
        "Multimodal Vision Fusion: Integrate satellite imagery and street-view photos using Convolutional / Vision Transformer backbones.",
        "Macroeconomic Temporal Factors: Ingest live Federal Reserve interest rates, mortgage trends, and inflation indices.",
        "Explainable AI (SHAP TreeExplainer): Deliver waterfall explanations directly in the frontend for each individual prediction.",
        "Automated Retraining Pipeline: Drift monitoring and automated weekly model updates using AWS Lambda and S3 triggers."
    ]
    for h in horizons:
        ps = c2tf.add_paragraph()
        ps.text = "🚀 " + h
        ps.font.size = Pt(12)
        ps.font.color.rgb = C_TEXT
        ps.space_before = Pt(8)

    s9.notes_slide.notes_text_frame.text = (
        "Speaker Notes: To conclude, EstateClassify AI bridges the gap between academic machine learning and production cloud software. "
        "For future work, we plan to incorporate multimodal aerial imagery using Vision Transformers and macroeconomic interest rate feeds. "
        "Thank you for your time. I am now open to any questions!"
    )

    prs.save(output_pptx)
    print(f"✅ Presentation successfully generated at: {output_pptx}")
    return output_pptx

if __name__ == "__main__":
    create_deck()
