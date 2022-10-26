"""
Script to view code switched examples for a given language
:author: gurnoorsingh (20221022)
"""

import os
import re
import jsonlines
from utils.translate import translate_text

DATA_DIR = "/home/gurnoor/massive/1.0/data"
FILES = ["hi-IN.jsonl", "kn-IN.jsonl", "ml-IN.jsonl", "ta-IN.jsonl", "te-IN.jsonl"]
CODE_SWITCHED_DIR = "./code_switched_data"

for file in FILES:
    code_switched_file = jsonlines.open(os.path.join(CODE_SWITCHED_DIR, file), 'w')
    with jsonlines.open(os.path.join(DATA_DIR, file)) as fh:
        for row in fh:
            if row["partition"] != "test":
                continue
            utt = row["utt"]
            if re.match(".*[a-zA-Z].*", utt):
                print(utt)
                print(translate_text(utt, "en", "hi"))
                code_switched_file.write(row)
    code_switched_file.close()
