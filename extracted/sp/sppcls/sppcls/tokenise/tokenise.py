import csv
from os.path import join, splitext, basename
import spacy


def tokenise(input_text: str):
    nlp = spacy.load("de_core_news_lg")
    doc = nlp(input_text)
    result = []
    for sent_idx, sent in enumerate(doc.sents):
        for token in sent:
            result.append((token.i, sent_idx, token.text.replace("\n", " "), token.idx, token.idx + len(token.text)))
    return result


def main(in_file_path, output_folder_path):
    with open(in_file_path, "rt", encoding="utf-8") as in_file:
        input_filename = splitext(basename(in_file_path))[0]
        input_text = in_file.read()
        tokens = tokenise(input_text)

    with open(join(output_folder_path, f"{input_filename}_tokenized.tsv"), "wt", encoding="utf-8") as out_file:
        writer = csv.writer(out_file, delimiter="\t", lineterminator="\n")
        writer.writerow(["id", "sent_id", "token", "start", "end"])
        for token in tokens:
            writer.writerow(token)


if __name__ == '__main__':
    pass
