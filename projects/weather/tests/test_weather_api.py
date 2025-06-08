"""Tests for the WeatherAPI class."""

import pytest
from typing import Callable
from unittest.mock import Mock, MagicMock
from utils.api import WeatherAPI
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.location import Location


@pytest.fixture
def mock_geocoder() -> Callable[[], Mock]:
    """Mock the Nominatim geocoder."""
    mock_class = MagicMock()
    mock_class.geocode.return_value = Location(
        address="New York City",
        point=(40.7128, -74.0060),
        raw={"place_id": 123, "osm_type": "node"},
    )
    return mock_class


@pytest.fixture
def mock_weather_client(mocker):
    """Mock the OpenMeteo client."""
    mock = mocker.patch("utils.api.openmeteo_requests.Client")
    return mock


@pytest.fixture
def mock_weather_api(mock_weather_client, mock_geocoder):
    """Create a WeatherAPI instance with mock resources."""
    return WeatherAPI(client=mock_weather_client, geocoder=mock_geocoder)

@pytest.fixture
def weather_api():
    """Create a WeatherAPI instance with default resources."""
    return WeatherAPI()


def test_mock_geocoder(mock_geocoder):
    """Test the mock geocoder."""
    location = mock_geocoder.geocode("New York City")
    mock_geocoder.geocode.assert_called_once_with("New York City")
    assert location.address == "New York City"
    assert location.latitude == 40.7128
    assert location.longitude == -74.0060


def test_geocode_location_success(mock_weather_api):
    """Test successful geocoding of a location."""
    lat, lon = mock_weather_api.geocode_location("New York City")
    mock_weather_api.geocoder.geocode.assert_called_once_with("New York City")
    assert lat == pytest.approx(40.7128, abs=1e-3)
    assert lon == pytest.approx(-74.0060, abs=1e-3)


def test_geocode_location_not_found(weather_api):
    """Test geocoding when location is not found."""
    with pytest.raises(ValueError, match="Location not found: Invalid City"):
        print(weather_api.geocode_location("Invalid City"))


def test_geocode_location_service_error(weather_api, mock_geocoder):
    """Test geocoding when service has an error."""
    mock_geocoder.return_value.geocode.side_effect = GeocoderTimedOut("Timeout")
    with pytest.raises(ValueError, match="Geocoding service error: Timeout"):
        weather_api.geocode_location("New York City")


def test_get_current_weather(weather_api):
    """Test getting current weather data."""
    mock_response = {
        "current": {
            "temperature_2m": 20.5,
            "relative_humidity_2m": 65,
            "apparent_temperature": 21.0,
            "precipitation": 0.0,
            "rain": 0.0,
            "weather_code": 1,
            "wind_speed_10m": 10.5,
            "wind_direction_10m": 180,
        }
    }
    mock_client = mock_weather_client.return_value
    mock_client.return_value = Mock(**mock_response)

    result = weather_api.get_current_weather(40.7128, -74.0060)

    assert result["temperature"] == 20.5
    assert result["humidity"] == 65
    assert result["feels_like"] == 21.0
    assert result["precipitation"] == 0.0
    assert result["rain"] == 0.0
    assert result["weather_code"] == 1
    assert result["wind_speed"] == 10.5
    assert result["wind_direction"] == 180
