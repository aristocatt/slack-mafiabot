import roles
import time
import gamesetups

"""Handles the Players that are queued to play the game, or that are still alive in the game"""


class GameLobby:

    def __init__(self):
        self.game_lobby = {}
        self.id_user_hash = {}
        self.game_state = 0

    def set_game_state(self, state):
        self.game_state = state

    def get_game_state(self):
        return self.game_state

    def add_player(self,user_name,user_id):
        if user_name in self.game_lobby:
            return user_name + " you have already joined the game!"

        else:
            self.game_lobby[user_name] = roles.Vanilla()
            self.id_user_hash[user_id] = user_name
            return user_name + " has joined the game!"

    def clear_lobby(self):
        self.game_lobby = {}
        print('lobby_cleared')

    def get_lobby(self):
        return self.game_lobby

    def get_hash(self):
        return self.id_user_hash

    def remove_player(self, user_name):
        del self.game_lobby[user_name]

    def update_players(self, players):
        self.game_lobby = players





