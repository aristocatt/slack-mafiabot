from threading import Timer
import time
from gameaction import handle_action
from slackclient import SlackClient
AT_BOT = "<@U3RC29X0A>"
def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']
    return None, None, None

def check(lobby):
    town = 0
    mafia = 0
    for x in lobby:
        if lobby[x].alliance == 'town':
            town += 1
        elif lobby[x].alliance == 'mafia':
            mafia += 1

    if mafia >= town:
        print("Mafia wins")
    elif mafia == 0:
        print("Town wins")
    return False


def gameloop(state, Lobby, slack_client):
    while state == 3:
        #if check(Lobby.get_lobby()) == False:
            #return
        day_time = time.time() + 10
        while time.time() < day_time:
            command, channel, user_id = parse_slack_output(slack_client.rtm_read())
            if command and channel and user_id:
                id_hash = Lobby.get_hash()
                user_name = None
                try:
                    user_name = id_hash[user_id]
                    print(user_name)
                except:
                    print("something happened")

                handle_action(command, channel, Lobby, user_name)

