import copy
class GameState:
    initial_state = None

    def __init__(self, map, agents, last_agents_playerid):
        self.map = map
        self.agents = agents
        self.last_agent_playerid = last_agents_playerid
        self.win = False
        self.lose = False
        self.path1 = []


    def adjust_win_lose (self):
        actions_length = [self.get_legal_actions(agent_id) for agent_id in range(len(self.agents))]
        if not any(actions_length[1:]) and actions_length[0]:
            self.win = True
        elif not actions_length[0] and any(actions_length[1:]):
            self.lose = True
        elif not any(actions_length):
            self.lose = True if self.last_agent_played_id is not None and self.last_agent_played_id != 0 else False
            self.win = True if self.last_agent_played_id is not None and self.last_agent_played_id == 0 else False

    def copy(self):
        map_copy = copy.deepcopy(self.map)
        agents_copy = [a.copy() for a in self.agents]
        last_agent_played_id_copy = self.last_agent_played_id
        return GameState(map_copy, agents_copy, last_agent_played_id_copy)

    def is_win(self):
        return self.win

    def is_lose(self):
        return self.lose

    def is_position_legal(self, position, agent):
        row, col = position
        return 0 <= row < len(self.map) and \
        0 <= col < len(self.map[0]) \
        and self.map[row][col] in agent.legal_fields() or position == agent.position()

    def get_legal_actions(self, agent_id):
        agent = self.agents[agent_id]
        if not agent.is_active():
            return []
        agent_pos = agent.position()
        actions = []
        for act_name, act_dir in Action.actions.items():
            new_agent_pos = tuple(map(sum, zip(agent_pos, act_dir)))
            if self.is_position_legal(new_agent_pos, agent):
                actions.append(act_name)
        return actions

    
    def apply_action(self, agent_id, action):
        state = self.copy()
        agent = state.agents[agent_id]
        old_agent_pos = agent.position()
        new_agent_pos = tuple(map(sum, zip(old_agent_pos, Action.actions[action])))
        if not self.is_position_legal(new_agent_pos, agent):
            raise Exception(f'ERR: {action} is not legal! '
                            f'Agent position: {old_agent_pos}')
        state.map[old_agent_pos[0]][old_agent_pos[1]] = 'h'
        state.map[new_agent_pos[0]][new_agent_pos[1]] = agent.kind()
        agent.apply_action(action)
        state.last_agent_played_id = agent_id
        return state

        pass