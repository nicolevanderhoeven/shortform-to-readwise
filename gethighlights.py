import re
import glob
import os
import requests
import calendar
import time
import json

from variables import authToken, readwiseToken

readwiseUrl = 'https://readwise.io/api/v2/highlights/'
dict = {}
dict['highlights'] = []
contents = []
dictData = {}

# Get highlights
response = requests.get('https://www.shortform.com/api/highlights/?sort=date', headers={"Authorization": "Basic " + authToken})

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
            if prop == 'created':
                value = key[prop]
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
response = requests.post(
    url=readwiseUrl,
    headers={"Authorization": "Token " + readwiseToken},
    json=dict
)
