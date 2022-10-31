"""
Module to get tfidf scores for the hindi and tamil datasets
:author: gurnoorsingh (20221031)
"""
import os
import re
import jsonlines
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = "/home/gurnoor/massive/1.0/data"

def get_idfs(lang='hi'):
    file = f"{lang}-IN.jsonl"
    content = []
    unique_words = set()
    with jsonlines.open(os.path.join(DATA_DIR, file)) as fh:
        for row in fh:
            content.append(row["utt"])
            for word in row["utt"].split():
                unique_words.add(word)

    # need to add vocabulary explicitly, otherwise some words
    # were being skipped
    tfidf = TfidfVectorizer(vocabulary=unique_words)
    tfidf.fit_transform(content)

    # tuple of word, idf pairs
    idf_values = dict()
    for word, idf in zip(tfidf.get_feature_names(), tfidf.idf_):
        # non english word
        if re.match("[a-zA-Z]", word) is None:
            idf_values[word] = idf

    return idf_values

def main():
    idf_values = get_idfs()
    for word, idf in idf_values.items():
        print(word, idf)

if __name__ == '__main__':
    main()