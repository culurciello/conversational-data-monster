# text similarity
# inspired by: https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python

import sys
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('stsb-roberta-large')

text_options = [
    "plot the country versus the population",
    "plot countries versus population",
    "plot country vs population",
    "load data",
    "clear all data",
    "load a dataset",
    "load dataset",
]


def match_text(text_options, text_to_compare):
    embeddings = model.encode(text_options, convert_to_tensor=True)
    embedinput = model.encode(text_to_compare, convert_to_tensor=True)

    similarity = []
    for i, line in enumerate(text_options):
        # print(line, text_to_compare)
        s = util.pytorch_cos_sim(embeddings[i], embedinput).item()
        similarity.append(s)
  
    print(similarity) 



if __name__ == '__main__':

    if len(sys.argv)>1:
        text_to_compare = sys.argv[1] # TEST
    else:
        text_to_compare = "plot country versus population"

    match_text(text_options, text_to_compare)
