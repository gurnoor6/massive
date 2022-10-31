"""
Module to get localization tokens for a given language in different splits
The purpose of doing this is to see the overlap between the tokens
in train and test sets
:author: gurnoorsingh (20221027)
"""
import os
import jsonlines
import argparse
from collections import defaultdict
from multiset import Multiset

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--lang", help="2 letter filename with country code e.g. hi-IN", required=True)
parser.add_argument("-d", "--duplicates", help="If this flag is set, duplicates are considered while counting the common tokens", action="store_true")
args = parser.parse_args()

DATA_DIR = "/home/gurnoor/massive/1.0/data"

# counter to get the count of incorrectly labelled sentences
incorrect_label_counter = 0

if args.duplicates:
    tokens = defaultdict(lambda: Multiset())
else:
    tokens = defaultdict(lambda: set())

with jsonlines.open(os.path.join(DATA_DIR, f"{args.lang}.jsonl")) as fh:
    for row in fh:
        for slot_method in row["slot_method"]:
            slot = slot_method["slot"]
            method = slot_method["method"]

            if method == "localization":
                annot_utt = row["annot_utt"]
                slot_idx = annot_utt.find(slot)
                filler_end_idx = annot_utt.find("]", slot_idx)
                try:
                    token = annot_utt[slot_idx:filler_end_idx]\
                            .split(":")[1]\
                            .strip()
                except:
                    incorrect_label_counter += 1

                tokens[row["partition"]].add(token)

print(f"====== {incorrect_label_counter} sentences skipped due to incorrect label=======")

train_tokens, test_tokens = tokens["train"], tokens["test"]
overlap_tokens = train_tokens.intersection(test_tokens)

print("Train tokens:", len(train_tokens))
print("Test tokens:", len(test_tokens))
print("Overlap tokens:", len(overlap_tokens))
