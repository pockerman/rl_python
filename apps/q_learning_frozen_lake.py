"""
Train a Q-learning agent on Frozen Lake
"""
import gym
from tensorboardX import SummaryWriter
from algorithms.q_learning import QLearning
from algorithms.algorithm_base import TrainMode


class Agent(QLearning):

    def __init__(self, env_name: str, gamma: float,
                 eta: float, n_max_itrs: int, use_action_with_greedy_method: bool) -> None:
        super(Agent, self).__init__(env=gym.make(env_name),
                                    gamma=gamma, eta=eta, use_decay=False,
                                    use_action_with_greedy_method=use_action_with_greedy_method,
                                    n_max_iterations=n_max_itrs, tolerance=1.0e-10,
                                    train_mode=TrainMode.STOCHASTIC)

    def play_episode(self, test_env):
        total_reward = 0.0
        state = test_env.reset()
        while True:
            _, action = self.best_value_and_action(state)
            new_state, reward, is_done, _ = test_env.step(action)
            total_reward += reward
            if is_done:
                break
            state = new_state
        return total_reward


if __name__ == '__main__':

    TEST_EPISODES = 20
    GAMMA = 0.9
    ETA = 0.2
    ENV_NAME = "FrozenLake-v0"

    test_env = gym.make(ENV_NAME)
    writer = SummaryWriter(comment="-q-learning")
    agent = Agent(env_name=ENV_NAME,
                  gamma=0.9, eta=ETA, n_max_itrs=20,
                  use_action_with_greedy_method=False)

    agent.reset()

    iter_no = 0
    best_reward = 0.0

    while True:

        iter_no += 1

        # step the agent in the environment
        agent.one_episode_iteration()

        reward = 0.0
        for tepisode in range(TEST_EPISODES):
            reward += agent.play_episode(test_env=test_env)
        reward /= TEST_EPISODES

        writer.add_scalar("reward", reward, iter_no)

        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))
            best_reward = reward

        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            break

    writer.close()