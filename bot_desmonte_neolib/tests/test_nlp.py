from unittest import TestCase
from .. import nlp

class TestNLP(TestCase):

    def test_extract_target_from_tweet(self):
        phrases_and_targets = {
            'O desmonte da educação pública no Brasil é um projeto do governo neoliberal': 'da educação pública no Brasil',
            'O desmonte da educação pública, no Brasil, é um projeto do governo neoliberal': 'da educação pública',
            'Não podemos ser coniventes com o desmonte do SUS!': 'do SUS',
            'Devemos protestar contra o desmonte das políticas públicas neste país.': 'das políticas públicas neste país',
            'Quando tomaremos ações contra o desmonte que estamos vendo acontecer?': 'que estamos vendo acontecer',
            'É grave o desmonte dos recursos naturais da Amazônia, é muito grave!': 'dos recursos naturais da Amazônia',
            'Quando vamos prestar atenção no desmonte do parque industrial de Manaus?': 'do parque industrial de Manaus',
            'É inacreditável o desmonte da educação pública, gratuita e de qualidade': 'da educação pública, gratuita e de qualidade',
            'O desmonte da Lava-Jato fará muito mal ao país nos próximos anos': 'da Lava-Jato'
        }
        for phrase, target in phrases_and_targets.items():
            r = nlp.extract_target_from_tweet(phrase)
            self.assertEqual(r, target, f'Expected "{target}", got "{r}"')