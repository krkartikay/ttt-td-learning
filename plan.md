# Plan

1. Firstly, we need a way to store and manipulate the game state.
    - Dataclass in python
2. We will need to implement the library for agent
    - Random Agent
    - TD Learning Agent
3. To do self play


## Questions

1. How do we store game state?
    - Dataclass?
    - Protocol buffers?
    - Numpy?
    - We can get started with something simple and port to numpy later for speed.
    - Or, we can get started with numpy directly! <- DECIDED

2. What should be the API for this be?

```py
s: State
    s.__init__() -> State (starting State)
    s.__init__(r: State) -> State (Copies r)
    s.print()
    s.turn() -> -1 or 1 (== 'O' or 'X')
    s.fill(x: int)
    s.__hash__() -> int   (!)
    s.__eq__(r: State) -> bool
    s.possible_moves() -> List[int]
    s.terminated() -> bool
    s.winner() -> -1 or 0 or 1 (== 'O' or 'X')
```

## Agent

API:

```py
a: Agent
    a.__init__() -> Agent (fresh agent)
    a.select_move(s: State) -> int (Move)
    a.update_reward(s: State, r: State, reward: float) -> void (s = initial state, r = final state)
```

TD Learning:

V(State) += alpha * [V(next state) - V(state)]


## UI Loop

1. Show (print) game state
2. Ask user to fill one of the squares
3. Want the agent to select a move
4. Fill the square
5. Check if game terminated
6. Loop back until terminated

