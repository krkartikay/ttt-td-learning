from collections import defaultdict

from ttt import State, value_to_symbol
from random_agent import RandomAgent
from td_agent import TDAgent


def main():
    outcome_counts = defaultdict(int)
    r_agent = RandomAgent(1)
    t_agent = TDAgent(-1)
    for i in range(1000):
        print("Play #%02d" % i)
        outcome = play_agents(r_agent, t_agent)
        outcome_counts[outcome] += 1
    print("\nFinal outcomes:\n")
    print(outcome_counts)


def play_agents(agent_1, agent_2):
    s = State()
    agents = {1: agent_1, -1: agent_2, 0: None}

    while not s.terminated():
        s.print()
        agent = agents[s.turn()]
        move, move_type = agent.select_move(s)
        print("Random move selected by agent:", move, move_type)
        s_old = State(s)
        s.fill(move)
        agent.update_reward(s_old, s, 0, move_type)  # reward always 0

    s.print()
    print("Winner: ", value_to_symbol[s.winner()])

    return agents[s.winner()]


if __name__ == "__main__":
    main()
