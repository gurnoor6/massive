"""
Module to get localization samples from all samples
:author: gurnoorsingh (20221020)
"""
import os
import jsonlines

DATA_DIR = "./data"
LOCALIZATION_DIR_PATH = "./localization_data"

for file in os.listdir(DATA_DIR):
    filepath = os.path.join(DATA_DIR, file)
    localization_file_path = os.path.join(LOCALIZATION_DIR_PATH, file)

    # create a localization filtered profile for that specific locale
    localization_fh = jsonlines.open(localization_file_path, 'w')
    with jsonlines.open(filepath) as fh:
        for row in fh:
            # slot_method will not exist in english dataset
            if "slot_method" in row:
                # filter all localization samples and write them to a file
                # if any of the slots used the localization methos
                # classify the sentence as a localization sample
                if any(slots["method"] == "localization" for slots in row["slot_method"]):
                    localization_fh.write(row)

    localization_fh.close()