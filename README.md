# Personal Space Tracker

A real-time space data visualization application that provides information about celestial events, rocket launches, and exoplanets.

## Features

- **Upcoming Rocket Launches**: Track SpaceX and other space agency launches
- **Exoplanet Explorer**: Discover and learn about recently found exoplanets
- **Astronomy Events**: Stay updated with celestial events and reminders
- **Live Space Data**: Track ISS location and near-Earth asteroids
- **Search Functionality**: Find specific space events and objects
- **Random Space Facts**: Learn interesting space trivia

## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your API keys:
   ```
   NASA_API_KEY=your_nasa_api_key
   ```
   Get your NASA API key from: https://api.nasa.gov/

## Running the App

To run the app locally:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `api/`: API integration modules
- `utils/`: Utility functions and helpers
- `components/`: Streamlit UI components
- `data/`: Static data and cached responses
- `requirements.txt`: Project dependencies

## Technologies Used

- Python 3.8+
- Streamlit
- NASA API
- SpaceX API
- Open Notify API
- Plotly for visualizations
