import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from api.space_data import SpaceAPI
from utils.helpers import format_number, get_hazard_emoji

def show_live_space_data():
    space_api = SpaceAPI()
    
    # Create tabs for different live data
    tab1, tab2 = st.tabs(["ISS Tracker", "Near-Earth Objects"])
    
    with tab1:
        st.subheader("🛸 International Space Station Location")
        
        # Get ISS location
        iss_data = space_api.get_iss_location()
        
        if iss_data:
            # Create a DataFrame for the ISS location
            iss_df = pd.DataFrame([{
                'lat': iss_data['latitude'],
                'lon': iss_data['longitude'],
                'name': 'ISS'
            }])
            
            # Create a map using plotly
            fig = px.scatter_mapbox(
                iss_df,
                lat='lat',
                lon='lon',
                hover_name='name',
                zoom=1
            )
            
            fig.update_layout(
                mapbox_style="open-street-map",
                margin={"r":0,"t":0,"l":0,"b":0}
            )
            
            # Display the map
            st.plotly_chart(fig, use_container_width=True)
            
            # Display coordinates
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Latitude", f"{format_number(iss_data['latitude'])}°")
            with col2:
                st.metric("Longitude", f"{format_number(iss_data['longitude'])}°")
            
            # Add timestamp
            st.caption(f"Last updated: {datetime.fromtimestamp(iss_data['timestamp'])}")
        else:
            st.error("Unable to fetch ISS location data. Please try again later.")
    
    with tab2:
        st.subheader("☄️ Near-Earth Objects")
        
        # Get asteroid data
        asteroids = space_api.get_asteroid_data()
        
        if asteroids:
            # Create a summary
            total_asteroids = len(asteroids)
            hazardous_count = sum(1 for ast in asteroids if ast['is_potentially_hazardous_asteroid'])
            
            # Display summary metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Objects", total_asteroids)
            with col2:
                st.metric("Potentially Hazardous", hazardous_count)
            
            # Display detailed information for each asteroid
            st.subheader("Detailed Information")
            
            for asteroid in asteroids:
                # Create an expander for each asteroid
                with st.expander(f"{asteroid['name']} {get_hazard_emoji(asteroid['is_potentially_hazardous_asteroid'])}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Estimated Diameter:**")
                        st.write(f"Min: {format_number(asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'])} km")
                        st.write(f"Max: {format_number(asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'])} km")
                        
                        st.write("**Relative Velocity:**")
                        st.write(f"{format_number(float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))} km/h")
                    
                    with col2:
                        st.write("**Miss Distance:**")
                        st.write(f"{format_number(float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']))} km")
                        
                        st.write("**Close Approach Date:**")
                        st.write(asteroid['close_approach_data'][0]['close_approach_date_full'])
        else:
            st.error("Unable to fetch asteroid data. Please try again later.")
