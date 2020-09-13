"""Holds the logic to get a Tweepy API object. Assumes a "key.env" file
exists in the a 'resources' directory in the same folder.

The API object can be retrieved with the APIWrapper().api singleton.
When the API constructor receives a False argument (not the default
behavior), console messages will be exhibited to guide the user to
retrieve an access token, which should be done if it is not yet in the
.env file. When this script is run directly, the constructor is called
with False as an argument.
"""
import tweepy
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Final
from pathlib import Path

BOT_HANDLE: Final[str] = 'desmonte_neolib'

def _get_environment_var(environment_var: str) -> str:
    env_path = Path(__file__).parent / 'resources' / 'keys.env'
    load_dotenv(dotenv_path=env_path)
    r = getenv(environment_var)
    if r is not None:
        return r
    else:
        raise Exception('Environment variable not found')

class APIWrapper:
    """A singleton for tweepy.API"""

    _instance: Optional[tweepy.API] = None

    def __init__(self, env_has_access_token: bool = True):
        # The possibility of env_has_access_token being False is the
        # very reason why this is all inside a class, and not just in a
        # global variable.
        self.env_has_access_token = env_has_access_token

    @property
    def api(self):
        if __class__._instance:
            return __class__._instance
        else:
            __class__._instance = self.instantiate_new_api()
            return __class__._instance

    def instantiate_new_api(self) -> tweepy.API:
        env_vars_to_get = ['consumer_key', 'consumer_secret']
        if self.env_has_access_token:
            env_vars_to_get.extend(['access_token', 'access_token_secret'])
        kwargs = {
            to_get: _get_environment_var('TWITTER_' + to_get.upper())
            for to_get in env_vars_to_get
        }
        return tweepy.API(AuthHandler(**kwargs).auth)

class AuthHandler:
    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token: Optional[str] = None,
                 access_token_secret: Optional[str] = None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        if not access_token or not access_token_secret:
            self.get_access_token()
        else:
            self.auth.set_access_token(access_token, access_token_secret)

    def get_auth_url(self) -> str:
        try:
            redirect_url = self.auth.get_authorization_url()
        except tweepy.TweepError:
            raise Exception('Could not get request token')
        return redirect_url

    def get_access_token(self):
        redirect_url = self.get_auth_url()
        print(f'Authorize the app in: {redirect_url}')
        verifier_code = input('Enter verifier code: ')
        self.request_token = self.auth.request_token['oauth_token']
        self.auth.request_token = {
            'oauth_token': self.request_token,
            'oauth_token_secret': verifier_code
        }
        try:
            self.auth.get_access_token(verifier_code)
        except tweepy.TweepError:
            raise Exception('Failed to get access token')
        print('Save these in the .env file:',
              f'ACCESS_TOKEN: {self.auth.access_token}',
              f'ACCESS_TOKEN_SECRET: {self.auth.access_token_secret}',
              sep='\n')
        input('Press ENTER to continue...')

if __name__ == "__main__":
    APIWrapper(env_has_access_token=False).api