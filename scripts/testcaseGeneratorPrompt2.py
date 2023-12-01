import random


def calculate_traffic_coefficient(
    vehicles, cycles_waited, pedestrians, cycles_pedestrians_wait
):
    return vehicles * (cycles_waited + 1) + (pedestrians / 4) * (
        cycles_pedestrians_wait + 1
    )


def generate_random_traffic_conditions():
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


def combine_lane_pairs(directions_data):
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


def decide_signal_to_open(directions_data, combined_lane_pairs):
    # Check for emergency vehicles
    for direction, conditions in directions_data.items():
        if (
            conditions["emergency_vehicles_through_right"] > 0
            or conditions["emergency_vehicles_left"] > 0
        ):
            return f"Emergency: Open {direction}"

    # Decide based on traffic coefficients
    max_coefficient = -1
    signal_to_open = None
    for lane_pair, vehicles in combined_lane_pairs.items():
        traffic_coefficient = calculate_traffic_coefficient(
            vehicles, 1, 0, 0
        )  # Simplified for this example
        if traffic_coefficient > max_coefficient:
            max_coefficient = traffic_coefficient
            signal_to_open = lane_pair

    return signal_to_open


def decide_signal_to_open_round_robin(directions_data):
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


def simulate_traffic_scenario():
    directions = ["North", "South", "East", "West"]
    scenario = {
        direction: generate_random_traffic_conditions() for direction in directions
    }
    combined_lane_pairs = combine_lane_pairs(scenario)
    decision = decide_signal_to_open(scenario, combined_lane_pairs)
    round_robin_decision = decide_signal_to_open_round_robin(scenario)

    return scenario, combined_lane_pairs, decision, round_robin_decision


def create_prompt(scenario):
    prompt = "Consider a traffic control scenario at a four-way intersection. The traffic conditions are as follows:\n\n"

    for direction, data in scenario.items():
        prompt += f"- {direction} Direction: {data['vehicles_through_right']} vehicles for through/right, {data['vehicles_left']} vehicles for left, {data['cycles_waited_through_right']} cycle wait for through/right, {data['cycles_waited_left']} cycles wait for left, {data['pedestrians_parallel']} pedestrians waiting, {data['cycles_pedestrians_wait']} cycles wait since last pedestrian, {data['emergency_vehicles_through_right']} emergency vehicles for through/right, {data['emergency_vehicles_left']} emergency vehicles for left.\n"

    prompt += "\nBased on these conditions, which direction should be prioritized for the next signal change to optimize traffic flow, considering vehicle and pedestrian wait times, counts, and the presence of emergency vehicles?"

    return prompt


# Generate a traffic scenario
traffic_scenario = simulate_traffic_scenario()[0]

# Create a prompt based on the generated scenario


# # Generate a test case
test_case, combined_lane_pairs, decision, round_robin = simulate_traffic_scenario()
# print("Test Case Traffic Conditions:")
# for direction, conditions in test_case.items():
#     print(f"{direction}: {conditions}")

print("\nCombined Lane Pairs Traffic Conditions:")
for lane_pair, vehicles in combined_lane_pairs.items():
    print(f"{lane_pair}: {vehicles} vehicles")


prompt = create_prompt(test_case)
print(prompt)

print("\nDecision:", decision)

print("\nRound Robin Decision:", round_robin)

# generate for round robin case
