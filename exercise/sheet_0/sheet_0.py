import irsim

# env = irsim.make("keyboard_control_mpl.yaml", save_ani=False, full=False)
env = irsim.make("sheet_0.yaml", save_ani=False, full=False)

for _i in range(1000):
    env.step()
    env.render(0.05)
    env._env_plot.robot_pos = (env.get_robot_state()[0][0], env.get_robot_state()[1][0])
    if env.done():
        break

env.end(3)
