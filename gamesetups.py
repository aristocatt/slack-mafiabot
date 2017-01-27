import math
import random
from roles import *
from game import GameHandler

'''dict of setups.  Right now the functionality is limited.
I need to change the size key to a "minsize" and "maxsize" key.
And I should have one setup with huge variation in the min and max size keys, that
basically just sets up a mountainous game and assigns Mafia Roles based on the number
of players'''
setups = [{
    'name': 'test',
    'minsize': 1,
    'maxsize': 1,
    'resolve': ['!kill'],
    'roles': [
        Mafia()
    ]
},
    {
        'name':'test2',
        'minsize': 1,
        'maxsize': 1,
        'resolve': ['!kill'],
        'roles': [
            Vanilla()
        ]
    },
    {
        'name':'test3',
        'minsize': 3,
        'maxsize' : 6,
        'resolve': ['!kill'],
        'roles':[
            Mafia(),
            Mafia()
        ]
    },

    {
        'name': 'test4',
        'minsize': 7,
        'maxsize':11,
        'resolve': ['!kill'],
        'roles': [
            Mafia(),
            Mafia()
        ]
    }]

#randomply select a suitable setup and return it
def select_setup(size):
    possible_setups = []
    for x in setups:
        if size >= x['minsize'] or size <= x['maxsize']:
            possible_setups.append(x)
    setup = random.choice(possible_setups)
    return setup

#randomly assign roles to payers
def prepare_game(setup, Lobby):
    players = Lobby.get_lobby()
    print(players)
    shuffle = list(players.keys())
    random.shuffle(shuffle)
    for x in setup['roles']:
        players[shuffle[0]] = x
        shuffle.pop(0)
    Lobby.update_players(players)
    print(Lobby.get_lobby())

#create the game state
def begin_game(Lobby):
    players = Lobby.get_lobby()
    setup = select_setup(len(players))
    prepare_game(setup, Lobby)

    Game = GameHandler(setup['resolve'])
    return Game








