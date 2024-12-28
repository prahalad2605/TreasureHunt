import random
import heapq
import pygame
import time

class Node:
    _counter = 0

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
        self.order = Node._counter
        Node._counter += 1

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return (self.f, self.order) < (other.f, other.order)
    
def draw_grid(screen, grid, agent_pos, enemy_pos, goal_pos, cell_size, agent_img, enemy_img, goal_img):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if (y, x) == agent_pos:
                screen.blit(agent_img, rect)
            elif (y, x) == enemy_pos:
                screen.blit(enemy_img, rect)
            elif (y, x) == goal_pos:
                screen.blit(goal_img, rect)
            elif grid[y][x] == 1:
                pygame.draw.rect(screen, (128, 128, 128), rect)  # Draw walls in gray
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Draw grid lines
    
def a_star(grid, start, end):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize open and closed list
    open_list = []
    closed_list = []

    heapq.heappush(open_list, (start_node.f, start_node))

    # Loop until the end
    while len(open_list) > 0:
        _, current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child == open_node[1] and child.g > open_node[1].g]) > 0:
                continue

            heapq.heappush(open_list, (child.f, child))

    return None

def generate_grid(width, height, wall_chance):
    return [[1 if random.random() < wall_chance else 0 for _ in range(width)] for _ in range(height)]

def get_random_position(grid, exclude_positions):
    while True:
        position = (random.randint(0, len(grid)-1), random.randint(0, len(grid[0])-1))
        if grid[position[0]][position[1]] == 0 and position not in exclude_positions:
            return position

def print_grid(grid, agent_pos, enemy_pos, goal_pos):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if (r, c) == agent_pos:
                print("A", end="")
            elif (r, c) == enemy_pos:
                print("E", end="")
            elif (r, c) == goal_pos:
                print("G", end="")
            elif grid[r][c] == 0:
                print(".", end="")
            else:
                print("#", end="")
        print()

def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
def display_message(screen, message, width, height):
    font = pygame.font.SysFont(None, 55)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(2)


def main():
    pygame.init()
    width, height = 10, 10
    cell_size = 40
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("A* Pathfinding Game")

    # Load images
    agent_img = pygame.image.load('agent.png')
    enemy_img = pygame.image.load('enemy.png')
    goal_img = pygame.image.load('diamond.png')

    # Resize images
    agent_img = pygame.transform.scale(agent_img, (cell_size, cell_size))
    enemy_img = pygame.transform.scale(enemy_img, (cell_size, cell_size))
    goal_img = pygame.transform.scale(goal_img, (cell_size, cell_size))

    wall_chance = 0.2
    grid = generate_grid(width, height, wall_chance)
    agent_pos = get_random_position(grid, [])
    enemy_pos = get_random_position(grid, [agent_pos])
    goal_pos = get_random_position(grid, [agent_pos, enemy_pos])

    while distance(agent_pos, enemy_pos) < 5 or distance(agent_pos, goal_pos) < 5:
        agent_pos = get_random_position(grid, [])
        enemy_pos = get_random_position(grid, [agent_pos])
        goal_pos = get_random_position(grid, [agent_pos, enemy_pos])

    clock = pygame.time.Clock()
    running = True
    agent_moved = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = agent_pos
                if event.key == pygame.K_w and agent_pos[0] > 0 and grid[agent_pos[0] - 1][agent_pos[1]] == 0:
                    new_pos = (agent_pos[0] - 1, agent_pos[1])
                elif event.key == pygame.K_a and agent_pos[1] > 0 and grid[agent_pos[0]][agent_pos[1] - 1] == 0:
                    new_pos = (agent_pos[0], agent_pos[1] - 1)
                elif event.key == pygame.K_s and agent_pos[0] < height - 1 and grid[agent_pos[0] + 1][agent_pos[1]] == 0:
                    new_pos = (agent_pos[0] + 1, agent_pos[1])
                elif event.key == pygame.K_d and agent_pos[1] < width - 1 and grid[agent_pos[0]][agent_pos[1] + 1] == 0:
                    new_pos = (agent_pos[0], agent_pos[1] + 1)

                if grid[new_pos[0]][new_pos[1]] == 0:
                    agent_pos = new_pos
                    agent_moved = True

        if agent_moved:
            path = a_star(grid, enemy_pos, agent_pos)
            if path and len(path) > 1:
                enemy_pos = path[1]

        if agent_pos == goal_pos:
            display_message(screen, "You Won!", width * cell_size, height * cell_size)
            running = False

        if enemy_pos == agent_pos:
            display_message(screen, "Enemy has captured!", width * cell_size, height * cell_size)
            running = False

        screen.fill((0, 0, 0))
        draw_grid(screen, grid, agent_pos, enemy_pos, goal_pos, cell_size, agent_img, enemy_img, goal_img)
        pygame.display.flip()

        agent_moved = False
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
