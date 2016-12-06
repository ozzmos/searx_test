"""
 Swisscows (Web, Images)

 @website     https://swisscows.ch
 @provide-api no

 @using-api   no
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, content
"""

from cgi import escape
from json import loads
from urllib import urlencode, unquote
import re

# engine dependent config
categories = ['general', 'images']
paging = True
language_support = True

# search-url
base_url = 'https://swisscows.ch/'
search_string = '?{query}&page={page}'

# regex
regex_json = re.compile('initialData: {"Request":(.|\n)*},\s*environment')
regex_json_remove_start = re.compile('^initialData:\s*')
regex_json_remove_end = re.compile(',\s*environment$')
regex_img_url_remove_start = re.compile('^https?://i\.swisscows\.ch/\?link=')


# do search-request
def request(query, params):
    if params['language'] == 'all':
        ui_language = 'browser'
        region = 'browser'
    else:
        region = params['language'].replace('_', '-')
        ui_language = params['language'].split('_')[0]

    search_path = search_string.format(
        query=urlencode({'query': query,
                         'uiLanguage': ui_language,
                         'region': region}),
        page=params['pageno'])

    # image search query is something like 'image?{query}&page={page}'
    if params['category'] == 'images':
        search_path = 'image' + search_path

    params['url'] = base_url + search_path

    return params


# get response from search-request
def response(resp):
    results = []

    json_regex = regex_json.search(resp.content)

    # check if results are returned
    if not json_regex:
        return []

    json_raw = regex_json_remove_end.sub('', regex_json_remove_start.sub('', json_regex.group()))
    json = loads(json_raw)

    # parse results
    for result in json['Results'].get('items', []):
        result_title = result['Title'].replace(u'\uE000', '').replace(u'\uE001', '')

        # parse image results
        if result.get('ContentType', '').startswith('image'):
            img_url = unquote(regex_img_url_remove_start.sub('', result['Url']))

            # append result
            results.append({'url': result['SourceUrl'],
                            'title': escape(result['Title']),
                            'content': '',
                            'img_src': img_url,
                            'template': 'images.html'})

        # parse general results
        else:
            result_url = result['Url'].replace(u'\uE000', '').replace(u'\uE001', '')
            result_content = result['Description'].replace(u'\uE000', '').replace(u'\uE001', '')

            # append result
            results.append({'url': result_url,
                            'title': escape(result_title),
                            'content': escape(result_content)})

    # parse images
    for result in json.get('Images', []):
        # decode image url
        img_url = unquote(regex_img_url_remove_start.sub('', result['Url']))

        # append result
        results.append({'url': result['SourceUrl'],
                        'title': escape(result['Title']),
                        'content': '',
                        'img_src': img_url,
                        'template': 'images.html'})

    # return results
    return results
