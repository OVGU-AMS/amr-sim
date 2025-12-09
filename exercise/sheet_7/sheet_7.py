import irsim
import numpy as np
import math
from typing import List


'''
EXERCISE SHEET 7

In this exercise a position estimation is calculated, based on the LiDAR measurements of the robot.
Additionally, the identity of the hit wall is known, as well as its geometrical properties.
Using this a virtual measurement is constructed, which is then used to calculate the position of the robot.

This time the estimate is calculated using recursive least squares.
'''

def transform_to(x: np.ndarray, t: np.ndarray, a: float):
    '''Transforms a pose or velocity into an other coordinate frame by translating and rotating.
    (This function was already implemented in sheet 1)

    Args:
        x (np.ndarray): State or velocity which should be transformed to a new coordinate frame.
        t (np.ndarray): Translation of the original coordinate frame in the target frame.
        a (float): Angle of the original coordinate frame in the target frame.

    Returns:
        np.ndarray: Pose or velocity in the new coordinate frame.
    '''
    
    R = np.array([[math.cos(a), - math.sin(a)],
                  [math.sin(a), math.cos(a)]])
    
    x_transformed = t + R @ x
    
    return x_transformed

def build_H(normals):
    """
    Builds the measurement mapping matrix H from the normals of the walls.
    
    Args:
        normals (np.ndarray): Normal vectors of the walls
    
    Returns:
        np.ndarray: Measurement mapping matrix H
    """

    H = np.stack(normals)
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
    
    s = np.cos(deltas) * lidar_ranges
    y = wall_dists + s
    return y

def build_gain(previous_C, H, W):
    """Calculates the gain matrix K

    Args:
        previous_C (np.ndarray): Covariance of the estimate of the previous time step.
        H (np.ndarray): Measuremten mapping matrix.
        W (np.ndarray): Weighting matirx / Error of the current measurement.

    Returns:
        np.ndarray: Gain matrix K
    """
    
    # TODO create the gain matrix K using the equation from the lecture
    K = 
    
    return K

def position_from_recursive_lsq(previous_estimate, previous_covariance, normal, wall_dist, delta, lidar_range):
    """
    Calculates a new position estimation of the robot using one lidar measurement to a wall and the previous estimation.

    Args:
        previous_estimate (np.ndarray): Position estimate as `(x,y)` calculated in the previous time step.
        previous_covariance (np.ndarray): Covariance of the estimate of the previous time step.
        normal (np.ndarray): Normal vector of the hit wall.
        wall_dist (np.ndarray): Distance of the hit wall to the coordinate origin. 
            Together with `normal` they describe the wall as line using the hessian form.
        delta (np.ndarray): Angle between the normal vector of the wall and the LiDAR ray hitting the wall
        lidar_range (np.ndarray): Measured ranges of the LiDAR rays.

    Returns:
        np.ndarray: Position of the robot as `(x,y)`
    """

    # TODO build the weighting / error matrix (HINT the standard deviation of the lidar is 0.2) 
    W = 
    
    # TODO fill the H and y by passing the correct values in the respecting functions
    H = 
    y = 
    
    # TODO fill K by passing the correct values in the respecting function
    K = 
    
    # TODO use the equations from the lecture to compute x and C
    x = 

    C = 
    
    return x, C


# ---- Not relevant for you ----


env = irsim.make("sheet_7.yaml", save_ani=False, full=False)

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

        # Calculate the distance of wall to origin
        c = n / (normal[1] - m*normal[0])
        
        normals.append(normal)
        wall_dists.append(c)
        deltas.append(delta)
        lidar_ranges.append(lidar_measurements[i][0])
    estimation = np.array([0,0])
    covariance = np.array([[1000,0],[0,1000]])
    for normal, wall_dist, delta, lidar_range in zip (normals, wall_dists,deltas,lidar_ranges):
        estimation, covariance = position_from_recursive_lsq(estimation, covariance, np.array([normal]), np.array([wall_dist]),np.array([delta]),np.array([lidar_range]))
    env._env_plot.estimation_pos = estimation

    if env.done():
        break

env.end(3)
