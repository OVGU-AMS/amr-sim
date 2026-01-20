"""
TASK 2
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D
import plotting as pltng


class LinearConstVelModel:
    def __init__(self, init):
        # Arbitrary initialisation of state
        self.state = init
        self.sim_timestep = 0
        self.stateTransition = np.array([[1, 0.5, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0.5],[0, 0, 0, 1]])
        self.stateErrorCov = 0.01*np.array([[0.5**3/3,0.5**2/2,0,0],[0.5**2/2,0.5,0,0],[0,0,0.5**3/3,0.5**2/2],[0,0,0.5**2/2,0.5]])
        return
    
    def generate_next_sim_timestep(self):
        # Get the get next state
        self.state = self.stateTransition@self.state + np.random.multivariate_normal(np.zeros(4), self.stateErrorCov)
        self.sim_timestep += 1
        return


class PosSensor:
    def __init__(self):
        self.sim_timestep = 0
        return
    
    def get_measurement(self, gt_val):
        # Measure position according to a measurement model
        m = np.array([gt_val[0], gt_val[2]]) + np.random.multivariate_normal(np.zeros(2), 0.1*np.eye(2))
        self.sim_timestep += 1
        return m


class DistSensor:
    def __init__(self, position):
        self.sim_timestep = 0
        self.position = position
        return
    
    def get_measurement(self, gt_val):
        # Measure distance according to a measurement model using the saved sensors position
        d = np.linalg.norm(np.array([gt_val[0], gt_val[2]]) - self.position) + np.random.normal(0, 0.5)
        self.sim_timestep += 1
        return d


class KFEstimator:
    def __init__(self, init_est, init_cov):
        self.sim_timestep = 0
        self.state = init_est
        self.cov = init_cov
        return
    
    def get_estimate(self, measurement):
        # Wrap the estimate function so self is not modifiable by accident
        self.state, self.cov = KFEstimator.estimate(measurement, self.state, self.cov, self.sim_timestep)
        self.sim_timestep += 1
        return

    @staticmethod
    def estimate(measurement, state, covariance, sim_timestep):
        """
        Task: Implement this function. 
        
        Available variables are:
        measurement - the position measurement of the current state of the system in the form:
            np.array([x_pos (m), y_pos (m)])
            where each element is a floating-point number (scalar value).
        state - the previous estimated state of the system in the form: 
            np.array([x_pos (m), x_vel (m/s), y_pos (m), y_vel (m/s)])
            where each element is a floating-point number (scalar value).
        covariance - the error covariance of the previous estimated state of the system in the form:
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
        S = 
        T = 
        sigma_p = 

        # TODO Construct system matrix A and system noise covariance Q
        A = 
        Q = 

        # TODO Construct measurement matrix H and measurement noise matrix R
        H = 
        R = 

        # TODO Predict next state and covariance (prediction step)
        xp = 
        Pp =

        # TODO Compute Kalman gain
        K = 

        # TODO Incorporate measurement into predicted state and covariance (update step)
        xu = 
        Pu = 

        return xu, Pu


class EKFEstimator:
    def __init__(self, init_est, init_cov, sensor_positions):
        self.sim_timestep = 0
        self.state = init_est
        self.cov = init_cov
        self.positions = sensor_positions
        return
    
    def get_estimate(self, measurements):
        # Wrap the estimate function so self is not modifiable by accident
        self.state, self.cov = EKFEstimator.estimate(self.positions, measurements, self.state, self.cov, self.sim_timestep)
        self.sim_timestep += 1
        return

    @staticmethod
    def estimate(sensor_positions, measurements, state, covariance, sim_timestep):
        """
        Task: Implement this function. 
        
        Available variables are:
        sensor_positions - a list of positions of sensors in the form:
            [np.array([x_pos_1 (m), y_pos_1 (m)]), np.array([x_pos_1 (m), y_pos_1 (m)]), ..., np.array([x_pos_1 (m), y_pos_1 (m)])]
            where is element is an np.array, within which, each element is a floating-point number (scalar value).
        measurements - stacked measurement vector of distances from sensor positions to the current position of the state of the system in the form:
            np.array([dist_1 (m), dist_2 (m), ..., dist_n (m), y_pos_n (m)])
            where each element is a floating-point number (scalar value).
        state - the previous estimated state of the system in the form: 
            np.array([x_pos (m), x_vel (m/s), y_pos (m), y_vel (m/s)])
            where each element is a floating-point number (scalar value).
        covariance - the error covariance of the previous estimated state of the system in the form:
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
        return (np.array([0,1,0,1]), np.eye(4))
        raise NotImplementedError


class Simulation:
    def __init__(self, ground_truth_init, filter_state_init, filter_cov_init, dist_sensor_positions, sim_timesteps):
        # Save relevant variables
        self.gt = LinearConstVelModel(ground_truth_init)
        self.sensor_positions = dist_sensor_positions
        self.pos_sensor = PosSensor()
        self.dist_sensors = [DistSensor(p) for p in dist_sensor_positions]
        self.kf = KFEstimator(filter_state_init, filter_cov_init)
        self.ekf = EKFEstimator(filter_state_init, filter_cov_init, dist_sensor_positions)
        self.max_sim_timesteps = sim_timesteps
        return
    
    def run(self):
        # Create plot parameters
        fig = plt.figure()
        fig.set_size_inches(w=9,h=5)
        # KF plot
        ax_pos = fig.add_subplot(121)
        ax_pos.set_title("KF with Position Measurements")
        ax_pos.set_xlabel("x position")
        ax_pos.set_ylabel("y position")
        # EKF plot
        ax_dist = fig.add_subplot(122)
        ax_dist.set_title("EKF with Distance Measurements")
        ax_dist.set_xlabel("x position")
        ax_dist.set_ylabel("y position")
        # measurements and covariances make the plots too busy, remove them after each time step
        to_remove = []

        # Create legend here as the gradual building of lines doesn't work nicely with legend()
        pos_line = Line2D([0], [0], color='grey', marker='.', linewidth=1)
        sensor_line = Line2D([0], [0], color='red', linewidth=1, linestyle='None', marker='o')
        m_pos_line = Line2D([0], [0], color='lightgrey', linewidth=1, linestyle='None', marker='x')
        m_dist_line = Line2D([0], [0], color='lightgrey', linewidth=1, linestyle='-')
        est_line = Line2D([0], [0], color='green', marker='.', linewidth=1)
        fig.legend([pos_line, sensor_line, m_pos_line, m_dist_line, est_line], ['True Position', 'Distance Sensor', 'Position Measurement', 'Distance Measurement', 'Estimate'])

        # Plot initial positions, measurements and estimates
        m_pos = self.pos_sensor.get_measurement(self.gt.state)
        ms_dist = [s.get_measurement(self.gt.state) for s in self.dist_sensors]

        
        # GT and measurements
        ax_pos.scatter(self.gt.state[0], self.gt.state[2], marker='.', color='grey')
        ax_dist.scatter(self.gt.state[0], self.gt.state[2], marker='.', color='grey')
        to_remove.append(ax_pos.scatter(m_pos[0], m_pos[1], marker='x', color='lightgrey'))
        for i,d in enumerate(ms_dist):
            ax_dist.scatter(self.sensor_positions[i][0], self.sensor_positions[i][1], marker='o', color='red')
            e = Ellipse(xy=self.sensor_positions[i], width=2*d, height=2*d, angle=0, linestyle='-', edgecolor='lightgrey', fill=None)
            to_remove.append(e)
            ax_dist.add_artist(e)

        # Estimates
        ax_pos.scatter(self.kf.state[0], self.kf.state[2], marker='.', color='green')
        ax_dist.scatter(self.ekf.state[0], self.ekf.state[2], marker='.', color='green')
        # Covariances are plotted at 2 standard deviations
        ellipse = pltng.get_cov_ellipse(np.array([[self.kf.cov[0][0], self.kf.cov[0][2]], 
                                                  [self.kf.cov[2][0], self.kf.cov[2][2]]]), 
                                        np.array([self.kf.state[0], self.kf.state[2]]), 
                                        2, fill=False, linestyle='-', edgecolor='green')
        ax_pos.add_artist(ellipse)
        to_remove.append(ellipse)
        ellipse = pltng.get_cov_ellipse(np.array([[self.ekf.cov[0][0], self.ekf.cov[0][2]], 
                                                  [self.ekf.cov[2][0], self.ekf.cov[2][2]]]), 
                                        np.array([self.ekf.state[0], self.ekf.state[2]]), 
                                        2, fill=False, linestyle='-', edgecolor='green')
        ax_dist.add_artist(ellipse)
        to_remove.append(ellipse)

        # Save current states to draw line from them to next in next timestep
        prev_gt = self.gt.state
        prev_est_pos = self.kf.state
        prev_est_dist = self.ekf.state
        plt.pause(0.05)

        # Plot positions, measurements and estimates at each time
        for _ in range(self.max_sim_timesteps):
            # Clear cluttering components to be redrawn for next timestep
            for p in to_remove:
                p.remove()
            to_remove = []

            # generate and measure
            self.gt.generate_next_sim_timestep()
            m_pos = self.pos_sensor.get_measurement(self.gt.state)
            ms_dist = [s.get_measurement(self.gt.state) for s in self.dist_sensors]
            self.kf.get_estimate(m_pos)
            self.ekf.get_estimate(np.block(ms_dist))

            # Plot
            ax_pos.scatter(self.gt.state[0], self.gt.state[2], marker='.', color='grey')
            ax_dist.scatter(self.gt.state[0], self.gt.state[2], marker='.', color='grey')
            ax_pos.plot([prev_gt[0], self.gt.state[0]], [prev_gt[2], self.gt.state[2]], color='grey', linewidth=1)
            ax_dist.plot([prev_gt[0], self.gt.state[0]], [prev_gt[2], self.gt.state[2]], color='grey', linewidth=1)
            to_remove.append(ax_pos.scatter(m_pos[0], m_pos[1], marker='x', color='lightgrey'))
            for i,d in enumerate(ms_dist):
                ax_dist.scatter(self.sensor_positions[0], self.sensor_positions[1], marker='o', color='red')
                e = Ellipse(xy=self.sensor_positions[i], width=2*d, height=2*d, angle=0, linestyle='-', edgecolor='lightgrey', fill=None)
                to_remove.append(e)
                ax_dist.add_artist(e)
            ax_pos.scatter(self.kf.state[0], self.kf.state[2], marker='.', color='green')
            ax_pos.plot([prev_est_pos[0], self.kf.state[0]], [prev_est_pos[2], self.kf.state[2]], linewidth=1, color='green')
            ax_dist.scatter(self.ekf.state[0], self.ekf.state[2], marker='.', color='green')
            ax_dist.plot([prev_est_dist[0], self.ekf.state[0]], [prev_est_dist[2], self.ekf.state[2]], linewidth=1, color='green')
            # Covariances are plotted at 2 standard deviations
            ellipse = pltng.get_cov_ellipse(np.array([[self.kf.cov[0][0], self.kf.cov[0][2]], 
                                                      [self.kf.cov[2][0], self.kf.cov[2][2]]]), 
                                            np.array([self.kf.state[0], self.kf.state[2]]), 
                                            2, fill=False, linestyle='-', edgecolor='green')
            ax_pos.add_artist(ellipse)
            to_remove.append(ellipse)
            ellipse = pltng.get_cov_ellipse(np.array([[self.ekf.cov[0][0], self.ekf.cov[0][2]], 
                                                      [self.ekf.cov[2][0], self.ekf.cov[2][2]]]), 
                                            np.array([self.ekf.state[0], self.ekf.state[2]]), 
                                            2, fill=False, linestyle='-', edgecolor='green')
            ax_dist.add_artist(ellipse)
            to_remove.append(ellipse)

            # Save current as previous
            prev_gt = self.gt.state
            prev_est_pos = self.kf.state
            prev_est_dist = self.ekf.state
            plt.pause(0.05)
        plt.show()


# Run sim when running this file
if __name__ == "__main__":
    gt_init = np.array([0,1,0,1])
    filter_state_init = np.array([0,1,0,1])+np.random.multivariate_normal(np.zeros(4), 2+np.eye(4))
    filter_cov_init = 2+np.eye(4)
    sensor_positions = [np.array([-20, 0]),
                        np.array([0, -20]),
                        np.array([20, 0]),
                        np.array([0, 20])]
    sim = Simulation(gt_init, filter_state_init, filter_cov_init, sensor_positions, 20)
    sim.run()








