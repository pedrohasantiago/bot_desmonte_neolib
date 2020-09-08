from typing import Final, Optional, Iterator
import tweepy
from .auth import APIWrapper, BOT_HANDLE
from . import nlp

API: Final[tweepy.API] = APIWrapper().api

queries = {
    'desmonte': '"desmonte do" OR "desmonde da" OR "desmonde de" -filter:links',
    'from_bot': f'from:{BOT_HANDLE}'
}

def get_last_own_tweet() -> Optional[tweepy.Status]:
    r = API.search(queries['from_bot'], result_type='recent')
    if r:
        return r[0]
    else:
        return None

def iter_desmonte_tweets(
        since_last_own_tweet: bool = True) -> Iterator[tweepy.Status]:
    search_params = {
        'q': queries['desmonte'],
        'lang': 'pt',
        'result_type': 'recent',
        'tweet_mode': 'extended',
        'count': '30' # Default is 15
    }
    if since_last_own_tweet and (own_last_tweet := get_last_own_tweet()):
        search_params['since_id'] = own_last_tweet.id
    cursor = tweepy.Cursor(API.search, **search_params)
    iterator = cursor.items()
    # Somehow, results may not have "desmonte" in them. Let's filter
    # these tweets out:
    yield from filter(lambda tweet: 'desmonte' in tweet.full_text, iterator)

def iter_target_from_all_tweets() -> Iterator[str]:
    """First searches in recent tweets only, than in all tweets."""
    for boolean in (True, False):
        for tweet in iter_desmonte_tweets(since_last_own_tweet=boolean):
            yield nlp.extract_target_from_tweet(tweet.full_text)

def has_bot_tweeted_this(desmonte_target: str) -> bool:
    results = API.search(f'"{desmonte_target}" {queries["from_bot"]}')
    if results:
        return True
    else:
        return False