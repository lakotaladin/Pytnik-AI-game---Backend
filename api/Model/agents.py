import copy

class Agent():
    def __init__(self, position):
        self.row= position[0]
        self.col = position[1]
        self.place_to(position)
        self.last_action=None
        self.id = None
        self.active = True

    def get_id(self):
            return self.id
        
    def is_active(self):
            return self.active
    def set_active(self, active):
        self.active = active

    def copy(self):
        agent_copy = copy.copy(self)
        agent_copy.place_to(self.position())
        return agent_copy

    def move_towards(self, position):
        row = position[0] - self.row
        col = position[1] - self.col
        return (row,col)

    def get_legal_actions(self, state):
        return state.get_legal_actions(self.id)
    
    def get_last_action(self):
        return self.last_action
    
    # def apply_action(self, action):
    #     self.last_action = action
    #     self.place_to(tuple(map(sum, zip(self.position(), Action.actions[action]))))
    #     return (self.row, self.col)

    def place_to(self, position):
        self.row = position[0]
        self.col = position[1]
        pass
    def position(self):
        return self.row, self.col

    @staticmethod
    def legal_fields():
        return 'r'

    def get_next_action(self, state, max_levels):
        pass
