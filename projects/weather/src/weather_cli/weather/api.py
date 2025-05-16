"""Weather API interaction module."""

from pyowm import OWM

class WeatherAPI:
    """Weather API wrapper for OpenWeatherMap."""
    
    def __init__(self, api_key):
        """Initialize the API wrapper."""
        self.owm = OWM(api_key)
        self.mgr = self.owm.weather_manager()
    
    def get_current_weather(self, location):
        """Get current weather for a location."""
        pass
    
    def get_forecast(self, location):
        """Get weather forecast for a location."""
        pass
