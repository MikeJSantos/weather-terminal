from .enum.unit import Unit 

class UnitConverter:
    # Converts temperature units between Celsius & Fahrenheit
    def __init__(self, parser_default_unit, destination_unit = None):
        self._parser_default_unit = parser_default_unit
        self._destination_unit = destination_unit
        self._convert_functions = {
            Unit.CELSIUS: self._to_celsius,
            Unit.FAHRENHEIT: self._to_fahrenheit
        }
    
    @property
    def destination_unit(self):
        return self._destination_unit

    @destination_unit.setter
    def destination_unit(self, destination_unit):
        self._destination_unit = destination_unit
    
    def convert(self, temp):
        # parse temp to a float, determine if destination_unit is different than
        # default unit and perform necessary convresions, then return formatted result
        try:
            temperature = float(temp)
        except ValueError:
            return 0
        
        if (self.destination_unit == self._parser_default_unit or self.destination_unit is None):
            return self._format_results(temperature)
        
        func = self._convert_functions[self.destination_unit]
        result = func(temperature)
        
        return self._format_results(result)

    def _format_results(self, value):
        return int(value) if value.is_integer() else f'{value:.1f}'

    def _to_celsius(self, fahrenheit_temp):
        result = (fahrenheit_temp - 32) * 5/9
        return result
    
    def _to_fahrenheit(self, celsius_temp):
        result = (celsius_temp * 9/5) + 32
        return result