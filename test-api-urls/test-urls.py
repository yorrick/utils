#!/usr/bin/env python

from collections import namedtuple, defaultdict
import urllib2
import base64
import pprint
import json


SiteInfo = namedtuple('SiteInfo', 'dns http_user http_password')


SITES = {
    'dev from inside':  SiteInfo('devapi.mtl.auto', '', ''),
    'dev from outside': SiteInfo('devapi.mtlevolio.com', 'voiturolio-dev', 'F557Gj4_CiqggYU1apbVAfw9'),
    'staging': SiteInfo('stagapi.mtlevolio.com', 'voiturolio-dev', '2I5OlwMdj2RBRAdGIE0h8_iW'),
    'prod': SiteInfo('api.mtlevolio.com', 'voiturolio-dev', 'wZsNG0ppmLigcnHWO5_yiuIl'),
}


LANGUAGES = (
    '/en',
    '/fr',
)

URLS = (
    '/promos/oem/all_makes/on/',
    '/promos/house/on/',
)


def all_api_urls():
    return ((site_desc,
             'http://{}{}{}'.format(site_info.dns, lang, url),
             site_info.http_user,
             site_info.http_password,
    ) for site_desc, site_info in SITES.items() for lang in LANGUAGES for url in URLS)


def is_success(response):
    # 200
    if not response.getcode() == 200:
        return (False, 'Wrong return code: {0}'.format(response.getcode()))

    # json content
    content_type = response.info().getheader('Content-Type')
    if not 'json' in content_type:
        return (False, 'Wrong content type: {0}'.format(content_type))

    try:
        json.loads(response.read())
    except Exception as e:
        return (False, 'Exception during json content load: {0}'.format(e))

    return (True, '')


def make_request(url, user, password):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    return urllib2.urlopen(request)


def test_urls():
    commands = all_api_urls()

    responses = ((desc, url, make_request(url, user, password))
        for desc, url, user, password in commands)

    results = list((desc, url, is_success(response)) for desc, url, response in responses)

    dict_result = defaultdict(list)
    for desc, url, res_tuple in results:
        dict_result[desc].append((url, res_tuple))

    pp = pprint.PrettyPrinter(indent=4, width=200)
    pp.pprint(dict(dict_result))


if __name__ == '__main__':
    test_urls()


## dev current from inside
#curl http://devapi.mtl.auto/en/promos/oem/all_makes/on/
#curl http://devapi.mtl.auto/en/promos/house/on/
#
## dev current from outside (with auth)
#curl -u voiturolio-dev:F557Gj4_CiqggYU1apbVAfw9 http://devapi.mtlevolio.com/en/promos/oem/all_makes/on/
#curl -u voiturolio-dev:F557Gj4_CiqggYU1apbVAfw9 http://devapi.mtlevolio.com/en/promos/house/on/
#
## dev stable from inside
#curl http://api.mtl.auto/en/promos/oem/all_makes/on/
#curl http://api.mtl.auto/en/promos/house/on/
#
## dev current from outside (with auth)
#curl -u voiturolio-dev:F557Gj4_CiqggYU1apbVAfw9 http://api.mtl.auto/en/promos/oem/all_makes/on/
#curl -u voiturolio-dev:F557Gj4_CiqggYU1apbVAfw9 http://api.mtlevolio.com/en/promos/house/on/ FAIL
#
## staging
#curl -u voiturolio-dev:2I5OlwMdj2RBRAdGIE0h8_iW http://stagapi.mtlevolio.com/en/promos/oem/all_makes/on/
#curl -u voiturolio-dev:2I5OlwMdj2RBRAdGIE0h8_iW http://stagapi.mtlevolio.com/en/promos/house/on/
#
## prod
#curl -u voiturolio-dev:2I5OlwMdj2RBRAdGIE0h8_iW http://api.mtlevolio.com/en/promos/oem/all_makes/on/
#curl -u voiturolio-dev:2I5OlwMdj2RBRAdGIE0h8_iW http://api.mtlevolio.com/en/promos/house/on/
