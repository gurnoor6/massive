"""
Module to get samples in Kannada that are predicted wrongly for
localization but correctly for unchanged and vice versa
:author: gurnoorsingh (20221027)
"""
import jsonlines

localization_predicted = dict()
localization_truth = dict()
unchanged_predicted = dict()
unchanged_truth = dict()
with jsonlines.open("localization.jsonl") as fh:
    for row in fh:
        localization_predicted[row["id"]] = row

with jsonlines.open("localization_out.jsonl") as fh:
    for row in fh:
        localization_truth[row["id"]] = row

with jsonlines.open("unchanged.jsonl") as fh:
    for row in fh:
        unchanged_predicted[row["id"]] = row

with jsonlines.open("unchanged_out.jsonl") as fh:
    for row in fh:
        unchanged_truth[row["id"]] = row

wrong_predicted_localization = set()
for k, v in localization_predicted.items():
    if localization_predicted[k]["pred_annot_utt"] != localization_truth[k]["annot_utt"]:
        wrong_predicted_localization.add(k)

wrong_predicted_unchanged = set()
for k,v in unchanged_predicted.items():
    if unchanged_predicted[k]["pred_annot_utt"] != unchanged_truth[k]["annot_utt"]:
        wrong_predicted_unchanged.add(k)

print(len(wrong_predicted_localization))
print(len(wrong_predicted_unchanged))
print("# common wrong predictions:", len(wrong_predicted_localization.intersection(wrong_predicted_unchanged)))

only_localization_wrong = wrong_predicted_localization - wrong_predicted_unchanged
only_unchanged_wrong = wrong_predicted_unchanged - wrong_predicted_localization
print("# Only localization wrong:", len(only_localization_wrong))
print("# Only unchanged wrong:", len(only_unchanged_wrong))

fh = open("localization_wrong.txt", "w")
for idx in only_localization_wrong:
    fh.write(' '.join(localization_predicted[idx]['utt']) + "\n")
    fh.write(localization_predicted[idx]["pred_annot_utt"] + "\n")
    fh.write(localization_truth[idx]["annot_utt"] + "\n\n")
fh.close()

fh = open("unchanged_wrong.txt", "w")
for idx in only_unchanged_wrong:
    fh.write(' '.join(unchanged_predicted[idx]['utt']) + "\n")
    fh.write(unchanged_predicted[idx]["pred_annot_utt"] + "\n")
    fh.write(unchanged_truth[idx]["annot_utt"] + "\n\n")
fh.close()
