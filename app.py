import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
from components.rocket_launches import show_rocket_launches
from components.exoplanet_explorer import show_exoplanet_explorer
from components.live_data import show_live_space_data
from utils.helpers import get_random_space_fact

# Load environment variables
load_dotenv()

# Check for NASA API key
if not os.getenv('NASA_API_KEY'):
    st.error("NASA API key not found. Please add it to your .env file.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Personal Space Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application title and description
st.title("🌎 Personal Space Tracker")
st.markdown("""
    Explore real-time space data, track celestial events, and discover the wonders of our universe!
    """)

# Random space fact in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**🌟 Random Space Fact**")
st.sidebar.markdown(get_random_space_fact())
st.sidebar.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Page",
    ["Home", "Rocket Launches", "Exoplanet Explorer", "Live Space Data"]
)

# Import page modules based on selection
if page == "Home":
    st.header("Welcome to Personal Space Tracker!")
    
    # Display current time in different time zones
    st.subheader("Current Time")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        utc_time = datetime.now(pytz.UTC)
        st.metric("UTC", utc_time.strftime("%H:%M:%S"))
    
    with col2:
        et_time = datetime.now(pytz.timezone('US/Eastern'))
        st.metric("Eastern Time", et_time.strftime("%H:%M:%S"))
    
    with col3:
        pt_time = datetime.now(pytz.timezone('US/Pacific'))
        st.metric("Pacific Time", pt_time.strftime("%H:%M:%S"))
    
    # Featured content
    st.subheader("Featured Content")
    st.markdown("""
        - 🚀 **Latest Rocket Launches**: Stay updated with upcoming space missions
        - 🌍 **Exoplanet Discoveries**: Explore newly found worlds beyond our solar system
        - ☄️ **Astronomy Events**: Track celestial events and phenomena
        - 🛸 **ISS Tracker**: Follow the International Space Station in real-time
    """)

elif page == "Rocket Launches":
    show_rocket_launches()

elif page == "Exoplanet Explorer":
    show_exoplanet_explorer()

elif page == "Live Space Data":
    show_live_space_data()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Data provided by NASA, SpaceX, and Open Notify APIs")
