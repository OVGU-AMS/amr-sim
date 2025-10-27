import irsim
import numpy as np
from typing import List


'''
EXERCISE SHEET 1

In this exercise some basic functions for coordinate frame transformations are developed.
They build the foundation of every calculation in robotics, as well as in this lecture.
The functions you develop here may also be used in later programming tasks.
'''


def transform_to(x: np.ndarray, t: np.ndarray, a: float):
    '''Transforms a pose or velocity into an other coordinate frame by translating and rotating.

    Args:
        x (np.ndarray): State or velocity which should be transformed to a new coordinate frame.
        t (np.ndarray): Translation of the original coordinate frame in the target frame.
        a (float): Angle of the original coordinate frame in the target frame.

    Returns:
        np.ndarray: Pose or velocity in the new coordinate frame.
    '''
    
    # TODO 1a: construct the rotation matrix R using the passed angle a  
    # TODO 1b: calculate the new x using the rotation matrix R and the translation
    
    x_transformed = x
    
    return x_transformed

def transform_wheel_to_global(robot_pose: np.ndarray, wheel_pose: np.ndarray):
    '''Transforms the position of the wheel to the global coordinate frame

    Args:
        robot_pose (np.ndarray): Pose of the robot as vector with `(x,y,a)^T` where `x, y` are the position 
            and `a` the heading in the global coordinate frame.
        wheel_pose (np.ndarray): Pose of the wheel relative to the robots center with `(x,y,a)^T` 
            where `x, y` are the position and `a` the heading.
        
    Returns:
        np.ndarray: The wheels pose in the global coordinate frame.

    '''
    
    #TODO 2a: Use the transform_to function to transform the wheel_pose to the global coordinate frame using the robots position and heading
    
    wheel_global = wheel_pose

    return wheel_global

def transform_measurement_to_global(robot_pose: np.ndarray, lidar_pose: np.ndarray, measurements: List[np.ndarray]):
    '''Transforms a LiDAR measurement to the global coordinate frame

    Args:
        robot_pose (np.ndarray): Pose of the robot as vector with `(x,y,a)^T` where `x, y` are the position 
            and `a` the heading in the global coordinate frame.
        lidar_pose (np.ndarray): Pose of the LiDAR sensor as vector with `(x,y,a)^T` where `x, y` are the position 
            and `a` the heading in the robots coordinate frame.
        measurement (List[np.ndarray]): Measurements of a LiDAR sensor. Elements of the list contain `(x,y,w)^T` 
            where `x, y` are the positions of the measurements relative to the robots coordinate frame and `w`
            the angle of the measurement ray.
        
    Returns:
        List[np.ndarray]: Transformed LiDAR measurements in the global coordinate frame. Should only contain a list of 
            `(x,y)^T` with the locations of the measurements.
    '''
    
    # TODO 2b: Transform the measurements to the global coordinate frame by using a two step approach and the transform_to function.
    #          First convert the measurement to the robots coordinate frame using the angle of the ray and the pose of the sensor.
    #          Then transform this to the global frame by using the robots pose.
    
    measurements_global = measurements

    return measurements_global

def transform_velocity_to_global(robot_pose: np.ndarray, velocity: np.ndarray):
    '''Transforms the relative velocity of the robot to a velocity in the global coordinate frame

    Args:
        robot_pose (np.ndarray): Pose of the robot as vector with `(x,y,a)^T` where `x, y` are the position and `a` the heading in the global coordinate frame.
        velocity (np.ndarray): Velocity of the robot in the robot coordinate frame with `(x,y)^T`, containing the velocity in x and y direction.
        
    Returns:
        np.ndarray: Velocity for the robot in the global frame with `(x,y)^T`.
    '''
    
    # TODO 2c: Transform the relative velocity of the robot to the velocity in the global reference frame.
    #          Use the robots orientation and the implemented transform_to function.
    
    velocity_global = velocity

    return velocity_global

# ---- Not relevant for you ----

env = irsim.make("sheet_1.yaml", save_ani=False, full=False)

for _i in range(1000):
    env.step()
    env.render(0.05)
    env._env_plot.robot_pos = (env.get_robot_state()[0][0], env.get_robot_state()[1][0])
    if env.done():
        break

env.end(3)