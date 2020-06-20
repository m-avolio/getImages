#!/usr/bin/env python3

import flickrapi
import requests
import os
import shutil
import time
import random
import sys



# API access
flickr = flickrapi.FlickrAPI('7da4eab8d8524b10523562ff506a365e', 'f13d5c53b7777994', cache=True)

# Get Id
groupUrl = 'https://www.flickr.com/groups/sony_alpha/pool/'
group = flickr.urls.lookupGroup(url=groupUrl).find('group')
groupId = group.get('id')

# Make folder for group
dir = group.find('groupname').text
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)
os.chdir(dir)

# Get photos from pool
urls = []
pages = 380

# Get list of photo URLs
for i in range(1, pages):

    # Attempt to connect
    for attempt in range(2):
        try:
            photos = flickr.groups.pools.getPhotos(group_id=groupId, extras='url_c', page=i).find('photos')
            break
        except (ConnectionError, TimeoutError):
            print("trying again...")
        except Exception as e:
            print(e)
            if attempt == 2:
                sys.exit(e)
        time.sleep(random.randint(2500, 3000))

    for j, photo in enumerate(photos):
        url = photo.get('url_c')
        if url is not None:
            urls.append(url)
            print("page " + str(i))
            print("num " + str(j))

# Download pictures and save pictures
for i, url in enumerate(urls):
    num = str(i).zfill(5)
    print(num)
    # Attempt to get request
    for attempt in range(3):
        try:
            image = requests.get(url)
            break
        except (ConnectionError, TimeoutError):
            print("try again...")
        except Exception as e:
            print(e)
            if attempt == 2:
                sys.exit(e)
        time.sleep(random.randint(2500, 3000))

    file = open("SonyAlpha_"+str(num)+".jpg", 'wb')
    file.write(image.content)
    file.close()


