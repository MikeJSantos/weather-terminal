import sys
from argparse import ArgumentParser
from weatherterm.core import parser_loader
from weatherterm.core import ForecastType
from weatherterm.core import Unit

def _validate_forecast_args(args):
    if args.forecast_option is None:
        err_msg = ('One of these arguments must be used: '
                   '-td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend')
        print(f'{argparser.prog}: error: {err_msg}', file = sys.stderr)
        sys.exit()
        