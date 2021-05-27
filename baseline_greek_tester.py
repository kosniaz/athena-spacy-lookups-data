import spacy
from spacy.language import Language

@Language.component("pos_preprocessor")
def pos_preprocessor(doc, pos_tag="NOUN"):
    """
    Function to set manual the pos before the lemmatizer

    This function will handle only the case that we have on doc (one word) in
    the sentence that we wont to be lemmatized
    """

    for i, token in enumerate(doc):
        token.pos_ = pos_tag

    return doc

nlp = spacy.load("el_core_news_md")

nlp.add_pipe("pos_preprocessor",before="lemmatizer")

word = "Πεταλούδας"

doc = nlp.make_doc(word)

for name, proc in nlp.pipeline:
    if name == "pos_preprocessor":
       doc = proc(doc,"NOUN")
    elif name == "lemmatizer":
        print("Pre lemmatization: {}".format(doc.text))
        doc = proc(doc)
        print("Post lemmatization: {}".format(doc[0].lemma_))
        

print(doc.text)