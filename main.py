import pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH+1, HEIGHT + 80))

clock = pygame.time.Clock()

font = pygame.font.SysFont("bell", 28)

class Node:
        def __init__(self, x, y, node_side):
            self.x, self.y = x, y
            self.neighbours = []
            self.is_obstacle = False
            self.parent = None
            self.visited = False
            self.node_side = node_side
            self.color = BLACK
            self.path_part = False
            self.h = 99999
            self.f = 99999
            self.g = 99999

        def draw(self, screen):
            if self.visited and not self.path_part :
                self.color = YELLOW
            pygame.draw.rect(screen, self.color, (self.x * self.node_side + 1, self.y * self.node_side + 1, self.node_side-1, self.node_side-1))
        
        # Heiristic function using Manhattan distance
        def heuristic(self, end_node):
            self.h = abs(self.x - end_node.x) + abs(self.y - end_node.y)

# Adding adjacent nodes as neighbours
def add_neigh(grid, rows, cols):
    for i in range(rows):
        for j in range(cols):
            # Add neighbours only if node isn't an obstacle
            if not grid[i][j].is_obstacle:
                if i > 0:
                    grid[i][j].neighbours.append(grid[i - 1][j])
                if i < rows - 1:
                    grid[i][j].neighbours.append(grid[i + 1][j])
                if j < cols - 1:
                    grid[i][j].neighbours.append(grid[i][j + 1])
                if j > 0:
                    grid[i][j].neighbours.append(grid[i][j - 1])

def a_star(screen, grid, start_node, end_node, rows, cols):
    open_list = [start_node]
    closed_list = [[False for _ in range(cols)] for x in range(rows)]
    path = []

    while(len(open_list) > 0):
        clock.tick(30)
        current_node = open_list.pop(0)

        #Current node has been visited
        i, j = current_node.x, current_node.y
        closed_list[i][j] = True
        current_node.visited = True

        # Destination node found
        if current_node.x == end_node.x and current_node.y == end_node.y:
            while(current_node):
                current_node.path_part = True
                path.append(current_node)
                current_node = current_node.parent
            break
        
        for neighbour in current_node.neighbours:
            if not neighbour.is_obstacle:
                # If goal node is reached
                if neighbour == end_node:
                    neighbour.parent = current_node
                    neighbour.f = 0
                    open_list[0] = neighbour
                    break
                
                # If neighbour exists in closed_list then ignore it
                if closed_list[neighbour.x][neighbour.y] == True:
                    continue

                neighbour.parent = current_node # Set parent of successor nodes
                neighbour.heuristic(end_node) # Calculate h(n) using heuriistic function
                neighbour.g = current_node.g + 1 # Set g value of neighbor as parent + 1 since cost if uniform
                neighbour.f = neighbour.g + neighbour.h

                # Check if node exists in OPEN list
                found = False
                for node in open_list:
                    if node.x == neighbour.x and node.y == neighbour.y:
                        found = True # Node is found in OPEN
                        # If f value is already less then ignore this node
                        if node.f < neighbour.f:
                            break
                        else:
                            open_list.remove(node)
                            open_list.append(neighbour)
                # If node doesn't exist in OPEN list then add it
                if not found:
                    open_list.append(neighbour)    
        # open_list is a priority queue
        # sort it according to priority
        open_list.sort(key = lambda node: node.f)
        
        current_node.draw(screen)
        pygame.display.update()
    
    for i, node in enumerate(path):
        node.color = BLUE
        node.draw(screen)
        pygame.display.update()
    
    # Change colors of start and end node for better visualization
    start_node.color = RED
    start_node.draw(screen)
    end_node.color = GREEN
    end_node.draw(screen)
    pygame.display.update()
        

# Main function
def main():
    # Instruction to be displayed
    messages = [
        "Press Enter after you're done drawing obstacles",
        "Select the starting point",
        "Select the ending point",
        "Press Enter to start A* Search",
        "Finding the optimal path...",
        "Optimal Path found! Press Enter to Reset"
    ]
    # Index of instruction/msg
    msg_index = 0

    # Creating the graph/grid
    rows, cols = 30, 30
    # Length of side of each square node
    node_side = 600 // rows
    grid = [[Node(i, j, node_side) for j in range(cols)] for i in range(rows)]
    
    add_neigh(grid, rows, cols)

    screen.fill(BLACK)
    running = True
    drawing_obstacles = False
    drawing_start = False
    drawing_end = False
    start_node = None
    end_node = None

    while(running):
        screen.fill(BLACK)
        # Drawing the actual grid
        for i in range(rows + 1):
            pygame.draw.line(screen, GREY, (i * node_side, 0), (i * node_side, HEIGHT), 1) # Columns
            pygame.draw.line(screen, GREY, (0, i * node_side), (WIDTH, i * node_side), 1) # Rows           

        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Determine action depending on the instruction being displayed
                if msg_index == 0:
                    drawing_obstacles = True
                elif msg_index == 1:
                    drawing_start = True
                elif msg_index == 2:
                    drawing_end = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing_obstacles = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Done drawing obstacles now next instruction
                    if msg_index == 0:
                        msg_index = msg_index + 1
                    elif msg_index == 3:
                        msg_index += 1
                    # Reset everything
                    elif msg_index == 5:
                        main()
        
        if drawing_obstacles:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_x // node_side, mouse_y // node_side # Converting mouse pos to indices of graph
            grid[mouse_x][mouse_y].is_obstacle = True
            grid[mouse_x][mouse_y].color = GREY

        if drawing_start:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_x // node_side, mouse_y // node_side # Converting mouse pos to indices of graph
            # Starting node will be colored red
            grid[mouse_x][mouse_y].color = RED
            start_node = grid[mouse_x][mouse_y]
            drawing_start = False
            msg_index += 1
            # Set f and g value of start node to 0
            start_node.f = 0
            start_node.g = 0

        if drawing_end:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_x // node_side, mouse_y // node_side # Converting mouse pos to indices of graph
            # Ending node will be colored green
            grid[mouse_x][mouse_y].color = GREEN
            end_node = grid[mouse_x][mouse_y]
            drawing_end = False
            msg_index += 1

            # Calling the heuristiic function for each node
            # for row in grid:
            #     for node in row:
            #         node.heuristic(end_node)

        # Display the instruction
        instruction = font.render(messages[msg_index], True, WHITE)
        screen.blit(instruction, (20, 620)) 

        for i in range(rows):
            for j in range(cols):
                grid[i][j].draw(screen)
        pygame.display.update()

        if msg_index == 4:
            #bfs(screen, start_node, end_node)
            a_star(screen, grid, start_node, end_node, rows, cols)
            msg_index += 1

main()