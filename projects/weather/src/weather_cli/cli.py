"""Main CLI interface for the weather application."""

import click
from weather_cli.weather.api import WeatherAPI
from weather_cli.utils.config import load_config

@click.group()
def cli():
    """Weather CLI tool for checking weather conditions and forecasts."""
    pass

@cli.command()
@click.argument('location')
def current(location):
    """Get current weather for a location."""
    pass

@cli.command()
@click.argument('location')
def forecast(location):
    """Get weather forecast for a location."""
    pass

if __name__ == '__main__':
    cli()
