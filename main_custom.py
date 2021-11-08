import os
import shutil
import string
import urllib
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from urllib import request

from bs4 import BeautifulSoup

BASE_URL = "https://tenor.com/search"
SEARCH_TERM = "sausage party"
# restricted to 50 for initial load
# expansion possible, but requires more effort
MAX_ITEM_COUNT = 5000
BASE_DOWNLOAD_DIR = f"downloaded"
DOWNLOAD_DIR = f"{BASE_DOWNLOAD_DIR}/{SEARCH_TERM}"
THREAD_POOL_SIZE = 20


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


def download_gif(url: string):
    urllib.request.urlretrieve(url, f"{DOWNLOAD_DIR}/{url.split('/')[-1]}")


def main():
    clean()

    # fetch gif list
    search_url = f"{BASE_URL}/{urllib.parse.quote(SEARCH_TERM)}-gifs?limit={MAX_ITEM_COUNT}"
    bs = BeautifulSoup(urllib.request.urlopen(search_url).read(), features='lxml')
    gif_list_div = bs.find('div', attrs={'class': 'GifList'})

    # initialize thread pool
    pool = ThreadPoolExecutor(THREAD_POOL_SIZE)
    gif_count = 1
    # handle single gifs
    for gif_item_fig in gif_list_div.find_all('figure', attrs={'class': 'GifListItem'}):
        # extract gif url
        gif_item_img = gif_item_fig.find('img')
        gif_item_src = gif_item_img['src']

        # trigger download
        print(f"{gif_count} / {MAX_ITEM_COUNT} {gif_item_src}")
        # async variant
        future = pool.submit(download_gif, gif_item_src)
        # wait every few hundred items for threads to finish - prevents pool queue to overflow and do nasty stuff
        """if company_count % 400 == 0:
            future.result()"""
        # sync variant
        # download_gif(gif_item_src)
        gif_count += 1

        # cancel if max crawl count has been reached
        if gif_count > MAX_ITEM_COUNT:
            break


if __name__ == '__main__':
    main()
