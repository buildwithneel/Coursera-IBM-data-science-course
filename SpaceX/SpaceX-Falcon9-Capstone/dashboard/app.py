"""
SpaceX Falcon 9 Landing Prediction - Interactive Analytics Dashboard
=====================================================================
A professional, reactive Plotly Dash application providing real-time
exploration of SpaceX Falcon 9 launch performance, booster landing outcomes,
payload capacity limits, and launch complex statistics.

To run:
    python dashboard/app.py
Then open http://127.0.0.1:8050 in your web browser.
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

# Load processed SpaceX dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "dataset_part_2.csv")
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Processed dataset not found at {DATA_PATH}. Run src/data_wrangling.py first.")

df = pd.read_csv(DATA_PATH)
df["ClassLabel"] = df["Class"].map({1: "Successful Landing", 0: "Failed / Expended"})

# Unique launch sites for dropdown
site_options = [{"label": "All Launch Sites", "value": "ALL"}]
for site in sorted(df["LaunchSite"].unique()):
    site_options.append({"label": site, "value": site})

min_payload = int(df["PayloadMass"].min())
max_payload = int(df["PayloadMass"].max())

# Initialize Dash application
app = Dash(__name__, title="SpaceX Falcon 9 Launch Analytics")
server = app.server

# Modern dark aerospace theme styling
DARK_BG = "#0B132B"
CARD_BG = "#1C2541"
TEXT_COLOR = "#FFFFFF"
ACCENT_BLUE = "#48CAE4"
ACCENT_GREEN = "#06D6A0"
ACCENT_RED = "#EF476F"
ACCENT_ORANGE = "#FF9F1C"

card_style = {
    "backgroundColor": CARD_BG,
    "borderRadius": "10px",
    "padding": "18px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
    "marginBottom": "20px"
}

app.layout = html.Div(
    style={"backgroundColor": DARK_BG, "color": TEXT_COLOR, "fontFamily": "Segoe UI, sans-serif", "padding": "25px", "minHeight": "100vh"},
    children=[
        # Title and Header Banner
        html.Div(
            style={"textAlign": "center", "marginBottom": "25px"},
            children=[
                html.H1("🚀 SpaceX Falcon 9 First Stage Landing Analytics Dashboard", style={"color": ACCENT_BLUE, "margin": "0 0 10px 0"}),
                html.P(
                    "Interactive Mission Operations and Predictive Analytics Control Center",
                    style={"color": "#A0AEC0", "fontSize": "16px", "margin": "0"}
                )
            ]
        ),

        # Control Panel: Filters & Sliders
        html.Div(
            style=card_style,
            children=[
                html.H3("⚙️ Mission Control Filters", style={"color": ACCENT_ORANGE, "marginTop": "0"}),
                html.Div(
                    style={"display": "flex", "flexWrap": "wrap", "gap": "20px"},
                    children=[
                        # Launch Site Dropdown
                        html.Div(
                            style={"flex": "1", "minWidth": "250px"},
                            children=[
                                html.Label("Select Launch Site:", style={"fontWeight": "bold", "marginBottom": "6px", "display": "block"}),
                                dcc.Dropdown(
                                    id="site-dropdown",
                                    options=site_options,
                                    value="ALL",
                                    placeholder="Select a Launch Site",
                                    searchable=True,
                                    style={"color": "#000"}
                                )
                            ]
                        ),
                        # Outcome Filter
                        html.Div(
                            style={"flex": "1", "minWidth": "250px"},
                            children=[
                                html.Label("Landing Outcome Filter:", style={"fontWeight": "bold", "marginBottom": "6px", "display": "block"}),
                                dcc.RadioItems(
                                    id="outcome-radio",
                                    options=[
                                        {"label": " All Outcomes  ", "value": "ALL"},
                                        {"label": " Success Only  ", "value": "1"},
                                        {"label": " Failure Only", "value": "0"}
                                    ],
                                    value="ALL",
                                    inline=True,
                                    style={"paddingTop": "8px"}
                                )
                            ]
                        ),
                        # Payload Slider
                        html.Div(
                            style={"flex": "2", "minWidth": "320px"},
                            children=[
                                html.Label("Payload Mass Range (kg):", style={"fontWeight": "bold", "marginBottom": "6px", "display": "block"}),
                                dcc.RangeSlider(
                                    id="payload-slider",
                                    min=0,
                                    max=16000,
                                    step=500,
                                    marks={0: "0 kg", 4000: "4k kg", 8000: "8k kg", 12000: "12k kg", 16000: "16k kg"},
                                    value=[min_payload, max_payload]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # KPI Metric Cards
        html.Div(
            id="kpi-container",
            style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "15px", "marginBottom": "20px"}
        ),

        # Visualizations Grid
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
            children=[
                # Chart 1: Success Rate Pie / Distribution
                html.Div(
                    style=card_style,
                    children=[
                        html.H4("🎯 Landing Success Distribution", style={"color": ACCENT_BLUE, "marginTop": "0"}),
                        dcc.Graph(id="success-pie-chart")
                    ]
                ),
                # Chart 2: Payload vs Landing Outcome Scatter
                html.Div(
                    style=card_style,
                    children=[
                        html.H4("⚖️ Payload Mass vs Landing Outcome", style={"color": ACCENT_BLUE, "marginTop": "0"}),
                        dcc.Graph(id="success-payload-scatter-chart")
                    ]
                )
            ]
        ),

        # Chart 3: Historical Launch Trend & Trajectory Over Time
        html.Div(
            style=card_style,
            children=[
                html.H4("📈 Yearly Launch Cadence & Success Volume", style={"color": ACCENT_BLUE, "marginTop": "0"}),
                dcc.Graph(id="yearly-trend-chart")
            ]
        ),

        # Footer
        html.Div(
            style={"textAlign": "center", "color": "#718096", "fontSize": "13px", "marginTop": "20px"},
            children=[
                html.P("IBM Data Science Professional Certificate Capstone | SpaceX Falcon 9 Analysis")
            ]
        )
    ]
)


# Callback to update KPIs and Visualizations
@app.callback(
    [
        Output("kpi-container", "children"),
        Output("success-pie-chart", "figure"),
        Output("success-payload-scatter-chart", "figure"),
        Output("yearly-trend-chart", "figure")
    ],
    [
        Input("site-dropdown", "value"),
        Input("outcome-radio", "value"),
        Input("payload-slider", "value")
    ]
)
def update_dashboard(selected_site, selected_outcome, payload_range):
    # Filter dataset
    low, high = payload_range
    filtered_df = df[(df["PayloadMass"] >= low) & (df["PayloadMass"] <= high)]

    if selected_site != "ALL":
        filtered_df = filtered_df[filtered_df["LaunchSite"] == selected_site]

    if selected_outcome != "ALL":
        filtered_df = filtered_df[filtered_df["Class"] == int(selected_outcome)]

    # Compute KPIs
    total_selected = len(filtered_df)
    total_success = int(filtered_df["Class"].sum()) if total_selected > 0 else 0
    total_failure = total_selected - total_success
    success_rate = (total_success / total_selected * 100) if total_selected > 0 else 0.0
    avg_payload = filtered_df["PayloadMass"].mean() if total_selected > 0 else 0.0

    kpi_cards = [
        html.Div(
            style={"backgroundColor": "#132A52", "padding": "14px", "borderRadius": "8px", "textAlign": "center", "border": f"1px solid {ACCENT_BLUE}"},
            children=[
                html.Div("Total Launches Selected", style={"color": "#CBD5E0", "fontSize": "12px"}),
                html.Div(f"{total_selected}", style={"color": "#FFF", "fontSize": "26px", "fontWeight": "bold", "marginTop": "4px"})
            ]
        ),
        html.Div(
            style={"backgroundColor": "#132A52", "padding": "14px", "borderRadius": "8px", "textAlign": "center", "border": f"1px solid {ACCENT_GREEN}"},
            children=[
                html.Div("Landing Success Rate", style={"color": "#CBD5E0", "fontSize": "12px"}),
                html.Div(f"{success_rate:.1f}%", style={"color": ACCENT_GREEN, "fontSize": "26px", "fontWeight": "bold", "marginTop": "4px"})
            ]
        ),
        html.Div(
            style={"backgroundColor": "#132A52", "padding": "14px", "borderRadius": "8px", "textAlign": "center", "border": f"1px solid {ACCENT_ORANGE}"},
            children=[
                html.Div("Successful Recoveries", style={"color": "#CBD5E0", "fontSize": "12px"}),
                html.Div(f"{total_success} / {total_selected}", style={"color": ACCENT_ORANGE, "fontSize": "26px", "fontWeight": "bold", "marginTop": "4px"})
            ]
        ),
        html.Div(
            style={"backgroundColor": "#132A52", "padding": "14px", "borderRadius": "8px", "textAlign": "center", "border": "1px solid #9C27B0"},
            children=[
                html.Div("Average Payload Mass", style={"color": "#CBD5E0", "fontSize": "12px"}),
                html.Div(f"{avg_payload:,.0f} kg", style={"color": "#CE93D8", "fontSize": "26px", "fontWeight": "bold", "marginTop": "4px"})
            ]
        )
    ]

    # Chart 1: Pie / Donut Chart
    if selected_site == "ALL":
        # Group by site
        site_success = filtered_df.groupby("LaunchSite")["Class"].sum().reset_index()
        fig_pie = px.pie(
            site_success,
            values="Class",
            names="LaunchSite",
            title="Total Successful Landings by Launch Site",
            color_discrete_sequence=["#00B4D8", "#0077B6", "#90E0EF"],
            hole=0.4
        )
    else:
        # Success vs Failure for selected site
        outcome_df = filtered_df["ClassLabel"].value_counts().reset_index()
        outcome_df.columns = ["Outcome", "Count"]
        fig_pie = px.pie(
            outcome_df,
            values="Count",
            names="Outcome",
            title=f"Success vs Failure Breakdown for {selected_site}",
            color="Outcome",
            color_discrete_map={"Successful Landing": "#06D6A0", "Failed / Expended": "#EF476F"},
            hole=0.4
        )

    fig_pie.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font_color=TEXT_COLOR,
        margin=dict(t=40, b=20, l=20, r=20)
    )

    # Chart 2: Payload vs Outcome Scatter Plot
    fig_scatter = px.scatter(
        filtered_df,
        x="PayloadMass",
        y="FlightNumber",
        color="ClassLabel",
        hover_data=["LaunchSite", "Orbit", "Serial"],
        title="Correlation Between Payload Mass, Flight Sequence & Landing Success",
        labels={"PayloadMass": "Payload Mass (kg)", "FlightNumber": "Flight Number", "ClassLabel": "Outcome"},
        color_discrete_map={"Successful Landing": "#06D6A0", "Failed / Expended": "#EF476F"},
        size=[12] * len(filtered_df) if len(filtered_df) > 0 else []
    )
    fig_scatter.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor="#111B30",
        font_color=TEXT_COLOR,
        xaxis=dict(gridcolor="#233554"),
        yaxis=dict(gridcolor="#233554"),
        margin=dict(t=40, b=20, l=20, r=20)
    )

    # Chart 3: Yearly Trend Bar Chart
    yearly_df = filtered_df.groupby(["Year", "ClassLabel"]).size().reset_index(name="Launches")
    fig_trend = px.bar(
        yearly_df,
        x="Year",
        y="Launches",
        color="ClassLabel",
        barmode="stack",
        title="Yearly Falcon 9 Launch Volume & Landing Success Evolution",
        color_discrete_map={"Successful Landing": "#06D6A0", "Failed / Expended": "#EF476F"}
    )
    fig_trend.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor="#111B30",
        font_color=TEXT_COLOR,
        xaxis=dict(gridcolor="#233554", dtick=1),
        yaxis=dict(gridcolor="#233554"),
        margin=dict(t=40, b=20, l=20, r=20)
    )

    return kpi_cards, fig_pie, fig_scatter, fig_trend


if __name__ == "__main__":
    print("Launching SpaceX Falcon 9 Analytics Dashboard...")
    print("Open your browser and navigate to: http://127.0.0.1:8050")
    app.run(debug=False, port=8050)
