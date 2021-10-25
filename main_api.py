import string
import urllib
import urllib.parse
import shutil
import os
import json

from urllib import request
from concurrent.futures import ThreadPoolExecutor

SEARCH_TERM = "sausage party"
MAX_ITEM_COUNT = 100
BASE_DOWNLOAD_DIR = f"downloaded"
DOWNLOAD_DIR = f"{BASE_DOWNLOAD_DIR}/{SEARCH_TERM}"
API_KEY = "i_dont_matter_anyways"
BASE_URL = f"https://g.tenor.com/v1/search?media_filter=minimal&limit=50&key={API_KEY}"


def clean():
    # create base download dir if not exists
    if not os.path.exists(BASE_DOWNLOAD_DIR):
        os.mkdir(BASE_DOWNLOAD_DIR)

    # remove possible leftovers from previous crawling
    if os.path.exists(DOWNLOAD_DIR):
        try:
            shutil.rmtree(DOWNLOAD_DIR)
        except OSError as e:
            print(f"Error: {DOWNLOAD_DIR} : {e.strerror}")

    # create download dir for search term
    os.mkdir(DOWNLOAD_DIR)


def download_gif(url: string, item_name: string):
    urllib.request.urlretrieve(url, f"{DOWNLOAD_DIR}/{item_name}.gif")


def main():
    clean()

    # split in chunks of 50 (api limit for single fetch = 50)
    for chunk_idx in range(int(MAX_ITEM_COUNT / 50)):
        print(f"--- START CHUNK {chunk_idx + 1} ---")

        # fetch gif list
        search_url = f"{BASE_URL}&q={urllib.parse.quote(SEARCH_TERM)}&pos={chunk_idx * 50}"
        gif_list_json = json.loads(urllib.request.urlopen(search_url).read())['results']

        # initialize thread pool
        pool = ThreadPoolExecutor(20)
        gif_count = 1
        # handle single gifs
        for gif_item in gif_list_json:
            # extract gif name & url
            gif_item_name = gif_item['content_description']
            gif_item_url = gif_item['media'][0]['gif']['url']

            # trigger download
            print(f"{chunk_idx * 50 + gif_count} / {MAX_ITEM_COUNT} {gif_item_url}")
            # async variant
            future = pool.submit(download_gif, gif_item_url, gif_item_name)
            # wait every few hundred items for threads to finish - prevents pool queue to overflow and do nasty stuff
            """if company_count % 400 == 0:
                future.result()"""
            # sync variant
            # download_gif(gif_item_url, gif_item_name)
            gif_count += 1

        print(f"--- END CHUNK {chunk_idx + 1} ---")


if __name__ == '__main__':
    main()
