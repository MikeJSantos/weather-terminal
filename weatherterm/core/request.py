import os
from selenium import webdriver

class Request:
    def __init__(self, base_url):
        self._phantomjs_path = os.path.join(
            os.curdir, 'phantomjs/bin/phantomjs'
        )

        self._base_url = base_url
        self._driver = webdriver.PhantomJS(self._phantomjs_path)

    def fetch_data(self, forecast_option, area_code):
        # Performs the URL request and returns the page source
        # throwing an exception if a 404 code is returned
        url = self._base_url.format(forecast_option = forecast_option, area_code = area_code)
        self._driver.get(url)

        if self._driver.title == '404 Not Found':
            error_message = 'Could not find the area that you''re searching for'
            raise Exception(error_message)
        
        return self._driver.page_source