"""
SpaceX Capstone: Folium Geographic Visualization Module
------------------------------------------------------
Generates an interactive geographic map of SpaceX launch sites,
individual launch touchdown outcomes, and proximity to coastlines,
railways, highways, and urban centers.
Saves to visuals/folium/launch_sites_map.html.
"""

import os
import logging
import math
import folium
from folium.plugins import MarkerCluster, MousePosition
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_part_2.csv")
MAP_OUTPUT_PATH = os.path.join(BASE_DIR, "visuals", "folium", "launch_sites_map.html")

# Launch site exact geographical locations
LAUNCH_SITES = {
    "CCAFS SLC 40": {
        "lat": 28.562302,
        "lon": -80.577356,
        "name": "Cape Canaveral Space Force Station SLC-40",
        "state": "Florida",
        "coastline": (28.56367, -80.56763),
        "highway": (28.56321, -80.57077),
        "railway": (28.57206, -80.58525),
        "city": (28.3922, -80.6077)  # Cape Canaveral City
    },
    "KSC LC 39A": {
        "lat": 28.573255,
        "lon": -80.646895,
        "name": "Kennedy Space Center Launch Complex 39A",
        "state": "Florida",
        "coastline": (28.58022, -80.64242),
        "highway": (28.57351, -80.65545),
        "railway": (28.57390, -80.65420),
        "city": (28.6122, -80.8076)  # Titusville
    },
    "VAFB SLC 4E": {
        "lat": 34.632834,
        "lon": -120.610745,
        "name": "Vandenberg Space Force Base Space Launch Complex 4E",
        "state": "California",
        "coastline": (34.63467, -120.62534),
        "highway": (34.63750, -120.62120),
        "railway": (34.63580, -120.62400),
        "city": (34.6391, -120.4579)  # Lompoc
    }
}


def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formula to compute geodesic distance in kilometers between two GPS coordinates."""
    R = 6373.0  # Approximate radius of Earth in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def build_interactive_map():
    os.makedirs(os.path.dirname(MAP_OUTPUT_PATH), exist_ok=True)
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Initialize map centered on the USA launch corridor
    site_map = folium.Map(location=[30.0, -95.0], zoom_start=5, tiles="OpenStreetMap")

    # Add MousePosition plugin to allow interactive coordinate reading
    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    mouse_position = MousePosition(
        position="topright",
        separator=" | Long: ",
        empty_string="Unavailable",
        lng_first=False,
        num_digits=20,
        prefix="Lat: ",
        lat_formatter=formatter,
        lng_formatter=formatter,
    )
    site_map.add_child(mouse_position)

    # 1. Add Launch Site Markers and Circles
    for site_key, site_info in LAUNCH_SITES.items():
        site_lat = site_info["lat"]
        site_lon = site_info["lon"]
        site_df = df[df["LaunchSite"] == site_key]
        total_launches = len(site_df)
        successes = int(site_df["Class"].sum())
        success_rate = (successes / total_launches * 100) if total_launches > 0 else 0

        # Circular perimeter buffer (10 km radius)
        folium.Circle(
            location=[site_lat, site_lon],
            radius=1000,
            color="#1A237E",
            fill=True,
            fill_color="#3F51B5",
            fill_opacity=0.25,
            tooltip=f"{site_info['name']} (Launch Perimeter)"
        ).add_to(site_map)

        # Site Icon Marker
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 200px;">
            <h4 style="color: #0D47A1; margin-bottom: 4px;">{site_key}</h4>
            <b>Full Name:</b> {site_info['name']}<br>
            <b>State:</b> {site_info['state']}<br>
            <hr style="margin: 5px 0;">
            <b>Total Launches:</b> {total_launches}<br>
            <b>Successful Landings:</b> {successes}<br>
            <b>Success Rate:</b> <span style="color: {'green' if success_rate >= 70 else 'orange'}; font-weight: bold;">{success_rate:.1f}%</span>
        </div>
        """
        folium.Marker(
            location=[site_lat, site_lon],
            icon=folium.Icon(color="darkblue", icon="rocket", prefix="fa"),
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{site_key}: {success_rate:.1f}% Success"
        ).add_to(site_map)

        # 2. Add Proximity Lines to Coastline, Highway, and City
        for feature_name, coords in [
            ("Coastline", site_info["coastline"]),
            ("Highway", site_info["highway"]),
            ("City", site_info["city"])
        ]:
            dist_km = calculate_distance(site_lat, site_lon, coords[0], coords[1])
            line_color = "#00838F" if feature_name == "Coastline" else "#F57C00" if feature_name == "Highway" else "#C2185B"
            
            # Polyline connecting launch site to point of interest
            folium.PolyLine(
                locations=[[site_lat, site_lon], [coords[0], coords[1]]],
                color=line_color,
                weight=2.5,
                opacity=0.8,
                dash_array="5, 10" if feature_name != "Coastline" else None,
                tooltip=f"{site_key} to {feature_name}: {dist_km:.2f} km"
            ).add_to(site_map)

            # Distance marker at the destination
            folium.Marker(
                location=[coords[0], coords[1]],
                icon=folium.DivIcon(
                    html=f"""<div style="font-size: 10pt; font-weight: bold; color: {line_color}; background: white; padding: 2px 4px; border-radius: 3px; border: 1px solid {line_color}; white-space: nowrap;">{feature_name}: {dist_km:.2f} km</div>"""
                )
            ).add_to(site_map)

    # 3. Add Launch Missions MarkerCluster (Color-coded by Landing Outcome)
    marker_cluster = MarkerCluster(name="Falcon 9 Launches").add_to(site_map)

    for _, row in df.iterrows():
        site_key = row["LaunchSite"]
        base_coords = LAUNCH_SITES.get(site_key, {"lat": row.get("Latitude", 28.56), "lon": row.get("Longitude", -80.57)})
        
        # Slight jitter for missions from the same site to spread nicely in cluster
        lat = base_coords["lat"]
        lon = base_coords["lon"]
        is_success = row["Class"] == 1

        marker_color = "green" if is_success else "red"
        icon_name = "check" if is_success else "times"
        outcome_label = "Successful Landing" if is_success else "Unsuccessful / Expended"

        mission_popup = f"""
        <div style="font-family: Arial, sans-serif; min-width: 180px;">
            <b style="color: {'#2E7D32' if is_success else '#C62828'};">Flight #{row['FlightNumber']} ({row['Serial']})</b><br>
            <b>Date:</b> {row['Date']}<br>
            <b>Payload Mass:</b> {row['PayloadMass']:.1f} kg<br>
            <b>Orbit:</b> {row['Orbit']}<br>
            <b>Site:</b> {site_key}<br>
            <b>Outcome:</b> {row['Outcome']} ({outcome_label})
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color=marker_color, icon=icon_name, prefix="fa"),
            popup=folium.Popup(mission_popup, max_width=250),
            tooltip=f"Flight #{row['FlightNumber']}: {outcome_label}"
        ).add_to(marker_cluster)

    # 4. Add Interactive Legend
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 30px; left: 30px; width: 240px; height: 190px; 
        background-color: white; border: 2px solid #0D47A1; border-radius: 8px;
        z-index: 9999; font-size: 12px; padding: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        font-family: Arial, sans-serif;
    ">
        <b style="color: #0D47A1; font-size: 13px;">SpaceX Map Legend</b><br>
        <hr style="margin: 6px 0;">
        <i class="fa fa-rocket" style="color: #1A237E;"></i>&nbsp; Launch Complex Sites<br>
        <span style="color: green; font-weight: bold;">●</span>&nbsp; Successful Landing (Class 1)<br>
        <span style="color: red; font-weight: bold;">●</span>&nbsp; Failed / Expended Landing (Class 0)<br>
        <span style="color: #00838F; font-weight: bold;">―</span>&nbsp; Coastline Proximity Line<br>
        <span style="color: #F57C00; font-weight: bold;">--</span>&nbsp; Highway Distance<br>
        <span style="color: #C2185B; font-weight: bold;">--</span>&nbsp; Nearest Urban City<br>
    </div>
    """
    site_map.get_root().html.add_child(folium.Element(legend_html))

    site_map.save(MAP_OUTPUT_PATH)
    logging.info(f"Saved interactive Folium launch map to {MAP_OUTPUT_PATH}")
    return MAP_OUTPUT_PATH


if __name__ == "__main__":
    print("=== Phase 6: Generating Folium Interactive Launch Map ===")
    out = build_interactive_map()
    print(f"Map successfully generated at: {out}")
