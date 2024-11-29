import streamlit as st
import plotly.express as px
import pandas as pd
from api.space_data import SpaceAPI
from utils.helpers import calculate_distance_au_to_ly, format_number

def show_exoplanet_explorer():
    space_api = SpaceAPI()
    
    # Fetch exoplanet data
    exoplanets = space_api.get_exoplanets()
    
    if not exoplanets:
        st.error("Unable to fetch exoplanet data. Please try again later.")
        return
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(exoplanets)
    
    # Sidebar filters
    st.sidebar.subheader("Filter Exoplanets")
    
    # Distance filter
    max_distance = float(df['pl_orbsmax'].max())
    distance_range = st.sidebar.slider(
        "Distance from Star (AU)",
        0.0,
        max_distance,
        (0.0, max_distance)
    )
    
    # Planet size filter
    max_radius = float(df['pl_rade'].max())
    radius_range = st.sidebar.slider(
        "Planet Radius (Earth Radii)",
        0.0,
        max_radius,
        (0.0, max_radius)
    )
    
    # Apply filters
    mask = (
        (df['pl_orbsmax'] >= distance_range[0]) &
        (df['pl_orbsmax'] <= distance_range[1]) &
        (df['pl_rade'] >= radius_range[0]) &
        (df['pl_rade'] <= radius_range[1])
    )
    filtered_df = df[mask]
    
    # Main content
    st.subheader("Recently Discovered Exoplanets")
    
    # Visualization
    fig = px.scatter(
        filtered_df,
        x='pl_orbsmax',
        y='pl_rade',
        hover_name='pl_name',
        hover_data=['pl_orbper', 'pl_masse'],
        title='Exoplanet Distribution',
        labels={
            'pl_orbsmax': 'Distance from Star (AU)',
            'pl_rade': 'Planet Radius (Earth Radii)',
            'pl_orbper': 'Orbital Period (days)',
            'pl_masse': 'Planet Mass (Earth Mass)'
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed list
    st.subheader("Exoplanet Details")
    
    for _, planet in filtered_df.iterrows():
        with st.expander(f"{planet['pl_name']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Distance from Star:**", 
                        f"{format_number(planet['pl_orbsmax'])} AU")
                st.write("**Orbital Period:**", 
                        f"{format_number(planet['pl_orbper'])} days")
                st.write("**Planet Radius:**", 
                        f"{format_number(planet['pl_rade'])} Earth radii")
            
            with col2:
                st.write("**Planet Mass:**", 
                        f"{format_number(planet['pl_masse'])} Earth masses")
                st.write("**Star Type:**", 
                        planet.get('st_spectype', 'Unknown'))
                
                # Calculate if planet is in habitable zone (simplified)
                # This is a very basic approximation
                orbital_distance = float(planet['pl_orbsmax'])
                star_temp = float(planet.get('st_teff', 5778))  # Sun = 5778K
                
                # Rough estimate of habitable zone
                inner_hz = (star_temp/5778)**2 * 0.75  # Inner edge
                outer_hz = (star_temp/5778)**2 * 1.8   # Outer edge
                
                is_habitable = inner_hz <= orbital_distance <= outer_hz
                
                st.write("**Potentially Habitable:**", 
                        "Yes ✨" if is_habitable else "No")
