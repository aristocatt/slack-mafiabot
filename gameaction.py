"""Handles in actions that affect the game"""

def handle_action(command, channel, Lobby, Game, user_name):
    players = Lobby.get_lobby().keys()
    print(players)
    user = Lobby.get_lobby()[user_name]
    period = Game.period
    action = user.get_actions(period = period)
    print(action)
    command = command.split(' ', 1)
    print(action[command[0]])
    if action[command[0]]:
        if period: #if it's day
            response, channel = action[command[0]](user_name,command, Game, players)
            return response, channel
        elif not period: #if it's night
            Game.queue_action(user, command, players)
            return None, None


    else:
        return "Improper Command", user_name





