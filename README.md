# Weather Terminal

This is a console application, written in Python, that scrapes weather forecast info from http://www.weather.com, using BeautifulSoup for HTML parsing & PhantomJS (included with Selenium) to drive the HTTP request.

Based on [Python Programming Blueprints](https://www.packtpub.com/application-development/python-programming-blueprints).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

## Usage


```python
# Get today's forecast
python -m weatherterm -p WeatherComParser -a {area_code} 
# 5-day
python -m weatherterm -p WeatherComParser -a {area_code} -5d
# 10-day
python -m weatherterm -p WeatherComParser -a {area_code} -10d
# Weekend
python -m weatherterm -p WeatherComParser -a {area_code} -w
```