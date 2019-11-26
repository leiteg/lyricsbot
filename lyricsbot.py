#!/usr/bin/env python3

import tweepy as tp
import logging
import sys
import os

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


logging.basicConfig(level=logging.INFO,
                    filename='log-lyricsbot.txt',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='[%Y/%d/%m %H:%M:%S]')
log = logging.getLogger()


def create_api():
    auth = tp.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    API = tp.API(auth)
    try:
        API.verify_credentials()
        log.info("Tweepy API created successfully!")
    except tp.TweepError as e:
        log.critical("Error verifying Tweept API credentials.\n\t%s", str(e))
        sys.exit(1)
    return API


def update_status(api, verses, index):
    if index >= len(verses):
        index = index % len(verses)
    try:
        status = verses[index]
        api.update_status(status)
        log.info(f"Status updated sucessfully! Status: '{status}'")
    except IndexError as e:
        log.critical("Index error.\n\t%s", str(e))
        sys.exit(3)
    except tp.TweepError as e:
        log.error("Error updating status.\n\t%s", str(e))
    return index + 1


def load_verses(fname):
    verses = []
    try:
        with open(fname) as f:
            verses = [verse.strip() for verse in f.readlines() if verse]
        log.info('Verses loaded sucessfully!')
    except FileNotFoundError as e:
        log.critical('Error loading verses from file.\n\t%s', str(e))
        sys.exit(2)
    return verses


def load_index():
    index = 0
    try:
        with open('index.txt', 'r') as f:
            index = int(f.readline())
        log.info('Index loaded sucessfully!')
    except FileNotFoundError as e:
        log.warning("Error loading index from file.\n\t%s", str(e))
    return index


def save_index(index):
    with open('index.txt', 'w') as f:
        f.write(str(index))


def main():
    log.info('===============================================================')
    lyrics_file = sys.argv[1] if len(sys.argv) > 1 else 'lyrics.txt'
    verses = load_verses(lyrics_file)
    index = load_index()
    api = create_api()
    index = update_status(api, verses, index)
    save_index(index)


if __name__ == '__main__':
    main()
