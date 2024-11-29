import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
from api.space_data import SpaceAPI
from utils.helpers import format_datetime, calculate_time_until, filter_launches

def show_rocket_launches():
    space_api = SpaceAPI()
    
    # Fetch launches
    launches = space_api.get_upcoming_launches()
    
    # Filters
    st.sidebar.subheader("Filter Launches")
    
    # Date range filter
    start_date = st.sidebar.date_input(
        "Start Date",
        datetime.now()
    )
    end_date = st.sidebar.date_input(
        "End Date",
        datetime.now() + timedelta(days=90)
    )
    
    # Organization filter
    organizations = ["All", "SpaceX", "NASA", "ULA", "Rocket Lab"]
    selected_org = st.sidebar.selectbox("Organization", organizations)
    
    # Apply filters
    filtered_launches = filter_launches(
        launches,
        start_date=datetime.combine(start_date, datetime.min.time()),
        end_date=datetime.combine(end_date, datetime.max.time()),
        organization=None if selected_org == "All" else selected_org
    )
    
    # Display launches
    if filtered_launches:
        # Timeline visualization
        fig = go.Figure()
        
        for launch in filtered_launches:
            launch_date = datetime.strptime(launch['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
            fig.add_trace(go.Scatter(
                x=[launch_date],
                y=[launch['name']],
                mode='markers+text',
                name=launch['name'],
                text=[launch['name']],
                textposition='top center'
            ))
        
        fig.update_layout(
            title="Launch Timeline",
            xaxis_title="Date",
            yaxis_title="Mission",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed launch information
        for launch in filtered_launches:
            with st.expander(f"{launch['name']} - {format_datetime(launch['date'])}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Launch Time:**", format_datetime(launch['date']))
                    st.write("**Time Until Launch:**", calculate_time_until(launch['date']))
                    st.write("**Rocket:**", launch['rocket'])
                
                with col2:
                    st.write("**Launchpad:**", launch['launchpad'])
                    if launch['details']:
                        st.write("**Mission Details:**", launch['details'])
    else:
        st.warning("No launches found matching the selected criteria.")
