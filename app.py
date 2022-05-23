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
import numpy as np

# command parser:
from command_parser import parse_command


app = Flask(__name__)
app.debug = True

dataset_file = 'datasets/population_by_country_2020.csv'
with open(dataset_file, 'r') as infile:
  reader = csv.reader(infile)
  dataset = list(reader)


def plot(a, b, limit=10, figsize=(8, 6), dpi=120, fontsize=12):
    # plot a versus b - finding a,b in dataset
    # find match in a:
    ai = [i for i, s in enumerate(dataset[0]) if a.lower() in s.lower()]
    # find match in b:
    bi = [i for i, s in enumerate(dataset[0]) if b.lower() in s.lower()]
    data = np.array(dataset)
    
    # create figure
    fig = Figure(figsize=figsize, dpi=dpi)
    ax = fig.subplots()
    ax.set_title(a+" vs "+b, fontsize=fontsize)
    ax.set_xlabel(a, fontsize=fontsize)
    ax.set_ylabel(b, fontsize=fontsize)
    ax.plot(data[1:limit, ai[0]], data[1:limit, bi[0]].astype(float))

    # save plot to file
    # fig.savefig("test_figs.png", format="png") # uncomment this to save png file

    # save plot to buffer / no file
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return data


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
                plot=None, 
                dialogue_usr=None)
        if command:
            # text processing
            response = parse_command(command)

            try:
                r = response['action']
                
                if r == 'load':
                    app.data = dataset
                
                elif r == 'plot':
                    if response['objects'][0] and response['objects'][1]:
                        app.plot = plot(response['objects'][0], response['objects'][1])
                
                elif r == 'clear':
                    if response['objects']:
                        if response['objects'][0]:
                            if response['objects'][0] == 'data':
                                app.data = None
                            elif response['objects'][0] == 'plot':
                                app.plot = None
                    else:
                        app.data = None
                        app.plot = None
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
        plot=app.plot, 
        dialogue_usr=app.dialogue_usr)


if __name__ == '__main__':
    app.data = None
    app.plot = None
    app.dialogue_usr = []
    
    app.run()
