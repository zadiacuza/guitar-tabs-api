from server import app
import sys
from flask import request, jsonify
from urllib.parse import urlparse
from .tab_parser import dict_from_ultimate_tab
from .tab_parser import json_from_ultimate_tab
from bs4 import BeautifulSoup



SUPPORTED_UG_URI = 'tabs.ultimate-guitar.com'

@app.route('/')
def index():
    return 'hi'

@app.route('/tab')
def tab():
    try:
        ultimate_url = request.args.get('url')

        # Ensure sanitized URL
        parsed_url = urlparse(ultimate_url)
        location = parsed_url.netloc

        if location != SUPPORTED_UG_URI:
            # Show ultimate URL for debugging
            return jsonify({'error': 'unsupported URL scheme', 'ultimate_url': parsed_url}), 500
            raise Exception('unsupported URL scheme')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    tab_dict = dict_from_ultimate_tab(ultimate_url)
    
    return tab_dict
