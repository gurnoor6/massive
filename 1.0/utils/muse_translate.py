"""
Module to use MUSE to get bilingual translations
:author: gurnoorsingh (20221031)
"""

def get_translate_dict(src_lang='hi'):
    path = "/home/gurnoor/massive/1.0/utils/MUSE_repo/data/{}-en.txt"
    translate_dict = dict()
    with open(path.format(src_lang)) as fh:
        for line in fh.readlines():
            words = line.strip().split()
            src_word = words[0].strip()
            tgt_word = words[1].strip()
            translate_dict[src_word] = tgt_word

    return translate_dict


def main():
    translate_dict = get_translate_dict("hi")
    print(translate_dict["गुलाबी"])

if __name__ == '__main__':
    main()