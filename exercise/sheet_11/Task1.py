"""
TASK 1
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import plotting as pltng


class ConstTurnModel:
    def __init__(self, init):
        # Arbitrary initialisation of state
        self.state = init
        self.sim_timestep = 0
        return
    
    def generate_next_sim_timestep(self):
        # Wrap the get next state function so self is not modifiable by accident
        self.state = ConstTurnModel.get_next_state(self.state, self.sim_timestep)
        self.sim_timestep += 1
        return
    
    @staticmethod
    def get_next_state(state, sim_timestep):
        """
        Task: Implement this function. 
        
        Available variables are:
        state - the previous state of the system in the form: 
            np.array([x_pos (m), x_vel (m/s), y_pos (m), y_vel (m/s)])
            where each element is a floating-point number (scalar value).
        sim_timestep - the previous integer time of the system

        Return value should be in the form: 
            np.array([x_pos (m), x_vel (m/s), y_pos (m), y_vel (m/s)])
            where each element is a floating-point number (scalar value).
        """
        
        # TODO Set model parameters
        w = 
        T = 
        Q = 

        # TODO Compute system matrix A
        A = 
        
        # TODO Compute next state plus multivariate Gaussian random vector
        next_state = 
        
        return next_state


class Predictor:
    def __init__(self, init):
        self.sim_timestep = 0
        self.est = init
        self.cov = np.zeros((4,4))
        return
    
    def get_prediction(self):
        # Wrap the predict function so self is not modifiable by accident
        self.est, self.cov = Predictor.predict(self.est, self.cov, self.sim_timestep)
        self.sim_timestep += 1
        return

    @staticmethod
    def predict(state, covariance, sim_timestep):
        """
        Task: Implement this function. 
        
        Available variables are:
        state - the prediction of the previous state of the system in the form: 
            np.array([x_pos (m), x_vel (m/s), y_pos (m), y_vel (m/s)])
            where each element is a floating-point number (scalar value).
        covariance - the error covariance of the prediction of the previous state of the system in the form:
            np.array([[x_11, x_12, x_13, x_14],
                      [x_21, x_22, x_23, x_24],
                      [x_31, x_32, x_33, x_34],
                      [x_41, x_42, x_43, x_44]])
            where each element is a floating-point number (scalar value).
        sim_timestep - the current integer time of the system

        Return value should be in the form: 
            (a, b)
            where a = np.array([x_pos (m), x_vel (m/s), y_pos (m), y_vel (m/s)])
            and   b = np.array([[x_11, x_12, x_13, x_14],
                                [x_21, x_22, x_23, x_24],
                                [x_31, x_32, x_33, x_34],
                                [x_41, x_42, x_43, x_44]])
            where each element is a floating-point number (scalar value).
        """
        # TODO Set model parameters
        w = 
        T = 
        Q = 

        # TODO Construct system matrix A
        A =
        
        # TODO Predict next state and compute the covariance
        state =
        covariance = 
        
        return state, covariance 


class Simulation:
    def __init__(self, init, monte_carlo_runs, sim_timesteps):
        # Save relevant variables
        self.gts = [ConstTurnModel(init) for _ in range(monte_carlo_runs)]
        self.pred = Predictor(init)
        self.tracks = monte_carlo_runs
        self.max_sim_timesteps = sim_timesteps
        return
    
    def run(self):
        # Create plot parameters
        fig = plt.figure()
        fig.set_size_inches(w=6,h=5)
        ax = fig.add_subplot(111)
        ax.set_title("Model Prediction and Error")
        ax.set_xlabel("x position")
        ax.set_ylabel("y position")
        arrow_scale = 0.3

        # Create legend here as the gradual building of lines doesn't work nicely with legend()
        pred_line = Line2D([0], [0], color='green', marker='.', linewidth=1)
        pred_vel_line = Line2D([0], [0], color='lightgreen', linewidth=1)
        sim_line = Line2D([0], [0], color='blue', marker='.', linewidth=1)
        sim_vel_line = Line2D([0], [0], color='lightblue', linewidth=1)
        fig.legend([pred_line, pred_vel_line, sim_line, sim_vel_line], ['Prediction', 'Prediction Velocity', 'Simulated Track', 'Simulated Track Velocity'])

        # Plot initial prediction
        prev_pred = self.pred.est
        ax.scatter(self.pred.est[0], self.pred.est[2], marker='.', color='green')
        ax.arrow(self.pred.est[0], self.pred.est[2], arrow_scale*self.pred.est[1], arrow_scale*self.pred.est[3], head_width=0.1, color='lightgreen', linewidth=1)

        # Plot predictions following the implemented predictor above
        for _ in range(self.max_sim_timesteps):
            self.pred.get_prediction()
            ax.scatter(self.pred.est[0], self.pred.est[2], marker='.', color='green')
            ax.plot([prev_pred[0], self.pred.est[0]], [prev_pred[2], self.pred.est[2]], linewidth=1, color='green')
            ax.arrow(self.pred.est[0], self.pred.est[2], arrow_scale*self.pred.est[1], arrow_scale*self.pred.est[3], head_width=0.1, color='lightgreen', linewidth=1)
            # Cvoariances are plotted at 2 standard deviations
            ellipse = pltng.get_cov_ellipse(np.array([[self.pred.cov[0][0], self.pred.cov[0][2]], 
                                                      [self.pred.cov[2][0], self.pred.cov[2][2]]]), 
                                            np.array([self.pred.est[0], self.pred.est[2]]), 
                                            2, fill=False, linestyle='-', edgecolor='green')
            ax.add_artist(ellipse)
            prev_pred = self.pred.est
            plt.pause(0.05)
        
        # Plot the initial simulated ground truths
        prev_gts = [gt.state for gt in self.gts]
        ax.scatter([x.state[0] for x in self.gts], [x.state[2] for x in self.gts], color='blue', marker='.', linewidth=1)
        for i in range(len(self.gts)):
            ax.arrow(self.gts[i].state[0], self.gts[i].state[2], arrow_scale*self.gts[i].state[1], arrow_scale*self.gts[i].state[3], head_width=0.1, color='lightblue', linewidth=1)
        
        # Plot all individual ground truth simulations
        for _ in range(self.max_sim_timesteps):
            for i in range(len(self.gts)):
                self.gts[i].generate_next_sim_timestep()
            ax.scatter([x.state[0] for x in self.gts], [x.state[2] for x in self.gts], color='blue', marker='.', linewidth=1)
            for i in range(len(self.gts)):
                ax.plot([prev_gts[i][0], self.gts[i].state[0]], [prev_gts[i][2], self.gts[i].state[2]], color='blue', linewidth=1)
                ax.arrow(self.gts[i].state[0], self.gts[i].state[2], arrow_scale*self.gts[i].state[1], arrow_scale*self.gts[i].state[3], head_width=0.1, color='lightblue', linewidth=1)
            
            prev_gts = [gt.state for gt in self.gts]
            plt.pause(0.02)
        plt.show()


# Run sim when running this file
if __name__ == "__main__":
    init = np.array([0,1,0,1])
    sim = Simulation(init, 10, 10)
    sim.run()








