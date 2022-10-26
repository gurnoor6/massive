"""
Module to separate all localization instances into test set
so we can infer on the localization samples
:author: gurnoorsingh (20221026)
"""
import os
import shutil
import jsonlines

DATA_DIR = "/home/gurnoor/massive/1.0/data"
PROCESSED_DATA_DIR = "/home/gurnoor/massive/1.0/zeroshot_localization_data"
FILES = ["hi-IN.jsonl", "kn-IN.jsonl", "ml-IN.jsonl", "ta-IN.jsonl", "te-IN.jsonl"]

def get_localization_number(filepath):
    cntr = 0
    with jsonlines.open(filepath) as fh:
        for row in fh:
            if "slot_method" in row:
                for slot_method in row["slot_method"]:
                    if slot_method["method"] == "localization" \
                        and row["partition"] == "train":
                        cntr += 1
                        break
    
    return cntr

for file in os.listdir(DATA_DIR):
    data_file = os.path.join(DATA_DIR, file)
    processed_data_file = os.path.join(PROCESSED_DATA_DIR, file)

    # if not an indian language, copy data as it is
    if file not in FILES:
        shutil.copyfile(data_file, processed_data_file)
        continue

    processed_fh = jsonlines.open(processed_data_file, 'w')

    # counter to keep a track of localization samples shifted from
    # train to test. A positive value +x means x localization samples
    # have been shifted (or will be shifted) from train into test set
    # Used to keep a track of number of samples to shift from train
    data_shift_cntr = get_localization_number(data_file)

    # counter to decide whether to add to test or dev
    add_to_test_cntr = 0

    with jsonlines.open(data_file) as fh:
        for row in fh:
            # boolean indicating whether the sentence is localization sentence
            is_localization_sent = False

            # must be true for indian languages
            assert "slot_method" in row

            for slot_method in row["slot_method"]:
                # remove localization samples from train partition
                # however keep them in both dev and test samples
                if slot_method["method"] == "localization":
                    is_localization_sent = True
                    if row["partition"] == "train":

                        # Distribute localization samples among test and dev sets
                        # the distribution is done considering ratio of number of
                        # samples and test and dev sets to keep total number constant
                        if add_to_test_cntr >= 0:
                            row["partition"] = "test"
                            add_to_test_cntr -= 1
                        else:
                            row["partition"] = "dev"
            
            if not is_localization_sent \
                and data_shift_cntr > 0 \
                and row["partition"] != "train":

                # keep track of from where was the sample removed
                if row["partition"] == "test":
                    add_to_test_cntr += 1

                row["partition"] = "train"
                data_shift_cntr -= 1

            processed_fh.write(row)

    print(file, data_shift_cntr)
