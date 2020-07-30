import re
from bs4 import BeautifulSoup
from weatherterm.core import Forecast, Mapper, Request, UnitConverter
from weatherterm.core.enum import ForecastType, Unit

class WeatherComParser:
    def __init__(self):
        self._forecast_function_mappings = {
            ForecastType.TODAY:    self._today_forecast,
            ForecastType.FIVEDAYS: self._five_day_forecast,
            ForecastType.TENDAYS:  self._ten_day_forecast,
            ForecastType.WEEKEND:  self._weekend_forecast
        }
        self._request = Request('http://weather.com/weather/{forecast_option}/l/{area_code}')
        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)

    def run(self, args):
        # Main method that parses weather info based on the selected forecast option
        self._forecast_type = args.forecast_option
        forecast_function = self._forecast_function_mappings[self._forecast_type]
        return forecast_function(args)

    def _today_forecast(self, args):
        bs = self._make_http_request(args)
        
        container = bs.find("div", {"data-testid": "CurrentConditionsContainer"})
        criteria = [
            ('span', 'data-testid', 'TemperatureValue'),
            ('div', 'data-testid', 'wxPhrase'),
            ('div', 'class', 'tempHiLoValue')
        ]
        weather_conditions = self._parse(container, criteria, "tuple")

        if len(weather_conditions) < 1:
            raise Exception('Could not parse weather forecast for today.')

        weatherinfo = weather_conditions[0]
        curr_temp = self._clear_str_number(weatherinfo['TemperatureValue'])

        temp_info = weatherinfo['tempHiLoValue'].split('/')
        high_temp = self._clear_str_number(temp_info[0])
        low_temp  = self._clear_str_number(temp_info[1])

        # Parses the "Weather Today in {location}" card for wind & humidity
        details_container = bs.find("section", { "data-testid" : "TodaysDetailsModule"})
        wind     = details_container.find("span", {"data-testid":"Wind"}).get_text()
        humidity = details_container.find("span", {"data-testid": "PercentageValue"}).get_text()

        # Determine wind direction
        wind_direction_style = details_container.find("svg", {"name": "wind-direction"})["style"]
        degrees = re.findall(r'\d+', wind_direction_style)
        if not degrees:
            self._wind_direction_mappings = {
                "0": "S",
                "45": "SW",
                "90": "W",
                "135": "NW",
                "180": "N",
                "225": "NE",
                "270": "E",
                "315": "SE"
            }
            if degrees[0] in self._wind_direction_mappings:
                wind = self._wind_direction_mappings[degrees[0]] + " " + wind

        self._unit_converter.dest_unit = args.unit

        td_forecast = Forecast(
            self._unit_converter.convert(curr_temp),
            humidity,
            wind,
            high_temp   = self._unit_converter.convert(high_temp),
            low_temp    = self._unit_converter.convert(low_temp),
            description = weatherinfo['wxPhrase']
        )

        return [td_forecast]

    def _five_day_forecast(self, args):
        bs = self._make_http_request(args)

        container = bs.find('table', class_ = 'twc-table').tbody
        criteria = {
            'date-time': 'span',
            'day-detail': 'span',
            'description': 'td',
            'temp': 'td',
            'wind': 'td',
            'humidity': 'td'
        }
        results = self._parse(container, criteria)

        return self._prepare_data(results, args)

    def _ten_day_forecast(self, args):
        bs = self._make_http_request(args)

        results = self._parse_list_forecast(bs, args)

        # 10 day forecast actually returns 15 days. Pare the list down
        if self._forecast_type == ForecastType.TENDAYS:
            results = results[:10]

        return self._prepare_data(results, args)

    def _weekend_forecast(self, args):
        bs = self._make_http_request(args)

        container = bs.find('section', class_ = 'ls-mod').div.div
        criteria = {
            'weather-cell': 'header',
            'temp': 'p',
            'weather-phrase': 'h3',
            'wind-conditions': 'p',
            'humidity': 'p'
        }
        partial_results = self._parse(container, criteria)

        mapper = Mapper()
        mapper.remap_key('wind-conditions', 'wind')
        mapper.remap_key('weather-phrase', 'description')
        results = mapper.remap(partial_results)

        return self._prepare_data(results, args)

    def _make_http_request(self, args):
        # Makes the HTTP request & returns a BeautifulSoup object

        # TODO: Remove this debugger code when done
        # filename_mappings = {
        #     ForecastType.TODAY: "today.html",
        #     ForecastType.FIVEDAYS: "5day.html",
        #     ForecastType.TENDAYS: "10day.html",
        #     ForecastType.WEEKEND: "weekend.html"
        # }
        # filename = filename_mappings[self._forecast_type]
        # with open(filename, encoding = "utf-8") as f:
        #     content = f.read()

        content = self._request.fetch_data(
            self._forecast_type.value,
            args.area_code
        )
        bs = BeautifulSoup(content, 'html.parser')
        return bs

    def _parse(self, container, criteria, useTuple = None):
        results = [self._get_data(item, criteria) for item in container.children] 
        return [result for result in results if result]

    def _get_data(self, container, search_items):
        # Called by _parse() to return a list of controls in the DOM container that match search_items
        scraped_data = {}

        if type(search_items) is dict:
            # dictionary (key = class name, value = HTML tag)
            for key, value in search_items.items():
                result = container.find(value, class_ = key)
                data = None \
                    if result is None \
                    else result.get_text()
                if data is not None:
                    scraped_data[key] = data
        elif type(search_items) is list and type(search_items[0]) == tuple:
            # tuple list (HTML tag, attribute name, attribute ID)
            for tpl in search_items:
                result = container.find(tpl[0], {"class": re.compile(tpl[2])}) \
                    if tpl[1] == 'class' \
                    else container.find(tpl[0], {tpl[1]: tpl[2]})
                data = None \
                    if result is None \
                    else result.get_text()
                if data is not None:
                    scraped_data[tpl[2]] = data

        return scraped_data

    def _clear_str_number(self, str_number):
        # Clears out non-numeric characters from str_number
        self._only_digits_regex = re.compile('[0-9]+')
        result = self._only_digits_regex.match(str_number)
        return '--' if result is None else result.group()
    
    def _parse_list_forecast(self, bs, args):
        # Only _partially_ works for 5 day
        container = bs.find('table', class_ = 'twc-table').tbody
        criteria = {
            'date-time': 'span',
            'day-detail': 'span',
            'description': 'td',
            'temp': 'td',
            'wind': 'td',
            'humidity': 'td'
        }

        return self._parse(container, criteria)

    def _prepare_data(self, results, args):
        # Used by 5day/10day/weekend forecasts
        forecast_result = []

        self._unit_converter.dest_unit = args.unit
        # self._temp_regex = re.compile(r'([0-9]+)\D{,2}([0-9]+)')

        for item in results:
            high_temp, low_temp = re.findall(r'\d+', item['temp'])

            # specific to weekend forecast markup
            try:
                dateinfo              = item['weather-cell']
                date_time, day_detail = dateinfo[:3], dateinfo[3:]
                item['date-time']     = date_time
                item['day-detail']    = day_detail
            except KeyError:
                pass

            day_forecast = Forecast(
                self._unit_converter.convert(item['temp']),
                item['humidity'],
                item['wind'],
                high_temp     = self._unit_converter.convert(high_temp),
                low_temp      = self._unit_converter.convert(low_temp),
                description   = item['description'].strip(),
                forecast_date = f'{item["date-time"]} {item["day-detail"]}',
                forecast_type = self._forecast_type
            )

            forecast_result.append(day_forecast)

        return forecast_result