"""Weather API interaction module."""

from typing import Dict, List, Tuple
import openmeteo_requests
from openmeteo_sdk import WeatherApiResponse
from openmeteo_sdk.Variable import Variable
from openmeteo_sdk.VariableWithValues import VariableWithValues
from geopy.geocoders.base import Geocoder
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable


class WeatherAPI:
    """Weather API wrapper for Open-Meteo."""

    def __init__(self, client:openmeteo_requests.Client=None, geocoder: Geocoder = None):
        """Initialize the API wrapper."""
        self.client = client or openmeteo_requests.Client()
        self.geocoder = geocoder or Nominatim(user_agent="weather-cli")

    def _api_request(self, params: Dict) -> WeatherApiResponse:
        """Make a weather API request for a single location.

        Args:
            params (dict): Request parameters

        Returns:
            dict: API response
        """
        return self.client.weather_api(
            url="https://api.open-meteo.com/v1/forecast", params=params
        )[0]

    def parse_variables(self, variables: List[VariableWithValues]) -> Dict[str, Dict]:
        """Parse weather variables into a structured format.

        Args:
        variables: List of weather variables

        Returns:
        Dictionary of dictionaries containing parsed variable information,
        keyed by the variable type.
        """
        # Get the variable class attributes to map integers to names
        var_names = {
            getattr(Variable, attr): attr
            for attr in dir(Variable)
            if not attr.startswith("_") and isinstance(getattr(Variable, attr), int)
        }

        parsed_vars = {}
        for var in variables:
            var_type = var_names.get(var.Variable(), "unknown")
            parsed_vars[var_type] = {
                "code": var.Variable(),
                "value": var.Value(),
                "altitude": var.Altitude(),
                "unit": var.Unit(),
            }
        return parsed_vars

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
                "wind_direction_10m",
            ],
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "mm",
        }

        response = self._api_request(params)
        current = response.Current()
        print(f"Current time {current.Time()}")

        current_variables = list(
            map(lambda i: current.Variables(i), range(0, current.VariablesLength()))
        )

        parsed_vars = self.parse_variables(current_variables)
        print(parsed_vars)

        return {
            "temperature": parsed_vars["temperature"]["value"],
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
                "weather_code",
            ],
            "forecast_days": 1,
        }

        response = self.client.weather_api(
            url="https://api.open-meteo.com/v1/forecast", params=params
        )
        hourly = response.get("hourly", {})

        forecasts = []
        for i in range(24):  # Next 24 hours
            forecasts.append(
                {
                    "time": hourly.get("time", [])[i] if "time" in hourly else None,
                    "temperature": hourly.get("temperature_2m", [])[i]
                    if "temperature_2m" in hourly
                    else None,
                    "humidity": hourly.get("relative_humidity_2m", [])[i]
                    if "relative_humidity_2m" in hourly
                    else None,
                    "precipitation_prob": hourly.get("precipitation_probability", [])[i]
                    if "precipitation_probability" in hourly
                    else None,
                    "weather_code": hourly.get("weather_code", [])[i]
                    if "weather_code" in hourly
                    else None,
                }
            )

        return forecasts

    def get_daily_forecast(
        self, latitude: float, longitude: float, days: int = 7
    ) -> List[Dict]:
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
                "weather_code",
            ],
            "forecast_days": days,
        }

        response = self.client.weather_api(
            url="https://api.open-meteo.com/v1/forecast", params=params
        )
        daily = response.get("daily", {})

        forecasts = []
        for i in range(days):
            forecasts.append(
                {
                    "date": daily.get("time", [])[i] if "time" in daily else None,
                    "temp_max": daily.get("temperature_2m_max", [])[i]
                    if "temperature_2m_max" in daily
                    else None,
                    "temp_min": daily.get("temperature_2m_min", [])[i]
                    if "temperature_2m_min" in daily
                    else None,
                    "precipitation": daily.get("precipitation_sum", [])[i]
                    if "precipitation_sum" in daily
                    else None,
                    "precipitation_prob": daily.get(
                        "precipitation_probability_max", []
                    )[i]
                    if "precipitation_probability_max" in daily
                    else None,
                    "weather_code": daily.get("weather_code", [])[i]
                    if "weather_code" in daily
                    else None,
                }
            )

        return forecasts
