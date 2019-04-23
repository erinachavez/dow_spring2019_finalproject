from flask import Blueprint

ca_blueprint = Blueprint('chain_abstractions', __name__)

import json
import spacy
import random
import tracery
from tracery.modifiers import base_english

# initialize spaCy
nlp = spacy.load("en")

def findMatch(i, this_thread, compounds):
    for j in compounds["compounds"]:
        if i["secondWord"] == j["firstWord"]:
            if len(this_thread) == 0 or i != this_thread[-1]:
                this_thread.append(i)
            this_thread.append(j)
            i = j
            this_thread = findMatch(i, this_thread, compounds)
            break

    return this_thread

def getType(word):
    doc = nlp(word)

    for word in doc:
        if word.pos_ == "ADJ" or word.pos_ == "ADP":
            return "to be"

        elif word.pos_ == "VERB":
            return "to"

        elif word.pos_ == "NOUN":
            return "a"

        else:
            return ""

@ca_blueprint.route('/chain_abstractions')
def chain_abstractions():
    # load words and clues
    four = json.load(open("assets/clues_four.json"))
    five = json.load(open("assets/clues_five.json"))
    six = json.load(open("assets/clues_six.json"))

    source = dict(four["data"], **five["data"], **six["data"])

    # load compound words
    compounds = json.load(open("assets/compounds.json"))

    all_threads = []
    this_thread = []

    # get all possible threads in compounds.json
    for i in compounds["compounds"]:
        final_thread = findMatch(i, this_thread, compounds)

        if len(final_thread) != 0:
            all_threads.append(final_thread)

        this_thread = []

    # matching threads to clues
    poem_threads_all = []
    poem_thread = {}

    for thread in all_threads:
        for i in range(len(thread)):
            if thread[i]["firstWord"] in source.keys():
                this_word = (thread[i]["firstWord"],thread[i]["secondWord"])
                poem_thread[this_word] = source[thread[i]["firstWord"]]

            else:
                break

        poem_threads_all.append(poem_thread)
        poem_thread = {}

    # clean up poem threads
    poem_threads_len = len(poem_threads_all)
    poem_threads = []

    for i in range(poem_threads_len - 1):
        if len(poem_threads_all[i]) > 1:
            poem_threads.append(poem_threads_all[i])

    # put it all together
    poem_thread = random.choice(poem_threads)

    last_phrase = ""
    last_word = ""
    first = True

    poem = ""

    for key,value in poem_thread.items():
        rules = {
            "body_first": "<p>#phrase.capitalize# #word#</p><p>&nbsp;&nbsp;&nbsp;&nbsp;is #phrase# #clue#,</p><p>#numSpace#but #phrase# #compound# is</p>",
            "body_noun_first": "<p>#word.a.capitalize#</p><p>&nbsp;&nbsp;&nbsp;&nbsp;is #clue.a#,</p><p>#numSpace#but #compound.a# is</p>",

            "body": "<p>#phrase# #word#</p><p>&nbsp;&nbsp;&nbsp;&nbsp;is #phrase# #clue#,</p><p>#numSpace#but #phrase# #compound# is</p>",
            "body_noun": "<p>#word.a#</p><p>&nbsp;&nbsp;&nbsp;&nbsp;is #clue.a#,</p><p>#numSpace#but #compound.a# is</p>",

            "phrase": getType(key[0]),
            "word": key[0],
            "clue": value,
            "numSpace": "&nbsp;"*(len("#clue#") + len(key[1])),
            "compound": key[0] + key[1]
        }

        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)

        if first and getType(key[0]) == "a":
            poem += grammar.flatten("#body_noun_first#")
            first = False

        elif first:
            poem += grammar.flatten("#body_first#")
            first = False

        elif getType(key[0]) == "a":
            poem += grammar.flatten("#body_noun#")

        else:
            poem += grammar.flatten("#body#")

        last_phrase = getType(key[0])
        last_word = key[1]


    last_line_rules = {
        "last": "#phrase# #word#?",
        "last_noun": "#word.a#?",
        "phrase": last_phrase,
        "word": last_word
    }
    grammar = tracery.Grammar(last_line_rules)
    grammar.add_modifiers(base_english)

    if last_phrase == "a":
        poem += grammar.flatten("#last_noun#")

    else:
        poem += grammar.flatten("#last#")

    return poem
