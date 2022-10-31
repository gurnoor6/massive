"""
Module to create code switch augmentation data to get
improvement by adding english words to some dataset
We will compare these results with baseline results
:author: gurnoorsingh (20221031)
"""

import os
import re
import jsonlines
from utils.get_tfidf import get_idfs
from utils.muse_translate import get_translate_dict

DATA_DIR = "/home/gurnoor/massive/1.0/data"
TARGET_DIR = "/home/gurnoor/massive/1.0/code_switch_augmentation_data"
FILES = ["ta-IN.jsonl", "hi-IN.jsonl"]

def translate_utt(utt, annot_utt, idfs, translate_dict):
    words_and_idfs = []
    for word in utt.split():
        if re.match("[a-zA-Z]", word) is None:
            words_and_idfs.append((word, idfs[word]))
    
    if len(words_and_idfs) == 0:
        return utt, annot_utt

    words_and_idfs.sort(key=lambda x: x[1], reverse=True)
    top_word = words_and_idfs[0][0]

    if top_word in translate_dict:
        top_word_translation = translate_dict[top_word]
        new_utt = utt.replace(top_word, top_word_translation)
        new_annot_utt = annot_utt.replace(top_word, top_word_translation)
        return new_utt, new_annot_utt
    
    return utt, annot_utt

for file in FILES:
    augmented_fh = jsonlines.open(os.path.join(TARGET_DIR, file), 'w')
    translate_dict = get_translate_dict(file.split("-")[0])
    idfs = get_idfs(file)
    with jsonlines.open(os.path.join(DATA_DIR, file)) as fh:
        for row in fh:
            if row["partition"] == "test":
                utt = row["utt"]
                annot_utt = row["annot_utt"]

                new_utt, new_annot_utt = translate_utt(utt, annot_utt, idfs, translate_dict)

                row["utt"] = new_utt
                row["annot_utt"] = new_annot_utt

                augmented_fh.write(row)
    augmented_fh.close()