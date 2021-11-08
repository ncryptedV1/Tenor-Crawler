# Tenor-Crawler
A small demonstration of web crawlers exemplary on tenor. Automatically crawl a set amount of gifs for a given search term.
An implementation for using an API and parsing static websites.

## Prerequisites
- [Python 3](https://www.python.org/) (adaptation to Python 2 is possible but requires a few tweaks)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## Usage
- choose which way you want to fetch data:
  - API: `main_api.py`
  - Custom (via parsing by Beautiful Soup): `main_custom.py`
- adapt crawl parameters (variables at the beginning of the respective script):
  - `SEARCH_TERM`: search term to download gifs for
  - `MAX_ITEM_COUNT`: maximum amount of gifs to download
  - `BASE_DOWNLOAD_DIR`: relative directory path to target folder
  - `THREAD_POOL_SIZE`: amount of threads to use for parallel downloading
  - Optional `API_KEY`: only present in `main_api.py` and needs to be supplied for the API-call
    - for some reason it doesn't matter whether the key is valid (at least in this use case)
- run the script

## Notes
- by default both scripts work asynchronously - can be adapted to synchronous variant in `main` method

## Presentation
The slides of the presentation can be found [here](https://docs.google.com/presentation/d/1mUG8m51f02DZMbdAGZz4GQBeIMiC9Sgs4OaTIWvG5Nw/edit?usp=sharing).
