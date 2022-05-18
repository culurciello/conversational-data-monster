# conversational data monster
# web app with gradio

# import time
# import os
# import json
import csv

import gradio as gr

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# command parser:
from command_parser import parse_command


dataset_file = 'datasets/population_by_country_2020.csv'
with open(dataset_file, 'r') as infile:
  reader = csv.reader(infile)
  dataset = list(reader)


def plot(a, b, limit=10, figsize=(8, 6), dpi=120, command=""):
    # find match in a:
    ai = [i for i, s in enumerate(dataset[0]) if a.lower() in s.lower()]
    # find match in b:
    bi = [i for i, s in enumerate(dataset[0]) if b.lower() in s.lower()]
    data = np.array(dataset)
    plt.plot(data[1:limit, ai[0]], data[1:limit, bi[0]])
    plt.title(command)
    return plt.gcf()


def dialogue(command, history):
    history = history or []
    # get user command
    print('User input:', command)
    if command:
        # text processing
        response = parse_command(command)

        try:
            r = response['action']
            
            if r == 'load':
                demo.data = dataset[0:3]
                reply = "Ok"
            
            elif r == 'plot':
                if response['objects'][0] and response['objects'][1]:
                    demo.plot = plot(response['objects'][0], response['objects'][1], command=command)
                    reply = "Ok"
            
            elif r == 'clear':
                if response['objects']:
                    if response['objects'][0]:
                        if response['objects'][0] == 'data':
                            demo.data = None
                        elif response['objects'][0] == 'plot':
                            demo.plot = None
                else:
                    demo.data = None
                    demo.plot = None

                reply = "Ok"
            
            else:
                None
                reply = "Not sure here..."
        except:
            print("Not a valid command!")

    history.append((command, reply))
    return history, history, demo.data, demo.plot

chatbot = gr.Chatbot(color_map=("green", "gray"))

demo = gr.Interface(
        title="Conversational Data Monster",
        description="Load data and plot it with natural language commands",
        fn=dialogue, 
        inputs=["text", "state"],
        outputs=[chatbot, "state", "dataframe", "plot"],
        article="Try by typing: 'load data', 'plot country versus population', etc.",
    )


if __name__ == '__main__':
    # demo data:
    demo.data = None
    demo.plot = None
    # demo.history = [] # dialogue history
    
    demo.launch()
