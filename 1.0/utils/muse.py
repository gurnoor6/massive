"""
Module to use MUSE to get bilingual translations
:author: gurnoorsingh (20221031)
"""

def translate(src, src_lang='hi'):
    path = "/home/gurnoor/massive/1.0/utils/MUSE_repo/data/{}-en.txt"
    with open(path.format(src_lang)) as fh:
        for line in fh.readlines():
            words = line.strip().split()
            src_word = words[0].strip()
            if src_word == src:
                return words[1].strip()

    return None


def main():
    print(translate("போடு", "ta"))

if __name__ == '__main__':
    main()