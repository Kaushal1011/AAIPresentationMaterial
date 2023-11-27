import random


def generate_traffic_scenario():
    """
    Generates a random traffic scenario based on the given rules and calculates the traffic coefficient.
    Returns the scenario data and the decision on which signal to open.
    """
    # Randomly generate time of day
    time_of_day = f"{random.randint(0, 23):02d}{random.randint(0, 59):02d}"

    # Traffic properties for each direction
    directions = ["North", "South", "East", "West"]
    traffic_data = {}
    for direction in directions:
        traffic_data[direction] = {
            "vehicles_through_right": random.randint(0, 20),
            "vehicles_left": random.randint(0, 10),
            "wait_through_right": random.randint(0, 5),
            "wait_left": random.randint(0, 5),
            "pedestrians": random.randint(0, 10),
            "wait_pedestrians": random.randint(0, 5),
            "emergency_through_right": random.randint(0, 1),
            "emergency_left": random.randint(0, 0),
        }

    # Calculate traffic coefficient for each direction
    traffic_coefficients = {}
    for direction, data in traffic_data.items():
        coef = (
            data["vehicles_through_right"] * data["wait_through_right"]
            + data["vehicles_left"] * data["wait_left"]
            + data["pedestrians"] * data["wait_pedestrians"]
        )
        traffic_coefficients[direction] = coef

    # Determine which signal to open based on traffic coefficient and emergency vehicles
    max_coef = -1
    signal_to_open = ""
    for direction, coef in traffic_coefficients.items():
        if (
            traffic_data[direction]["emergency_through_right"] > 0
            or traffic_data[direction]["emergency_left"] > 0
        ):
            signal_to_open = f"Emergency: Open {direction}"
            break
        if coef > max_coef:
            max_coef = coef
            signal_to_open = direction

    return time_of_day, traffic_data, signal_to_open


# Generate multiple test cases
test_cases = [generate_traffic_scenario() for _ in range(5)]

print(test_cases)
