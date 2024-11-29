import requests
import os
from datetime import datetime, timedelta
import streamlit as st

class SpaceAPI:
    def __init__(self):
        self.nasa_api_key = os.getenv('NASA_API_KEY')
        if not self.nasa_api_key:
            st.error("NASA API key not found. Please check your .env file.")
        self.spacex_api_url = "https://api.spacexdata.com/v4"
        self.nasa_api_url = "https://api.nasa.gov"
        self.iss_api_url = "http://api.open-notify.org"

    def get_upcoming_launches(self):
        """Fetch upcoming SpaceX launches"""
        try:
            st.info("Fetching upcoming launches...")
            response = requests.get(f"{self.spacex_api_url}/launches/upcoming")
            st.write(f"SpaceX API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                launches = response.json()
                formatted_launches = [{
                    'name': launch['name'],
                    'date': launch['date_utc'],
                    'details': launch.get('details', 'No details available'),
                    'rocket': launch.get('rocket', 'Unknown rocket'),
                    'launchpad': launch.get('launchpad', 'Unknown launchpad')
                } for launch in launches]
                st.success(f"Successfully fetched {len(formatted_launches)} launches")
                return formatted_launches
            else:
                st.error(f"Failed to fetch launches. Status code: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error fetching launches: {str(e)}")
            return []

    def get_astronomy_picture(self):
        """Fetch NASA's Astronomy Picture of the Day"""
        try:
            st.info("Fetching astronomy picture of the day...")
            params = {'api_key': self.nasa_api_key}
            response = requests.get(
                f"{self.nasa_api_url}/planetary/apod",
                params=params
            )
            st.write(f"NASA APOD API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                st.success("Successfully fetched astronomy picture")
                return data
            else:
                st.error(f"Failed to fetch APOD. Status code: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching APOD: {str(e)}")
            return None

    def get_iss_location(self):
        """Get current ISS location"""
        try:
            st.info("Fetching ISS location...")
            response = requests.get(f"{self.iss_api_url}/iss-now.json")
            st.write(f"ISS API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                location = {
                    'latitude': float(data['iss_position']['latitude']),
                    'longitude': float(data['iss_position']['longitude']),
                    'timestamp': data['timestamp']
                }
                st.success("Successfully fetched ISS location")
                return location
            else:
                st.error(f"Failed to fetch ISS location. Status code: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching ISS location: {str(e)}")
            return None

    def get_asteroid_data(self):
        """Get near-Earth asteroid data"""
        try:
            st.info("Fetching asteroid data...")
            today = datetime.now().strftime('%Y-%m-%d')
            params = {
                'api_key': self.nasa_api_key,
                'start_date': today,
                'end_date': today
            }
            response = requests.get(
                f"{self.nasa_api_url}/neo/rest/v1/feed",
                params=params
            )
            st.write(f"NASA Asteroid API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                # Extract asteroids for today
                asteroids = data['near_earth_objects'][today]
                st.success(f"Successfully fetched {len(asteroids)} asteroids")
                return asteroids
            else:
                st.error(f"Failed to fetch asteroid data. Status code: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching asteroid data: {str(e)}")
            return None

    def get_exoplanets(self):
        """Get exoplanet data from NASA Exoplanet Archive"""
        try:
            st.info("Fetching exoplanet data...")
            # Using the NASA Exoplanet Archive TAP service
            query = "select+pl_name,pl_orbper,pl_rade,pl_masse,pl_disc,sy_dist,hostname+from+ps+where+default_flag=1+order+by+pl_disc+desc+limit+50"
            response = requests.get(
                "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
                params={
                    'query': query,
                    'format': 'json'
                }
            )
            st.write(f"Exoplanet API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"Successfully fetched {len(data)} exoplanets")
                return data
            else:
                st.error(f"Failed to fetch exoplanet data. Status code: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error fetching exoplanet data: {str(e)}")
            return None
