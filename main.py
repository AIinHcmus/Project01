import heapq

import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man AI - Blue Ghost BFS")

# Maze Layout (1 = Wall, 0 = Path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Fixed Pac-Man Position
PACMAN_POS = (1, 1)


# BFS Algorithm
def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            print(path)
            return path
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (x + dx, y + dy)
            if 0 <= next_pos[0] < COLS and 0 <= next_pos[1] < ROWS and next_pos not in visited and maze[next_pos[1]][next_pos[0]] == 0:
                queue.append((next_pos, path + [next_pos]))
    return []

# DFS Algorithm
def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (x, y), path = stack.pop()
        if (x, y) == goal:
            print(f"Goal reached: {x}, {y}")
            return path
        visited.add((x, y))
        # Try moving in all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (x + dx, y + dy)
            # Check if the next position is within bounds and not a wall
            if (0 <= next_pos[0] < COLS and 0 <= next_pos[1] < ROWS and
                    next_pos not in visited and maze[next_pos[1]][next_pos[0]] == 0):
                stack.append((next_pos, path + [next_pos]))
    return []  # Return an empty list if no path is found


# UCS Algorithm for Orange Ghost
def ucs(start, goal):
    priority_queue = [(0, start, [start])]
    visited = set()

    while priority_queue:
        cost, (x, y), path = heapq.heappop(priority_queue)

        if (x, y) == goal:
            return path  # Return the optimal path

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (x + dx, y + dy)

            if 0 <= next_pos[0] < COLS and 0 <= next_pos[1] < ROWS and maze[next_pos[1]][next_pos[0]] == 0:
                if next_pos not in visited:
                    heapq.heappush(priority_queue, (cost + 1, next_pos, path + [next_pos]))

    return []  # No valid path found


# A* Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    priority_queue = [(0, start, [start])]
    visited = set()

    while priority_queue:
        cost, (x, y), path = heapq.heappop(priority_queue)

        if (x, y) == goal:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (x + dx, y + dy)
            if 0 <= next_pos[0] < COLS and 0 <= next_pos[1] < ROWS and next_pos not in visited and maze[next_pos[1]][
                next_pos[0]] == 0:
                new_cost = cost + 1
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(priority_queue, (priority, next_pos, path + [next_pos]))
    return []

# BlueGhost Class
class BlueGhost:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color

    def move(self):
        if (self.x, self.y) == PACMAN_POS:
            return
        path = bfs((self.x, self.y), PACMAN_POS)
        if len(path) > 1:
            self.x, self.y = path[1]

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# PinkGhost Class
class PinkGhost:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.path = []  # Store the current DFS path
        self.target_pos = PACMAN_POS  # Track Pac-Man's position

    def move(self):
        if (self.x, self.y) == self.target_pos:
            return

        # Recompute path only if Pac-Man moved or no path exists
        if not self.path or self.target_pos != PACMAN_POS:
            self.target_pos = PACMAN_POS
            self.path = dfs((self.x, self.y), self.target_pos)

        # Move to the next step in the path if available
        if len(self.path) > 1:
            self.x, self.y = self.path[1]
            self.path.pop(0)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# OrangeGhost Class
class OrangeGhost:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color

    def move(self):
        if (self.x, self.y) == PACMAN_POS:
            return
        path = ucs((self.x, self.y), PACMAN_POS)
        if len(path) > 1:
            self.x, self.y = path[1]

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# RedGhost Class
class RedGhost:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color

    def move(self):
        if (self.x, self.y) == PACMAN_POS:
            return
        path = a_star((self.x, self.y), PACMAN_POS)
        if len(path) > 1:
            self.x, self.y = path[1]

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Initialize Ghosts
blue_ghost = BlueGhost(8, 1, BLUE)
pink_ghost = PinkGhost(8, 2, PINK)
orange_ghost = OrangeGhost(8, 3, ORANGE)
red_ghost = RedGhost(8, 4, RED)

# Main Loop
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    blue_ghost.move()
    pink_ghost.move()
    orange_ghost.move()
    red_ghost.move()

    # Draw Maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW,
                       (PACMAN_POS[0] * GRID_SIZE + GRID_SIZE // 2, PACMAN_POS[1] * GRID_SIZE + GRID_SIZE // 2),
                       GRID_SIZE // 2 - 2)

    # Draw Ghosts
    blue_ghost.draw()
    pink_ghost.draw()
    orange_ghost.draw()
    red_ghost.draw()

    pygame.display.update()
    pygame.time.delay(300)

pygame.quit()
