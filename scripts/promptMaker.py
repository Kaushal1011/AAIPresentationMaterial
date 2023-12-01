import os


def parse_traffic_data(data):
    """
    Parses the traffic data from the input format into a human-readable description.
    """
    # Splitting the data into different lines
    lines = data.split("\n")

    # Extracting the time of the day
    time_of_day = lines[0]

    # Parsing data for each direction
    directions = ["North", "South", "East", "West"]
    direction_data = {}
    for i, direction in enumerate(directions):
        start_index = 1 + i * 8
        direction_info = {
            "vehicles_through_right": lines[start_index],
            "vehicles_left": lines[start_index + 1],
            "wait_through_right": lines[start_index + 2],
            "wait_left": lines[start_index + 3],
            "pedestrians": lines[start_index + 4],
            "wait_pedestrians": lines[start_index + 5],
            "emergency_through_right": lines[start_index + 6],
            "emergency_left": lines[start_index + 7],
        }
        direction_data[direction] = direction_info

    return time_of_day, direction_data


def create_prompt(time_of_day, direction_data):
    """
    Creates a prompt for the language model based on the parsed traffic data.
    """
    prompt = f"Consider a traffic control scenario at a four-way intersection in an urban area at {time_of_day[:2]}:{time_of_day[2:]} AM. The traffic conditions are as follows:\n\n"

    for direction, data in direction_data.items():
        prompt += f"- {direction} Direction: {data['vehicles_through_right']} vehicles for through/right, {data['vehicles_left']} vehicles for left, {data['wait_through_right']} cycle wait for through/right, {data['wait_left']} cycles wait for left, {data['pedestrians']} pedestrians waiting, {data['wait_pedestrians']} cycles wait since last pedestrian, {data['emergency_through_right']} emergency vehicles for through/right, {data['emergency_left']} emergency vehicles for left.\n"

    prompt += "\nGiven these conditions and the operational principles of an actuated traffic signal control system, answer the following questions:\n\n1. Which direction should be prioritized for the next signal change, considering vehicle and pedestrian wait times and counts?\n2. Are there any specific lanes within these directions that should be given priority based on the current traffic conditions?\n3. Given the low traffic volume typical of this time of night, should the signal timing be adjusted to reduce wait times for vehicles and pedestrians?\n4. Are there any additional considerations or suggestions for traffic management in this scenario, based on the provided data?"

    return prompt


def load_and_parse_file(file_path):
    """
    Loads a file from the given path and parses the traffic data.
    """
    with open(file_path, "r") as file:
        data = file.read()

    time_of_day, direction_data = parse_traffic_data(data)
    return create_prompt(time_of_day, direction_data)


# Specify the file path
file_path = "./tests/normaltrafficscenario.txt"

# Check if the file exists
if os.path.exists(file_path):
    # Load and parse the file, then create the prompt
    prompt = load_and_parse_file(file_path)
    print(prompt)
else:
    prompt = "File not found."
    print(prompt)
