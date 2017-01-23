"""Handles in actions that affect the game"""

def handle_action(command, channel, Lobby, Game, user_name):
    players = Lobby.get_lobby().keys()
    user = Lobby.get_lobby()[user_name]
    period = Game.period
    action = user.get_actions(period = period)
    command = command.split(' ', 1)
    try:
        action[command[0]]
        if period: #if it's day
            response, channel = action[command[0]](user_name,command, Game, players)
            return response, channel
        elif not period: #if it's night
            Game.queue_action(user, command, players, action[command[0]],)
            return None, None


    except:
        return "Improper Command", user_name





