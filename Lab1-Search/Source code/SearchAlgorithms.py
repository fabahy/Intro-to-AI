from math import sqrt
from Space import *
from Constants import *

''' Hàm hiển thị màu từng trạng thái của node '''
def displayNode(node:Node, screen:pygame.Surface, color, speed = 15):
    node.set_color(color)
    node.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(speed)

def DFS(g:Graph, sc:pygame.Surface):
    pygame.time.set_timer(0, 0)
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    ''' Khởi tạo start '''
    current_node = g.grid_cells[open_set[0]]
    ''' Mở rộng node cho đến khi tìm được đích '''
    while True:
        displayNode(current_node, sc, yellow)
        ''' Kiểm tra current node có phải là đích ? '''
        if g.is_goal(current_node):
            break
        neighbors = g.get_neighbors(current_node)
        for neighbor in neighbors:
            ''' Kiểm tra node đã được duyệt qua chưa ? '''
            if neighbor.value not in open_set and neighbor.value not in closed_set:
                open_set.append(neighbor.value)
                displayNode(neighbor, sc, red) 
                displayNode(current_node, sc, blue)
                ''' Lưu vết tạo đường đi '''
                father[neighbor.value] = current_node.value
                current_node = neighbor
                break
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
        else: #TH: mở rộng đến node cuối cùng nhưng chưa phải là node đích
            item = open_set.pop(-1)
            closed_set.append(item)
            displayNode(current_node, sc, red)
            current_node = g.grid_cells[open_set[-1]]
    displayNode(g.goal, sc, purple)
    ''' Tìm lại các node được mở rộng trước khi đến đích '''
    temp_goal = g.goal
    while True:
        tracking = g.grid_cells[father[temp_goal.value]]
        ''' Vẽ đường đi '''
        pygame.draw.line(sc, green, (tracking.x, tracking.y), (temp_goal.x, temp_goal.y))
        displayNode(tracking, sc, grey)
        if g.start.value == tracking.value:
            displayNode(g.start, sc, orange)
            break  
        temp_goal = tracking
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

def BFS(g:Graph, sc:pygame.Surface):
    pygame.time.set_timer(0, 0)
    open_set = [g.start.value]
    closed_set = []
    father = [-1]*g.get_len()
    ''' Khởi tạo start '''
    current_node = g.grid_cells[open_set[0]]
    ''' Mở rộng node cho đến khi tìm được node đích '''
    while True:
        item = open_set.pop(0)
        closed_set.append(item)
        displayNode(current_node, sc, yellow)
        ''' Kiểm tra current node có phải là đích ? '''
        if g.is_goal(current_node):
            break
        neighbors = g.get_neighbors(current_node)
        for neighbor in neighbors:
            if neighbor.value not in open_set and neighbor.value not in closed_set:
                open_set.append(neighbor.value)
                displayNode(neighbor, sc, red)
                ''' Lưu vết tạo đường đi '''
                father[neighbor.value] = current_node.value
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
        displayNode(current_node, sc, blue)
        current_node = g.grid_cells[open_set[0]]
    displayNode(g.goal, sc, purple)
    ''' Tìm lại các node được mở rộng trước khi đến đích '''
    temp_goal = g.goal
    while True:
        tracking = g.grid_cells[father[temp_goal.value]]
        ''' Vẽ đường đi '''
        pygame.draw.line(sc, green, (tracking.x, tracking.y), (temp_goal.x, temp_goal.y))
        displayNode(tracking, sc, grey)
        if g.start.value == tracking.value:
            displayNode(g.start, sc, orange)
            break
        temp_goal = tracking
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

def UCS(g:Graph, sc:pygame.Surface):
    pygame.time.set_timer(0, 0)
    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0
    while True:
        ''' Khởi tạo start với chi phí nhỏ nhất'''
        item = min(open_set, key=open_set.get)
        current_node = g.grid_cells[item]
        del open_set[current_node.value]
        closed_set.append(item)
        displayNode(current_node, sc, yellow)
        ''' Kiểm tra current node có phải là đích ? '''
        if g.is_goal(current_node):
            break
        neighbors = g.get_neighbors(current_node)
        for neighbor in neighbors:
            ''' Lưu lại chi phí current node'''
            temp_cost = cost[current_node.value] + 1
            if neighbor.value not in closed_set and neighbor.value not in open_set:
                father[neighbor.value] = current_node.value
                open_set[neighbor.value] = temp_cost
                displayNode(neighbor, sc, red)
            elif neighbor.value in open_set:
                if temp_cost < open_set[neighbor.value]: #Ưu tiên node có chi phí nhỏ nhất
                    father[neighbor.value] = current_node.value
                    open_set[neighbor.value] = temp_cost
                    displayNode(neighbor, sc, red)      
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
        displayNode(current_node, sc, blue)
    displayNode(g.goal, sc, purple)
    ''' Tìm lại các node được mở rộng trước khi đến đích '''
    temp_goal = g.goal
    while True:
        tracking = g.grid_cells[father[temp_goal.value]]
        ''' Vẽ đường đi '''
        pygame.draw.line(sc, green, (tracking.x, tracking.y), (temp_goal.x, temp_goal.y))
        displayNode(tracking, sc, grey)
        if g.start.value == tracking.value:
            displayNode(g.start, sc, orange)
            break
        temp_goal = tracking
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

def heuristic(current:Node, goal:Node) -> float:
    # Euclidean distance
    dx = (current.x-TILE/2)/TILE - (goal.x-TILE/2)/TILE
    dy = (current.y-TILE/2)/TILE - (goal.y-TILE/2)/TILE
    result = sqrt(dx* dx + dy * dy)
    return result

def AStar(g:Graph, sc:pygame.Surface):
    pygame.time.set_timer(0, 0)
    open_set = {}
    open_set[g.start.value] = 0
    closed_set:list[int] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0

    ucs_clock = pygame.time.Clock()
    fps = 10

    while True:
        ''' Khởi tạo start với chi phí nhỏ nhất'''
        item = min(open_set, key=open_set.get)
        cost[item] = cost[father[item]] + 1
        current_node = g.grid_cells[item]
        del open_set[current_node.value]
        closed_set.append(item)
        displayNode(current_node, sc, yellow)
        ''' Kiểm tra current node có phải là đích ? '''
        if g.is_goal(current_node):
            break
        neighbors = g.get_neighbors(current_node)
        for neighbor in neighbors:
            ''' Lưu lại chi phí current node'''
            temp_cost = cost[current_node.value]  + 1
            if neighbor.value not in closed_set and neighbor.value not in open_set:
                father[neighbor.value] = current_node.value
                open_set[neighbor.value] = temp_cost + heuristic(neighbor, g.goal)
                displayNode(neighbor, sc, red)
            elif neighbor.value in open_set:
                if (temp_cost + heuristic(neighbor, g.goal)) < open_set[neighbor.value]:
                    father[neighbor.value] = current_node.value
                    open_set[neighbor.value] = temp_cost + heuristic(neighbor, g.goal)
                    displayNode(neighbor, sc, red)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
        displayNode(current_node, sc, blue)
    displayNode(g.goal, sc, purple)
    ''' Tìm lại các node được mở rộng trước khi đến đích '''
    temp_goal = g.goal
    while True:
        tracking = g.grid_cells[father[temp_goal.value]]
        ''' Vẽ đường đi '''
        pygame.draw.line(sc, green, (tracking.x, tracking.y), (temp_goal.x, temp_goal.y))
        displayNode(tracking, sc, grey)
        if g.start.value == tracking.value:
            displayNode(g.start, sc, orange)
            break
        temp_goal = tracking
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()