import sys
from argparse import ArgumentParser
from weatherterm.core import parser_loader, ForecastType, Unit, SetUnitAction

parsers = parser_loader.load('./weatherterm/parsers')

def _validate_forecast_args(args):
    # Defines default command line arguments, if they aren't supplied
    if args.forecast_option is None:
        args.forecast_option = ForecastType.TODAY
        print(f'Forecasting option not specified. Defaulting to {args.forecast_option}')

    if args.parser is None:
        args.parser = next(iter(parsers))
        print(f'Weather parser not specified. Defaulting to {args.parser}')

# Construct the arguments parser
argparser = ArgumentParser(
    prog = 'weatherterm',
    description = 'Weather info from weather.com on your terminal'
)
required = argparser.add_argument_group('required arguments')

# Define required arguments
required.add_argument(
    '-a',
    '--areacode',
    dest = 'area_code',
    help = 'The code area to get the weather broadcast from. It can be obtained at https://weather.com'
)

unit_values = [name.title() for name, value in Unit.__members__.items()]

# Define optional arguments
argparser.add_argument(
    '-p',
    '--parser',
    choices  = parsers.keys(),
    required = False,
    dest     = 'parser',
    help     = 'Specify which parser is going to be used to scrape weather information'
)
argparser.add_argument(
    '-u',
    '--unit',
    choices  = unit_values,
    required = False,
    action   = SetUnitAction,
    dest     = 'unit',
    help     = 'Specify the unit that will be used to display the temperatures.'
)
argparser.add_argument(
    '-td',
    '--today',
    dest   = 'forecast_option',
    action = 'store_const',
    const  = ForecastType.TODAY,
    help   = 'Show the weater forecast for the current day'
)
argparser.add_argument(
    '-5d',
    '--fivedays',
    dest   = 'forecast_option',
    action = 'store_const',
    const  = ForecastType.FIVEDAYS,
    help   = 'Shows the weather forecast for the next 5 days'
)
argparser.add_argument(
    '-10d',
    '--tendays',
    dest   = 'forecast_option',
    action = 'store_const',
    const  = ForecastType.TENDAYS,
    help   = 'Shows the weather forecast for the next 10 days'
)
argparser.add_argument(
    '-w',
    '--weekend',
    dest   = 'forecast_option',
    action = 'store_const',
    const  = ForecastType.WEEKEND,
    help   = 'Shows the weather forecast for the next or current weekend'
)
argparser.add_argument(
    '-v',
    '--version',
    action  = 'version',
    version = '%(prog)s 1.0'
)

# Parse & validate command line arguments
args = argparser.parse_args()
_validate_forecast_args(args)

# Determine which weather parser to use
cls = parsers[args.parser]
parser = cls()

# Run the weather parser & output the results
results = parser.run(args)

for result in results:
    print(str(result))