# Simulator for AMR Lecture

For the exercise of the AMR lecture, this simulator is used to visualize the learned algorithms and provide a practical implementation.

## Prerequisite

- Python: >= 3.9

## Installation

```
git clone https://github.com/OVGU-AMS/amr-sim.git
cd ir-sim   
pip install -e .  
```

Base on IR-SIM:

# Intelligent Robot Simulator (IR-SIM)

**Documentation:** [https://ir-sim.readthedocs.io/en](https://ir-sim.readthedocs.io/en)

**IR-SIM** is an open-source, Python-based, lightweight robot simulator designed for navigation, control, and AI learning. It provides a simple, user-friendly framework with built-in collision detection for modeling robots, sensors, and environments. Ideal for academic and educational use, IR-SIM enables rapid prototyping of robotics and AI algorithms in custom scenarios with minimal coding and hardware requirements.

## Features

- Simulate robot platforms with diverse kinematics, sensors, and behaviors  ([support](#support)). 
- Quickly configure and customize scenarios using straightforward YAML files. No complex coding required.
- Visualize simulation outcomes using a naive visualizer matplotlib for immediate debugging.
- Support collision detection and behavior control for each object.

## Usage

### Quick Start

```python

import irsim

env = irsim.make('robot_world.yaml') # initialize the environment with the configuration file

for i in range(300): # run the simulation for 300 steps

    env.step()  # update the environment
    env.render() # render the environment

    if env.done(): break # check if the simulation is done
        
env.end() # close the environment
```

YAML Configuration: robot_world.yaml

```yaml

world:
  height: 10  # the height of the world
  width: 10   # the width of the world
  step_time: 0.1  # 10Hz calculate each step
  sample_time: 0.1  # 10 Hz for render and data extraction 
  offset: [0, 0] # the offset of the world on x and y 

robot:
  kinematics: {name: 'diff'}  # omni, diff, acker
  shape: {name: 'circle', radius: 0.2}  # radius
  state: [1, 1, 0]  # x, y, theta
  goal: [9, 9, 0]  # x, y, theta
  behavior: {name: 'dash'} # move toward to the goal directly 
  color: 'g' # green
```

### Advanced Usage

The advanced usages are listed in the [usage](https://github.com/hanruihua/ir-sim/tree/main/usage)

## Acknowledgement

- [IR-Sim](https://github.com/hanruihua/ir-sim)
- [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics)






