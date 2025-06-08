"""Tests for the WeatherAPI class."""

import pytest
from typing import Callable
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_class() -> Callable[[], Mock]:
    """Mock a class with functions."""
    mock_class = Mock()
    mock_class.say_hi.return_value = "Hello"
    return mock_class


@pytest.fixture
def magic_mock_class() -> Callable[[], Mock]:
    """Mock a class with functions."""
    mock_class = MagicMock()
    mock_class.say_hi.return_value = "Hello Magic"
    return mock_class


def test_mock_class(mock_class):
    """Test successful geocoding of a location."""
    greeting = mock_class.say_hi()
    mock_class.say_hi.assert_called_once()
    assert greeting == "Hello"


def test_magic_mock_class(magic_mock_class):
    """Test successful geocoding of a location."""
    greeting = magic_mock_class.say_hi()
    magic_mock_class.say_hi.assert_called_once()
    assert greeting == "Hello Magic"
