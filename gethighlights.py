import re
import glob
import os
import requests
import calendar
import time
import json
import datetime

from variables import authToken, readwiseToken

readwiseUrl = 'https://readwise.io/api/v2/highlights/'
dict = {}
dict['highlights'] = []
contents = []
dictData = {}

# Get highlights
response = requests.get('https://www.shortform.com/api/highlights/?sort=date', headers={"Authorization": "Basic " + authToken, "X-Sf-Client": "11.7.0"})

# Parse JSON body
obj = json.loads(response.content)
for item in obj: # data
    for key in obj[item]: # unnamed full highlight obj
        dictData = {}
        for prop in key: # content, created, id, quote, text...
            if prop == 'content':
                for param in key[prop]: # content_type, doc, id, order, title, url_slug
                    if param == 'doc':
                        for meta in key[prop][param]: # author, cover_image, doc_type, id, title, url_slug
                            value = key[prop][param][meta]
                            if meta == 'author':
                                dictData['author'] = value
                            if meta == 'cover_image':
                                dictData['imageUrl'] = 'https:' + value.replace('\\','')
                            if meta == 'title':
                                dictData['title'] = 'Shortform-' + value
                            if meta == 'url_slug':
                                dictData['source_url'] = 'https://www.shortform.com/app/book/' + value
                    if param == 'order':
                        dictData['location'] = key[prop][param]
                        dictData['location_type'] = 'page'
            if prop == 'created':
                # value = key[prop]
                # Shortform date format: 2021-08-14T21:14:43.107973+00:00
                # Readwise's expected format: 2020-07-14T20:11:24+00:00
                # Current output format: 2021-09-02T18:56:39+00:00
                # Turn value into datetime, remove microseconds, convert it to string, and add : in the timezone.
                value = datetime.datetime.strptime(key[prop], '%Y-%m-%dT%H:%M:%S.%f%z')
                value = value.replace(microsecond=0)
                value = value.strftime('%Y-%m-%dT%H:%M:%S%z')
                tzMins = value[-2:]
                value = value[:-2] + ':' + tzMins
                dictData['highlighted_at'] = value
            if prop == 'quote':
                value = key[prop]
                dictData['text'] = value.replace('\n','')
            if prop == 'text':
                value = key[prop]
                if value != '':
                    dictData['note'] = value
        if dictData != {}:
            dictData['source_type'] = 'book'
            dict['highlights'].append(dictData)

# Send highlights to Readwise
# response = requests.post(
#     url=readwiseUrl,
#     headers={"Authorization": "Token " + readwiseToken},
#     json=dict
# )

print(dict)
