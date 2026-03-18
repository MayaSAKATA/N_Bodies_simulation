from operator import pos
import numpy as np
from scipy.spatial import distance_matrix, distance
import time
from galaxy_generator import generate_star_color
from visualizer3d_vbo import Visualizer3D
import sys
import numba

G = 1.560339e-13 # Gravitationnal constant

def initialize_grid(positions):
    """
    Initialize the global variable square_size and radius of the square
    """
    global square_size, radius
    size_x = max(positions[:, 0]) - min(positions[:, 0])
    size_y = max(positions[:, 1]) - min(positions[:, 1])
    size_z = max(positions[:, 2]) - min(positions[:, 2])
    square_size_list = [size_x, size_y, size_z]
    square_size = [x * 1.05/20 for x in square_size_list] # Ajust size with a margin
    # square_size = [size_x, size_y, size_z]*1.05 / 20 # Ajust size with a margin
    radius = np.sqrt(size_x**2 + size_y**2 + size_z**2)
    return square_size, radius

#@numba.njit
def assign_to_grid(positions):
    """
    Assign each star to a grid square : grid = {(grid_x, grid_y): [index1, index2, ...}
    For each square coordinates (grid_x, grid_y) we have a list of idx of stars
    """
    global square_size
    grid = {}
    for i, pos in enumerate(positions):
        grid_x = int(pos[0] // square_size[0])
        grid_y = int(pos[1] // square_size[1])
        key = (grid_x, grid_y)
        if key not in grid:
            grid[key] = []
        grid[key].append(i)
    return grid

#@numba.njit
def center_gravity(positions, mass):
    """
    Calculate the center of gravity of a set of stars.
    """
    total_mass = np.sum(mass)

    center_of_mass_x = np.sum([x*m for x,m in zip(positions[0, :], mass)])
    center_of_mass_y = np.sum([y*m for y,m in zip(positions[1, :], mass)])
    center_of_mass_z = np.sum([z*m for z,m in zip(positions[2, :], mass)])

    return [center_of_mass_x/total_mass, center_of_mass_y/total_mass, center_of_mass_z/total_mass], total_mass


#@numba.njit(parallel=True)
def calculate_acceleration(positions, mass):
    """
    Calculate the gravitational accelerations on each body due to all other bodies.
    Based on this formula : accel[i] = f[i] / m[i] 
    """
    global square_size, radius
    grid = assign_to_grid(positions) # Update grid assignment at each step

    n = positions.shape[0]
    accelerations = np.zeros((n, 3), dtype=np.float64) 


    #for i in numba.prange(n):
    for i in range(n):
        acc = np.zeros(3)
        for key, indices in grid.items():
            for id in indices :
                center_mass, total_mass = center_gravity(positions, mass)
                pos = positions[id, :] # positions de l'etoile id
                dist = distance.euclidean(center_mass, pos)

                if 0.5 * dist > radius :
                    diff = center_mass - positions[i, :]
                    if dist > 1e-10 :
                        acc += G * total_mass * diff /(dist**3)

                else :
                    for j in range(n):
                        if i == j:
                            continue
                        diff = positions[j, :] - positions[i, :]
                        dist = np.sqrt(diff[0]*diff[0] + diff[1]*diff[1] + diff[2]*diff[2])
                        if dist > 1e-10:
                            acc += G * mass[j] * diff / (dist**3)
        
        accelerations[i] = acc

    return accelerations

def step(dt):
    """
    Updates the all the positions in the system after a time step dt.
    """
    global positions, velocity, mass
    acc = calculate_acceleration(positions, mass)

    new_positions = positions + velocity * dt + 0.5 * acc * dt**2

    new_acc = calculate_acceleration(new_positions, mass)

    new_velocity = velocity + 0.5 * (acc + new_acc) * dt

    # upater doesn't edit variables, returns new values
    positions = new_positions
    velocity = new_velocity
    return positions


def load_galaxy(filename):
    """
    Load a system of bodies from a file like (mass, positionsx, positionsy, positionsz, velocityx, velocityy, velocityz)
    """
    positions = [] # [[0, 0, 0], [0, 0, 0], ...]
    velocity = [] # [[0, 0, 0], [0, 0, 0], ...]
    color = []  # [(255, 255, 255), (255, 255, 255), ...]
    mass = [] # [1.0, 1.0, ...]

    with open(filename, 'r') as file:
        for line in file:
            data = list(map(float, line.split()))
            positions.append(data[1:4])
            velocity.append(data[4:7])
            color.append(generate_star_color(data[0]))
            mass.append(data[0])
    return np.array(positions), np.array(velocity), np.array(mass), np.array(color)

if __name__ == "__main__":

    global positions, velocity, mass, color, square_size, radius
    positions, velocity, mass, color  = load_galaxy("data/galaxy_{}".format(sys.argv[2] if len(sys.argv) > 2 else "100"))
    
    square_size, radius = initialize_grid(positions)

    dt = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-2

    #Time the execution of 10 steps
    start_time = time.time()
    for _ in range(10):
        step(dt)
    end_time = time.time()
    print(f"Time for 10 steps ({len(mass)} bodies): {end_time - start_time:.4f} seconds\n")
    
    # Visualization
    luminosities = np.ones(len(positions), dtype=np.float32)
    bounds = ((-3, 3), (-3, 3), (-3, 3))

    visualizer = Visualizer3D(positions, color, luminosities, bounds)
    visualizer.run(updater=step, dt=dt)