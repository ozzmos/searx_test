"""
 Yahoo (Web)

 @website     https://yandex.ru/
 @provide-api ?
 @using-api   no
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, content
"""

from cgi import escape
from urllib import urlencode
from lxml import html
from searx.search import logger

logger = logger.getChild('yandex engine')

# engine dependent config
categories = ['general']
paging = True
language_support = True  # TODO

default_tld = 'com'
language_map = {'ru': 'ru',
                'ua': 'uk',
                'tr': 'com.tr'}

# search-url
base_url = 'https://yandex.{tld}/'
search_url = 'search/?{query}&p={page}'

results_xpath = '//div[@class="serp-item serp-item_plain_yes clearfix i-bem"]'
url_xpath = './/h2/a/@href'
title_xpath = './/h2/a//text()'
content_xpath = './/div[@class="serp-item__text"]//text()'


def request(query, params):
    lang = params['language'].split('_')[0]
    host = base_url.format(tld=language_map.get(lang) or default_tld)
    params['url'] = host + search_url.format(page=params['pageno'] - 1,
                                             query=urlencode({'text': query}))
    return params


# get response from search-request
def response(resp):
    dom = html.fromstring(resp.text)
    results = []

    for result in dom.xpath(results_xpath):
        try:
            res = {'url': result.xpath(url_xpath)[0],
                   'title': escape(''.join(result.xpath(title_xpath))),
                   'content': escape(''.join(result.xpath(content_xpath)))}
        except:
            logger.exception('yandex parse crash')
            continue

        results.append(res)

    return results
