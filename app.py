# conversational data monster
# web app

import time
import os
import json
import csv
import base64
from io import BytesIO
from flask import Flask, jsonify, request, render_template, send_file
from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
import numpy as np

# command parser:
from command_parser import parse_command


app = Flask(__name__)
app.debug = True

dataset_file = 'datasets/population_by_country_2020.csv'
with open(dataset_file, 'r') as infile:
  reader = csv.reader(infile)
  dataset = list(reader)


def plot(a, b, limit=10, figsize=(8, 6), dpi=120):
    # find match in a:
    ai = [i for i, s in enumerate(dataset[0]) if a.lower() in s.lower()]
    # find match in b:
    bi = [i for i, s in enumerate(dataset[0]) if b.lower() in s.lower()]
    data = np.array(dataset)
    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=figsize, dpi=dpi)
    ax = fig.subplots()
    # ax.plot(dataset[0], dataset[1])
    ax.plot(data[1:limit, ai[0]], data[1:limit, bi[0]])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    return data


# def plottest(a, b):
#     # find match in a:
#     ai = [i for i, s in enumerate(dataset[0]) if a.lower() in s.lower()]
#     # find match in b:
#     bi = [i for i, s in enumerate(dataset[0]) if b.lower() in s.lower()]
#     data = np.array(dataset)
#     plt.plot(data[1:10, ai[0]], data[1:10, bi[0]])
#     plt.show()

# print(dataset[0:3])
# plottest('country', 'population')


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []

    if request.method == "POST":
        # get user command
        try:
            command = request.form['textInput']
            app.dialogue_usr.append(command)
            print('User input:', command)
        except:
            errors.append(
                "Not a valid command!"
            )
            return render_template('index.html', 
                errors=errors, 
                data=None, 
                data_image=None, 
                dialogue_usr=None)
        if command:
            # text processing
            response = parse_command(command)
            print(response)

            try:
                r = response['action']
                if r == 'load':
                    app.data = dataset
                elif r == 'plot':
                    if response['objects'][0] and response['objects'][1]:
                        app.data_image = plot(response['objects'][0], response['objects'][1])
                elif r == 'clear':
                    app.data = None
                    app.data_image = None
                    app.dialogue_usr = []
                else:
                    None
            except:
                errors.append(
                "Not a valid command!"
            )


    return render_template('index.html', 
        errors=errors, 
        data=app.data, 
        data_image=app.data_image, 
        dialogue_usr=app.dialogue_usr)


if __name__ == '__main__':
    app.data = None
    app.data_image = None
    app.dialogue_usr = []
    
    app.run()
