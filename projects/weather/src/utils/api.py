"""Weather API interaction module."""

from typing import Dict, List, Tuple
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

class WeatherAPI:
    """Weather API wrapper for Open-Meteo."""
    
    def __init__(self):
        """Initialize the API wrapper."""
        self.client = openmeteo_requests.Client()
        self.geocoder = Nominatim(user_agent="weather_cli")
    
    def geocode_location(self, location: str) -> Tuple[float, float]:
        """Convert location string to coordinates.
        
        Args:
            location (str): Location string (city name, address, or zip code)
            
        Returns:
            Tuple[float, float]: Latitude and longitude coordinates
            
        Raises:
            ValueError: If location cannot be found or geocoding fails
        """
        try:
            location_data = self.geocoder.geocode(location)
            if location_data is None:
                raise ValueError(f"Location not found: {location}")
            return location_data.latitude, location_data.longitude
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            raise ValueError(f"Geocoding service error: {str(e)}")
    
    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """Get current weather for a location.
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            
        Returns:
            dict: Current weather conditions including temperature, humidity, etc.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "rain",
                "weather_code",
                "wind_speed_10m",
                "wind_direction_10m"
            ],
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm"
        }
        
        response = self.client.weather_api(url="https://api.open-meteo.com/v1/forecast", params=params)
        current = response.get("current", {})
        
        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "feels_like": current.get("apparent_temperature"),
            "precipitation": current.get("precipitation"),
            "rain": current.get("rain"),
            "weather_code": current.get("weather_code"),
            "wind_speed": current.get("wind_speed_10m"),
            "wind_direction": current.get("wind_direction_10m")
        }
    
    def get_hourly_forecast(self, latitude: float, longitude: float) -> List[Dict]:
        """Get hourly forecast for next 24 hours.
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            
        Returns:
            List[dict]: List of hourly forecasts with weather conditions
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                "weather_code"
            ],
            "forecast_days": 1
        }
        
        response = self.client.weather_api(url="https://api.open-meteo.com/v1/forecast", params=params)
        hourly = response.get("hourly", {})
        
        forecasts = []
        for i in range(24):  # Next 24 hours
            forecasts.append({
                "time": hourly.get("time", [])[i] if "time" in hourly else None,
                "temperature": hourly.get("temperature_2m", [])[i] if "temperature_2m" in hourly else None,
                "humidity": hourly.get("relative_humidity_2m", [])[i] if "relative_humidity_2m" in hourly else None,
                "precipitation_prob": hourly.get("precipitation_probability", [])[i] if "precipitation_probability" in hourly else None,
                "weather_code": hourly.get("weather_code", [])[i] if "weather_code" in hourly else None
            })
        
        return forecasts
    
    def get_daily_forecast(self, latitude: float, longitude: float, days: int = 7) -> List[Dict]:
        """Get daily forecast for specified number of days.
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            days (int, optional): Number of days to forecast. Defaults to 7.
            
        Returns:
            List[dict]: List of daily forecasts with weather conditions
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "weather_code"
            ],
            "forecast_days": days
        }
        
        response = self.client.weather_api(url="https://api.open-meteo.com/v1/forecast", params=params)
        daily = response.get("daily", {})
        
        forecasts = []
        for i in range(days):
            forecasts.append({
                "date": daily.get("time", [])[i] if "time" in daily else None,
                "temp_max": daily.get("temperature_2m_max", [])[i] if "temperature_2m_max" in daily else None,
                "temp_min": daily.get("temperature_2m_min", [])[i] if "temperature_2m_min" in daily else None,
                "precipitation": daily.get("precipitation_sum", [])[i] if "precipitation_sum" in daily else None,
                "precipitation_prob": daily.get("precipitation_probability_max", [])[i] if "precipitation_probability_max" in daily else None,
                "weather_code": daily.get("weather_code", [])[i] if "weather_code" in daily else None
            })
        
        return forecasts
