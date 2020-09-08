import spacy

nlp = spacy.load('pt_core_news_md') # The model is in site-packages

def extract_target_from_tweet(phrase: str) -> str:
    doc = nlp(phrase)
    for token in doc:
        if token.text.lower() == 'desmonte':
            target_token = token
            break
    else:
        raise Exception('"Broken" not found in input')
    rights = list(target_token.rights)
    # We only want the subtree that's the closest to "desmonte"
    # (ie, the first one to the right of it)
    subtree_init, *_, subtree_end = rights[0].subtree
    return doc[subtree_init.i : subtree_end.i + 1].text