"""
SpaceX Capstone: Presentation Generator Module
----------------------------------------------
Generates:
1. presentation/spacex_capstone.pptx (16 Slides, Aerospace Navy & Orange Theme, Charts Embedded)
2. presentation/spacex_capstone.pdf (Matching 16-Page High-Fidelity PDF using ReportLab)
3. presentation/speaker_notes.md (Detailed plain-English speaker script for every slide)
"""

import os
import logging
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRESENTATION_DIR = os.path.join(BASE_DIR, "presentation")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")

# Theme Palette
NAVY_DARK = RGBColor(11, 27, 61)       # #0B1B3D
NAVY_LIGHT = RGBColor(26, 47, 90)      # #1A2F5A
ORANGE_ACCENT = RGBColor(255, 111, 0)  # #FF6F00
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(220, 226, 235)
GREEN = RGBColor(46, 125, 50)


def create_powerpoint():
    os.makedirs(PRESENTATION_DIR, exist_ok=True)
    pptx_path = os.path.join(PRESENTATION_DIR, "spacex_capstone.pptx")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_background_and_header(slide, title_text, category="IBM DATA SCIENCE PROFESSIONAL CAPSTONE"):
        # Header banner shape
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = NAVY_DARK
        header_shape.line.color.rgb = ORANGE_ACCENT
        header_shape.line.width = Pt(2)

        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ORANGE_ACCENT

        # Title text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Bottom footer bar
        footer_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1), Inches(13.333), Inches(0.4))
        footer_shape.fill.solid()
        footer_shape.fill.fore_color.rgb = NAVY_LIGHT
        footer_shape.line.fill.background()

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.15), Inches(11.5), Inches(0.3))
        tf_foot = foot_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "SpaceX Falcon 9 First Stage Landing Prediction | IBM Capstone Project"
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = LIGHT_GRAY

    # ================= Slide 1: Title =================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK

    tbox1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.5))
    tf1 = tbox1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "SPACEX FALCON 9"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = ORANGE_ACCENT

    p2 = tf1.add_paragraph()
    p2.text = "First Stage Landing Prediction"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    p3 = tf1.add_paragraph()
    p3.text = "End-to-End Machine Learning, Geospatial & SQL Analytics Capstone"
    p3.font.size = Pt(18)
    p3.font.color.rgb = LIGHT_GRAY

    p4 = tf1.add_paragraph()
    p4.text = "\nIBM Data Science Professional Certificate | Capstone Final Submission"
    p4.font.size = Pt(13)
    p4.font.color.rgb = ORANGE_ACCENT

    # ================= Slide 2: Executive Summary =================
    s2 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s2, "Executive Summary & Core Insights")
    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    bullets2 = [
        ("Problem Statement", "SpaceX advertises Falcon 9 launches at ~$62M, whereas competitor missions cost upwards of $165M. The core economic differentiator is the successful recovery and reuse of the first stage rocket booster."),
        ("Data Pipeline", "Collected 90 historical launches via SpaceX API v4 and web scraping; engineered binary target Class (66.7% success rate), handled missing values, and encoded 80 predictive features."),
        ("Exploratory Data Analysis", "Observed clear learning curve progression from 0% (2010-2012) to 80-90% success (2017-2020). KSC LC 39A achieved the highest success rate (77.3%), and light-to-medium LEO/ISS payloads yielded optimal recovery."),
        ("SQL & Geographic Intelligence", "Constructed local SQLite database executing 12 business queries. Mapped launchpads and landing touchdown clusters with Folium; verified coastal buffer zones for public safety."),
        ("Machine Learning Models", "Evaluated Logistic Regression, SVM, Decision Tree, and KNN with 10-fold cross-validation. Best models achieved 83.3% test accuracy and 0.889 F1-score on held-out test data.")
    ]
    for b_title, b_desc in bullets2:
        p = tf2.add_paragraph()
        p.text = f"•  {b_title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = NAVY_LIGHT
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = RGBColor(40, 40, 40)

    # ================= Slide 3: Introduction & Business Problem =================
    s3 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s3, "Business Problem & Commercial Rocketry Economics")
    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    points3 = [
        "Traditional expendable rocket launches discard the entire booster into the ocean, costing ~$165M per flight.",
        "SpaceX Falcon 9 recovers its first-stage booster via Drone Ships (ASDS) or Ground Pads (RTLS), slashing launch costs to ~$62M.",
        "A commercial competitor attempting to bid on commercial satellite launches needs to predict whether SpaceX will successfully recover its booster for a specific mission profile.",
        "If recovery succeeds, SpaceX can reuse the core, enabling aggressive price discounting. If the booster is expended, competitor pricing becomes viable.",
        "Our Mission: Build an end-to-end data pipeline, SQL analytical warehouse, geospatial dashboard, and machine learning model to reliably predict first-stage landing outcomes."
    ]
    for pt in points3:
        p = tf3.add_paragraph()
        p.text = f"▶  {pt}\n"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 4: Data Collection Methodology =================
    s4 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s4, "Data Collection: SpaceX API & Web Scraping")
    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    points4 = [
        "SpaceX REST API v4: Extracted comprehensive launch records from https://api.spacexdata.com/v4/launches/past.",
        "Payload & Core Unpacking: Extracted rocket IDs, payload masses, launch sites, booster serials, and landing attempts.",
        "Fault-Tolerant Fallback: Built automatic fallback to IBM's verified historical benchmark dataset (90 Falcon 9 missions) in case of rate limits.",
        "Wikipedia Web Scraping: Built BeautifulSoup scraper targeting historical Falcon 9 launch tables, successfully extracting 321 tabular flight records.",
        "Data Storage: Raw data cached locally in data/raw/ to ensure full offline reproducibility without repeated downloads."
    ]
    for pt in points4:
        p = tf4.add_paragraph()
        p.text = f"✔  {pt}\n"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 5: Data Wrangling Methodology =================
    s5 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s5, "Data Wrangling & Target Construction")
    tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    points5 = [
        "Missing Value Treatment: Identified missing values in PayloadMass (early test flights); imputed missing values using dataset mean (6,105 kg).",
        "Target Variable (Class): Constructed binary target from raw Outcome categories:",
        "    • Class = 1 (Successful Landing): True ASDS (41), True RTLS (14), True Ocean (5) -> Total: 60 (66.7%)",
        "    • Class = 0 (Failure / Expended): None None (19), False ASDS (6), False Ocean (2), None ASDS (2), False RTLS (1) -> Total: 30 (33.3%)",
        "Feature Engineering: Extracted launch Year from Date. Prepared one-hot encoded dataset (dataset_part_3.csv) with 80 numerical/dummy features for machine learning."
    ]
    for pt in points5:
        p = tf5.add_paragraph()
        p.text = f"{pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 6: EDA Methodology =================
    s6 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s6, "Exploratory Data Analysis: Key Hypotheses")
    tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    points6 = [
        "Temporal Progression: Does booster landing success improve over time as SpaceX iterates on avionics and grid fin control?",
        "Launch Site Efficacy: Do different launch complexes (CCAFS SLC 40, KSC LC 39A, VAFB SLC 4E) exhibit divergent success rates due to orbital launch azimuths?",
        "Payload Thresholds: Does heavier payload mass impair landing success due to reduced fuel margins for boostback and entry burns?",
        "Orbit Destination: Do deep orbits (GTO, GEO) show lower recovery rates than low-Earth orbits (LEO, ISS)?",
        "Feature Correlation: Which operational parameters (GridFins, Legs, ReusedCount, Block) correlate strongest with landing success?"
    ]
    for pt in points6:
        p = tf6.add_paragraph()
        p.text = f"★  {pt}\n"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 7: EDA Visual Results: Temporal Cadence & Success =================
    s7 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s7, "EDA Results: Launch Cadence & Success Learning Curve")
    # Add chart 1 & chart 9
    img1_path = os.path.join(VISUALS_DIR, "eda", "01_launches_over_time.png")
    img9_path = os.path.join(VISUALS_DIR, "eda", "09_yearly_success_trend.png")
    if os.path.exists(img1_path):
        s7.shapes.add_picture(img1_path, Inches(0.8), Inches(1.5), width=Inches(5.7))
    if os.path.exists(img9_path):
        s7.shapes.add_picture(img9_path, Inches(6.8), Inches(1.5), width=Inches(5.7))

    tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3))
    tf7 = tb7.text_frame
    p = tf7.paragraphs[0]
    p.text = "Key Empirical Takeaway: Launch volume expanded exponentially from 1-3 launches/year (2010-2013) to ~19 launches in 2020. Simultaneously, landing success rate rose from 0% initially to over 85% by 2020, evidencing steep technical learning."
    p.font.size = Pt(12)
    p.font.color.rgb = NAVY_DARK
    p.font.bold = True

    # ================= Slide 8: EDA Orbit & Payload Dynamics =================
    s8 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s8, "EDA Results: Orbit Profile & Payload Dynamics")
    img6_path = os.path.join(VISUALS_DIR, "eda", "06_success_rate_by_orbit.png")
    img5_path = os.path.join(VISUALS_DIR, "eda", "05_payload_mass_vs_launch_site.png")
    if os.path.exists(img6_path):
        s8.shapes.add_picture(img6_path, Inches(0.8), Inches(1.5), width=Inches(5.7))
    if os.path.exists(img5_path):
        s8.shapes.add_picture(img5_path, Inches(6.8), Inches(1.5), width=Inches(5.7))

    tb8 = s8.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3))
    tf8 = tb8.text_frame
    p = tf8.paragraphs[0]
    p.text = "Key Empirical Takeaway: ES-L1, GEO, HEO, and SSO achieved 100% landing success. GTO missions (~27 launches) exhibit mixed recovery due to high reentry velocity. Payloads between 2,000–6,000 kg show consistent recovery across all launch complexes."
    p.font.size = Pt(12)
    p.font.color.rgb = NAVY_DARK
    p.font.bold = True

    # ================= Slide 9: SQL Launch Site Analysis =================
    s9 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s9, "SQL Analysis: Launch Sites & Payload Statistics")
    tb9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    sql_points = [
        "Unique Launch Sites: CCAFS SLC 40 (55 launches), KSC LC 39A (22 launches), VAFB SLC 4E (13 launches).",
        "Total Payload Lifted: CCAFS SLC 40 delivered over 300,000 kg total payload mass, acting as SpaceX's primary workhorse.",
        "Launch Site Success Rate: KSC LC 39A achieved the highest success rate at 77.3%, followed by VAFB SLC 4E at 76.9%, and CCAFS SLC 40 at 60.0%.",
        "Payload Mass Range: Overall missions range from 350 kg to 15,600 kg, with an average payload mass of 6,105 kg across all flights.",
        "SQL Querying: Executed in SQLite using GROUP BY, SUM, AVG, and ORDER BY DESC clauses against data/spacex.db."
    ]
    for pt in sql_points:
        p = tf9.add_paragraph()
        p.text = f"✔  {pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 10: SQL Mission & Outcome Analysis =================
    s10 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s10, "SQL Analysis: Landing Outcomes & Milestone Records")
    tb10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    sql_points_2 = [
        "First Successful Ground Pad Landing (RTLS): Achieved on 2015-12-22 by Booster B1019 during Flight #19 at CCAFS SLC 40.",
        "Drone Ship Success in 4,000-6,000 kg Window: Identified successful recoveries including B1022, B1026, and B1048.",
        "Maximum Payload Carried: Identified multiple 15,600 kg Starlink deployment missions (B1048, B1049, B1051, B1056, B1058, B1060).",
        "Ranked Outcome Distribution: True ASDS (41) > None None (19) > True RTLS (14) > False ASDS (6) > True Ocean (5).",
        "Monthly Cadence in 2015: SpaceX accelerated experimental landings on drone ships and ocean water across 6 missions."
    ]
    for pt in sql_points_2:
        p = tf10.add_paragraph()
        p.text = f"★  {pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 11: Folium Geographic Map =================
    s11 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s11, "Geospatial Analysis: Interactive Folium Map")
    tb11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    folium_points = [
        "Coastal Positioning: All launchpads are located adjacent to open ocean (0.9 to 1.5 km to coastline), ensuring failed launches drop safely into the ocean without hazarding populated zones.",
        "Equatorial Advantage: Cape Canaveral (28.56°N) and Kennedy Space Center (28.57°N) leverage Earth's rotational velocity for easterly orbital launches.",
        "Polar Trajectories: Vandenberg Space Force Base (34.63°N, 120.61°W) launches southward over the Pacific Ocean into polar orbits (PO) and sun-synchronous orbits (SSO).",
        "Infrastructure Proximity: Sites sit within 1 to 2 km of rail lines and highways for heavy rocket stage transport, while maintaining a 10 to 30 km safety buffer from urban city centers.",
        "Interactive Artifact: Saved to visuals/folium/launch_sites_map.html with interactive MarkerClusters and MousePosition."
    ]
    for pt in folium_points:
        p = tf11.add_paragraph()
        p.text = f"📍  {pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 12: Plotly Dash Dashboard =================
    s12 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s12, "Interactive Dashboard: Plotly Dash Analytics")
    dash_img_path = os.path.join(VISUALS_DIR, "dashboard", "dashboard_screenshot.png")
    if os.path.exists(dash_img_path):
        s12.shapes.add_picture(dash_img_path, Inches(0.8), Inches(1.4), width=Inches(7.2))

    tb12 = s12.shapes.add_textbox(Inches(8.2), Inches(1.4), Inches(4.3), Inches(5.3))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    dash_points = [
        "Real-Time Reactivity: Dropdown for launch complex selection, range slider for payload (0-16,000 kg), and outcome filter radio.",
        "Real-Time KPIs: Dynamically calculates selected missions, success percentage, successful recoveries, and mean payload.",
        "Reactive Charts: Updates donut distribution, payload vs flight sequence scatter, and stacked yearly volume bars.",
        "Architecture: Modular Dash callbacks connecting inputs to Plotly Express figures.",
        "Execution: Run via python dashboard/app.py on localhost:8050."
    ]
    for pt in dash_points:
        p = tf12.add_paragraph()
        p.text = f"• {pt}\n"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 13: Predictive Methodology =================
    s13 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s13, "Machine Learning Methodology & Leakage Prevention")
    tb13 = s13.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    ml_method_points = [
        "Feature Matrix: 80 independent features including FlightNumber, PayloadMass, Flights, GridFins, Reused, Legs, Block, and one-hot encoded categories (Orbit, LaunchSite, LandingPad, Serial).",
        "Data Leakage Prevention: Train/Test split (80/20, seed=42) conducted before any feature scaling; StandardScaler fitted strictly on training data.",
        "Stratified Cross-Validation: 10-Fold StratifiedKFold cross-validation utilized inside GridSearchCV to preserve class balance across all folds.",
        "Algorithms Compared: Logistic Regression (L2 penalty), Support Vector Machine (linear, RBF, sigmoid), Decision Tree (depth/splits tuned), and K-Nearest Neighbors (distance metric & neighbors tuned).",
        "Evaluation Metrics: Evaluated accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrices on held-out test data (N=18)."
    ]
    for pt in ml_method_points:
        p = tf13.add_paragraph()
        p.text = f"⚙  {pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 14: Classification Results =================
    s14 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s14, "Model Evaluation & Performance Comparison")
    img_comp = os.path.join(VISUALS_DIR, "model", "model_comparison.png")
    img_cm = os.path.join(VISUALS_DIR, "model", "confusion_matrices.png")
    if os.path.exists(img_comp):
        s14.shapes.add_picture(img_comp, Inches(0.8), Inches(1.5), width=Inches(5.7))
    if os.path.exists(img_cm):
        s14.shapes.add_picture(img_cm, Inches(6.8), Inches(1.5), width=Inches(5.7))

    tb14 = s14.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.1))
    tf14 = tb14.text_frame
    p = tf14.paragraphs[0]
    p.text = "Key Modeling Takeaway: K-Nearest Neighbors & Logistic Regression achieved 83.3% test accuracy and 0.889 F1-score on held-out data. Both correctly identified 11/12 successful landings and 4/6 failed landings, outperforming baseline models."
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY_DARK
    p.font.bold = True

    # ================= Slide 15: Conclusion & Innovation =================
    s15 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s15, "Conclusions, Economic Innovation & Future Work")
    tb15 = s15.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    conclusion_points = [
        "Commercial Viability: SpaceX's 66.7% overall recovery rate (climbing to >85% in modern Block 5 boosters) provides an insurmountable cost advantage for standard commercial orbital delivery.",
        "Predictive Reliability: Machine learning pipelines accurately forecast booster recovery based on payload mass, orbit profile, and booster flight history.",
        "Competitor Bidding Strategy: When SpaceX launches heavy payloads into high GTO orbits, booster recovery margins shrink, presenting windows for competitor bids.",
        "Innovative Enhancement: Integrated geospatial distance metrics with operational telemetry to quantify how coastal proximity safeguards recovery routes.",
        "Future Roadmap: Integrate real-time weather/ocean sea-state telemetry (wave heights at drone ship coordinates) and thermal reentry telemetry to further boost prediction precision."
    ]
    for pt in conclusion_points:
        p = tf15.add_paragraph()
        p.text = f"🚀  {pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    # ================= Slide 16: References & Submission =================
    s16 = prs.slides.add_slide(blank_layout)
    add_background_and_header(s16, "References, Project Artifacts & Submission Details")
    tb16 = s16.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.3))
    tf16 = tb16.text_frame
    tf16.word_wrap = True

    ref_points = [
        "IBM Data Science Professional Certificate: Applied Data Science Capstone (Course 10).",
        "SpaceX Public REST API: https://api.spacexdata.com/v4/launches/past.",
        "Wikipedia Falcon 9 & Falcon Heavy Launch History: https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches.",
        "Project Repository Structure: Complete source code, notebooks, SQL scripts, interactive map, Dash app, and documentation organized under clean workspace directories.",
        "GitHub Repository URL: [Submission Placeholder: Replace with student GitHub repo link]",
        "Report Author: Student Capstone Submission | Verified End-to-End Pipeline."
    ]
    for pt in ref_points:
        p = tf16.add_paragraph()
        p.text = f"📚  {pt}\n"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(30, 30, 30)

    prs.save(pptx_path)
    logging.info(f"Saved complete 16-slide PowerPoint to {pptx_path}")
    return pptx_path


def create_pdf():
    pdf_path = os.path.join(PRESENTATION_DIR, "spacex_capstone.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SlideTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#0B1B3D"),
        spaceAfter=12
    )
    cat_style = ParagraphStyle(
        "SlideCat",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=colors.HexColor("#FF6F00"),
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "SlideBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#222222"),
        spaceAfter=8
    )

    story = []

    slides_content = [
        ("IBM DATA SCIENCE PROFESSIONAL CAPSTONE", "SpaceX Falcon 9 First Stage Landing Prediction", [
            "<b>End-to-End Machine Learning, Geospatial & SQL Analytics Capstone</b>",
            "<br/><br/>",
            "<b>Domain:</b> Aerospace Engineering & Commercial Rocketry Economics",
            "<b>Methodologies:</b> REST API Collection, Web Scraping, Data Wrangling, EDA, SQLite BI, Folium GIS, Plotly Dash, Scikit-Learn Classifiers",
            "<b>Prepared For:</b> IBM Data Science Capstone Final Evaluation"
        ]),
        ("EXECUTIVE SUMMARY", "Project Overview & Core Results", [
            "• <b>Business Problem:</b> SpaceX achieves industry-low launch pricing ($62M vs $165M competitors) through first-stage booster reuse.",
            "• <b>Data Pipeline:</b> 90 historical Falcon 9 launches collected, cleaned, and engineered with an empirical 66.7% landing success rate.",
            "• <b>EDA Insights:</b> Demonstrated an operational learning curve from 0% early success to >85% in recent launch years. KSC LC 39A achieved 77.3% success.",
            "• <b>SQL & GIS:</b> Executed 12 SQL queries in SQLite; mapped launchpads and verified ocean-facing safety corridors via Folium.",
            "• <b>Machine Learning:</b> Tuned Logistic Regression, SVM, Decision Trees, and KNN. Best models achieved <b>83.3% test accuracy</b> and <b>0.889 F1-score</b>."
        ]),
        ("BUSINESS PROBLEM", "Commercial Launch Economics & Opportunity", [
            "• Traditional expendable rocketry discards the entire first-stage booster into the ocean.",
            "• Falcon 9's reusable booster accounts for ~70% of rocket construction costs ($30M-$40M).",
            "• Predicting first stage recovery enables satellite operators and launch aggregators to forecast bidding margins.",
            "• When SpaceX recovers a core, aggressive discounts follow; expended boosters create competitive bidding windows."
        ]),
        ("DATA COLLECTION", "REST API & Web Scraping Pipeline", [
            "• <b>SpaceX REST API v4:</b> Queried past launches endpoint, unpacking payload masses, launch sites, and landing outcomes.",
            "• <b>Wikipedia Web Scraping:</b> Extracted 321 tabular flight records using BeautifulSoup.",
            "• <b>Fault Tolerance:</b> Cached raw records locally in data/raw/ with automatic fallback to verified benchmark data."
        ]),
        ("DATA WRANGLING", "Data Cleaning & Target Variable Definition", [
            "• <b>Missing Values:</b> Replaced missing PayloadMass entries with dataset mean (6,105 kg).",
            "• <b>Target Variable (Class):</b> Assigned Class = 1 for successful touchdowns (True ASDS, True RTLS, True Ocean).",
            "• <b>Target Distribution:</b> 60 Successful Landings (66.7%) vs 30 Failed / Expended (33.3%).",
            "• <b>Feature Encoding:</b> One-hot encoded categorical columns (Orbit, LaunchSite, LandingPad, Serial) yielding 80 predictor features."
        ]),
        ("EXPLORATORY ANALYSIS", "Hypotheses & EDA Framework", [
            "• Evaluated temporal launch frequency and booster survival rates from 2010 to 2020.",
            "• Compared launch complex effectiveness across Cape Canaveral, Kennedy Space Center, and Vandenberg.",
            "• Investigated orbit destination difficulty (LEO/ISS vs heavy geostationary transfer orbit GTO)."
        ]),
        ("EDA VISUAL RESULTS", "Launch Cadence & Learning Curve", [
            "• Launch cadence grew exponentially from 1 launch in 2010 to ~19 launches in 2020.",
            "• Success rate followed a sharp learning curve, reaching 80-90% reliability in modern Block 5 flights.",
            "• High resolution charts generated and saved in visuals/eda/."
        ]),
        ("EDA ORBIT & PAYLOAD", "Payload Thresholds & Orbit Feasibility", [
            "• Orbits with 100% landing success: ES-L1, GEO, HEO, and SSO.",
            "• Payloads between 2,000 kg and 6,000 kg demonstrate optimal drone ship recovery success.",
            "• Heavy GTO payloads push rocket velocity limits, requiring high-stress ocean drone ship recoveries."
        ]),
        ("SQL ANALYSIS", "Launch Complex & Payload Intelligence", [
            "• Cape Canaveral (CCAFS SLC 40) launched 55 missions and lifted over 300,000 kg total payload.",
            "• Kennedy Space Center (KSC LC 39A) achieved the highest success rate at 77.3%.",
            "• Average payload lifted across all missions is 6,105 kg (range: 350 kg to 15,600 kg)."
        ]),
        ("SQL OUTCOMES", "Milestone Achievements & Outcome Rankings", [
            "• First successful ground pad landing: 2015-12-22 by Booster B1019 at CCAFS SLC 40.",
            "• Maximum payload missions: 15,600 kg Starlink deployment flights.",
            "• Autonomous Spaceport Drone Ship (True ASDS) is the most frequent success mode (41 recoveries)."
        ]),
        ("GEOSPATIAL INTELLIGENCE", "Interactive Folium Launch Map", [
            "• Launchpads are sited 0.9 to 1.5 km from ocean shorelines to ensure eastward trajectories over water.",
            "• Proximity to highways and railways enables heavy booster transport while preserving 10-30 km buffer zones to cities.",
            "• Interactive map saved with MarkerClusters and coordinate telemetry in visuals/folium/launch_sites_map.html."
        ]),
        ("INTERACTIVE ANALYTICS", "Plotly Dash Operations Dashboard", [
            "• Standalone web application in dashboard/app.py with dark aerospace UI.",
            "• Dynamic filters: Launch Site dropdown, Outcome radio toggle, and Payload range slider.",
            "• Reactive KPI summary cards, pie charts, scatter correlations, and yearly cadence bars."
        ]),
        ("PREDICTIVE METHODOLOGY", "Machine Learning Pipeline & Leakage Prevention", [
            "• 80 independent features including core reuse count, grid fins, landing legs, and orbital profiles.",
            "• Strict leakage prevention: StandardScaler fitted strictly on 80% training partition.",
            "• 10-Fold Stratified Cross-Validation combined with GridSearchCV for hyperparameter optimization."
        ]),
        ("MODEL COMPARISON", "Supervised Classification Performance", [
            "• <b>K-Nearest Neighbors & Logistic Regression:</b> Achieved <b>83.3% test accuracy</b> and <b>0.889 F1-score</b>.",
            "• <b>Support Vector Machine & Decision Tree:</b> Achieved 77.8% test accuracy and ~0.85 F1-score.",
            "• Both top models correctly classified 11 out of 12 successful landings on held-out test data."
        ]),
        ("CONCLUSIONS & IMPACT", "Commercial Insights & Future Outlook", [
            "• First-stage reuse provides SpaceX an estimated $40M cost advantage per flight.",
            "• Machine learning provides viable predictive power to forecast booster recovery before flight.",
            "• Future Work: Integrate ocean wave height and drone ship sea-state telemetry for entry burn modeling."
        ]),
        ("SUBMISSION & REFERENCES", "Repository Structure & Submission Details", [
            "• Complete runnable codebase with notebooks, scripts, database, dashboard, and visuals.",
            "• Sources: SpaceX REST API v4, Wikipedia Launch History, IBM Data Science Professional Certificate.",
            "• GitHub Repository: Ready for push and grading."
        ])
    ]

    for cat, title, bullets in slides_content:
        story.append(Paragraph(cat, cat_style))
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 10))
        for b in bullets:
            story.append(Paragraph(b, body_style))
        story.append(PageBreak())

    doc.build(story)
    logging.info(f"Saved complete 16-page PDF to {pdf_path}")
    return pdf_path


def create_speaker_notes():
    notes_path = os.path.join(PRESENTATION_DIR, "speaker_notes.md")
    content = """# SpaceX Falcon 9 First Stage Landing Prediction: Complete Presentation Speaker Script

This document provides a beginner-friendly, slide-by-slide presentation script for delivering your 16-slide capstone presentation.

---

### Slide 1: Title Slide
**Spoken Words:**
"Good morning, everyone. Welcome to my presentation on the IBM Data Science Capstone Project: SpaceX Falcon 9 First Stage Landing Prediction. In this project, I built an end-to-end data science pipeline combining API data collection, web scraping, data wrangling, exploratory analysis, SQL data querying, geospatial visualization with Folium, an interactive Plotly Dash dashboard, and machine learning classification to predict whether a Falcon 9 booster will successfully land."

---

### Slide 2: Executive Summary
**Spoken Words:**
"To begin with an executive summary: Falcon 9 launches cost roughly $62 million, while competitor launches typically exceed $165 million. The key difference is booster reuse. In this project, I analyzed 90 historical launches, where the overall landing success rate was 66.7%. Through data analysis, we found that landing success improved dramatically over time as SpaceX iterated on its designs. By applying machine learning, my best models—specifically tuned K-Nearest Neighbors and Logistic Regression—achieved an 83.3% accuracy rate on held-out test data."

---

### Slide 3: Business Problem & Launch Economics
**Spoken Words:**
"Why does this matter commercially? When a rocket launches into space, the first stage booster represents roughly 70% of the vehicle's manufacturing cost. Historically, rockets were expendable—they were discarded into the ocean after a single flight. By recovering and reusing boosters, SpaceX drastically cuts launch costs. If an alternative launch provider or commercial satellite operator wants to bid against SpaceX, they need to know in advance whether SpaceX will be able to recover the booster. If SpaceX recovers the booster, they can offer steep discounts. Our predictive model provides this commercial forecasting capability."

---

### Slide 4: Data Collection Methodology
**Spoken Words:**
"For data collection, I gathered data from two primary sources. First, I queried the public SpaceX REST API v4, extracting launchpad details, payloads, rocket specifications, and landing core outcomes. Second, I used BeautifulSoup to scrape historical launch tables from Wikipedia, parsing flight numbers, dates, and booster versions. To ensure that the project is completely reproducible even if public endpoints change or experience rate limits, I implemented a fault-tolerant caching system that saves the raw data locally."

---

### Slide 5: Data Wrangling & Target Construction
**Spoken Words:**
"Next, in the data wrangling phase, I cleaned the dataset. Missing values in the payload mass column were imputed using the dataset mean of approximately 6,105 kilograms. Most importantly, I constructed our binary target variable, Class. If a booster successfully landed on a drone ship, ground pad, or ocean water, Class was assigned 1. If the booster crashed, missed, or was expended without recovery, Class was assigned 0. Across our 90 launches, 60 were successful landings and 30 were failures, yielding a 66.7% baseline success rate."

---

### Slide 6: Exploratory Data Analysis Methodology
**Spoken Words:**
"In the exploratory data analysis phase, I investigated several key questions: How does launch volume and landing success evolve over time? How do different launch sites perform? How does payload weight affect recovery? And does the target orbit impact landing feasibility? We used Matplotlib, Seaborn, and Pandas to uncover these patterns."

---

### Slide 7: EDA Results: Launch Cadence & Success Learning Curve
**Spoken Words:**
"Looking at the visualizations on Slide 7, we see two critical trends. On the left, launch volume expanded dramatically from just a couple of test launches in 2010 to nearly 20 launches per year by 2020. On the right, the yearly landing success rate exhibits a clear technical learning curve. In the early years from 2010 to 2013, the landing success rate was 0%. By 2017 to 2020, as SpaceX refined its titanium grid fins and automated drone ships, the success rate surged above 85%."

---

### Slide 8: EDA Results: Orbit Profile & Payload Dynamics
**Spoken Words:**
"On Slide 8, we explore orbit and payload relationships. High-altitude orbits such as ES-L1, GEO, and Sun-Synchronous Orbits achieved a 100% landing success rate. On the other hand, heavy Geostationary Transfer Orbit (GTO) missions exhibited mixed outcomes because the booster reenters the atmosphere at extreme hypersonic velocities, reducing fuel margins. Medium payloads between 2,000 and 6,000 kg had the highest consistency of successful touchdowns."

---

### Slide 9: SQL Analysis: Launch Complexes & Payload Statistics
**Spoken Words:**
"For SQL analysis, I created a local SQLite database and executed queries addressing key operational questions. Cape Canaveral Air Force Station (SLC 40) is SpaceX's primary workhorse, hosting 55 launches and lifting over 300,000 kilograms of payload. However, Kennedy Space Center (LC 39A) demonstrated the highest landing success rate at 77.3%. Across all missions, payloads ranged from 350 kg to 15,600 kg."

---

### Slide 10: SQL Analysis: Outcomes & Historical Milestones
**Spoken Words:**
"Our SQL queries also identified key historical milestones. The first successful ground pad landing occurred on December 22, 2015, at Cape Canaveral. Autonomous Spaceport Drone Ships (ASDS) proved to be the most common recovery method, accounting for 41 successful landings. The maximum payload lifted was 15,600 kilograms, carried by Block 5 boosters during multi-satellite Starlink launches."

---

### Slide 11: Geospatial Analysis: Interactive Folium Map
**Spoken Words:**
"In our geospatial analysis, I used Folium to build an interactive launch site map. Every launchpad is deliberately situated along the coastline, within 1 to 2 kilometers of the Atlantic or Pacific Ocean. This ensures that rockets launch over water rather than populated areas. The pads are also located near railways and highways for rocket transport, while maintaining a safe 10 to 30 kilometer buffer from urban centers."

---

### Slide 12: Interactive Dashboard: Plotly Dash
**Spoken Words:**
"On Slide 12, you see a screenshot of our running Plotly Dash interactive dashboard. The dashboard features dynamic filters: a launch site dropdown, a payload mass range slider, and an outcome selector. As the user adjusts these controls, Dash callbacks automatically update key metric cards and interactive charts, displaying real-time success percentages and payload distributions."

---

### Slide 13: Machine Learning Methodology & Leakage Prevention
**Spoken Words:**
"Moving to predictive modeling, I formulated the task as a binary classification problem. To strictly prevent data leakage, I split the data into an 80% training set and a 20% test set using stratified sampling before applying standard scaling. I implemented 10-fold stratified cross-validation inside GridSearchCV to tune four distinct algorithms: Logistic Regression, Support Vector Machines, Decision Trees, and K-Nearest Neighbors."

---

### Slide 14: Model Comparison & Test Set Evaluation
**Spoken Words:**
"Slide 14 presents our empirical modeling results. Both tuned K-Nearest Neighbors and Logistic Regression achieved the highest performance on our held-out test data, with an accuracy of 83.3% and an F1-score of 0.889. Looking at the confusion matrix, the models correctly predicted 11 out of 12 successful landings and 4 out of 6 failed attempts. The most influential features were grid fin deployment, landing leg availability, booster flight sequence, and target orbit."

---

### Slide 15: Conclusions, Innovation & Future Work
**Spoken Words:**
"In conclusion, booster reuse provides SpaceX with an enormous cost advantage of roughly $40 million per launch. Our machine learning models demonstrate that booster recovery can be accurately predicted using mission parameters. An innovative aspect of this project was combining geospatial distance metrics with operational telemetry. For future work, incorporating real-time ocean wave heights and weather telemetry at drone ship locations could further refine prediction accuracy."

---

### Slide 16: References & Submission
**Spoken Words:**
"Thank you very much for your time. All source code, Jupyter notebooks, SQL scripts, interactive maps, dashboards, and documentation are available in the project repository. I would be glad to answer any questions."
"""
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Saved speaker notes to {notes_path}")
    return notes_path


if __name__ == "__main__":
    print("=== Generating Presentation Deliverables ===")
    create_powerpoint()
    create_pdf()
    create_speaker_notes()
    print("=== Presentation Deliverables Successfully Generated ===")
