"""
Module to get localization samples from all samples
:author: gurnoorsingh (20221020)
"""
import os

DATA_FOLDER = "./data"
for file in os.listdir(DATA_FOLDER):
    print(file)