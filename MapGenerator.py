import random

# Add input validation and error checking


def printGrid(grid):
    """Prints the given grid"""
    print()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end=" ")
        print()


class MapGenerator:
    def __init__(self, rows, cols, num_obstacles, num_pickup_points, scale_factor):
        self.rows = rows
        self.cols = cols
        self.num_obstacles = num_obstacles
        self.num_pickup_points = num_pickup_points
        self.scale_factor = scale_factor
        self.base_grid = [['#'] * (cols + 2) for _ in range(rows + 2)]
        self.base_obstacle_positions = set((i, j) for j in range(1, cols + 1) for i in range(
            1, rows + 1))

    def generate(self):
        grid = [row[:] for row in self.base_grid]
        obstacle_positions = self.base_obstacle_positions.copy()
        free_positions = set()
        valid_free_positions = set()

        num_to_free = self.rows * self.cols - self.num_obstacles
        to_pick_random = num_to_free // self.scale_factor
        num_to_free -= to_pick_random

        while to_pick_random > 0:
            cur_pos = random.choice(tuple(obstacle_positions))
            obstacle_positions.remove(cur_pos)
            grid[cur_pos[0]][cur_pos[1]] = '='
            free_positions.add(cur_pos)
            to_pick_random -= 1

        while num_to_free > 0:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            random_dir = random.choice(directions)
            new_pos = (cur_pos[0] + random_dir[0], cur_pos[1] + random_dir[1])

            if not (1 <= new_pos[0] <= self.rows and 1 <= new_pos[1] <= self.cols):
                continue

            cur_pos = (new_pos[0], new_pos[1])

            if new_pos not in free_positions:
                grid[new_pos[0]][new_pos[1]] = '='
                obstacle_positions.remove(new_pos)
                free_positions.add(new_pos)
                valid_free_positions(new_pos)
                num_to_free -= 1

        taxi_pos = random.choice(tuple(valid_free_positions))
        valid_free_positions.remove(taxi_pos)
        free_positions.remove(taxi_pos)
        grid[taxi_pos[0]][taxi_pos[1]] = 'T'
        print('Taxi:', taxi_pos)

        pickup_coords = []

        for _ in range(self.num_pickup_points):
            pickup_pos = random.choice(tuple(valid_free_positions))
            free_positions.remove(pickup_pos)
            valid_free_positions.remove(pickup_pos)
            pickup_coords.append(pickup_pos)

        return grid, pickup_coords


if __name__ == '__main__':
    map_gen = MapGenerator(5, 5, 4, 4, 2)
    grid, pickup_coords = map_gen.generate()
    printGrid(grid)
    print(pickup_coords)
