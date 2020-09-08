from unittest import TestCase
from .. import tweet

class TestTweet(TestCase):

    def test_make_tweet(self):
        targets = [
            'da educação pública no Brasil',
            'da educação pública',
            'do SUS',
            'das políticas públicas neste país',
            'que estamos vendo acontecer',
            'dos recursos naturais da Amazônia',
            'do parque industrial de Manaus',
            'da educação pública, gratuita e de qualidade',
            'da Lava-Jato'
        ]

        subject = tweet.tweet_parts['subject']
        predicates = tweet.tweet_parts['predicates']
        
        all_poss = []
        for predicate in predicates:
            if isinstance(predicate, tuple):
                assert len(predicate) == 2, 'Expected composable predicates to be a tuple with 2 elements'
                for compl in predicate[1]:
                    all_poss.append(subject + ' ' + predicate[0].format(compl=compl))
            elif isinstance(predicate, str):
                all_poss.append(subject + ' ' + predicate)
            else:
                raise Exception('Predicate in tweet.tweet_parts has unexpected type')

        for target in targets:
            self.assertIn(tweet.make_tweet(target), [poss.format(target=target) for poss in all_poss])