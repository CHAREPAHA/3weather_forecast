import pytest
import requests
from unittest.mock import patch, mock_open
from src.weather_api import get_weather, get_weather_forecast

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get

def test_get_weather_success(mock_requests_get):
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Moscow",
        "main": {"temp": 10.0},
        "weather": [{"description": "ясно"}]
    }

    with patch("os.path.exists", return_value=False):
        with patch("builtins.open", new=mock_open()):
            result = get_weather("Moscow", "fake_api_key")

            assert result == {
                "city": "Moscow",
                "temperature": 10.0,
                "description": "ясно"
            }

