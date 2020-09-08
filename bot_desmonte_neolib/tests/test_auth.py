from unittest import TestCase
from unittest.mock import patch
import tweepy
from .. import auth

class TestAuth(TestCase):
    
    def test_get_environment_var(self):
        # Testing return type
        required_vars = ['TWITTER_CONSUMER_KEY',
                         'TWITTER_CONSUMER_SECRET',
                         'TWITTER_BEARER_TOKEN',
                         'TWITTER_ACCESS_TOKEN',
                         'TWITTER_ACCESS_TOKEN_SECRET']
        for required_var in required_vars:
            self.assertIsInstance(auth._get_environment_var(required_var), str)
        # Tesing return value
        mocked_val = 'mocked_env_val'
        auth_path = __package__.split('.')[0] + '.auth'
        with patch(f'{auth_path}.getenv', return_value=mocked_val):
            self.assertEqual(auth._get_environment_var('anything'), mocked_val)

    def test_api(self):
        api = auth.APIWrapper().api
        # Is it a singleton?
        api2 = auth.APIWrapper().api
        self.assertIs(api, api2)
        # Correct type?
        self.assertIsInstance(api, tweepy.API)
        # Can we actually tweet?
        text = 'Testing API'
        status = api.update_status('Testing API')
        self.assertEqual(api.get_status(status.id).text, text)
        api.destroy_status(status.id)