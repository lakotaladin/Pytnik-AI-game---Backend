import random

from .agents import Agent

class BotAgent(Agent):
  agent_names = {'1': 'aki', '2': 'jocke', '3': 'uki', '4': 'micko'}
  ID = 0
def __init__(self, position):
        super(BotAgent, self).__init__(position)
        BotAgent.ID += 1
        self.id = BotAgent.ID
        
class Aki(BotAgent):
    def __init__(self, position):
        super().__init__(position)

    @staticmethod
    def kind():
        return '1'

    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)
        states_list = [state.apply_action(self.id, act) for act in actions]
        coll = list(zip(actions, states_list))
        if len(coll):
            coll = sorted(coll, key=lambda st: sum(tuple(map(lambda i, j: abs(i - j),
                          st[1].agents[0].position(), st[1].agents[self.id].position()))))
            return coll[0][0]
        return None