from unittest import TestCase
from unittest.mock import patch
from .. import search
from .. import nlp

class TestNLP(TestCase):

    def test_iter_target_from_all_tweets(self):
        # When nlp.extract_target_from_tweet raises custom error
        with patch(__name__ + '.nlp.spacy.tokens.Token') as mock_token:
            mock_token.rights = iter([])
            i = search.iter_target_from_all_tweets()
            a_string = next(i)
            if not a_string or not isinstance(a_string, str):
                raise Exception