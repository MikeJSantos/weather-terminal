import requests, base64, json
from .authorization import Authorization
from pytify.core import BadRequestError

def get_auth_key(client_id, client_secret):
    byte_keys = bytes(f'{client_id}:{client_secret}', 'utf-8')
    encoded_key = base64.b64encode(byte_keys)
    return encoded_key.decode('utf-8')

def _client_credentials(config):
    auth_key = get_auth_key(config.client_id, config.client_secret)
    headers = {'Authorization': f'Basic {auth_key}'}

    options = {
        'grant_type': 'client_credentials',
        'json': 'true'
    }

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers = headers,
        data    = options
    )

    content = json.loads(response.content.decode('utf-8'))

    if response.status_code == 400:
        error_description = content.get('error_description')
        raise BadRequestError(error_description)

    access_token = content.get('access_token', None)
    token_type   = content.get('token_type', None)
    expires_in   = content.get('expires_in', None)
    scope        = content.get('scope', None)

    return Authorization(access_token, token_type, expires_in, scope, None)

def authenticate(config):
    return _client_credentials(config)