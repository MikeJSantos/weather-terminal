import requests, json
from urllib.parse import quote
from .search_type import SearchType
from pytify.core import read_config

def _search(criteria, auth, search_type):
    config = read_config()

    if not criteria:
        raise AttributeError('"criteria" parameter is required.')

    q_type = search_type.name.lower()
    url = f'{config.base_url}/search?q={quote(criteria)}&type={q_type}'
    headers = {'Authorization': f'Bearer {auth.access_token}'}

    response = requests.get(url, headers = headers)

    return json.loads(response.text)

def search_artist(criteria, auth):
    return _search(criteria, auth, SearchType.ARTIST)

def search_album(criteria, auth):
    return _search(criteria, auth, SearchType.ALBUM)

def search_playlist(criteria, auth):
    return _search(criteria, auth, SearchType.PLAYLIST)

def search_track(criteria, auth):
    return _search(criteria, auth, SearchType.TRACK)