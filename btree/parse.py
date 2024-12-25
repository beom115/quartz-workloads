import re

# Input data
with open('list-result.txt') as f:
	data = f.read()


# Parsing function
def parse_to_list(data):
    iterations = []
    current_iteration = {}

    for line in data.splitlines():
        if line.startswith("== Iteration"):
            if current_iteration:
                iterations.append(current_iteration)  # Save previous iteration
            current_iteration = {}  # Start a new iteration
        elif "Thread id" in line:
            match = re.search(r"\[(\d+)\]", line)
            if match:
                current_iteration['thread_id'] = int(match.group(1))
        elif ":" in line:
            _, key, value = map(str.strip, line.split(":", 2))
            key = key.replace(" ", "_").lower()
            try:
                value = int(value.split()[0])  # Extract numeric value
            except ValueError:
                pass  # Keep as string if not a number
            current_iteration[key] = value

    if current_iteration:  # Add the last iteration
        iterations.append(current_iteration)

    return iterations

# Parse the data
parsed_list = parse_to_list(data)

# Print the result
import pprint
pprint.pprint(parsed_list)

import pandas as pd

df = pd.DataFrame(parsed_list)
df.to_csv('parsed-result.csv')
