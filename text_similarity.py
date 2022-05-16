# text similarity
# inspired by: https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python

print('Loading SentenceTransformer...')

import sys
import numpy as np
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('stsb-roberta-large')

print('Done!')

commands_all = [
    "plot the country versus the population",
    "plot countries versus population",
    "plot country vs population",
    "load data",
    "clear all data",
    "load a dataset",
    "load dataset",
]


def match_text(text_commands, input_command):
    print('Embedding all possible commands...')
    embeddings = model.encode(commands_all, convert_to_tensor=True)
    print('Embedding input commands')
    embedinput = model.encode(input_command, convert_to_tensor=True)
    print('Done!')

    similarity = []
    for i, line in enumerate(commands_all):
        # print(line, input_command)
        s = util.pytorch_cos_sim(embeddings[i], embedinput).item()
        similarity.append(s)

    similarity = np.sort(similarity)[::-1]
    sorted_idx = np.argsort(similarity)[::-1]
  
    return similarity, sorted_idx


if __name__ == '__main__':

    if len(sys.argv)>1:
        input_command = sys.argv[1] # TEST
    else:
        input_command = "plot country versus population"


    print('You are comparing: ', input_command, ' to all possible commands!')

    similarity, sorted_idx = match_text(commands_all, input_command)

    for i,value in enumerate(similarity):
        print(commands_all[sorted_idx[i]], ' -- ', similarity[i])
