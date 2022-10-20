"""
Module to convert localization samples into corresponding unchanged versions
:author: gurnoorsingh (20221020)
"""
import os
import re
import jsonlines

DATA_DIR = "./data"
LOCALIZATION_DIR_PATH = "./localization_data"
UNCHANGED_DIR_PATH = "./unchanged_data"

# establish id to slots mapping for english dataset
id_to_slots_english = dict()
with jsonlines.open(os.path.join(DATA_DIR, "en-US.jsonl")) as fh:
    for row in fh:
        slots = [x.strip() for x in re.findall("\[(.*?)\]", row["annot_utt"])]
        slot_filler_dict = {
            x.split(":")[0].strip(): x.split(":")[1].strip() for x in slots
        }
        id_to_slots_english[row["id"]] = slot_filler_dict


for file in os.listdir(LOCALIZATION_DIR_PATH):
    filepath = os.path.join(LOCALIZATION_DIR_PATH, file)
    unchanged_fh = jsonlines.open(os.path.join(UNCHANGED_DIR_PATH, file), "w")

    with jsonlines.open(filepath) as fh:
        for row in fh:
            # skip for english dataset
            if "slot_method" not in row:
                continue

            locale_slot_str = [
                x.strip() for x in re.findall("\[(.*?)\]", row["annot_utt"])
            ]
            locale_slots = {
                x.split(":")[0].strip(): x.split(":")[1].strip()
                for x in locale_slot_str
            }

            english_slots = id_to_slots_english[row["id"]]

            localization_slots = []
            for slot in row["slot_method"]:
                if slot["method"] == "localization":
                    localization_slots.append(slot["slot"])

            for localization_slot in localization_slots:
                try:
                    filler_locale = locale_slots[localization_slot]
                    filler_english = english_slots[localization_slot]
                except:
                    print(locale_slots, row["annot_utt"], row["id"])

                row["utt"] = row["utt"].replace(filler_locale, filler_english)
                row["annot_utt"] = row["annot_utt"].replace(
                    filler_locale, filler_english
                )

            unchanged_fh.write(row)

    unchanged_fh.close()
