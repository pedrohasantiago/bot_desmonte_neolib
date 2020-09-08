import spacy
from spacy.lang import pt
from pathlib import Path

nlp = spacy.load(Path(__file__).parent / 'resources' / 'pt_core_news_md' / 'pt_core_news_md-2.3.0')

def extract_target_from_tweet(phrase: str) -> str:
    doc = nlp(phrase)
    for token in doc:
        if token.text.lower() == 'desmonte':
            target_token = token
            break
    else:
        raise Exception('"Broken" not found in input')
    rights = list(target_token.rights)
    # assert len(rights) == 1, (f'Expected a single set of children to the right'
    #                           f' of "desmonte" in "{phrase}", got: {rights}')
    subtree_init, *_, subtree_end = rights[0].subtree
    return doc[subtree_init.i : subtree_end.i + 1].text