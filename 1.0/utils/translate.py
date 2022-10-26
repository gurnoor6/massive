"""
Module to have functions related to translation
:author: gurnoorsingh (20221026)
"""
import os
from google.cloud import translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/gurnoor/massive/1.0/google_cloud_creds/key.json"
PROJECT_ID = "key-airlock-366105"
parent = f"projects/{PROJECT_ID}"
client = translate.TranslationServiceClient()

def translate_text(text, source_lang=None, target_lang="en"):
    response = client.translate_text(
        contents = [text],
        source_language_code=source_lang,
        target_language_code=target_lang,
        parent=parent
    )

    return response.translations[0].translated_text

if __name__ == '__main__':
    translate_text("hello", target_lang="hi")
