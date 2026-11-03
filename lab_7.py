import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import zipfile
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Lab 7 - Interactive Map Visualization",
    page_icon="🌍",
    layout="wide"
)

BASE_DIR = Path(__file__).parent

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    zip_path = BASE_DIR / "ne_110m_admin_0_countries.zip"
    extract_path = BASE_DIR / "ne_110m_admin_0_countries"

    # Extract ZIP if necessary
    if zip_path.exists() and not extract_path.exists():
        extract_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

    # Search for the shapefile, including nested folders
    shapefiles = list(extract_path.rglob("*.shp"))

    if not shapefiles:
        st.error(
            "Shapefile not found. Please check your ZIP file "
            "and make sure it contains the Natural Earth shapefile."
        )
        st.stop()

    gdf = gpd.read_file(shapefiles[0])

    # Population data
    if "POP_EST" in gdf.columns:
        gdf["pop_est"] = gdf["POP_EST"]
    elif "pop_est" not in gdf.columns:
        gdf["pop_est"] = 1000000

    # Country name
    if "NAME" in gdf.columns:
        gdf["country"] = gdf["NAME"]
    elif "name" in gdf.columns:
        gdf["country"] = gdf["name"]

    return gdf


gdf = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Map Visualization")

map_option = st.sidebar.radio(
    "Choose Visualization:",
    [
        "Map Cosmetics",
        "Map Visual Hierarchy",
        "Choropleth Map",
        "Geo Projection"
    ]
)

# Easter Egg
st.sidebar.markdown("---")
st.sidebar.caption("Muhammad Syafiq Zhafiri (26010258)")

chiikawa_path = BASE_DIR / "chiikawa.png"

if chiikawa_path.exists():
    st.sidebar.image(str(chiikawa_path), width=100)

# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------

st.title("Lab 7: Interactive Map Visualization")
st.write("Exploring different techniques in geographical data visualization.")

# --------------------------------------------------
# 1. MAP COSMETICS
# --------------------------------------------------

if map_option == "Map Cosmetics":

    st.header("1. Map Cosmetics")

    fig = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color="pop_est",
        hover_name="country",
        color_continuous_scale="Viridis",
        title="World Population Distribution"
    )

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue"
    )

    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 2. MAP VISUAL HIERARCHY
# --------------------------------------------------

elif map_option == "Map Visual Hierarchy":

    st.header("2. Map Visual Hierarchy")

    fig, ax = plt.subplots(figsize=(15, 8))

    gdf.plot(
        ax=ax,
        color="lightblue",
        edgecolor="black",
        linewidth=0.5
    )

    ax.set_title(
        "World Map: Visual Hierarchy",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_axis_off()

    st.pyplot(fig)

# --------------------------------------------------
# 3. CHOROPLETH MAP
# --------------------------------------------------

elif map_option == "Choropleth Map":

    st.header("3. Choropleth Map")

    # Reproject to an equal-area CRS before calculating area
    gdf_equal_area = gdf.to_crs("EPSG:6933").copy()

    gdf_equal_area["density"] = (
        gdf_equal_area["pop_est"]
        / (gdf_equal_area.geometry.area / 1_000_000)
    )

    fig = px.choropleth(
        gdf_equal_area,
        geojson=gdf_equal_area.geometry,
        locations=gdf_equal_area.index,
        color="density",
        hover_name="country",
        color_continuous_scale="YlOrRd",
        title="Estimated Population Density by Country",
        labels={"density": "People per km²"}
    )

    fig.update_geos(
        showcoastlines=True,
        showcountries=True
    )

    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 4. GEO PROJECTION
# --------------------------------------------------

elif map_option == "Geo Projection":

    st.header("4. Geographic Projection")

    projection_options = {
        "Mercator": "mercator",
        "Robinson": "robinson",
        "Mollweide": "mollweide",
        "Equal Earth": "equal earth"
    }

    selected_projection = st.selectbox(
        "Select Map Projection:",
        list(projection_options.keys())
    )

    fig = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color="pop_est",
        hover_name="country",
        color_continuous_scale="Viridis",
        title=f"World Map - {selected_projection} Projection"
    )

    fig.update_geos(
        projection_type=projection_options[selected_projection],
        showcoastlines=True,
        coastlinecolor="Black"
    )

    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.caption("Data Visualization Lab 7 | Interactive Map Visualization")
