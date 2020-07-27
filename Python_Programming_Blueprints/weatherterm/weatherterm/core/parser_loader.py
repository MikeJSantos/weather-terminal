import os
import re
import inspect

def _get_parser_list(dirName):
    # Returns all Python modules that don't have a '__' prefix 
    # in the given directory. File extensions are stripped
    files = [
        f.replace('.py', '')
        for f in os.listdir(dirName)
        if not f.startswith('__')
    ]
    return files

def _import_parsers(parserFiles):
    # Returns a parser dictionary <name, class object>. The method imports parserFiles
    # verifies that they're modules and filters on modules ending in 'parser'
    _modules = __import__(
        'weatherterm.parsers',
        globals(),
        locals(),
        parserFiles,
        0
    )

    regEx = re.compile('.+parser$', re.I)

    _parsers = [
        (key, value) for key, value in inspect.getmembers(_modules)
        if inspect.ismodule(value) and regEx.match(key)
    ]

    _parserDictionary = dict()

    for key, value in _parsers:
        _parserDictionary.update({
            key: value for key, value in inspect.getmembers(value)
            if inspect.isclass(value) and regEx.match(key)
        })

    return _parserDictionary

def load(dirName):
    # Main method. Builds & imports all parsers in the given directory ('weatherterm/parsers')
    parserfiles = _get_parser_list(dirName)
    return _import_parsers(parserfiles)

