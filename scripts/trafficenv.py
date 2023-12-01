import gymnasium as gym
import random


class TrafficSignalEnv(gym.Env):
    def __init__(self, mode="normal"):
        super(TrafficSignalEnv, self).__init__()
        self.mode = mode
        # Assuming a discrete action space with 4 actions: North, South, East, West
        # or NS-TR, NS-L, EW-TR, EW-L
        self.action_space = gym.spaces.Discrete(4)
        # State space can be represented in various ways, this is a simple example
        self.observation_space = gym.spaces.Dict(
            {
                "North": gym.spaces.Dict(
                    {
                        "vehicles_through_right": gym.spaces.Discrete(8),
                        "vehicles_left": gym.spaces.Discrete(11),
                        "cycles_waited_through_right": gym.spaces.Discrete(6),
                        "cycles_waited_left": gym.spaces.Discrete(6),
                        "pedestrians_parallel": gym.spaces.Discrete(11),
                        "cycles_pedestrians_wait": gym.spaces.Discrete(6),
                        "emergency_vehicles_through_right": gym.spaces.Discrete(1),
                        "emergency_vehicles_left": gym.spaces.Discrete(1),
                    }
                ),
                "South": gym.spaces.Dict(
                    {
                        "vehicles_through_right": gym.spaces.Discrete(8),
                        "vehicles_left": gym.spaces.Discrete(11),
                        "cycles_waited_through_right": gym.spaces.Discrete(6),
                        "cycles_waited_left": gym.spaces.Discrete(6),
                        "pedestrians_parallel": gym.spaces.Discrete(11),
                        "cycles_pedestrians_wait": gym.spaces.Discrete(6),
                        "emergency_vehicles_through_right": gym.spaces.Discrete(1),
                        "emergency_vehicles_left": gym.spaces.Discrete(1),
                    }
                ),
                "East": gym.spaces.Dict(
                    {
                        "vehicles_through_right": gym.spaces.Discrete(8),
                        "vehicles_left": gym.spaces.Discrete(11),
                        "cycles_waited_through_right": gym.spaces.Discrete(6),
                        "cycles_waited_left": gym.spaces.Discrete(6),
                        "pedestrians_parallel": gym.spaces.Discrete(11),
                        "cycles_pedestrians_wait": gym.spaces.Discrete(6),
                        "emergency_vehicles_through_right": gym.spaces.Discrete(1),
                        "emergency_vehicles_left": gym.spaces.Discrete(1),
                    }
                ),
                "West": gym.spaces.Dict(
                    {
                        "vehicles_through_right": gym.spaces.Discrete(8),
                        "vehicles_left": gym.spaces.Discrete(11),
                        "cycles_waited_through_right": gym.spaces.Discrete(6),
                        "cycles_waited_left": gym.spaces.Discrete(6),
                        "pedestrians_parallel": gym.spaces.Discrete(11),
                        "cycles_pedestrians_wait": gym.spaces.Discrete(6),
                        "emergency_vehicles_through_right": gym.spaces.Discrete(1),
                        "emergency_vehicles_left": gym.spaces.Discrete(1),
                    }
                ),
            }
        )

    def reset(self):
        self.state = self._generate_traffic_scenario()
        return self.state

    def step(self, action):
        correct_decision = self._decide_signal(action)
        reward = 1 if action == correct_decision else 0
        done = True
        return self.state, reward, done, {}

    def render(self, mode="human"):
        # Rendering logic (optional)
        pass

    def _generate_random_traffic_conditions(self):
        return {
            "vehicles_through_right": random.randint(0, 7),
            "vehicles_left": random.randint(0, 10),
            "cycles_waited_through_right": random.randint(0, 5),
            "cycles_waited_left": random.randint(0, 5),
            "pedestrians_parallel": random.randint(0, 10),
            "cycles_pedestrians_wait": random.randint(0, 5),
            "emergency_vehicles_through_right": 0,
            "emergency_vehicles_left": 0,
        }

    def _generate_traffic_scenario(self):
        directions = ["North", "South", "East", "West"]
        scenario = {
            direction: self._generate_random_traffic_conditions()
            for direction in directions
        }
        return scenario

    def _decide_signal(self, action):
        if self.mode == "normal":
            combined_lane_pairs = self._combine_lane_pairs(self.state)
            decision = self._decide_signal_normal(self.state, combined_lane_pairs)
            print(f"Decision: {decision}")
            action_map = {"NS-TR": 0, "NS-L": 1, "EW-TR": 2, "EW-L": 3}
            return action_map.get(decision)
        elif self.mode == "round_robin":
            decision = self._decide_signal_round_robin(self.state)
            print(f"Decision: {decision}")
            action_map = {"North": 0, "South": 1, "East": 2, "West": 3}
            return action_map.get(decision)
        else:
            raise ValueError("Invalid mode")

    def _decide_signal_normal(self, directions_data, combined_lane_pairs):
        # Check for emergency vehicles
        # for direction, conditions in directions_data.items():
        #     if (
        #         conditions["emergency_vehicles_through_right"] > 0
        #         or conditions["emergency_vehicles_left"] > 0
        #     ):
        #         return f"Emergency: Open {direction}"

        # Decide based on traffic coefficients
        max_coefficient = -1
        signal_to_open = None
        for lane_pair, vehicles in combined_lane_pairs.items():
            traffic_coefficient = self._calculate_traffic_coefficient(
                vehicles, 1, 0, 0
            )  # Simplified for this example
            if traffic_coefficient > max_coefficient:
                max_coefficient = traffic_coefficient
                signal_to_open = lane_pair

        return signal_to_open

    def _decide_signal_round_robin(self, directions_data):
        max_coef = -1
        signal_to_open = None
        traffic_coefficients = {}
        for direction, data in directions_data.items():
            coef = (
                data["vehicles_through_right"] * data["cycles_waited_through_right"]
                + data["vehicles_left"] * data["cycles_waited_left"]
                + data["pedestrians_parallel"] * data["cycles_pedestrians_wait"]
            )
            traffic_coefficients[direction] = coef

        for direction, coef in traffic_coefficients.items():
            if (
                directions_data[direction]["emergency_vehicles_through_right"] > 0
                or directions_data[direction]["emergency_vehicles_left"] > 0
            ):
                signal_to_open = f"Emergency: Open {direction}"
                break
            if coef > max_coef:
                max_coef = coef
                signal_to_open = direction

        return signal_to_open

    def _combine_lane_pairs(self, directions_data):
        # Combine North-South and East-West lane pairs
        ns_through_right = (
            directions_data["North"]["vehicles_through_right"]
            + directions_data["South"]["vehicles_through_right"]
        )
        ns_left = (
            directions_data["North"]["vehicles_left"]
            + directions_data["South"]["vehicles_left"]
        )
        ew_through_right = (
            directions_data["East"]["vehicles_through_right"]
            + directions_data["West"]["vehicles_through_right"]
        )
        ew_left = (
            directions_data["East"]["vehicles_left"]
            + directions_data["West"]["vehicles_left"]
        )

        combined = {
            "NS-TR": ns_through_right,
            "NS-L": ns_left,
            "EW-TR": ew_through_right,
            "EW-L": ew_left,
        }
        return combined

    def _calculate_traffic_coefficient(
        self, vehicles, cycles_waited, pedestrians, cycles_pedestrians_wait
    ):
        return vehicles * (cycles_waited + 1) + (pedestrians / 4) * (
            cycles_pedestrians_wait + 1
        )


if __name__ == "__main__":
    # Testing the environment in 'normal' mode
    print("Testing in 'normal' mode:")
    env = TrafficSignalEnv(mode="normal")
    for _ in range(5):  # Run 5 test cases
        state = env.reset()
        action = env.action_space.sample()  # Random action
        next_state, reward, done, info = env.step(action)
        print(f"State: {state}, Action: {action}, Reward: {reward}, Done: {done}")

    # Testing the environment in 'round_robin' mode
    print("\nTesting in 'round_robin' mode:")
    env = TrafficSignalEnv(mode="round_robin")
    for _ in range(5):  # Run 5 test cases
        state = env.reset()
        action = env.action_space.sample()  # Random action
        next_state, reward, done, info = env.step(action)
        print(f"State: {state}, Action: {action}, Reward: {reward}, Done: {done}")
