"""
Module to create code switch augmentation data to get
improvement by adding english words to some dataset
We will compare these results with baseline results
:author: gurnoorsingh (20221031)
"""

import os
import jsonlines

DATA_DIR = "/home/gurnoor/massive/1.0/data"
TARGET_DIR = "/home/gurnoor/massive/1.0/code_switch_augmentation_data"
FILES = ["ta-IN.jsonl", "hi-IN.jsonl"]

for file in FILES:
    augmented_fh = jsonlines.open(os.path.join(TARGET_DIR, file), 'w')
    with jsonlines.open(os.path.join(DATA_DIR, file)) as fh:
        for row in fh:
            if row["partition"] == "test":
                augmented_fh.write(row)
    augmented_fh.close()