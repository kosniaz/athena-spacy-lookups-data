#python script to load a lemmatizer object, load the custom rules and test them against a predefined json or csv file
"""
This script is made for handling - testing a custom spacy lemmatizer.

It will handle one file named: "lemmatizer_test.json" that is a json.
This file must have the following structure (remember python's dictionaries)

{"key_1": ["POS_TAG_1","TRUE_VALUE_1],
"key_2": ["POS_TAG_2","TRUE_VALUE_2],
...
...
"key_N": ["POS_TAG_N","TRUE_VALUE_N]}

DISCLAIMER: the second true value will be lowercased by default from spaCy.
Keep it that way.

After that, it will output a csv file with three columns.
The first will be for the test word (e.g. "Πεταλούδας" - key from dict - json)
The second will be for the spaCy lemmatized word
The third will be the true lemma (e.g. "Πεταλούδα" - value from dict - json)

The output file will be a csv with 4 columns. 
The first will be filled with the original test word
The second will be filled with the original lemmatized version
The third will be filled with the spaCy lemmatized version
The fourth will be an indicator that will have match, failed if there was the same 
    original - test lemmatized and spaCy lemmatized words.
"""
from logging import debug
from numpy.core.einsumfunc import _parse_possible_contraction
import spacy
import json

from spacy.language import Language

@Language.component("pos_preprocessor")
def pos_preprocessor(doc, pos_tag="NOUN"):
    """
    Function to set manual the pos before the lemmatizer

    This function will handle only the case that we have on doc (one word) in
    the sentence that we wont to be lemmatized
    """
    doc[0].pos_ = pos_tag

    return doc

lookups = spacy.lookups.Lookups()

nlp = spacy.blank("el")

#add tables from the spacy-lookups-data, the path needs to change
debug_mode = False

if debug_mode:
    for_debug = "spacy_test_ground/"
else:
    for_debug = ""
path_to_tables = "spacy-lookups-data/spacy_lookups_data/data/"

name_of_tables = ["el_lemma_exc.json",
                    "el_lemma_index.json",
                    "el_lemma_rules.json",
                    "el_lexeme_norm.json",
                    "el_lexeme_prob.json",
                    "el_lexeme_settings.json"]

for table in name_of_tables:

    table_f = open(for_debug + path_to_tables + table, "r")
    table_dict = json.load(table_f)
    table_f.close()

    table_name = table.replace(".json", "")
    table_name = table_name.replace("el_", "")
    
    lookups.add_table(table_name, table_dict)

config = {"mode": "rule",
            "overwrite": True}

lemmatizer = nlp.add_pipe("lemmatizer", config=config)
nlp.add_pipe("pos_preprocessor",before="lemmatizer")
lemmatizer.initialize(lookups=lookups)

nlp.initialize()

testing_f = open(for_debug + "lemmatizer_test.json", "r")
testing_dict = json.load(testing_f)
testing_f.close()

testing_keys = testing_dict.keys()

output_list = []

for count,test_word in enumerate(testing_keys):
    output_list.append([])
    output_list[count].append(test_word)

    pos_outWord = testing_dict[test_word]
    pos_tag = pos_outWord[0]
    true_output = pos_outWord[1]

    doc = nlp.make_doc(test_word)

    #custom walkthrough the components to
    #set manually the pos tag
    for name, proc in nlp.pipeline:
        if name == "pos_preprocessor":
            doc = proc(doc,pos_tag)
        else:
            doc = proc(doc)

    output_list[count].append(true_output)
    output_list[count].append(doc[0].lemma_)

#write the file
output_file = open("lemmatizer_test_output.csv","w")

for test_case in output_list:
    if test_case[1] == test_case[2]:
        output_file.write("{},{},{},{}\n".format(test_case[0],test_case[1],test_case[2],"match"))
    else:
        output_file.write("{},{},{},{}\n".format(test_case[0],test_case[1],test_case[2],"failed"))

output_file.close()