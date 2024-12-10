import re
import numpy as np

def process_coefficients(filename):
    coefficients = {"chase": [], "choose": [], "align": [], "cohesion": []}
    
    with open(filename, 'r') as file:
        for line in file:
            # Check if the line contains coefficients (ignore header lines)
            if "chase" in line and "choose" in line and "align" in line and "cohesion" in line:
                parts = line.strip().split()
                # Extract specific coefficients by their positions in the line
                coefficients["chase"].append(float(parts[5]))
                coefficients["choose"].append(float(parts[8]))
                coefficients["align"].append(float(parts[11]))
                coefficients["cohesion"].append(float(parts[14]))
    
    # Calculate mean and standard deviation for each coefficient
    stats = {}
    for key, values in coefficients.items():
        values_array = np.array(values)
        stats[key] = {
            "mean": np.mean(values_array),
            "std_dev": np.std(values_array)
        }
    
    return stats

# Example usage
stats = process_coefficients('kills.txt')
for coef, stat in stats.items():
    print(f"{coef.capitalize()} -> Mean: {stat['mean']:.5f}, Standard Deviation: {stat['std_dev']:.5f}")
