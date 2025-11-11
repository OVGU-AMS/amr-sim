import irsim
import numpy as np
from typing import List
import math


'''
EXERCISE SHEET 3

In this exercise we will implement the first estimation of the robots position, using the bicycle model,
discretized with the forward euler method. Because the model is not linear, we have to do a linearization
in every time step.
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
    
    R = np.array([[math.cos(a), - math.sin(a),0],
                  [math.sin(a), math.cos(a),0],
                  [0,0,1]])
    
    x_transformed = t + R @ x
    
    return x_transformed

def linearize_bicycle(robot_velocity: float, robot_steering_angle: float):
    '''Calculates a velocity vector in the robots coordinate frame, using the forward velocity and the steering angle.

    Args:
        robot_velocity (float): Forward velocity of the robot in the robot coordinate frame.
        robot_steering_angle (float): Steering angle of the robot.

    Returns:
        np.ndarray: Velocity vector in the new coordinate frame with `(x_dot,y_dot,a_dot)^T` where `x_dot, y_dot` are the linear velocities 
            in the robot coordinate frame and `a_dot` the angular velocity.
    '''
    
    # TODO 2a: Construct the velocity vector of the robot, using bicycle the motion model
    
    robot_velocity_vector = np.array([0,0,0])
    
    return robot_velocity_vector

def propagate(robot_velocity: float, robot_steering_angle: float, previous_estimation: np.ndarray, time_step: float):
    '''Propagates the robots position estimation forward by the movement input and the time step of the simulation.

    Args:
        robot_velocity (float): Forward velocity of the robot in the robot coordinate frame.
        robot_steering_angle (float): Steering angle of the robot.
        previous_estimation (np.ndarray): Previous pose estimation as vector with `(x,y,a)^T` where `x, y` are the position 
            and `a` the heading in the global coordinate frame.
        time_step (float): Time which passed since the last pose propagation was executed.
        
    Returns:
       np.ndarray: Propagated pose of the robot with `(x,y,a)^T`, where `x, y` are the position 
            and `a` the heading in the global coordinate frame.
    '''
    
    # TODO 2b: Propagate the robots pose estimation one time step into the future. First, create a linear velocity vector
    #          by using the linearize_bicycle function. Then transform the velocity to the global coordinate frame and calculate
    #          the new position estimation.

    new_estimation = previous_estimation
    return new_estimation



# ---- Not relevant for you ----



env = irsim.make("sheet_3.yaml", save_ani=False, full=False)

lines = [[1/25, 0, 'blue'],
         [25, 0, 'red'],
         [-1/25, 50, 'green'],
         [25,- 25*48, 'purple']
]

env._env_plot.init_lidar_lines(4)
env._env_plot.init_side_box()

estimated_pos = np.array([5.0,5.0,0.0])
for _i in range(1000):
    env.step()
    env.render(0.05)
    env._env_plot.robot_pos = (env.get_robot_state()[0][0], env.get_robot_state()[1][0])
    estimated_pos = propagate(env.get_robot_info().current_velocity.flatten()[0],env.get_robot_state()[3][0], estimated_pos,0.1)
    env._env_plot.estimation_pos = estimated_pos
    print(env.get_robot_state())
    if env.done():
        break

env.end(3)