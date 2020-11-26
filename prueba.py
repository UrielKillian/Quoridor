import pygame
import networkx

import matplotlib.pyplot as plt
from collections import deque

# Board Size Defined:
global rows
global columns
rows = 9
columns = 9
show_wall = False
rotacion = True

# Nodos eliminados por los muros
node1_x, node1_y = 0, 0
node2_x, node2_y = 0, 1
node3_x, node3_y = 1, 0
node4_x, node4_y = 1, 1
lista_node1_x = []
lista_node2_x = []
lista_node3_x = []
lista_node4_x = []
lista_node1_y = []
lista_node2_y = []
lista_node3_y = []
lista_node4_y = []
# 9x9 Board Graph creation
# (Rows, Columns) = (Y, X)
Board_Graph = networkx.Graph()
Board_Graph.add_nodes_from((i, j) for i in range(rows) for j in range(columns))
Board_Graph.add_edges_from((((i, j), (i - 1, j))
                            for i in range(rows) for j in range(columns) if i > 0))
Board_Graph.add_edges_from((((i, j), (i, j - 1))
                            for i in range(rows) for j in range(columns) if j > 0))
Board_Graph.add_node((4, 9))
# Testing
Board_Graph.add_edge((0, 8), (4, 9))
Board_Graph.add_edge((1, 8), (4, 9))
Board_Graph.add_edge((2, 8), (4, 9))
Board_Graph.add_edge((3, 8), (4, 9))
Board_Graph.add_edge((4, 8), (4, 9))
Board_Graph.add_edge((5, 8), (4, 9))
Board_Graph.add_edge((6, 8), (4, 9))
Board_Graph.add_edge((7, 8), (4, 9))
Board_Graph.add_edge((8, 8), (4, 9))


# Creating a wall will delete the edge
def RemoveEdge(x0, y0, x1, y1):
    Board_Graph.remove_edge((x0, y0), (x1, y1))
    return 0


# ToDo:
# Algorithm to place walls
# def PlaceWall():
# If degree return more than 1 then a wall can be placed
#	Board_Graph.degree[(0,0)]

def A_STAR(ini, fin):
    time_start = pygame.time.get_ticks()

    def invalid(x, y):
        return (x < 0) or (x >= rows) or (y < 0) or (y >= columns) \
               or (visit[x][y])

    def reconstructionPath():
        path = deque()
        ix = (fin[0], fin[1] - 1)
        while ix is not dad[ini]:
            path.appendleft(ix)
            ix = dad[ix]
        path.append((4, 9))
        return path

    visit = [[False for col in range(columns)] for row in range(rows)]
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dad = {}
    queue = deque()
    dad[ini] = (-1, -1)
    queue.appendleft(ini)
    visit[ini[0]][ini[1]] = True
    while len(queue):
        cur = queue.popleft()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(nx, ny)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                # visit[nx][ny] = True
                dad[(nx, ny)] = cur
    p = reconstructionPath()
    print("El camino elegido por A* es: ", p)
    # print(len(p))
    time_end = pygame.time.get_ticks()
    time = time_end - time_start
    return p[1], time


def BFS(ini, fin):
    time_start = pygame.time.get_ticks()

    def invalid(x, y):
        return (x < 0) or (x >= rows) or (y < 0) or (y >= columns) \
               or (visit[x][y])

    def reconstructionPath():
        path = deque()
        ix = fin
        while ix is not dad[ini]:
            path.appendleft(ix)
            ix = dad[ix]
        return path

    visit = [[False for col in range(columns)] for row in range(rows)]
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dad = {}
    queue = deque()
    dad[ini] = (-1, -1)
    queue.appendleft(ini)
    # visit[ini[0]][ini[1]] = True
    while len(queue):
        cur = queue.popleft()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(nx, ny)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                # visit[nx][ny] = True
                dad[(nx, ny)] = cur

    p = reconstructionPath()
    time_end = pygame.time.get_ticks()
    time = time_end - time_start
    return p, time


def Dijkstra(ini, fin):
    time_start = pygame.time.get_ticks()

    def invalid(x, y):
        return (x < 0) or (x >= rows) or (y < 0) or (y >= columns) \
               or (visit[x][y])

    def reconstructionPath():
        path = deque()
        ix = fin
        while ix is not dad[ini]:
            path.appendleft(ix)
            ix = dad[ix]

        return path

    visit = [[False for col in range(columns)] for row in range(rows)]
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    dad = {}
    queue = deque()
    dad[ini] = (-1, -1)
    queue.appendleft(ini)
    # visit[ini[0]][ini[1]] = True
    while len(queue):
        cur = queue.popleft()
        visit[cur[0]][cur[1]] = True
        for op in range(4):
            nx, ny = cur[0] + dx[op], cur[1] + dy[op]
            if (not invalid(nx, ny)) and (Board_Graph.has_edge(cur, (nx, ny))):
                queue.append((nx, ny))
                # visit[nx][ny] = True
                dad[(nx, ny)] = cur

    p = reconstructionPath()
    time_end = pygame.time.get_ticks()
    time = (time_end - time_start)  # output does not give the real value
    return p, time


# Board visual representation using Pygame
pygame.init()
pygame.display.set_caption("Trabajo Final - Complejidad Algoritmica")

# Font created
pygame.font.init()
font = pygame.font.SysFont("verdana", 16)

# Screen size defined:
global width
global height
width = 600
height = 600
size = (width, height)
color_square = (-2, -2)  # cuadrado rojo jugador falta implementar el 2 jugador
start_pos = (4, 8)
start_pos_2 = (4, 0)
algorithm = 1
algorithm_name = "A STAR"
path_lenght = 0
time = 0
path = None
path2 = None

# Colors defined:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (102, 51, 0)
COLOR_PIEZA = (255, 178, 102)

# Screen created:
screen = pygame.display.set_mode(size)
done = False
Movimiento = False


# Function to draw the board
def DrawBoard():
    SpaceX = int((width - 100) / columns)
    SpaceY = int((height - 100) / rows)
    for i in range(columns + 1):
        x = 50 + SpaceX * i
        pygame.draw.line(screen, BLACK, (x, 80), (x, SpaceX * columns + 80))
    for i in range(rows + 1):
        y = 80 + SpaceY * i
        pygame.draw.line(screen, BLACK, (50, y), (SpaceY * rows + 50, y))


def ConvertMousePos(MousePos):
    SpaceX = int((width - 100) / columns)
    SpaceY = int((height - 100) / rows)
    x = int((MousePos[0] - 50) / SpaceX)
    y = int((MousePos[1] - 80) / SpaceY)
    print("posicion del mouse x: ", x)
    print("posicion del mouse y: ", y)
    return x, y


def FillSquare(color, pos):
    SpaceX = int((width - 100) / columns)  # 100
    SpaceY = int((height - 100) / rows)  # 100

    x0 = 50 + SpaceX * pos[0]
    y0 = 80 + SpaceY * pos[1]

    pygame.draw.rect(screen, color, [x0, y0, SpaceX, SpaceY], 0)


def DrawPath(path):
    if path != None:
        for i in range(len(path)):
            FillSquare(GREEN, path[i])


def DrawWall(node1, node2):
    SpaceX = int((width - 100) / columns)
    SpaceY = int((height - 100) / rows)

    if node1[0] == node2[0]:
        x0 = 50 + SpaceX * node1[0]
        y0 = 80 + SpaceY * node2[1]
        x = 50 + SpaceX * (node2[0] + 1)
        y = y0
    elif node1[1] == node2[1]:
        x0 = 50 + SpaceX * node2[0]
        y0 = 80 + SpaceY * node1[1]
        x = x0
        y = 80 + SpaceY * (node2[1] + 1)

    pygame.draw.line(screen, BLUE, (x0, y0), (x, y), 5)


def RefreshScreen():
    screen.blit(instructions1, (0, 0))
    screen.blit(instructions2, (0, 16))
    screen.blit(instructions3, (0, 32))
    screen.blit(alg_name, (width - 200, 0))
    screen.blit(alg_time, (0, height - 21))
    screen.blit(path_len, (width - 200, height - 21))
    FillSquare(COLOR_PIEZA, start_pos)
    FillSquare(COLOR_PIEZA, start_pos_2)
    FillSquare(RED, color_square)
    DrawBoard()

    if len(lista_node1_x) != 0:
        for i in range(len(lista_node1_x)):
            temp_draw_wall_node1 = (lista_node1_x[i], lista_node1_y[i])
            temp_draw_wall_node2 = (lista_node2_x[i], lista_node2_y[i])
            temp_draw_wall_node3 = (lista_node3_x[i], lista_node3_y[i])
            temp_draw_wall_node4 = (lista_node4_x[i], lista_node4_y[i])
            DrawWall(temp_draw_wall_node1, temp_draw_wall_node2)
            DrawWall(temp_draw_wall_node3, temp_draw_wall_node4)

    pygame.display.flip()


# Game Loop:
while not done:
    for i in range (0, 8):
        if start_pos == (i, 0):
            print("--------------------------------------------------------")
            print("--------------> El jugador ha ganado  <-----------------")
            print("--------------------------------------------------------")
            done = True
    if start_pos_2 == (4, 9):
        print("---------------------------------------------------")
        print("--------------> El bot ha ganado <-----------------")
        print("---------------------------------------------------")
        done = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Clicking a tile will create a path to it from (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = ConvertMousePos(pygame.mouse.get_pos())
                start_pos_2 = pos
                screen.fill(BROWN)
                path2 = ()

            if event.button == 2:
                pos = ConvertMousePos(pygame.mouse.get_pos())
                color_square = pos
                screen.fill(BROWN)
                path2 = ()

            if event.button == 3:
                # pos = ConvertMousePos(pygame.mouse.get_pos())
                pos = (4, 9)  # Final Position
                pos_2 = (8, 0)
                if algorithm == 1:
                    alg_result = A_STAR(start_pos_2, pos)
                elif algorithm == 2:
                    # alg_result = BFS(start_pos_2, pos)
                    best_route_BFS = networkx.bellman_ford_path(Board_Graph, start_pos_2, (4, 9))
                    print("La mejor ruta es: ", best_route_BFS)
                    alg_result = best_route_BFS
                # alg_result = BFS(start_pos_2, pos_2)
                elif algorithm == 3:
                    # alg_result = Dijkstra(start_pos_2, pos)
                    best_route_dijkstra = networkx.dijkstra_path(Board_Graph, start_pos_2, (4, 9))
                    alg_result = best_route_dijkstra
                # alg_result = Dijkstra(start_pos_2, pos_2)

                path2 = deque([alg_result[1]])
                print("El recorrido es el siguiente: ", path2)
                path_lenght = len(path2)
                time = alg_result[1]
                screen.fill(BROWN)
                for i in range(len(path2)):
                    # FillSquare(GREEN, path[i])
                    # Delay added
                    # pygame.time.delay(100)
                    RefreshScreen()

        # Algorithm selection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dx = 0
                dy = -1
                nx, ny = start_pos[0] + dx, start_pos[1] + dy
                if (Board_Graph.has_edge(start_pos, (nx, ny))):
                    path = deque([(start_pos[0], start_pos[1] - 1)])
                    print("Key Up: ---> new pos: ", path)
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = +1
                nx, ny = start_pos[0] + dx, start_pos[1] + dy
                if (Board_Graph.has_edge(start_pos, (nx, ny))):
                    path = deque([(start_pos[0], start_pos[1] + 1)])
                    print("Key down: ---> new pos: ", path)
            if event.key == pygame.K_LEFT:
                dx = -1
                dy = 0
                nx, ny = start_pos[0] + dx, start_pos[1] + dy
                if (Board_Graph.has_edge(start_pos, (nx, ny))):
                    path = deque([(start_pos[0] - 1, start_pos[1])])
                    print("key left: ---> new pos: ", path)
            if event.key == pygame.K_RIGHT:
                dx = +1
                dy = 0
                nx, ny = start_pos[0] + dx, start_pos[1] + dy
                if (Board_Graph.has_edge(start_pos, (nx, ny))):
                    path = deque([(start_pos[0] + 1, start_pos[1])])
                    print("key right: ---> new pos: ", path)
            if event.key == pygame.K_1:
                algorithm = 1
                algorithm_name = "A STAR"
                screen.fill(BROWN)
            if event.key == pygame.K_2:
                algorithm = 2
                algorithm_name = "BFS"
                screen.fill(BROWN)
            if event.key == pygame.K_3:
                algorithm = 3
                algorithm_name = "Dijkstra"
                screen.fill(BROWN)
            if event.key == pygame.K_e:
                print("Visibilidad de la pared (Edicion): ", show_wall)
                if show_wall == False:
                    show_wall = True
                else:
                    show_wall = False
            if event.key == pygame.K_w:
                node1_y = node1_y - 1
                node2_y = node2_y - 1
                node3_y = node3_y - 1
                node4_y = node4_y - 1
            if event.key == pygame.K_d:
                node1_x = node1_x + 1
                node2_x = node2_x + 1
                node3_x = node3_x + 1
                node4_x = node4_x + 1
            if event.key == pygame.K_a:
                node1_x = node1_x - 1
                node2_x = node2_x - 1
                node3_x = node3_x - 1
                node4_x = node4_x - 1
            if event.key == pygame.K_s:
                node1_y = node1_y + 1
                node2_y = node2_y + 1
                node3_y = node3_y + 1
                node4_y = node4_y + 1
            if event.key == pygame.K_r:
                if rotacion:
                    node2_x = node2_x + 1
                    node2_y = node2_y - 1
                    node3_x = node3_x - 1
                    node3_y = node3_y + 1
                    rotacion = False
                else:
                    node2_x = node2_x - 1
                    node2_y = node2_y + 1
                    node3_x = node3_x + 1
                    node3_y = node3_y - 1
                    rotacion = True
            if event.key == pygame.K_SPACE:
                temp_node_1 = (node1_x, node1_y)
                temp_node_2 = (node2_x, node2_y)
                temp_node_3 = (node3_x, node3_y)
                temp_node_4 = (node4_x, node4_y)
                print("Nodo_x_1: ", node1_x)
                print("Nodo_y_1: ", node1_y)
                print("Nodo_x_2: ", node2_x)
                print("Nodo_y_2: ", node2_y)
                print("Nodo_x_3: ", node3_x)
                print("Nodo_y_3: ", node3_y)
                print("Nodo_x_4: ", node4_x)
                print("Nodo_y_4: ", node4_y)
                lista_node1_x.append(node1_x)
                lista_node1_y.append(node1_y)
                lista_node2_x.append(node2_x)
                lista_node2_y.append(node2_y)
                lista_node3_x.append(node3_x)
                lista_node3_y.append(node3_y)
                lista_node4_x.append(node4_x)
                lista_node4_y.append(node4_y)
                RemoveEdge(node1_x, node1_y, node2_x, node2_y)
                RemoveEdge(node3_x, node3_y, node4_x, node4_y)
                DrawWall(temp_node_1, temp_node_2)
                DrawWall(temp_node_3, temp_node_4)
        pygame.display.update()
        pygame.display.flip()
    if path2 != None:
        if len(path2) > 0:
            start_pos_2 = path2[0]
            path2.popleft()
    if path != None:
        if len(path) > 0:
            start_pos = path[0]
            path.popleft()

    # Overlay UI
    if show_wall:
        DrawWall((node1_x, node1_y), (node2_x, node2_y,))
        DrawWall((node3_x, node3_y), (node4_x, node4_y))
        pygame.display.flip()
    screen.fill(BROWN)
    instructions1 = font.render(
        "Click izquierdo -> Seleccionar punto de inicio", True, WHITE)
    instructions2 = font.render("Click derecho -> Generar camino", True, WHITE)
    instructions3 = font.render("1, 2 y 3-> Cambiar de algoritmo", True, WHITE)
    alg_name = font.render("Algoritmo: " + str(algorithm_name), True, WHITE)
    alg_time = font.render("Tiempo de ejecucion: " +
                           str(time) + "ms", True, WHITE)
    path_len = font.render("Nodos recorridos: " +
                           str(path_lenght), True, WHITE)
    pygame.time.delay(100)
    RefreshScreen()
