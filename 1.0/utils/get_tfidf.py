"""
Module to get tfidf scores for the hindi and tamil datasets
:author: gurnoorsingh (20221031)
"""
import os
import re
import jsonlines
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = "/home/gurnoor/massive/1.0/data"

def get_idfs(file="hi-IN.jsonl"):
    content = []
    document_freq = dict()
    with jsonlines.open(os.path.join(DATA_DIR, file)) as fh:
        for row in fh:
            for word in row["utt"].split():
                if re.match("[a-zA-Z]", word) is None:
                    document_freq[word] = document_freq.get(word, 0) + 1

    for word, df in document_freq.items():
        document_freq[word] = 1/df

    return document_freq

def main():
    idf_values = get_idfs("hi-IN.jsonl")
    idf_values_sorted = sorted(idf_values.items(), key=lambda x: x[1], reverse=True)
    for word, idf in idf_values_sorted:
        print(word, idf)

if __name__ == '__main__':
    main()