import re
import glob
import os
import requests
import calendar
import time
import json

from variables import authToken, filePath, readwiseToken

readwiseUrl = 'https://readwise.io/api/v2/highlights/'


with open(filePath + '/highlights.csv', 'w') as output_file:
    output_file.write('Highlight,Title,Author,URL,Note,Location,"Date"')

# Get highlights

response = requests.get('https://www.shortform.com/api/highlights/?sort=date', headers={"Authorization": "Basic " + authToken})
# print(response.content)

# Parse JSON body

dict = {}

obj = json.loads(response.content)
for item in obj: # data
    for key in obj[item]: # unnamed full highlight obj
        # value = item[key]
        # print(key + ': ' + value)
        # print(key)
        for prop in key: # content, created, id, quote, text...
            # print('prop = ' +  prop)
            if prop == 'content':
                for param in key[prop]: # content_type, doc, id, order, title, url_slug
                    # print(param)
                    if param == 'doc':
                        for meta in key[prop][param]: # author, cover_image, doc_type, id, title, url_slug
                            value = key[prop][param][meta]
                            if meta == 'author':
                                dict['author'] = value
                            if meta == 'cover_image':
                                dict['imageUrl'] = 'https://' + value.replace('\\','')
                            if meta == 'title':
                                dict['title'] = 'Shortform-' + value
                            if meta == 'url_slug':
                                dict['url'] = 'https://www.shortform.com/app/book/' + value
            if prop == 'created':
                value = key[prop]
                dict['date'] = value
            if prop == 'quote':
                value = key[prop]
                dict['highlight'] = value.replace('\n','')
            if prop == 'text':
                value = key[prop]
                dict['note'] = ' ' + value

        # Create CSV
        # with open(filePath + '/highlights.csv', 'a') as output_file:
        #     output_file.write('\n"' + dict['highlight'] + '",' + dict['title'] + ',' + dict['author'] + ',"' + dict['url'] + '","' + dict['note'] + '","","' + dict['date'] + '"')

        # Send data to Readwise
        body = {
            'highlights': [
                {
                    'text': dict['highlight'],
                    'title': dict['title'],
                    'author': dict['author'],
                    'image_url': dict['imageUrl'],
                    'source_url': dict['url'],
                    'source_type': 'book',
                    'note': dict['note'],
                    'highlighted_at': dict['date']
                },
            ],
        }
        response = requests.post(
            url=readwiseUrl,
            headers={"Authorization": "Token " + readwiseToken},
            json={
                'highlights': [{
                        'text': dict['highlight'],
                        'title': dict['title'],
                        'author': dict['author'],
                        'image_url': dict['imageUrl'],
                        'source_url': dict['url'],
                        'source_type': 'book',
                        'highlighted_at': dict['date'],
                }]
            }
        )
        print(response.content)
