import irsim
import numpy as np
import math
from typing import List


'''
EXERCISE SHEET 5

In this exercise a position estimation is calculated, based on the LiDAR measurements of the robot.
Additionally, the identity of the hit wall is known, as well as its geometrical properties.
Using this a virtual measurement is constructed, which is then used to calculate the position of the robot.
'''

def build_H(normals):
    """
    Builds the measurement mapping matrix H from the normals of the walls.
    
    Args:
        normals (np.ndarray): Normal vectors of the walls
    
    Returns:
        np.ndarray: Measurement mapping matrix H
    """

    # TODO build the H matrix using the normals
    
    H = np.array([[0.0,0.0],[0.0,0.0]])
    return H

def build_y(normals, wall_dists, deltas, lidar_ranges):
    """
    Creates the virtual measurements from known information about the walls, the measured range and angle.
    
    Args:
        normals (np.ndarray): Normal vectors of the hit walls.
        wall_dists (np.ndarray): Distances of the hit walls to the coordinate origin. 
            Together with `normals` they describe the walls as lines using the hessian form.
        deltas (np.ndarray): Angle of TODO decide lidar or lidar to normal
        lidar_ranges (np.ndarray): Measured ranges of the LiDAR rays

    Returns:
        np.ndarray: Virtual measurements
    """

    # TODO calculate the virtual measurements y. Use your derived transformation to orthogonal measurements.

    y = [0.0,0.0]

    return np.array(y)

def position_from_block_lsq(normals, wall_dists, deltas, lidar_ranges, lidar_pos, heading):
    """
    Calculates the position of the robot using lidar measurements to walls.

    Args:
        normals (np.ndarray): Normal vectors of the hit walls.
        wall_dists (np.ndarray): Distances of the hit walls to the coordinate origin. 
            Together with `normals` they describe the walls as lines using the hessian form.
        deltas (np.ndarray): Angle between LiDAR ray and normal vector of the wall.
        lidar_ranges (np.ndarray): Measured ranges of the LiDAR rays.
        lidar_pos (np.ndarray): Position of the LiDAR sensor in the robot coordinate frame.
        heading (float): Heading of the robot.

    Returns:
        np.ndarray: Position of the robot as `(x,y)`
    """
    
    # TODO Use the lidar rays, the known information about the walls and your implemented functions to calculate the position od the lidar.
    #      Then transform this to the robots position.
    
    p = np.array([0.0,0.0])
    
    return p


# ---- Not relevant for you ----


env = irsim.make("sheet_6.yaml", save_ani=False, full=False)

lines = [[1/25, 0, 'blue'],
         [25, 0, 'red'],
         [-1/25, 50, 'green'],
         [25,- 25*48, 'purple']
]

env._env_plot.init_lidar_lines(4)
env._env_plot.init_side_box()

for _i in range(1000):
    env.step()
    env.render(0.05)
    env._env_plot.robot_pos = (env.get_robot_state()[0][0], env.get_robot_state()[1][0])
    lidar_measurements = [np.array([r,0,env.get_lidar_scan()['angle_min'] + env.get_lidar_scan()['angle_increment'] * i]) for i,r in enumerate(env.get_lidar_scan()['ranges'])]
    hit_geoms = env.get_lidar_scan()["coords_hit"]
    robot_velocity = env.get_robot_info().current_velocity.flatten()
    robot_velocity[1] = 0
    robot_position = env.get_robot_state().flatten()[:-1]
    lidar_pose = np.array([2,0])

    normals = []
    wall_dists = []
    deltas = []
    lidar_ranges = []

    coords_rays = env.get_lidar_scan()["coords_rays"]
    for i,g in enumerate(hit_geoms):
        coord_1 = g.coords[0]
        coord_2 = g.coords[1]
        
        # Calculate parameters for line equation y = mx + n
        m = (coord_1[1] - coord_2[1]) / (coord_1[0] - coord_2[0])
        n = coord_1[1] - m * coord_1[0]
        
        # Calculate the normals
        normal = [(coord_2[1] - coord_1[1]),coord_2[0] - coord_1[0]]
        n_size = math.sqrt(math.pow(normal[0],2)+math.pow(normal[1],2))
        normal[0] = normal[0] / n_size
        normal[1] = normal[1] / n_size

        # Calculate angle between measurement and normal
        ray = [(coords_rays.geoms[i].coords[0][0] - coords_rays.geoms[i].coords[1][0]),coords_rays.geoms[i].coords[0][1] - coords_rays.geoms[i].coords[1][1]]

        delta = math.acos((normal[0] * ray[0] + ray[1] * normal[1]) / (math.sqrt(math.pow(ray[0],2)+ math.pow(ray[1],2)) * math.sqrt(math.pow(normal[0],2)+math.pow(normal[1],2))))

        if delta > math.pi /2:
            delta = math.pi - delta
            
        # Calculate the distance of wall to origin
        c = n / (normal[1] - m*normal[0])
        
        normals.append(normal)
        wall_dists.append(c)
        deltas.append(delta)
        lidar_ranges.append(lidar_measurements[i][0])
    estimation = position_from_block_lsq(normals, wall_dists,deltas,lidar_ranges, lidar_pose, robot_position[2])
    env._env_plot.estimation_pos = estimation

    if env.done():
        break

env.end(3)