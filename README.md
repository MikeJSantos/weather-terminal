# Weather Terminal

This is a Python console application that scrapes weather forecast info from http://www.weather.com, using BeautifulSoup for HTML parsing & PhantomJS (included with Selenium) to drive the HTTP request.

Based on [Python Programming Blueprints](https://www.packtpub.com/application-development/python-programming-blueprints).

## Installation

Create & activate a virtual environment
```bash
py -m venv env
./env/Scripts/activate.bat
```

Install [pip](https://pip.pypa.io/en/stable/) dependencies.
```bash
pip install -r requirements.txt
```

Download PhantomJS & extract the executable to /phantomjs/bin

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
