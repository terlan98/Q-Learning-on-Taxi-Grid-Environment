import random

# Add input validation and error checking


class MapGenerator:
    def __init__(self, rows, cols, num_obstacles):
        self.rows = rows
        self.cols = cols
        self.num_obstacles = num_obstacles
        self.base_grid = [['#'] * (cols + 2) for _ in range(rows + 2)]
        self.base_obstacle_positions = set((i, j) for i in range(
            1, rows + 1) for j in range(1, cols + 1))

    def generate(self):
        grid = [row[:] for row in self.base_grid]
        obstacle_positions = self.base_obstacle_positions.copy()
        free_positions = set()

        cur_pos = random.choice(tuple(obstacle_positions))
        grid[cur_pos[0]][cur_pos[1]] = '='
        free_positions.add(cur_pos)
        num_to_free = self.rows * self.cols - self.num_obstacles - 1

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
                num_to_free -= 1

        for marker in ['S', 'F', 'T']:
            marker_pos = random.choice(tuple(free_positions))
            free_positions.remove(marker_pos)
            grid[marker_pos[0]][marker_pos[1]] = marker

        return grid


if __name__ == '__main__':
    map_gen = MapGenerator(5, 1, 2)
    grid = map_gen.generate()
    print(grid)
