# command parser

# command format:
# <action> <object1> <atribute1> <object2> <atribute2> ...

# examples commands:
# load data
# plot country vs population 
# ...

# TEST with: # $ python3 command_parser.py 'plot country vs population'

import sys

# command actions:
ACTIONS = [
    'plot',
]

# object and command attributes:
ATTRIBUTES = [
    ['vs', 'versus'], # plot
]

# ignore words:
IGNORE = ['a', 'the', 'of', 'to', 'from']

COMMANDS_FIXED = {
    'load data'  :{"action":"load", "objects":["data"], "attributes":[], "msg":"loaded data!"}, # load test dataset
    'clear'      :{"action":"clear", "objects":[],}, # clear all app data
    'clear plot' :{"action":"clear", "objects":["plot"],}, # clear all app data
    'clear data' :{"action":"clear", "objects":["data"],}, # clear all app data
}

def parse_command(command):
    parsed_command = {"action":[], "objects":[], "attributes":[], "msg":""}
    
    # split complex command:
    split = command.split()

    # first evaluate simple fixed commands:
    if command in COMMANDS_FIXED.keys():
        return COMMANDS_FIXED[command]

    # evaluate some cases of complex commands:
    else:
        if len(split)>=3 and split[0] == 'plot':
            obj1 = split[1]
            # split[2] is 'vs' or 'versus'
            obj2 = split[3]
            # return 'plot ' + str(obj1) +' vs '+ str(obj2)
            parsed_command['action'] = split[0]
            parsed_command['objects'].append(obj1)
            parsed_command['objects'].append(obj2)
            parsed_command['msg'] = "plotted data!"

            return parsed_command


if __name__ == '__main__':

    command = sys.argv[1] # TEST

    parsed_command = parse_command(command)
    print(parsed_command)
