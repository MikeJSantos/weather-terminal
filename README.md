# Weather Terminal

This is a console application, written in Python, that scrapes weather forecast info from http://www.weather.com, using BeautifulSoup for HTML parsing & PhantomJS (included with Selenium) to drive the HTTP request.

Based on [Python Programming Blueprints](https://www.packtpub.com/application-development/python-programming-blueprints).

## Installation

```bash
# Create a virtual environment?
# Use [pip](https://pip.pypa.io/en/stable/) to install dependencies.
pip install -r requirements.txt
```

## Usage

```python
# Get today's forecast
py -m weatherterm -p WeatherComParser -a {area_code} 
# 5-day
py -m weatherterm -p WeatherComParser -a {area_code} -5d
# 10-day
py -m weatherterm -p WeatherComParser -a {area_code} -10d
# Weekend
py -m weatherterm -p WeatherComParser -a {area_code} -w
```
