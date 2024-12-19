import pygame
import heapq
import csv
import random  

# Define constants for the grid
WIDTH = 400  # window width
HEIGHT = 400  # window height
GRID_SIZE = 10  # size of each grid cell
ROWS = HEIGHT // GRID_SIZE  # number of rows
COLS = WIDTH // GRID_SIZE  # number of columns

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Color for the end point
GREEN = (0, 255, 0)  # Color for the start point
BLUE = (0, 0, 255)  # Color for the path
YELLOW = (255, 255, 0)  # Color for obstacles

# Define obstacle and free cell
OBSTACLE = -1
FREE = 0
START = 1
END = 2

# Define the grid for obstacles (1 for free, -1 for obstacles)
grid = [[FREE for _ in range(COLS)] for _ in range(ROWS)]
energy_limit = 1000

# A* Algorithm helpers
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, end):
    global energy_limit
    print(f"Starting A* from {start} to {end}")
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start))  # (f_score, (x, y))
    g_scores = {start: 0}
    f_scores = {start: heuristic(start, end)}
    came_from = {}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            print(f"Path found: {path[::-1]}")
            return path[::-1]  # Return reversed path (start -> end)

        closed_list.add(current)
        if energy_limit == 0:
            print("Energy limit reached")
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            print(f"Partial path due to energy limit: {path[::-1]}")
            return path[::-1]  # Return the current path (start -> current)
        energy_limit -= 1
        print(f"Energy left: {energy_limit}")
        for neighbor in get_neighbors(current):
            if neighbor in closed_list or not is_valid(neighbor):
                continue
            tentative_g_score = g_scores[current] + 1
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_list, (f_scores[neighbor], neighbor))

    print("No path found")
    return []  # No path found

def find_closest_goal(start, goals):
    closest_goal = None
    min_distance = float('inf')
    for goal in goals:
        distance = heuristic(start, goal)
        if distance < min_distance:
            min_distance = distance
            closest_goal = goal
    return closest_goal

def add_new_goal(goals, all_goals):
    while True:
        new_goal = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if grid[new_goal[1]][new_goal[0]] != OBSTACLE and new_goal not in all_goals and grid[new_goal[1]][new_goal[0]] != START:
            goals.append(new_goal)
            all_goals.append(new_goal)
            print(f"New goal added: {new_goal}")
            break

def a_star_multiple_goals(start, goals, all_goals):
    print(f"Starting A* with multiple goals from {start} to {goals}")
    path = []
    current_start = start
    while goals and energy_limit > 0:
        closest_goal = find_closest_goal(current_start, goals)
        partial_path = a_star(current_start, closest_goal)
        if not partial_path:
            break
        path.extend(partial_path[1:])  # Avoid duplicating the start point
        current_start = closest_goal
        goals.remove(closest_goal)
        add_new_goal(goals, all_goals)
    print(f"Final path: {path}")
    return path

def get_neighbors(position):
    x, y = position
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return neighbors

def is_valid(position):
    x, y = position
    if 0 <= x < COLS and 0 <= y < ROWS and grid[y][x] != OBSTACLE:
        return True
    return False

# Pygame visualization
def draw_grid(screen):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == OBSTACLE:
                color = BLACK  # Obstacles are black
            else:
                color = WHITE  # Free spaces are white
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_start_end(screen, start, ends):
    # Start is green
    pygame.draw.rect(screen, GREEN, (start[0] * GRID_SIZE, start[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Ends are red
    for end in ends:
        pygame.draw.rect(screen, RED, (end[0] * GRID_SIZE, end[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_path(screen, path, all_goals):
    if path:
        x, y = path[-1]  # Only draw the current position of the robot
        pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        if (x, y) in all_goals:
            pygame.time.wait(1000)
            all_goals.remove((x, y))

# Function to add obstacles (can be random or manually set)
def add_obstacles(start, ends):
    for _ in range(50):  # Add random obstacles
        x, y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
        if (x, y) != start and (x, y) not in ends:
            grid[y][x] = OBSTACLE

def save_grid_to_csv():
    with open('C:/Users/hnv/Gama_Workspace/Testing_GAMA_Python_API/includes/grid_state.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the number of columns and rows in the first two lines
        writer.writerow([COLS])
        writer.writerow([ROWS])

        # Write the obstacle coordinates
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == OBSTACLE:
                    writer.writerow([float(i), float(j)])

def save_start_and_goal_to_csv(start, ends):
    with open('C:/Users/hnv/Gama_Workspace/Testing_GAMA_Python_API/includes/start_end.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([start[0], start[1]])
        for e in ends:
            writer.writerow([e[0], e[1]])

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Visualization")

    # Define start and end positions
    start = (random.randint(0, 5), random.randint(0, 5))
    # Define multiple end positions
    ends = [(random.randint(0, COLS-1), random.randint(0, ROWS-1)) for _ in range(3)]
    all_goals = ends.copy()

    # Add some obstacles
    add_obstacles(start, ends)

    # Save to csv file
    save_grid_to_csv()

    # Run A* to find the path
    path = a_star_multiple_goals(start, ends, all_goals)

    save_start_and_goal_to_csv(start, all_goals)

    if path:
        # Save the path to CSV file
        with open('C:/Users/hnv/Gama_Workspace/Testing_GAMA_Python_API/includes/path.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for x, y in path:
                writer.writerow([x, y])

    # Visualization loop
    clock = pygame.time.Clock()
    running = True
    step = 0
    while running:
        screen.fill(WHITE)
        draw_grid(screen)
        draw_start_end(screen, start, all_goals)
        draw_path(screen, path[:step+1], all_goals)

        # Print the current step for debugging
        #print(f"Step: {step}, Current Position: {path[step]}")

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(10)
        if step < len(path) - 1:
            step += 1

    pygame.quit()

if __name__ == "__main__":
    main()
