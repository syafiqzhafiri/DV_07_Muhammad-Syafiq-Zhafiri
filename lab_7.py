import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# Load the Natural Earth dataset
@st.cache_data
def load_data():
    gdf = gpd.read_file(
        "ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
    )

    if 'pop_est' not in gdf.columns:
        np.random.seed(0)
        gdf['pop_est'] = np.random.randint(
            1e6, 1e9, size=len(gdf)
        )

    return gdf

gdf = load_data()

# Projection options
projection_options = {
    "Mercator": "EPSG:3395",
    "Robinson": "+proj=robin",
    "Mollweide": "+proj=moll",
    "Equal Earth": "EPSG:8857"
}

# Streamlit Setup
st.title("Interactive Map Visualization Examples")

st.sidebar.header("Choose a Map Type")

map_type = st.sidebar.radio(
    "Select Map Type",
    [
        "Map Cosmetics",
        "Map Visual Hierarchy",
        "Choropleth Map",
        "Geo Projection"
    ]
)

# 1. Map Cosmetics Example
if map_type == "Map Cosmetics":

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf.plot(
        ax=ax,
        color='skyblue',
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_title(
        "Styled Map Example",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_facecolor("lightgrey")

    st.pyplot(fig)


# 2. Map Visual Hierarchy Example
elif map_type == "Map Visual Hierarchy":

    country_col = 'name' if 'name' in gdf.columns else 'NAME'

    highlighted_countries = st.multiselect(
        "Select countries to highlight in red",
        gdf[country_col].unique(),
        default=[
            "Brazil",
            "India",
            "China",
            "Australia",
            "South Africa",
            "Russia"
        ]
    )

    gdf['color'] = gdf[country_col].apply(
        lambda x: 'red' if x in highlighted_countries
        else 'skyblue'
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf.plot(
        color=gdf['color'],
        edgecolor='black',
        linewidth=0.5,
        ax=ax
    )

    ax.set_title(
        "Map Visual Hierarchy with Selected Countries Highlighted in Red"
    )

    st.pyplot(fig)


# 3. Choropleth Map Example
elif map_type == "Choropleth Map":

    color_choice = st.selectbox(
        "Choose Color Scheme",
        ['OrRd', 'YlGn', 'Blues', 'Purples', 'Greens'],
        index=0
    )

    use_log_scale = st.checkbox(
        "Use Log Transformation",
        value=True
    )

    gdf['pop_density'] = (
        gdf['pop_est'] / gdf['geometry'].area
    )

    if use_log_scale:
        gdf['pop_density'] = np.log1p(
            gdf['pop_density']
        )

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf.plot(
        column='pop_density',
        cmap=color_choice,
        edgecolor='black',
        legend=True,
        ax=ax
    )

    ax.set_title(
        f"Population Density by Country (Color Scheme: {color_choice})"
    )

    st.pyplot(fig)


# 4. Geo Projection Example
elif map_type == "Geo Projection":

    proj_choice = st.selectbox(
        "Select a Projection",
        list(projection_options.keys())
    )

    color_choice = st.selectbox(
        "Choose Color Scheme",
        ['OrRd', 'YlGn', 'Blues', 'Purples', 'Greens'],
        index=0
    )

    use_log_scale = st.checkbox(
        "Use Log Transformation for Population Density",
        value=True
    )

    gdf['pop_density'] = (
        gdf['pop_est'] / gdf['geometry'].area
    )

    if use_log_scale:
        gdf['pop_density'] = np.log1p(
            gdf['pop_density']
        )

    gdf_proj = gdf.to_crs(
        projection_options[proj_choice]
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    gdf_proj.plot(
        column='pop_density',
        cmap=color_choice,
        edgecolor='black',
        legend=True,
        ax=ax
    )

    ax.set_title(
        f"Map in {proj_choice} Projection"
    )

    st.pyplot(fig)
    
# Easter Egg
st.sidebar.markdown("---")
st.sidebar.caption("Muhammad Syafiq Zhafiri (26010258)")
st.sidebar.image("chiikawa.png", width=100)