# conversational-data-monster

converse with your data

![demo_video](static/demo/conversational_data_monster.gif)

<!--## Installation

Requirements:
```
npm install
```-->


## Running

```
$ export FLASK_APP=app
$ flask run
```
or
```
python3 app.py
```

## Instructions

Example list of current commands:

- "load data"
- "plot country vs population"
- clear


Also see docs folder for info.


## better command parsing

There are multiple ways to write a command. For better command parsing and recognition (rather than fixed typing rules) one can use sentence transformers.

Using RoBERTa sentence embedding can be tested here:

`python3 text_similarity.py `