# Turn-based Game: A* Pathfinding

This is a simple turn-based game where the player moves an agent each turn, and the enemy moves toward the agent using the A* pathfinding algorithm. The game ends when the agent reaches the goal or is captured by the enemy.

## State Space

The grid map is represented as a 2D array with the following elements:
- **Agent**: The player-controlled character.
- **Enemy**: The AI-controlled character that moves toward the agent.
- **Walls**: Obstacles that block movement.
- **Open Spaces**: Free areas where movement is allowed.
- **Goal**: The target that the agent needs to reach.

### Example Grid Configuration

Here is a sample of a grid configuration in the game:

![Sample Grid](images/grid_sample.png)

## Test Cases

The following test cases can be used to test the effectiveness and reliability of the A* algorithm:

### Test Case 1: Agent Reaches the Goal

In this test case, the agent successfully reaches the goal without being captured by the enemy.

![Agent Reaches Goal](images/agent_goal_reach.png)

### Test Case 2: Enemy Captures the Agent

In this test case, the enemy captures the agent before it reaches the goal.

![Enemy Captures Agent](images/enemy_capture.png)

## Game Outcome Variability

- **Win**: The player successfully reaches the goal.
- **Loss**: The enemy captures the agent.

### Observations:
- **Randomness** plays a role in the game, as the initial positions of the agent, enemy, and goal are randomized.
- **Player's Strategy**: The player must move strategically to avoid the enemy and reach the goal.
- **Difficulty Level**: The difficulty varies based on the grid configuration and the positions of obstacles and characters.

## A* Pathfinding

The enemy uses the A* pathfinding algorithm to find the shortest path to the agent, adjusting its movement based on the agent's position each turn.

### Conclusion

This game offers a balance between strategy and randomness, providing a dynamic experience where each playthrough may have different outcomes based on the initial conditions and the player's decisions.
