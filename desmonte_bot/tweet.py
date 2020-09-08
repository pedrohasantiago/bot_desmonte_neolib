from typing import Final
import random
import tweepy
from .auth import APIWrapper
from . import search

API: Final[tweepy.API] = APIWrapper().api

tweet_parts = { # This is in global scope so it is easier to test
    'subject': 'O desmonte {target} é',
    'predicates': [
        ('a {compl} do neoliberalismo', ('meta', 'função', 'estratégia')),
        'o projeto neoliberal'
    ]
}

def tweet():
    for target in search.iter_target_from_all_tweets():
        if not search.has_bot_tweeted_this(target):
            text = make_tweet(target)
            API.update_status(text)
            break
    else:
        raise Exception('No "desmonte" tweet found')

def make_tweet(desmonte_target: str) -> str:
    predicate_parts = random.choice(tweet_parts['predicates'])
    if isinstance(predicate_parts, tuple):
        compl = random.choice(predicate_parts[1])
        predicate = predicate_parts[0].format(compl=compl)
    elif isinstance(predicate_parts, str):
        predicate = predicate_parts
    else:
        raise Exception('Unexpected type for predicate')
    return (tweet_parts['subject'] + ' ' + predicate).format(target=desmonte_target)