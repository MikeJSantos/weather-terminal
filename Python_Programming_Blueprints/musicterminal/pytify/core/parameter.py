from urllib.parse import urlencode

def validate_params(params, required = None):
    if required is None:
        return
    
    partial = {x: x in params.keys() for x in required}
    not_supplied = [x for x in partial.keys() if not partial[x]]

    if not_supplied:
        error_message = f'The parameter(s) `{", ".join(not_supplied)}` are required'
        raise AttributeError(error_message)

def prepare_params(params, required = None):
    if params is None and required is not None:
        error_message = f'The parameter(s) `{", ".join(required)}` are required'
        raise AttributeError(error_message)
    elif params is None and required is None:
        return ''
    else:
        validate_params(params, required)

    query = urlencode('&'.join([f'{key}={value}' for key, value in params.items()]))

    return f'?{query}'