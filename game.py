import time
from collections import defaultdict
import operator
import random


"""Game class.  Basically handles day/night cycles, grabs the resolve order for night actions,
handles vote tallying, and how night actions should resolve.
My thoughts are, any actions can resolve in only a few basic ways.  Either the
user committing the action is blocked from using it(this could be actions specific, or a
complete block of all avaialable actions) or the target(if there is one is protected
either from that specific action or from all actions.  After it queues the actions
then it should resolve them, one after another"""
class GameHandler:

    def __init__(self, ord_of_op):
        self.period = True
        self.countdown = time.time() + 120
        self.ord_of_op = ord_of_op
        self.vote = {}
        self.resolve = {
            #order:[player, action, command]}
         }


    def set_cycle(self, cycle):
        self.period = cycle
        if cycle == True:
            self.countdown = time.time() + 120  #set day time
        elif cycle == False:
            self.countdown = time.time() + 30  #set night time

    def check_cycle(self):
        if time.time() > self.countdown:
            return 1
        else: return 0

    def reset_votes(self):
        self.vote = {}

    def set_vote(self, user, target):
        self.vote[user] = target

    def tally_vote(self):
        tally = "The votes are: \n"
        votes = defaultdict(list)
        lynch = ["No Vote", 0]
        for x in self.vote:
            votes[self.vote[x]].append(x)
        for x in votes:
            tally += x + " has " + str(len(votes[x])) + " vote[s] by: " + str(votes[x]) + "\n"
            if len(votes[x]) > lynch[len(lynch)-1]:
                lynch = [x, len(votes[x])]
            elif len(votes[x]) == lynch[len(lynch)-1]:
                lynch.append(x)
        tally += "With " + str(lynch[len(lynch)-1]) + "vote[s], the following players are up for lynch: \n"
        lynch.pop(len(lynch)-1)
        for x in lynch:
            tally += x + " "
        tally += '\n'
        return tally, lynch

    def resolve_lynch(self):
        tally, lynch = self.tally_vote()
        tally += "Resolving lynch: \n"
        lynch_final = random.choice(lynch)
        self.reset_votes()
        return tally, lynch_final

    def queue_action(self,user, command, players, action):
        order = self.ord_of_op.index(command[0])
        command_response = user.check_input[command[0]](user, command, players)
        if command_response in players:
            self.resolve[order] = [user, command[0], command_response, action]
            return "Action recieved"
        else:
            return command_response



    def clear_queue(self):
        self.resolve = {}

    def resolve_action(self):
        resolve = sorted(self.resolve.items(), key = lambda y: y[0])
        protected_from = {
            #player: True or (tuple of strings[e.g. !kill])
        }
        prevented_from = {
            #player: True or (tuple of strings)
        }
        for x in resolve:
            user = x[1][0]
            action = user.night_actions  #change to user.get_actions()
            print(action)
            command = x[1][1] #so ugly...needs to be explained
            print(command)
            target = x[1][2]
            print(target)
            kill = action[command](target)
            return kill



