import pygame
import sys
from collections import deque

BLACK = (0, 0, 0)
CUSTOM_BLUE = (17, 89, 125)
CUSTOM_GREEN = (3, 252, 169)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SIZE = (900, 600)
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
GRID_POS_START = (200, 200)
GRID_POS_TARGET = (700, 400)
CUSTOM_ORANGE = (252, 152, 3)

pygame.init()
pygame.display.set_caption("Dijkstra's Path Finding")
WIN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
unvisited_queue = deque()
path = []


class Spot:
    def __init__(self, pos):
        self.x, self.y = pos
        self.is_wall = False
        self.id = pos
        self.adjacent = []
        self.distance = sys.maxsize
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor):
        self.adjacent.append(neighbor)

    def get_id(self):
        return self.id

    def draw(self, color, filled=1, shaped=False):
        if self.is_wall:
            color = BLACK
            filled = 0
        if shaped:
            pygame.draw.circle(
                WIN,
                color,
                (
                    BLOCK_SIZE * (self.x // BLOCK_SIZE) + BLOCK_SIZE // 2,
                    BLOCK_SIZE * (self.y // BLOCK_SIZE) + BLOCK_SIZE // 2,
                ),
                8,
            )
        else:
            rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, color, rect, filled)


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        self.vert_dict[node.get_id()] = node
        return node

    def get_vertex(self, node_pos):
        if node_pos in self.vert_dict:
            return self.vert_dict[node_pos]
        else:
            return None

    def add_neighbors(self, v):
        x, y = v.get_id()
        pos = x, y
        if x < SIZE[0] - BLOCK_SIZE:
            v.add_neighbor(graph.get_vertex((x + BLOCK_SIZE, y)))
        if x > 0:
            v.add_neighbor(graph.get_vertex((x - BLOCK_SIZE, y)))
        if y < SIZE[1] - BLOCK_SIZE:
            v.add_neighbor(graph.get_vertex((x, y + BLOCK_SIZE)))
        if y > 0:
            v.add_neighbor(graph.get_vertex((x, y - BLOCK_SIZE)))


def set_wall_nodes(pos, state):
    adj_pos = (
        BLOCK_SIZE * (pos[0] // BLOCK_SIZE),
        BLOCK_SIZE * (pos[1] // BLOCK_SIZE),
    )
    graph.get_vertex(adj_pos).is_wall = state


graph = Graph()

for x in range(0, SIZE[0], BLOCK_SIZE):
    for y in range(0, SIZE[1], BLOCK_SIZE):
        spot = Spot((x, y))
        graph.add_vertex(spot)

for v in graph:
    graph.add_neighbors(v)

start = graph.get_vertex(GRID_POS_START)
unvisited_queue.append(start)
start.visited = True


def main():
    start_dijkstra = False
    done_dijkstra = False
    no_solution = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    set_wall_nodes(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    set_wall_nodes(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    set_wall_nodes(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_dijkstra = True

        if start_dijkstra:
            if len(unvisited_queue) > 0:
                current = unvisited_queue.popleft()
                if current.get_id() == GRID_POS_TARGET:
                    temp = current
                    while temp.previous:
                        path.append(temp.previous)
                        temp = temp.previous
                    if not done_dijkstra:
                        done_dijkstra = True
                    elif done_dijkstra:
                        continue
                if done_dijkstra == False:
                    for neighbor in current.adjacent:
                        if not neighbor.visited and not neighbor.is_wall:
                            neighbor.visited = True
                            neighbor.previous = current
                            unvisited_queue.append(neighbor)
            else:
                if no_solution and not done_dijkstra:
                    print("No Solution")
                    no_solution = False
                else:
                    continue

        WIN.fill(CUSTOM_BLUE)
        for x in range(0, SIZE[0], BLOCK_SIZE):
            for y in range(0, SIZE[1], BLOCK_SIZE):
                spot = graph.get_vertex((x, y))
                if spot in path:
                    spot.draw(RED, filled=0)
                elif spot.visited:
                    spot.draw(CUSTOM_ORANGE, filled=0)
                if spot in unvisited_queue:
                    spot.draw(CUSTOM_BLUE, filled=0)
                    spot.draw(CUSTOM_ORANGE, filled=0, shaped=True)
                if (x, y) == GRID_POS_START:
                    spot.draw(YELLOW, filled=0)
                if (x, y) == GRID_POS_TARGET:
                    spot.draw(CUSTOM_GREEN, filled=0)
                else:
                    spot.draw(BLACK)

        pygame.display.flip()


main()
