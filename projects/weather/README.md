# Weather CLI Tool

A command-line interface for retrieving weather information using OpenWeatherMap API.

## Features (TODO)

- Current weather conditions
- Hourly forecast
- 7-day forecast
- Location search by city name or zip code

## Setup

Run the following commands from this directory to set up the project:

```bash
uv pip compile pyproject.toml --output-file requirements.txt
uv venv .venv --python 3.12
uv pip install --requirements requirements.txt
uv pip list
```

## Usage

To get current weather conditions in New York:

```bash
uv run weather-cli current "New York"
```

The command line tool can also be invoked as a python module:

```bash
uv run python -m weather_cli current "New York"
```

## Configuration

TODO: Add configuration details

## Development

Run the following command to recompile the requirements file:

```bash
uv pip compile pyproject.toml --output-file requirements.txt
```
