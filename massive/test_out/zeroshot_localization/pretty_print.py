import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--lang", help="2 letter language code", required=True)
args = parser.parse_args()

ex_match_str = "test_{}-IN_ex_match_acc"
intent_acc_str = "test_{}-IN_intent_acc"
slot_f1_str = "test_{}-IN_slot_micro_f1"

with open("result.json") as fh:
    obj = json.loads(fh.read())
    print(f"{obj[ex_match_str.format(args.lang)]*100:.2f}\n")
    print(f"{obj[intent_acc_str.format(args.lang)]*100:.2f}\n")
    print(f"{obj[slot_f1_str.format(args.lang)]:.2f}")