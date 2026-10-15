"""
SpaceX Capstone: Comprehensive Presentation Generator Module
-----------------------------------------------------------
Generates:
1. presentation/spacex_capstone.pptx (23 Slides, Aerospace Navy & Orange Theme, All Required Visuals, Full SQL Tasks, Folium Markers & Site Counts, Detailed Model Comparisons, Confusion Matrices & Exact Lab Links)
2. presentation/spacex_capstone.pdf (High-Fidelity PDF exported via native PowerPoint COM with full vector formatting)
3. presentation/speaker_notes.md (Complete slide-by-slide plain-English speaker script for all 23 slides)
"""

import os
import sys
import logging
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table as RLTable, TableStyle as RLTableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESENTATION_DIR = os.path.join(BASE_DIR, "presentation")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")

GITHUB_REPO_URL = "https://github.com/buildwithneel/Coursera-IBM-data-science-course"

# Theme Palette
NAVY_DARK = RGBColor(11, 27, 61)       # #0B1B3D
NAVY_LIGHT = RGBColor(26, 47, 90)      # #1A2F5A
NAVY_CARD = RGBColor(18, 38, 77)       # #12264D
ORANGE_ACCENT = RGBColor(255, 111, 0)  # #FF6F00
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(220, 226, 235)
MUTED_TEXT = RGBColor(180, 190, 205)
DARK_GRAY = RGBColor(35, 35, 35)
GREEN_ACCENT = RGBColor(46, 125, 50)
BORDER_GRAY = RGBColor(190, 205, 225)
LINK_BLUE = RGBColor(14, 116, 144)     # #0E7490


def add_background_and_header(slide, title_text, category="IBM DATA SCIENCE PROFESSIONAL CAPSTONE", lab_link=None):
    # Header banner shape
    header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    header_shape.fill.solid()
    header_shape.fill.fore_color.rgb = NAVY_DARK
    header_shape.line.color.rgb = ORANGE_ACCENT
    header_shape.line.width = Pt(2)

    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.08), Inches(11.5), Inches(0.28))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ORANGE_ACCENT

    # Title text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.34), Inches(11.5), Inches(0.7))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE

    # Bottom footer bar
    footer_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.08), Inches(13.333), Inches(0.42))
    footer_shape.fill.solid()
    footer_shape.fill.fore_color.rgb = NAVY_LIGHT
    footer_shape.line.fill.background()

    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(6.0), Inches(0.32))
    tf_foot = foot_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "SpaceX Falcon 9 First Stage Landing Prediction | IBM Data Science Capstone"
    p_foot.font.size = Pt(9)
    p_foot.font.color.rgb = LIGHT_GRAY

    # Footer methodology lab link
    link_display = f"🔗 Lab Link: {lab_link}" if lab_link else f"🔗 GitHub: {GITHUB_REPO_URL}"
    link_box = slide.shapes.add_textbox(Inches(6.8), Inches(7.12), Inches(5.8), Inches(0.32))
    tf_link = link_box.text_frame
    p_link = tf_link.paragraphs[0]
    p_link.text = link_display
    p_link.alignment = PP_ALIGN.RIGHT
    p_link.font.size = Pt(8.5)
    p_link.font.bold = True
    p_link.font.color.rgb = ORANGE_ACCENT


def create_card(slide, left, top, width, height, bg_color=None, border_color=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color if bg_color else RGBColor(246, 249, 252)
    card.line.color.rgb = border_color if border_color else BORDER_GRAY
    card.line.width = Pt(1.5)
    return card


def add_lab_banner(slide, left, top, width, height, lab_title, lab_url):
    banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(234, 242, 250)
    banner.line.color.rgb = LINK_BLUE
    banner.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.04), width - Inches(0.2), height - Inches(0.08))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"🔗 {lab_title}: "
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = LINK_BLUE
    run = p.add_run()
    run.text = lab_url
    run.font.bold = False
    run.font.size = Pt(8.5)
    run.font.color.rgb = NAVY_DARK


def create_powerpoint():
    os.makedirs(PRESENTATION_DIR, exist_ok=True)
    pptx_path = os.path.join(PRESENTATION_DIR, "spacex_capstone.pptx")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ================= Slide 1: Title Slide =================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.12), Inches(5.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE_ACCENT
    bar.line.fill.background()

    tbox1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.1), Inches(11.0), Inches(5.3))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "IBM DATA SCIENCE PROFESSIONAL CERTIFICATE | CAPSTONE FINAL PRESENTATION"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = ORANGE_ACCENT

    p1 = tf1.add_paragraph()
    p1.text = "SPACEX FALCON 9"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = ORANGE_ACCENT

    p2 = tf1.add_paragraph()
    p2.text = "First Stage Landing Prediction"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    p3 = tf1.add_paragraph()
    p3.text = "End-to-End Machine Learning, Geospatial & SQL Analytics Capstone"
    p3.font.size = Pt(17)
    p3.font.color.rgb = LIGHT_GRAY

    p4 = tf1.add_paragraph()
    p4.text = f"\n✔ Verified GitHub Repository URL (All Completed Notebooks & Python Code):\n{GITHUB_REPO_URL}"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = RGBColor(100, 200, 255)

    p5 = tf1.add_paragraph()
    p5.text = "Author: Student Capstone Submission | Evaluation Submission Format: PDF (.pdf) & PPTX (.pptx)"
    p5.font.size = Pt(10.5)
    p5.font.color.rgb = LIGHT_GRAY

    # ================= Slide 2: Executive Summary (Question 3) =================
    s2 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s2, "Executive Summary & Core Project Findings", lab_link=f"{GITHUB_REPO_URL}")
    
    create_card(s2, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_s2_left = s2.shapes.add_textbox(Inches(0.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_s2_left = tb_s2_left.text_frame
    tf_s2_left.word_wrap = True
    p = tf_s2_left.paragraphs[0]
    p.text = "Project Objectives & Economic Impact"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    bullets2_left = [
        ("Commercial Problem", "SpaceX advertises Falcon 9 launches at ~$62M, whereas competitor missions cost upwards of $165M. The $103M economic savings is driven entirely by recovering and reusing the first-stage booster."),
        ("Commercial Bidding Window", "If an alternative launch provider or satellite client knows booster recovery feasibility in advance, they can determine SpaceX pricing discounts and formulate competitive bids."),
        ("Target Construction", "Analyzed 90 historical launches. Created binary target Class (1 = Successful Landing, 0 = Failure/Expended). Baseline landing success rate is 66.7% (60 successes, 30 failures).")
    ]
    for b_title, b_desc in bullets2_left:
        p = tf_s2_left.add_paragraph()
        p.text = f"•  {b_title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    create_card(s2, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_s2_right = s2.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_s2_right = tb_s2_right.text_frame
    tf_s2_right.word_wrap = True
    p = tf_s2_right.paragraphs[0]
    p.text = "Methodological Framework & Empirical Results"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    bullets2_right = [
        ("Data Pipeline", "REST API v4 & Wikipedia scraping; handled missing payload via mean imputation (6,105 kg); engineered 80 features."),
        ("EDA & SQL Analytics", "Demonstrated clear operational learning curve from 0% (2010) to 84.2% (2020). Executed 12 SQL queries in SQLite covering site volume, milestone dates, and outcome rankings."),
        ("Geospatial & Dash", "Mapped coastal buffers (<1.5 km to sea) via Folium. Built reactive Plotly Dash interactive dashboard."),
        ("Supervised ML Winner", "Evaluated Logistic Regression, SVM, Decision Tree, and KNN with 10-fold CV. Best models: Tuned KNN & Logistic Regression achieved 83.33% Test Accuracy and 0.889 F1-score.")
    ]
    for b_title, b_desc in bullets2_right:
        p = tf_s2_right.add_paragraph()
        p.text = f"✔  {b_title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 3: Introduction & Business Problem (Question 4) =================
    s3 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s3, "Introduction: Commercial Rocketry Economics & Bidding", lab_link=f"{GITHUB_REPO_URL}")
    
    create_card(s3, Inches(0.8), Inches(1.35), Inches(11.7), Inches(5.5))
    tb3 = s3.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "The Strategic Imperative of First-Stage Booster Reusability"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    intro_points = [
        ("Expendable vs Reusable Paradigm", "Historically, orbital rocket launches were 100% expendable. The entire rocket was discarded into the Atlantic or Pacific ocean after a single flight, resulting in exorbitant launch costs exceeding $165M per flight."),
        ("Booster Cost Composition", "The Falcon 9 first-stage booster contains 9 Merlin 1D rocket engines, high-grade aerospace aluminium-lithium alloy tanks, avionics, and titanium grid fins, representing approximately 70% of total rocket manufacturing cost ($30M - $40M)."),
        ("Commercial Pricing Disruption", "By successfully recovering the first-stage core via Autonomous Spaceport Drone Ships (ASDS) or Return-To-Launch-Site ground pads (RTLS), SpaceX reuses boosters up to 10+ times, offering standard commercial launches at ~$62M."),
        ("Competitor Decision Support", "When satellite operators or launch service competitors (e.g., Arianespace, ULA, Rocket Lab) bid for launch contracts, anticipating whether SpaceX will recover the booster allows them to predict SpaceX's pricing margin and bid competitively."),
        ("Project Mission & Deliverables", "This project constructs a full-stack data science pipeline: API data collection, BeautifulSoup web scraping, SQLite data warehousing, Folium geospatial analytics, Plotly Dash dashboard, and machine learning classifiers to predict landing outcomes.")
    ]
    for title_txt, body_txt in intro_points:
        p = tf3.add_paragraph()
        p.text = f"▶  {title_txt}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = body_txt
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 4: Project Architecture & Pipeline Flow (Question 14) =================
    s4 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s4, "Project Architecture & End-to-End Technical Pipeline", lab_link=f"{GITHUB_REPO_URL}/blob/main/docs/project_architecture.md")

    arch_img_path = os.path.join(VISUALS_DIR, "architecture.png")
    if os.path.exists(arch_img_path):
        s4.shapes.add_picture(arch_img_path, Inches(0.8), Inches(1.35), width=Inches(11.7))

    create_card(s4, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.35))
    tb_arch = s4.shapes.add_textbox(Inches(0.95), Inches(5.65), Inches(11.4), Inches(1.2))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True
    p = tf_arch.paragraphs[0]
    p.text = "5-Tier Modular Data Architecture & Reproducibility Guarantees"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    arch_notes = [
        "• Ingestion -> Wrangling -> Analytics -> ML Modeling -> Multi-Format Deliverables (PPTX, PDF, Dashboard).",
        "• Strict Leakage Prevention: StandardScaler fitted strictly on 80% train split (N=72); test partition (N=18) kept isolated.",
        "• Offline Reproducibility: Cached raw data in data/raw/, processed datasets in data/processed/, and SQLite spacex.db."
    ]
    for an in arch_notes:
        p = tf_arch.add_paragraph()
        p.text = an
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ================= Slide 5: Data Collection Methodology & Lab Links (Question 5) =================
    s5 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s5, "Data Collection: SpaceX REST API v4 & Web Scraping", lab_link="notebooks/01_data_collection_api.ipynb")

    # Lab Links Banners
    add_lab_banner(s5, Inches(0.8), Inches(1.30), Inches(5.7), Inches(0.42), "Lab 1 Notebook", f"{GITHUB_REPO_URL}/blob/main/notebooks/01_data_collection_api.ipynb")
    add_lab_banner(s5, Inches(6.8), Inches(1.30), Inches(5.7), Inches(0.42), "Lab 2 Notebook", f"{GITHUB_REPO_URL}/blob/main/notebooks/02_web_scraping.ipynb")

    create_card(s5, Inches(0.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_dc1 = s5.shapes.add_textbox(Inches(0.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_dc1 = tb_dc1.text_frame
    tf_dc1.word_wrap = True
    p = tf_dc1.paragraphs[0]
    p.text = "1. SpaceX REST API v4 Integration (Lab 1)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    api_points = [
        ("API Endpoint", "Queried past launches endpoint: https://api.spacexdata.com/v4/launches/past."),
        ("Nested Entity Unpacking", "Extracted launch records and unpacked nested JSON objects: rocket IDs, payload masses, launch complexes, core serial numbers, flight reuse count, and landing attempt flags."),
        ("Falcon 9 Filtering", "Filtered dataset specifically for Falcon 9 vehicles, removing Falcon 1 test flights and Falcon Heavy configurations to maintain booster consistency."),
        ("Fault-Tolerant Caching", "Built automated local caching in data/raw/dataset_part_1.csv with fail-safe fallback to IBM's historical benchmark repository (90 flights)."),
        ("Source Code & Lab", "Completed in notebooks/01_data_collection_api.ipynb and src/data_collection.py.")
    ]
    for t, d in api_points:
        p = tf_dc1.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(9)
        run.font.color.rgb = DARK_GRAY

    create_card(s5, Inches(6.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_dc2 = s5.shapes.add_textbox(Inches(6.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_dc2 = tb_dc2.text_frame
    tf_dc2.word_wrap = True
    p = tf_dc2.paragraphs[0]
    p.text = "2. Wikipedia HTML Web Scraping (Lab 2)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    scrape_points = [
        ("Source URL", "Scraped historical tables from Wikipedia: List of Falcon 9 and Falcon Heavy launches."),
        ("BeautifulSoup Parsing", "Targeted HTML <table> elements with class 'wikitable', iterating through table rows and parsing table headers <th> and cells <td>."),
        ("Extracted Attributes", "Parsed Flight No., Launch Date, Booster Version, Launch Site, Payload, Orbit, Customer, and Launch Outcome."),
        ("Data Cleaning & Validation", "Handled row-spans, superscripts, references (e.g., [1]), and date formatting. Extracted 321 tabular records saved to data/raw/spacex_web_scraped.csv."),
        ("Source Code & Lab", "Completed in notebooks/02_web_scraping.ipynb and src/data_collection.py.")
    ]
    for t, d in scrape_points:
        p = tf_dc2.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(9)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 6: Data Wrangling Methodology & Lab Link (Question 5) =================
    s6 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s6, "Data Wrangling: Cleaning, Imputation & Target Construction", lab_link="notebooks/03_data_wrangling.ipynb")

    add_lab_banner(s6, Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.42), "Lab 3 Notebook Link", f"{GITHUB_REPO_URL}/blob/main/notebooks/03_data_wrangling.ipynb")

    create_card(s6, Inches(0.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_dw1 = s6.shapes.add_textbox(Inches(0.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_dw1 = tb_dw1.text_frame
    tf_dw1.word_wrap = True
    p = tf_dw1.paragraphs[0]
    p.text = "Missing Values & Target Variable (Class)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    dw_points1 = [
        ("Missing Value Analysis", "Audited nulls across all features. Identified 5 missing entries in PayloadMass (early test flights). Imputed missing values using the dataset mean of 6,104.95 kg."),
        ("Target Variable Construction", "Engineered binary target Class from raw landing Outcome:"),
        ("Class = 1 (Successful Landing)", "True ASDS (41 drone ship touchdowns) + True RTLS (14 ground pad landings) + True Ocean (5 controlled water landings) = 60 Successful Landings (66.7%)."),
        ("Class = 0 (Failure / Expended)", "None None (19 flights with no recovery attempt) + False ASDS (6 drone ship crashes) + False Ocean (2 ocean crashes) + None ASDS (2 failed attempts) + False RTLS (1 ground pad crash) = 30 Failures (33.3%).")
    ]
    for t, d in dw_points1:
        p = tf_dw1.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(9)
        run.font.color.rgb = DARK_GRAY

    create_card(s6, Inches(6.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_dw2 = s6.shapes.add_textbox(Inches(6.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_dw2 = tb_dw2.text_frame
    tf_dw2.word_wrap = True
    p = tf_dw2.paragraphs[0]
    p.text = "Feature Engineering & One-Hot Encoding"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    dw_points2 = [
        ("Launch Site Distribution", "CCAFS SLC 40: 55 launches (61.1%), KSC LC 39A: 22 launches (24.4%), VAFB SLC 4E: 13 launches (14.4%)."),
        ("Orbit Distribution", "Covered 11 distinct orbital profiles: GTO (27), ISS (21), VLEO (14), PO (9), LEO (7), SSO (5), MEO (3), ES-L1 (1), HEO (1), SO (1), GEO (1)."),
        ("Categorical Encoding", "Applied pd.get_dummies() on categorical features: Orbit, LaunchSite, LandingPad, and Serial."),
        ("Predictor Feature Matrix", "Assembled dataset_part_3.csv containing 80 numerical and one-hot encoded dummy features ready for machine learning algorithms."),
        ("Source Code & Lab", "Completed in notebooks/03_data_wrangling.ipynb and src/data_wrangling.py.")
    ]
    for t, d in dw_points2:
        p = tf_dw2.add_paragraph()
        p.text = f"✔ {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(9)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 7: EDA Methodology & Hypotheses (Question 6) =================
    s7 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s7, "Exploratory Data Analysis: Research Hypotheses & Framework", lab_link="notebooks/04_eda_visualizations.ipynb")

    add_lab_banner(s7, Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.42), "Lab 4 Notebook Link (EDA Visualization)", f"{GITHUB_REPO_URL}/blob/main/notebooks/04_eda_visualizations.ipynb")

    create_card(s7, Inches(0.8), Inches(1.80), Inches(11.7), Inches(5.05))
    tb7 = s7.shapes.add_textbox(Inches(1.0), Inches(1.90), Inches(11.3), Inches(4.85))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    p.text = "Four Foundational Hypotheses Guiding Exploratory Analysis"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    eda_hypotheses = [
        ("H1: Temporal Learning Curve Progression", "Hypothesis: As SpaceX accumulated launch cadence from 2010 to 2020 and iterated its booster avionics, titanium grid fins, and throttle-controllable Merlin engines from Block 1 to Block 5, landing success rate increased from near 0% to over 80%."),
        ("H2: Launch Complex Specialization & Success Variance", "Hypothesis: Different launch sites exhibit divergent landing success rates due to differing orbital azimuths, coastal flight corridors, and mission profiles (e.g., Kennedy Space Center LC 39A vs Cape Canaveral SLC 40)."),
        ("H3: Payload Mass Constraints on Propellant Margins", "Hypothesis: Heavier payload masses require greater ascent burn delta-V, reducing the reserve propellant remaining in the first-stage tanks for the boostback, entry, and landing burns, thereby lowering recovery probability."),
        ("H4: Orbital Energy Demands Impact Recovery Mode", "Hypothesis: High-energy missions (Geostationary Transfer Orbit - GTO) re-enter the atmosphere at extreme hypersonic velocities, requiring high-stress ocean drone ship (ASDS) recoveries with lower success compared to Low Earth Orbit (LEO) or ISS missions."),
        ("Methodology Implementation", "Investigated using Pandas, Matplotlib, and Seaborn to generate 10 high-resolution analytical figures saved to visuals/eda/, verified in notebooks/04_eda_visualizations.ipynb.")
    ]
    for h_title, h_desc in eda_hypotheses:
        p = tf7.add_paragraph()
        p.text = f"★  {h_title}: "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = h_desc
        run.font.bold = False
        run.font.size = Pt(9.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 8: EDA Tasks 1 & 2: Site vs Flight No & Payload (Question 8) =================
    s8 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s8, "EDA Tasks 1 & 2: Flight Number & Payload Mass vs Launch Site", lab_link="notebooks/04_eda_visualizations.ipynb")

    img4_path = os.path.join(VISUALS_DIR, "eda", "04_flight_number_vs_launch_site.png")
    img5_path = os.path.join(VISUALS_DIR, "eda", "05_payload_mass_vs_launch_site.png")
    if os.path.exists(img4_path):
        s8.shapes.add_picture(img4_path, Inches(0.8), Inches(1.35), width=Inches(5.7))
    if os.path.exists(img5_path):
        s8.shapes.add_picture(img5_path, Inches(6.8), Inches(1.35), width=Inches(5.7))

    create_card(s8, Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.7))
    tb8 = s8.shapes.add_textbox(Inches(0.95), Inches(5.30), Inches(11.4), Inches(1.6))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "Quantitative Findings: Task 1 (Flight No vs Site) & Task 2 (Payload vs Site)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    takeaways8 = [
        "• Task 1 (Flight No vs Site): CCAFS SLC 40 hosted all early flights (1-25) with initial experimental failures; KSC LC 39A entered service at Flight 30 with predominantly successful landings; VAFB SLC 4E operates steadily for polar orbits.",
        "• Task 2 (Payload vs Site): Payloads >10,000 kg are concentrated exclusively at Florida sites (CCAFS SLC 40 & KSC LC 39A); VAFB SLC 4E operates with payloads strictly under 10,000 kg.",
        "• Success Distribution: Higher flight numbers strongly correlate with successful landings across all three launch complexes, proving hardware maturity."
    ]
    for tk in takeaways8:
        p = tf8.add_paragraph()
        p.text = tk
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ================= Slide 9: EDA Tasks 3 & 4: Orbit Success Rate & Flight Number (Question 8) =================
    s9 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s9, "EDA Tasks 3 & 4: Success Rate & Flight Number vs Orbit Type", lab_link="notebooks/04_eda_visualizations.ipynb")

    img6_path = os.path.join(VISUALS_DIR, "eda", "06_success_rate_by_orbit.png")
    img7_path = os.path.join(VISUALS_DIR, "eda", "07_flight_number_vs_orbit.png")
    if os.path.exists(img6_path):
        s9.shapes.add_picture(img6_path, Inches(0.8), Inches(1.35), width=Inches(5.7))
    if os.path.exists(img7_path):
        s9.shapes.add_picture(img7_path, Inches(6.8), Inches(1.35), width=Inches(5.7))

    create_card(s9, Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.7))
    tb9 = s9.shapes.add_textbox(Inches(0.95), Inches(5.30), Inches(11.4), Inches(1.6))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "Quantitative Findings: Task 3 (Success vs Orbit) & Task 4 (Flight No vs Orbit)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    takeaways9 = [
        "• Task 3 (Success vs Orbit): Orbits ES-L1, GEO, HEO, and SSO achieved a 100% landing success rate; VLEO achieved 85.7%; ISS achieved 61.9%; GTO missions achieved 51.8% success.",
        "• Task 4 (Flight No vs Orbit): In early flights (1-40), GTO and ISS missions suffered landing failures. In later flights (>50), VLEO (Starlink) and modern ISS missions achieved near-perfect recovery.",
        "• Re-entry Velocity Impact: GTO missions enter at extreme velocity (~30,000 km/h), requiring high-stress ocean drone ship landings with tighter fuel reserves."
    ]
    for tk in takeaways9:
        p = tf9.add_paragraph()
        p.text = tk
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ================= Slide 10: EDA Tasks 5 & 6: Payload vs Orbit & Yearly Success Trend (Question 8) =================
    s10 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s10, "EDA Tasks 5 & 6: Payload Mass vs Orbit & Yearly Success Trend", lab_link="notebooks/04_eda_visualizations.ipynb")

    img8_path = os.path.join(VISUALS_DIR, "eda", "08_payload_mass_vs_orbit.png")
    img9_path = os.path.join(VISUALS_DIR, "eda", "09_yearly_success_trend.png")
    if os.path.exists(img8_path):
        s10.shapes.add_picture(img8_path, Inches(0.8), Inches(1.35), width=Inches(5.7))
    if os.path.exists(img9_path):
        s10.shapes.add_picture(img9_path, Inches(6.8), Inches(1.35), width=Inches(5.7))

    create_card(s10, Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.7))
    tb10 = s10.shapes.add_textbox(Inches(0.95), Inches(5.30), Inches(11.4), Inches(1.6))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "Quantitative Findings: Task 5 (Payload vs Orbit) & Task 6 (Yearly Trend Line)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    takeaways10 = [
        "• Task 5 (Payload vs Orbit): Heavy payloads (>10,000 kg) are concentrated in VLEO (Starlink) and achieved high success; GTO payloads range between 3,000-7,000 kg with mixed outcomes.",
        "• Task 6 (Yearly Success Trend): Landing success followed a clear learning curve: 0% in 2010-2013 -> 33.3% in 2014-2015 -> 66.7% in 2016 -> 80.0% in 2017 -> 84.2% in 2020.",
        "• Engineering Milestone: Transition to Block 5 boosters in 2018 established sustained high reliability (>80%)."
    ]
    for tk in takeaways10:
        p = tf10.add_paragraph()
        p.text = tk
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ================= Slide 11: EDA Cadence & Overall Success Distribution (Question 8) =================
    s11 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s11, "EDA Visual Results: Launch Cadence & Overall Success Distribution", lab_link="notebooks/04_eda_visualizations.ipynb")

    img1_path = os.path.join(VISUALS_DIR, "eda", "01_launches_over_time.png")
    img3_path = os.path.join(VISUALS_DIR, "eda", "03_overall_landing_success_rate.png")
    if os.path.exists(img1_path):
        s11.shapes.add_picture(img1_path, Inches(0.8), Inches(1.35), width=Inches(5.7))
    if os.path.exists(img3_path):
        s11.shapes.add_picture(img3_path, Inches(6.8), Inches(1.35), width=Inches(5.7))

    create_card(s11, Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.7))
    tb11 = s11.shapes.add_textbox(Inches(0.95), Inches(5.30), Inches(11.4), Inches(1.6))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    p = tf11.paragraphs[0]
    p.text = "Quantitative Findings: Annual Cadence Growth & Class Distribution"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    takeaways11 = [
        "• 19x Cadence Expansion: Launch frequency surged from 1-3 test flights per year (2010-2013) to ~19 launches per year by 2020.",
        "• Baseline Class Distribution: 60 Successful Landings (66.7%) vs 30 Failed / Expended Boosters (33.3%).",
        "• Operational Shift: Boosters evolved from expendable experimental hardware to industrial-scale reusability."
    ]
    for tk in takeaways11:
        p = tf11.add_paragraph()
        p.text = tk
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ================= Slide 12: SQL Tasks 1 to 4: Sites & Payload Statistics (Question 9) =================
    s12 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s12, "EDA with SQL: Tasks 1 to 4 (Launch Complexes & Payload Statistics)", lab_link="notebooks/05_sql_analysis.ipynb")

    add_lab_banner(s12, Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.42), "Lab 5 Notebook Link (EDA with SQL)", f"{GITHUB_REPO_URL}/blob/main/notebooks/05_sql_analysis.ipynb")

    create_card(s12, Inches(0.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_sql1 = s12.shapes.add_textbox(Inches(0.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_sql1 = tb_sql1.text_frame
    tf_sql1.word_wrap = True
    p = tf_sql1.paragraphs[0]
    p.text = "Tasks 1 & 2: Launch Sites & Cape Canaveral Queries"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    sql_code_1 = [
        ("Task 1: Names of Unique Launch Sites",
         "SELECT DISTINCT LaunchSite FROM SPACEXTBL;\n"
         "Result: CCAFS SLC 40, KSC LC 39A, VAFB SLC 4E"),
        ("Task 2: 5 Records where Launch Site begins with 'CCA'",
         "SELECT FlightNumber, Date, LaunchSite, BoosterVersion, PayloadMass\n"
         "FROM SPACEXTBL WHERE LaunchSite LIKE 'CCA%' LIMIT 5;\n"
         "Result: Flights #1 to #5 launched from CCAFS SLC 40 (2010 to 2013).")
    ]
    for q_title, q_body in sql_code_1:
        p = tf_sql1.add_paragraph()
        p.text = f"• {q_title}:\n"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = q_body
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    create_card(s12, Inches(6.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_sql2 = s12.shapes.add_textbox(Inches(6.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_sql2 = tb_sql2.text_frame
    tf_sql2.word_wrap = True
    p = tf_sql2.paragraphs[0]
    p.text = "Tasks 3 & 4: Total & Average Payload Statistics"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    sql_code_2 = [
        ("Task 3: Total Payload Mass by Launch Site",
         "SELECT LaunchSite, SUM(PayloadMass) AS TotalPayload,\n"
         "COUNT(*) AS TotalLaunches FROM SPACEXTBL GROUP BY LaunchSite;\n"
         "Result: CCAFS SLC 40 = 305,532 kg (55 flights)\n"
         "        KSC LC 39A = 168,198 kg (22 flights)\n"
         "        VAFB SLC 4E = 76,950 kg (13 flights)"),
        ("Task 4: Average, Min & Max Payload Mass",
         "SELECT ROUND(AVG(PayloadMass), 2) AS AvgPayload,\n"
         "MIN(PayloadMass) AS MinPayload, MAX(PayloadMass) AS MaxPayload\n"
         "FROM SPACEXTBL;\n"
         "Result: Average Payload = 6,104.95 kg\n"
         "        Min = 350 kg | Max = 15,600 kg")
    ]
    for q_title, q_body in sql_code_2:
        p = tf_sql2.add_paragraph()
        p.text = f"✔ {q_title}:\n"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = q_body
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 13: SQL Tasks 5 to 7: Milestones & Outcome Breakdown (Question 9) =================
    s13 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s13, "EDA with SQL: Tasks 5 to 7 (Landing Milestones & Mission Outcomes)", lab_link="notebooks/05_sql_analysis.ipynb")

    create_card(s13, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_sql3 = s13.shapes.add_textbox(Inches(0.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_sql3 = tb_sql3.text_frame
    tf_sql3.word_wrap = True
    p = tf_sql3.paragraphs[0]
    p.text = "Tasks 5 & 6: Ground Pad & Drone Ship Successes"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    sql_code_3 = [
        ("Task 5: Date of First Successful Ground Pad Landing (RTLS)",
         "SELECT MIN(Date) AS FirstSuccessDate, FlightNumber, LaunchSite\n"
         "FROM SPACEXTBL WHERE Outcome = 'True RTLS';\n"
         "Result: 2015-12-22 | Flight #19 | Booster B1019 | CCAFS SLC 40"),
        ("Task 6: Drone Ship Success with Payload between 4k-6k kg",
         "SELECT FlightNumber, Date, Serial, PayloadMass, LaunchSite\n"
         "FROM SPACEXTBL WHERE Outcome = 'True ASDS' AND\n"
         "PayloadMass BETWEEN 4000 AND 6000;\n"
         "Result: Boosters B1022 (JCSAT-14), B1026 (JCSAT-16), B1048")
    ]
    for q_title, q_body in sql_code_3:
        p = tf_sql3.add_paragraph()
        p.text = f"★ {q_title}:\n"
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = q_body
        run.font.bold = False
        run.font.size = Pt(9)
        run.font.color.rgb = DARK_GRAY

    create_card(s13, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_sql4 = s13.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_sql4 = tb_sql4.text_frame
    tf_sql4.word_wrap = True
    p = tf_sql4.paragraphs[0]
    p.text = "Task 7: Total Number of Successful & Failure Outcomes"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    sql_code_4 = [
        ("Task 7: Mission Outcomes Balance (Class = 1 vs Class = 0)",
         "SELECT CASE WHEN Class = 1 THEN 'Successful Landing'\n"
         "            ELSE 'Failure / Uncontrolled' END AS LandingStatus,\n"
         "COUNT(*) AS TotalCount, ROUND(COUNT(*)*100.0/90, 2) AS Percentage\n"
         "FROM SPACEXTBL GROUP BY Class ORDER BY TotalCount DESC;\n"
         "Result: Successful Landings (Class 1) = 60 flights (66.67%)\n"
         "        Failures / Expended (Class 0) = 30 flights (33.33%)"),
        ("Operational Significance",
         "This 2:1 class balance establishes our 66.7% baseline accuracy. Any predictive model must significantly outperform 66.7% to prove predictive utility.")
    ]
    for q_title, q_body in sql_code_4:
        p = tf_sql4.add_paragraph()
        p.text = f"✔ {q_title}:\n"
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = q_body
        run.font.bold = False
        run.font.size = Pt(9)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 14: SQL Tasks 8 to 10: Max Payload & Outcome Ranking (Question 9) =================
    s14 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s14, "EDA with SQL: Tasks 8 to 10 (Max Payload, 2015 Outcomes & Rankings)", lab_link="notebooks/05_sql_analysis.ipynb")

    create_card(s14, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_sql5 = s14.shapes.add_textbox(Inches(0.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_sql5 = tb_sql5.text_frame
    tf_sql5.word_wrap = True
    p = tf_sql5.paragraphs[0]
    p.text = "Tasks 8 & 9: Max Payload & 2015 Cadence"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    sql_code_5 = [
        ("Task 8: Boosters Carrying Maximum Payload Mass",
         "SELECT FlightNumber, Date, Serial, PayloadMass\n"
         "FROM SPACEXTBL WHERE PayloadMass = (SELECT MAX(PayloadMass) FROM SPACEXTBL);\n"
         "Result: Maximum Payload = 15,600 kg. Carried by Starlink Block 5 boosters: B1048, B1049, B1051, B1056, B1058, B1060."),
        ("Task 9: Monthly Landing Outcomes in Year 2015",
         "SELECT strftime('%m', Date) AS Month, Date, Serial, LaunchSite, Outcome\n"
         "FROM SPACEXTBL WHERE strftime('%Y', Date) = '2015' ORDER BY Date;\n"
         "Result: Shows experimental drone ship tests (False ASDS on 2015-01-10 & 2015-04-14) culminating in first RTLS success (2015-12-22).")
    ]
    for q_title, q_body in sql_code_5:
        p = tf_sql5.add_paragraph()
        p.text = f"★ {q_title}:\n"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = q_body
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    create_card(s14, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_sql6 = s14.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_sql6 = tb_sql6.text_frame
    tf_sql6.word_wrap = True
    p = tf_sql6.paragraphs[0]
    p.text = "Task 10: Ranked Landing Outcomes Frequency"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    sql_code_6 = [
        ("Task 10: Rank Count of Landing Outcomes (2010 to 2020)",
         "SELECT Outcome, COUNT(*) AS Frequency, CASE WHEN Outcome LIKE 'True%'\n"
         "THEN 'Success' ELSE 'Failure' END AS Category FROM SPACEXTBL\n"
         "WHERE Date BETWEEN '2010-06-04' AND '2020-11-05'\n"
         "GROUP BY Outcome ORDER BY Frequency DESC;\n"
         "Result: 1. True ASDS: 41 recoveries (Primary method)\n"
         "        2. None None: 19 expended / unattempted\n"
         "        3. True RTLS: 14 ground pad touchdowns\n"
         "        4. False ASDS: 6 drone ship crash landings\n"
         "        5. True Ocean: 5 controlled water touchdowns\n"
         "        6. False Ocean: 2 uncontrolled ocean crashes\n"
         "        7. None ASDS: 2 failed ocean attempts\n"
         "        8. False RTLS: 1 ground pad landing crash")
    ]
    for q_title, q_body in sql_code_6:
        p = tf_sql6.add_paragraph()
        p.text = f"✔ {q_title}:\n"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = q_body
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 15: Folium Launch Sites, Markers & Site Counts (Question 10) =================
    s15 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s15, "Geospatial Analysis: Folium Launch Site Markers & Counts", lab_link="notebooks/06_folium_launch_map.ipynb")

    add_lab_banner(s15, Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.42), "Lab 6 Notebook Link (Interactive Visual Analytics with Folium)", f"{GITHUB_REPO_URL}/blob/main/notebooks/06_folium_launch_map.ipynb")

    folium_img_path = os.path.join(VISUALS_DIR, "folium", "folium_map_screenshot.png")
    if os.path.exists(folium_img_path):
        s15.shapes.add_picture(folium_img_path, Inches(0.8), Inches(1.80), width=Inches(6.2))

    create_card(s15, Inches(7.2), Inches(1.80), Inches(5.3), Inches(5.05))
    tb15 = s15.shapes.add_textbox(Inches(7.35), Inches(1.88), Inches(5.0), Inches(4.85))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    p = tf15.paragraphs[0]
    p.text = "Launch Site Counts & Folium Marker Details"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    folium_counts = [
        ("CCAFS SLC 40 (Florida)", "55 total launches (33 successful landings, 22 failures / expended, 60.0% success rate). Primary launch workhorse."),
        ("KSC LC 39A (Florida)", "22 total launches (17 successful landings, 5 failures / expended, 77.3% success rate). Highest site success rate."),
        ("VAFB SLC 4E (California)", "13 total launches (10 successful landings, 3 failures / expended, 76.9% success rate). Polar orbit specialty."),
        ("Total Launch Sites", "3 unique launch complexes; 90 historical launches mapped."),
        ("MarkerCluster & Color Coding", "Folium MarkerCluster aggregates all 90 launches: Green icon (Class=1, 60 successes); Red icon (Class=0, 30 failures)."),
        ("Artifact & Code", "visuals/folium/launch_sites_map.html. Built via notebooks/06_folium_launch_map.ipynb & src/generate_map.py.")
    ]
    for f_title, f_desc in folium_counts:
        p = tf15.add_paragraph()
        p.text = f"📍  {f_title}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = f_desc
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 16: Folium Distance & Proximity Analysis (Question 10) =================
    s16 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s16, "Geospatial Analysis: Haversine Distances & Public Safety Corridors", lab_link="notebooks/06_folium_launch_map.ipynb")

    create_card(s16, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_dist1 = s16.shapes.add_textbox(Inches(0.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_dist1 = tb_dist1.text_frame
    tf_dist1.word_wrap = True
    p = tf_dist1.paragraphs[0]
    p.text = "Geodesic Haversine Distance Table"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    dist_table = [
        ("CCAFS SLC 40 (28.5623°N, 80.5774°W)",
         "• Coastline: 0.95 km (Atlantic Ocean)\n"
         "• Highway: 1.25 km (NASA Causeway / Samuel C. Phillips)\n"
         "• Railway: 1.15 km (Titan IV railroad spur)\n"
         "• Nearest City: 18.9 km (Cape Canaveral City)"),
        ("KSC LC 39A (28.5733°N, 80.6469°W)",
         "• Coastline: 1.12 km (Atlantic Ocean)\n"
         "• Highway: 1.62 km (Kennedy Pkwy)\n"
         "• Railway: 1.34 km (NASA Railroad)\n"
         "• Nearest City: 16.5 km (Titusville)"),
        ("VAFB SLC 4E (34.6328°N, 120.6107°W)",
         "• Coastline: 1.48 km (Pacific Ocean)\n"
         "• Highway: 1.85 km (Coast Rd)\n"
         "• Railway: 1.42 km (Union Pacific Railroad)\n"
         "• Nearest City: 14.8 km (Lompoc)")
    ]
    for d_name, d_vals in dist_table:
        p = tf_dist1.add_paragraph()
        p.text = f"★ {d_name}:\n"
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d_vals
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    create_card(s16, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_dist2 = s16.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_dist2 = tb_dist2.text_frame
    tf_dist2.word_wrap = True
    p = tf_dist2.paragraphs[0]
    p.text = "Strategic Rationale of Site Positioning"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    dist_insights = [
        ("Coastal Proximity (<1.5 km)", "Every launchpad is sited within 1.5 km of open ocean. Eastward orbital trajectories over the Atlantic (Florida) and southward trajectories over the Pacific (California) guarantee that catastrophic booster failures impact water rather than populated land."),
        ("Logistical Proximity (1-2 km)", "Direct access to heavy railroads and NASA causeway highways enables overland transport of 70-meter Falcon 9 first-stage cores from manufacturing in Hawthorne, CA."),
        ("Urban Buffer Zones (15-35 km)", "All pads maintain a strict 15-35 km buffer from urban city centers (Titusville, Cape Canaveral, Lompoc), protecting civilian populations from acoustic shockwaves and blast hazards."),
        ("Equatorial Rotational Boost", "Cape Canaveral (28.56°N) provides an additional ~410 m/s velocity boost from Earth's rotation for easterly launches, maximizing payload capacity.")
    ]
    for d_title, d_desc in dist_insights:
        p = tf_dist2.add_paragraph()
        p.text = f"✔  {d_title}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = d_desc
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 17: Plotly Dash Dashboard (Question 11) =================
    s17 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s17, "Interactive Dashboard: Plotly Dash Analytics Console", lab_link="dashboard/app.py")

    add_lab_banner(s17, Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.42), "Lab 7 Dashboard Script (Plotly Dash Web Application)", f"{GITHUB_REPO_URL}/blob/main/dashboard/app.py")

    dash_img_path = os.path.join(VISUALS_DIR, "dashboard", "dashboard_screenshot.png")
    if os.path.exists(dash_img_path):
        s17.shapes.add_picture(dash_img_path, Inches(0.8), Inches(1.80), width=Inches(6.2))

    create_card(s17, Inches(7.2), Inches(1.80), Inches(5.3), Inches(5.05))
    tb17 = s17.shapes.add_textbox(Inches(7.35), Inches(1.88), Inches(5.0), Inches(4.85))
    tf17 = tb17.text_frame
    tf17.word_wrap = True

    p = tf17.paragraphs[0]
    p.text = "Operational Dashboard Architecture & Dynamic UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    dash_details = [
        ("Launch Site Dropdown", "Allows users to filter across ALL sites or isolate CCAFS SLC 40, KSC LC 39A, or VAFB SLC 4E."),
        ("Payload Range Slider", "Interactive slider from 0 kg to 16,000 kg with 2,000 kg tick intervals for payload threshold exploration."),
        ("Outcome Filter Radio", "Filter flights by All Outcomes, Successes Only, or Failures Only."),
        ("Dynamic Reactive KPIs", "Real-time calculation of Selected Missions count, Overall Success %, Successful Landings count, and Mean Payload mass."),
        ("Reactive Charts", "Updates Donut outcome distribution, Payload vs Flight scatter plot with Class color coding, and stacked Yearly Cadence bars."),
        ("Implementation", "Standalone Flask/Dash application in dashboard/app.py running locally on port 8050.")
    ]
    for d_title, d_desc in dash_details:
        p = tf17.add_paragraph()
        p.text = f"• {d_title}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d_desc
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 18: Machine Learning Methodology & Lab Link (Question 7) =================
    s18 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s18, "Predictive Analysis: Machine Learning Methodology & Leakage Control", lab_link="notebooks/07_machine_learning.ipynb")

    add_lab_banner(s18, Inches(0.8), Inches(1.30), Inches(11.7), Inches(0.42), "Lab 8 Notebook Link (Machine Learning Classification)", f"{GITHUB_REPO_URL}/blob/main/notebooks/07_machine_learning.ipynb")

    create_card(s18, Inches(0.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_ml1 = s18.shapes.add_textbox(Inches(0.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_ml1 = tb_ml1.text_frame
    tf_ml1.word_wrap = True
    p = tf_ml1.paragraphs[0]
    p.text = "Data Preparation & Leakage Prevention"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    ml_points1 = [
        ("Feature Matrix (X)", "80 independent features derived from FlightNumber, PayloadMass, Flights, GridFins, Reused, Legs, Block, and one-hot encoded dummy variables for Orbit, LaunchSite, LandingPad, and Serial."),
        ("Target Vector (Y)", "Binary outcome Class: 1 = Successful Landing (60), 0 = Failure / Expended (30)."),
        ("Train/Test Partitioning", "Split into 80% training set (N=72) and 20% held-out test set (N=18) using stratified sampling (stratify=Y, random_state=42)."),
        ("Strict Leakage Prevention", "StandardScaler fitted strictly on training data (X_train). Test data (X_test) transformed using scaler parameters from training data without refitting."),
        ("Cross-Validation", "10-Fold StratifiedKFold cross-validation within GridSearchCV to maintain class balance across all validation folds.")
    ]
    for t, d in ml_points1:
        p = tf_ml1.add_paragraph()
        p.text = f"⚙ {t}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    create_card(s18, Inches(6.8), Inches(1.80), Inches(5.7), Inches(5.05))
    tb_ml2 = s18.shapes.add_textbox(Inches(6.95), Inches(1.88), Inches(5.4), Inches(4.85))
    tf_ml2 = tb_ml2.text_frame
    tf_ml2.word_wrap = True
    p = tf_ml2.paragraphs[0]
    p.text = "Algorithms & Hyperparameter Grids"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    ml_points2 = [
        ("Logistic Regression", "Tuned regularization parameter C: [0.01, 0.1, 1.0], penalty: 'l2', solver: 'lbfgs'."),
        ("Support Vector Machine (SVM)", "Tuned kernel: ['linear', 'rbf', 'sigmoid'], regularization C: [0.01, 0.1, 1.0, 10.0], gamma: ['scale', 'auto']."),
        ("Decision Tree Classifier", "Tuned splitting criterion: ['gini', 'entropy'], splitter: ['best', 'random'], max_depth: [2, 4, 6, 8], min_samples_split: [2, 5], min_samples_leaf: [1, 2]."),
        ("K-Nearest Neighbors (KNN)", "Tuned n_neighbors: [1 to 10], algorithm: ['auto', 'ball_tree', 'kd_tree'], distance metric parameter p: [1 (Manhattan), 2 (Euclidean)]."),
        ("Evaluation Strategy", "Models compared on CV accuracy, Test accuracy, Precision, Recall, F1-score, and Confusion Matrices.")
    ]
    for t, d in ml_points2:
        p = tf_ml2.add_paragraph()
        p.text = f"✔ {t}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 19: Model Comparison Table & Hyperparameters (Question 12) =================
    s19 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s19, "Predictive Analysis: Detailed Model Comparison Table & Hyperparameters", lab_link="notebooks/07_machine_learning.ipynb")

    img_comp = os.path.join(VISUALS_DIR, "model", "model_comparison.png")
    if os.path.exists(img_comp):
        s19.shapes.add_picture(img_comp, Inches(0.8), Inches(1.35), width=Inches(5.7))

    create_card(s19, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb19 = s19.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf19 = tb19.text_frame
    tf19.word_wrap = True

    p = tf19.paragraphs[0]
    p.text = "Comprehensive Model Comparison Matrix"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    model_rows = [
        ("K-Nearest Neighbors (KNN) - WINNER",
         "• Best Params: {'algorithm': 'auto', 'n_neighbors': 3, 'p': 1}\n"
         "• 10-Fold CV Train Accuracy: 86.43%\n"
         "• Test Accuracy: 83.33% | F1-Score: 0.889\n"
         "• Precision: 0.800 | Recall: 1.000 | ROC-AUC: 0.771"),
        ("Logistic Regression (Tied Best)",
         "• Best Params: {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}\n"
         "• 10-Fold CV Train Accuracy: 85.00%\n"
         "• Test Accuracy: 83.33% | F1-Score: 0.889\n"
         "• Precision: 0.800 | Recall: 1.000 | ROC-AUC: 0.833"),
        ("Support Vector Machine (SVM)",
         "• Best Params: {'C': 0.01, 'gamma': 'scale', 'kernel': 'linear'}\n"
         "• 10-Fold CV Train Accuracy: 86.43%\n"
         "• Test Accuracy: 77.78% | F1-Score: 0.857\n"
         "• Precision: 0.750 | Recall: 1.000 | ROC-AUC: 0.931"),
        ("Decision Tree Classifier",
         "• Best Params: {'criterion': 'gini', 'max_depth': 4, 'min_samples_leaf': 2, 'min_samples_split': 5}\n"
         "• 10-Fold CV Train Accuracy: 83.57%\n"
         "• Test Accuracy: 77.78% | F1-Score: 0.846\n"
         "• Precision: 0.786 | Recall: 0.917 | ROC-AUC: 0.708")
    ]
    for m_name, m_stats in model_rows:
        p = tf19.add_paragraph()
        p.text = f"★ {m_name}:\n"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = m_stats
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 20: Confusion Matrix Results & Error Analysis (Question 12) =================
    s20 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s20, "Predictive Analysis: Confusion Matrix Breakdown & Error Analysis", lab_link="notebooks/07_machine_learning.ipynb")

    img_cm = os.path.join(VISUALS_DIR, "model", "confusion_matrices.png")
    if os.path.exists(img_cm):
        s20.shapes.add_picture(img_cm, Inches(0.8), Inches(1.35), width=Inches(5.7))

    create_card(s20, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb20 = s20.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf20 = tb20.text_frame
    tf20.word_wrap = True

    p = tf20.paragraphs[0]
    p.text = "Detailed Test Confusion Matrix Breakdown (N=18)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    cm_breakdown = [
        ("KNN Confusion Matrix",
         "• True Positives (TP): 12 | True Negatives (TN): 3\n"
         "• False Positives (FP): 3 | False Negatives (FN): 0\n"
         "• Perfect Recall (1.000) on successful landings; no missed recoveries."),
        ("Logistic Regression Confusion Matrix",
         "• True Positives (TP): 12 | True Negatives (TN): 3\n"
         "• False Positives (FP): 3 | False Negatives (FN): 0\n"
         "• Exactly matches KNN's optimal classification profile."),
        ("SVM Confusion Matrix",
         "• True Positives (TP): 12 | True Negatives (TN): 2\n"
         "• False Positives (FP): 4 | False Negatives (FN): 0"),
        ("Decision Tree Confusion Matrix",
         "• True Positives (TP): 11 | True Negatives (TN): 3\n"
         "• False Positives (FP): 3 | False Negatives (FN): 1"),
        ("Commercial Error Impact",
         "In rocket bidding, False Negatives (predicting failure when booster lands) cause competitors to miss discounting windows. KNN and Logistic Regression achieve ZERO False Negatives (FN=0, Recall=100%).")
    ]
    for cm_title, cm_body in cm_breakdown:
        p = tf20.add_paragraph()
        p.text = f"✔ {cm_title}:\n"
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = cm_body
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 21: Feature Importance & Decision Drivers (Question 14 & 15) =================
    s21 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s21, "Feature Importance: Mechanical & Orbital Decision Drivers", lab_link="src/train_model.py")

    img_feat = os.path.join(VISUALS_DIR, "model", "feature_importance.png")
    if os.path.exists(img_feat):
        s21.shapes.add_picture(img_feat, Inches(0.8), Inches(1.35), width=Inches(5.7))

    create_card(s21, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb21 = s21.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf21 = tb21.text_frame
    tf21.word_wrap = True

    p = tf21.paragraphs[0]
    p.text = "Key Technical & Operational Decision Drivers"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    feat_drivers = [
        ("GridFins & Landing Legs", "GridFins and Legs are the strongest positive predictors of recovery. Missions without landing gear or grid fins represent early expendable flights with 0% landing feasibility."),
        ("Booster Block Iteration (Block 5)", "Transition to Block 5 design provides bolted titanium grid fins and thermal protection upgrades, significantly elevating survival odds over Block 1-4."),
        ("Payload Mass & Orbit Demands", "High payload mass coupled with high-energy GTO orbits exhibits negative recovery coefficients due to constrained propellant reserves for landing burns."),
        ("Reused Count & Flight Sequence", "FlightNumber and ReusedCount positively correlate with success, confirming the operational maturity learning curve of experienced flight cores."),
        ("Takeaway", "Machine learning effectively captures the interaction between booster hardware configuration and orbital mechanics constraints.")
    ]
    for f_title, f_desc in feat_drivers:
        p = tf21.add_paragraph()
        p.text = f"★  {f_title}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = f_desc
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 22: Conclusions, Innovation & Future Work (Question 13, 14, 15) =================
    s22 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s22, "Conclusions, Innovative Insights & Future Roadmap", lab_link=f"{GITHUB_REPO_URL}")

    create_card(s22, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_c1 = s22.shapes.add_textbox(Inches(0.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Conclusions & Commercial Takeaways (Question 13)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    conc_points = [
        ("Cost Asymmetry", "SpaceX's ~$62M launch pricing versus competitors' ~$165M provides a massive ~$103M commercial advantage per flight, driven by booster recovery."),
        ("Predictive Viability", "Supervised classification models (KNN & Logistic Regression) reliably forecast booster recovery with 83.33% accuracy using pre-launch mission parameters."),
        ("Commercial Bidding Window", "When SpaceX flies heavy payloads to GTO, recovery margins shrink (51.8% success), creating opportunities for competitor launch bidding."),
        ("Engineering Maturity", "Falcon 9 has proven that first-stage reusability is technically and commercially sustainable over 90+ missions.")
    ]
    for t, d in conc_points:
        p = tf_c1.add_paragraph()
        p.text = f"🚀 {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    create_card(s22, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.5))
    tb_c2 = s22.shapes.add_textbox(Inches(6.95), Inches(1.45), Inches(5.4), Inches(5.3))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Innovative Insights & Future Roadmap (Questions 14 & 15)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    innov_points = [
        ("Payload 'Sweet Spot'", "Identified that payloads between 2,000 kg and 5,300 kg represent the optimal operating window for drone ship recovery."),
        ("Geospatial Safety Corridors", "Quantified that all pads maintain <1.5 km ocean access and >15 km city buffer, optimizing launch safety corridors."),
        ("Current Limitations", "Dataset size is bounded to 90 historical launches; real-time ocean wave telemetry at drone ship coordinates was not available in historical logs."),
        ("Future Enhancements", "Integrate live NOAA marine weather telemetry (wave heights and wind speeds at drone ship GPS coordinates) and deploy deep neural networks for continuous trajectory modeling.")
    ]
    for t, d in innov_points:
        p = tf_c2.add_paragraph()
        p.text = f"★ {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = ORANGE_ACCENT
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    # ================= Slide 23: References, Project Repository & Submission (Question 1 & 2) =================
    s23 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s23, "Project Artifacts, Repository & Submission Verification", lab_link=f"{GITHUB_REPO_URL}")

    create_card(s23, Inches(0.8), Inches(1.35), Inches(11.7), Inches(5.5))
    tb23 = s23.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.2))
    tf23 = tb23.text_frame
    tf23.word_wrap = True

    p = tf23.paragraphs[0]
    p.text = "Verified Submission Deliverables & Repository Structure"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    ref_details = [
        ("Official GitHub Repository", GITHUB_REPO_URL),
        ("Completed Jupyter Notebooks", "7 Notebooks in notebooks/: 01_data_collection_api.ipynb, 02_web_scraping.ipynb, 03_data_wrangling.ipynb, 04_eda_visualizations.ipynb, 05_sql_analysis.ipynb, 06_folium_launch_map.ipynb, 07_machine_learning.ipynb."),
        ("Python Source Modules", "Production modules in src/: data_collection.py, data_wrangling.py, eda.py, run_sql.py, generate_map.py, train_model.py, create_presentation.py."),
        ("SQL Database & Queries", "data/spacex.db (SQLite database) and sql/queries.sql (12 business intelligence queries)."),
        ("Geospatial & Dashboard", "visuals/folium/launch_sites_map.html (interactive map) and dashboard/app.py (Plotly Dash web application)."),
        ("Final Presentation PDF", "presentation/spacex_capstone.pdf (Exported directly as .pdf complying with IBM Capstone rubric)."),
        ("Academic Program", "IBM Data Science Professional Certificate | Applied Data Science Capstone Final Evaluation.")
    ]
    for r_title, r_desc in ref_details:
        p = tf23.add_paragraph()
        p.text = f"✔  {r_title}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = GREEN_ACCENT
        run = p.add_run()
        run.text = r_desc
        run.font.bold = False
        run.font.size = Pt(8.5)
        run.font.color.rgb = DARK_GRAY

    prs.save(pptx_path)
    logging.info(f"Saved complete 23-slide PowerPoint to {pptx_path}")
    return pptx_path


def export_pdf_via_powerpoint(pptx_path, pdf_path):
    """Uses PowerPoint COM automation on Windows to generate a 100% faithful high-fidelity PDF."""
    try:
        import win32com.client
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        abs_pptx = os.path.abspath(pptx_path)
        abs_pdf = os.path.abspath(pdf_path)
        presentation = powerpoint.Presentations.Open(abs_pptx, WithWindow=False)
        # 32 = ppSaveAsPDF
        presentation.SaveAs(abs_pdf, 32)
        presentation.Close()
        powerpoint.Quit()
        logging.info(f"Successfully exported PPTX to PDF via PowerPoint COM: {pdf_path}")
        return True
    except Exception as e:
        logging.warning(f"PowerPoint COM export encountered an issue: {e}")
        return False


def create_speaker_notes():
    notes_path = os.path.join(PRESENTATION_DIR, "speaker_notes.md")
    content = f"""# SpaceX Falcon 9 First Stage Landing Prediction: Complete Presentation Speaker Script

This document provides a beginner-friendly, slide-by-slide presentation script for delivering your 23-slide capstone presentation.

---

### Slide 1: Title Slide & Project Overview
"Good morning, everyone. Welcome to my presentation on the IBM Data Science Professional Certificate Capstone Project: SpaceX Falcon 9 First Stage Landing Prediction. In this project, I built an end-to-end data science and machine learning pipeline that collects, wrangles, visualizes, and models historical SpaceX Falcon 9 launches to predict whether a booster's first stage will land successfully. All source code, completed Jupyter notebooks, SQL scripts, interactive dashboards, and datasets are hosted in my GitHub repository at {GITHUB_REPO_URL}."

---

### Slide 2: Executive Summary (Question 3)
"To begin with an executive summary: Falcon 9 launches cost roughly $62 million, whereas competitor launches frequently exceed $165 million. That staggering $103 million savings is made possible entirely by recovering and reusing the first-stage rocket booster. In this project, I analyzed 90 historical launches, where the overall landing success rate was 66.7%. Through exploratory data analysis, we uncovered a steep operational learning curve where landing success improved from 0% in early test years to over 84% in modern flights. Using machine learning, my best models—specifically tuned K-Nearest Neighbors and Logistic Regression—achieved an 83.33% accuracy rate and an 0.889 F1-score on held-out test data."

---

### Slide 3: Introduction & Business Problem (Question 4)
"Why does this matter commercially? When a rocket launches into space, the first-stage booster represents approximately 70% of the entire vehicle's manufacturing cost—roughly $30 million to $40 million. Historically, all rockets were expendable, discarded into the ocean after a single flight. By recovering boosters via drone ships or ground pads, SpaceX can reuse them multiple times and offer massive commercial discounts. For competitor launch providers or commercial satellite operators bidding on launch contracts, knowing in advance whether SpaceX will recover the booster allows them to predict SpaceX's pricing flexibility and calculate competitive bid margins."

---

### Slide 4: Project Architecture & Pipeline Flow (Question 14)
"Slide 4 illustrates our 5-tier project architecture. The pipeline begins with data ingestion via the SpaceX REST API v4 and Wikipedia web scraping, flows into data wrangling where we impute missing payload values and construct our binary target variable, transitions to analytical engines in SQLite, Folium, and Plotly Dash, and culminates in supervised machine learning classification. To ensure strict data integrity and prevent data leakage, feature scaling is fitted strictly on the 80% training split, keeping the 20% test partition completely held out."

---

### Slide 5: Data Collection Methodology & Lab Links (Question 5)
"For data collection, I extracted data from two complementary sources. First, I queried the public SpaceX REST API v4 past launches endpoint, unpacking nested JSON objects for payload masses, launch complexes, booster serial numbers, and core landing attempts. Second, I used BeautifulSoup to scrape historical Falcon 9 launch tables from Wikipedia, parsing 321 tabular flight records. Both completed Jupyter notebooks—Lab 1 for the API and Lab 2 for web scraping—are accessible via the direct GitHub links shown on the slide."

---

### Slide 6: Data Wrangling Methodology & Lab Link (Question 5)
"In the data wrangling phase (Lab 3), I audited the dataset for missing values. Missing payload masses in early test flights were imputed using the dataset mean of 6,104.95 kilograms. Next, I constructed our binary target variable, Class. If a booster achieved a successful touchdown on an Autonomous Spaceport Drone Ship, a ground pad, or controlled ocean water, Class was assigned 1. If the booster crashed, missed, or was expended without recovery, Class was assigned 0. Across our 90 flights, 60 were successful landings and 30 were failures, yielding a 66.7% baseline success rate. Finally, categorical variables were one-hot encoded into an 80-feature matrix for machine learning."

---

### Slide 7: Exploratory Data Analysis Methodology & Hypotheses (Question 6)
"In the exploratory data analysis phase (Lab 4), I formulated four core hypotheses: First, does booster landing success improve over time as SpaceX iterates on avionics and grid fin control? Second, do launch sites exhibit divergent success rates due to differing orbital azimuths? Third, does heavier payload mass reduce fuel reserves needed for landing burns? And fourth, do deep high-energy orbits like GTO show lower recovery rates than Low Earth Orbit? We used Pandas, Matplotlib, and Seaborn to test these hypotheses across 10 detailed visualizations."

---

### Slide 8: EDA Tasks 1 & 2: Launch Site vs Flight Number & Payload Mass (Question 8)
"On Slide 8, we evaluate IBM Capstone EDA Tasks 1 and 2. Task 1 on the left reveals that Cape Canaveral SLC 40 absorbed all early flights from 1 to 25 with experimental failures. Kennedy Space Center entered service around Flight 30 with predominantly successful touchdowns. Task 2 on the right demonstrates that heavy payloads exceeding 10,000 kilograms are launched exclusively from Florida complexes, whereas California's Vandenberg complex handles lighter payloads under 10,000 kg."

---

### Slide 9: EDA Tasks 3 & 4: Orbit Success Rate & Flight Number (Question 8)
"Slide 9 displays EDA Tasks 3 and 4. Task 3 shows that high-altitude orbits like ES-L1, GEO, HEO, and SSO achieved a 100% landing success rate, whereas GTO achieved only 51.8% success due to extreme re-entry velocities. Task 4 illustrates flight numbers versus orbit types: while early GTO and ISS flights experienced landing crashes, later flights beyond Flight 50 achieved near-perfect recovery across all orbits."

---

### Slide 10: EDA Tasks 5 & 6: Payload vs Orbit & Yearly Success Trend (Question 8)
"Slide 10 highlights EDA Tasks 5 and 6. Task 5 shows that heavy Starlink payloads are concentrated in Very Low Earth Orbit (VLEO) and achieved high recovery rates. Task 6 displays the yearly success trend line: landing success rose from 0% between 2010 and 2013, to 33.3% in 2014-2015, surging past 80% in 2017, and reaching 84.2% in 2020. The introduction of Block 5 boosters in 2018 established sustained high reliability."

---

### Slide 11: EDA Cadence & Overall Success Distribution (Question 8)
"Slide 11 reviews overall operational growth. Annual launch cadence expanded 19-fold, from 1 launch in 2010 to 19 launches in 2020. The donut chart on the right depicts our overall binary target balance: 60 successful landings, or 66.7%, versus 30 failed or expended attempts, or 33.3%."

---

### Slide 12: SQL Tasks 1 to 4: Launch Complexes & Payload Statistics (Question 9)
"Moving to SQL data analysis in Lab 5: Task 1 identified our three distinct launch sites: CCAFS SLC 40, KSC LC 39A, and VAFB SLC 4E. Task 2 queried the first five Cape Canaveral flights. Task 3 calculated total payload lifted: CCAFS lifted over 305,000 kilograms across 55 flights. Task 4 determined the average payload across all 90 flights as 6,105 kg, ranging from 350 kg to 15,600 kg."

---

### Slide 13: SQL Tasks 5 to 7: Milestones & Outcome Distributions (Question 9)
"Continuing SQL analysis: Task 5 identified the exact date of the world's first successful ground pad landing: December 22, 2015, by booster B1019 at Cape Canaveral. Task 6 queried drone ship successes carrying 4,000 to 6,000 kg, identifying boosters B1022, B1026, and B1048. Task 7 aggregated the 60 successful versus 30 failed mission outcomes."

---

### Slide 14: SQL Tasks 8 to 10: Max Payload, 2015 Outcomes & Rankings (Question 9)
"Completing our SQL queries: Task 8 identified Starlink Block 5 boosters carrying the maximum payload of 15,600 kg. Task 9 revealed monthly outcomes in 2015, showing experimental ocean splashes leading to the December RTLS breakthrough. Task 10 ranked recovery modes: Drone Ship landings (True ASDS) proved to be SpaceX's workhorse with 41 successful recoveries."

---

### Slide 15: Geospatial Analysis: Folium Launch Sites, Markers & Counts (Question 10)
"Slide 15 presents our interactive Folium map from Lab 6. We mapped all three launch complexes: CCAFS with 55 launches and a 60% success rate; KSC with 22 launches and a 77.3% success rate; and VAFB with 13 launches and a 76.9% success rate. The MarkerCluster plugin groups all 90 individual launches with green markers for successes and red markers for failures."

---

### Slide 16: Folium Distance & Proximity Analysis (Question 10)
"Slide 16 details our Haversine geodesic distance analysis. Every launchpad is situated within 0.95 to 1.5 kilometers of open water, ensuring that ascent failures drop harmlessly into the ocean. The complexes sit within 1 to 2 km of rail lines and highways for booster transport, while maintaining a safe 15 to 35 km buffer from urban population centers like Titusville and Lompoc."

---

### Slide 17: Interactive Dashboard: Plotly Dash (Question 11)
"Slide 17 highlights our interactive Plotly Dash analytics console from Lab 7. The dashboard allows users to dynamically filter flights by launch site, adjust payload mass from 0 to 16,000 kg, and toggle outcome categories. Reactive callbacks instantly update summary KPI cards, donut distributions, scatter plots, and yearly cadence bars."

---

### Slide 18: Predictive Analysis: Machine Learning Methodology (Question 7)
"Moving to predictive modeling in Lab 8, we formulated the task as a binary classification problem. To strictly prevent data leakage, we split our 80-feature dataset into an 80% training set and a 20% test set using stratified sampling, fitting StandardScaler strictly on the training partition. We implemented 10-fold stratified cross-validation inside GridSearchCV to tune Logistic Regression, Support Vector Machines, Decision Trees, and K-Nearest Neighbors."

---

### Slide 19: Model Comparison Table & Hyperparameters (Question 12)
"Slide 19 presents our empirical model comparison table. Both tuned K-Nearest Neighbors and Logistic Regression achieved the highest performance on our held-out test data, with 83.33% accuracy and an F1-score of 0.889. The optimal hyperparameters found by GridSearchCV are listed on the slide for each of the four algorithms."

---

### Slide 20: Confusion Matrix Results & Error Analysis (Question 12)
"Slide 20 provides the confusion matrix breakdown for all four models on the held-out test set of 18 flights. Both KNN and Logistic Regression correctly classified 12 out of 12 successful landings (100% recall) and 3 out of 6 failed attempts. Crucially, they produced ZERO False Negatives, meaning no successful booster recovery was missed."

---

### Slide 21: Feature Importance & Decision Drivers (Question 14 & 15)
"Slide 21 examines feature importance. GridFins and LandingLeg deployment are the strongest positive indicators of booster recovery. Transitioning to Block 5 boosters dramatically increased recovery odds. Conversely, heavy payloads destined for high-energy GTO orbits negatively impact recovery probability due to propellant limitations."

---

### Slide 22: Conclusions, Innovation & Future Roadmap (Question 13, 14, 15)
"In conclusion, booster reuse provides SpaceX with an insurmountable commercial cost advantage of roughly $103 million per flight. Our models demonstrate that booster recovery can be accurately predicted prior to launch. Key innovative findings included the 2,000 to 5,300 kg payload sweet spot and quantifying coastline safety buffer zones. For future work, incorporating real-time ocean wave heights and drone ship accelerometer telemetry could further refine landing predictions."

---

### Slide 23: References & Project Submission (Question 1 & 2)
"Thank you very much for your time. All source code, completed notebooks, SQL queries, interactive maps, dashboards, and deliverables are fully documented and accessible at my GitHub repository: {GITHUB_REPO_URL}. I am now glad to answer any questions."
"""
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Saved speaker notes to {notes_path}")
    return notes_path


if __name__ == "__main__":
    print("=== Generating SpaceX Capstone 23-Slide Presentation Deliverables ===")
    pptx_file = create_powerpoint()
    
    # Export PDF via native PowerPoint COM
    pdf_file = os.path.join(PRESENTATION_DIR, "spacex_capstone.pdf")
    pdf_file1 = os.path.join(PRESENTATION_DIR, "spacex_capstone1.pdf")
    success = export_pdf_via_powerpoint(pptx_file, pdf_file)
    if success:
        try:
            shutil.copyfile(pdf_file, pdf_file1)
            logging.info(f"Synced updated PDF to {pdf_file1}")
        except Exception as e:
            logging.warning(f"Could not sync spacex_capstone1.pdf: {e}")
            
    create_speaker_notes()
    print("=== All 23-Slide Deliverables Successfully Generated ===")
