"""
Module to count number of samples in train
dev and test for a given file
:author: gurnoorsingh (20221026)
"""
import jsonlines
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True,\
     help="Path of jsonl file for which the information is needed")
args = parser.parse_args()

counter = defaultdict(lambda: 0)
with jsonlines.open(args.file) as fh:
    for row in fh:
        counter[row["partition"]] += 1

for key, val in counter.items():
    print(key, val)
