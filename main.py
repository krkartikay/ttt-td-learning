import time
from collections import defaultdict

from ttt import State, value_to_symbol
from random_agent import RandomAgent
from td_agent import TDAgent
from metrics import tick, increment_metric, export_metrics


def main():
    outcome_counts = defaultdict(int)
    r_agent = RandomAgent(1)
    t_agent = TDAgent(-1)
    for i in range(10000):
        if i == 5000:
            t_agent.exploration_probability = 0
        print("Play #%02d" % i)
        outcome = play_agents(r_agent, t_agent)
        outcome_counts[outcome] += 1
        increment_metric("episodes")
        increment_metric("outcome_", str(outcome).replace("<", "_").replace(">", "_"))
    print("\nFinal outcomes:\n")
    print(outcome_counts)
    export_metrics()


def play_agents(agent_1, agent_2):
    s = State()
    agents = {1: agent_1, -1: agent_2, 0: None}
    agent_1.previous_state = None
    agent_2.previous_state = None

    s.print()

    while not s.terminated():

        agent = agents[s.turn()]
        print("Agent", agent, "selecting move")
        move = agent.select_move(s)
        print("Move selected by", agent, move)
        s = s.fill(move)
        s.print()

        if s.turn() == 1:
            print("updating reward for ", agent_2)
            agent_2.update_reward(s, 0)  # reward always 0

        tick()

    if s.turn() == -1:
        print("updating reward for ", agent_2)
        agent_2.update_reward(s, 0)  # reward always 0

    s.print()
    print("Winner: ", value_to_symbol[s.winner()])

    return agents[s.winner()]


if __name__ == "__main__":
    main()
