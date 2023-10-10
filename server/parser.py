import json
from bs4 import BeautifulSoup
from .tab import UltimateTab, UltimateTabInfo

def _tab_info_from_soup(soup: BeautifulSoup) -> UltimateTabInfo:
    '''
    Returns a populated UltimateTabInfo object based on the provided soup.
    Parses based on UG site construction as of 9/3/17.

    Parameters:
        - soup: A BeautifulSoup for a Ultimate Guitar tab's html (or html body)
    '''
    #get store data
    store_data      = soup.find(attrs={'class': 'js-store'})
    page_data       =  json.loads(store_data['data-content'])['store']['page']['data']
    page_tab        = page_data['tab']
    page_tabview    = page_data['tab_view']
    # Get song title and artist
    try:
        song_title   = page_tab['song_name']
    except:
        song_title = "UNKNOWN"

    try:
        artist_name = page_tab['artist_name']
    except:
        artist_name = "UNKNOWN"

    try:
        difficulty = page_tabview['ug_difficulty']
    except:
        difficulty = "UNKNOWN"

    try:
        key = page_tabview['meta']['tonality']
    except:
        key = "UNKNOWN"

    try:
        capo = page_tabview['meta']['capo']
    except:
        key = "UNKNOWN"

    try:
        tuning = page_tabview['meta']['tuning']['value']
    except:
        tuning = "UNKNOWN"

    try:
        author = page_tabview['meta']['author']['name']
    except:
        author = "UNKNOWN"

    tab_info = UltimateTabInfo(song_title, artist_name, author, difficulty, key, capo, tuning)
    display_as_json = json.dumps(tab_info, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    
    return tab_info


def html_tab_to_json_dict(html_body: str, pre_class_tags: [str]) -> json:
    '''
    Returns a json form of a 'pre' tag in an untimate guitar html tabs body.

    Parameters:
        - html_body: The full html body of an ultimate guitar tab site
        - pre_class_tags: An array of strings for the class names of a 'pre' tag where the chords are located to parse
    '''
    soup = BeautifulSoup(html_body, "html.parser")
    store_data      = soup.find(attrs={'class': 'js-store'})
    page_data       =  json.loads(store_data['data-content'])['store']['page']['data']
    page_tabview    = page_data['tab_view']

    # Get UltimateTabInfo object from soup html for artist, title, etc.
    tab_info = _tab_info_from_soup(soup)

    # Get tab's content from html (lyrics + chords)
    tabs_content = page_tabview['wiki_tab']['content']
    jsonToReturn = {
        'tab_info': tab_info.__dict__,
        'tabs_content': tabs_content
    }



    return jsonToReturn
