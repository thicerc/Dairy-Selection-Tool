import numpy as np
import streamlit as st

# Fixed Comparison Matrix
comparison_matrix = np.array([
    [1.000000, 0.945398, 0.876990, 1.039451, 0.763224, 0.572779, 0.834711, 0.816712, 0.675585, 1.086022, 0.791123, 0.930876, 1.048443, 0.853521],
    [0.945398, 1.000000, 0.927641, 1.099485, 0.807305, 0.605860, 0.882920, 0.863881, 0.714604, 1.148746, 0.836815, 0.984639, 1.108997, 0.902817],
    [0.876990, 0.927641, 1.000000, 1.185249, 0.870277, 0.653119, 0.951791, 0.931267, 0.770346, 1.238351, 0.902089, 1.061444, 1.195502, 0.973239],
    [1.039451, 1.099485, 1.185249, 1.000000, 0.734257, 0.551040, 0.803030, 0.785714, 0.649944, 1.044803, 0.761097, 0.895545, 1.008651, 0.821127],
    [0.763224, 0.807305, 0.870277, 0.734257, 1.000000, 0.750473, 1.093664, 1.070081, 0.885173, 1.422939, 1.036554, 1.219662, 1.373702, 1.118310],
    [0.572779, 0.605860, 0.653119, 0.551040, 0.750473, 1.000000, 1.457300, 1.425876, 1.179487, 1.896057, 1.381201, 1.625192, 1.830450, 1.490141],
    [0.834711, 0.882920, 0.951791, 0.803030, 1.093664, 1.457300, 1.000000, 0.978437, 0.809365, 1.301075, 0.947781, 1.115207, 1.256055, 1.022535],
    [0.816712, 0.863881, 0.931267, 0.785714, 1.070081, 1.425876, 0.978437, 1.000000, 0.827202, 1.329749, 0.968668, 1.139785, 1.283737, 1.045070],
    [0.675585, 0.714604, 0.770346, 0.649944, 0.885173, 1.179487, 0.809365, 0.827202, 1.000000, 1.607527, 1.171018, 1.377880, 1.551903, 1.263380],
    [1.086022, 1.148746, 1.238351, 1.044803, 1.422939, 1.896057, 1.301075, 1.329749, 1.607527, 1.000000, 0.728460, 0.857143, 0.965398, 0.785915],
    [0.791123, 0.836815, 0.902089, 0.761097, 1.036554, 1.381201, 0.947781, 0.968668, 1.171018, 0.728460, 1.000000, 1.176651, 1.325260, 1.078873],
    [0.930876, 0.984639, 1.061444, 0.895545, 1.219662, 1.625192, 1.115207, 1.139785, 1.377880, 0.857143, 1.176651, 1.000000, 1.126298, 0.916901],
    [1.048443, 1.108997, 1.195502, 1.008651, 1.373702, 1.830450, 1.256055, 1.283737, 1.551903, 0.965398, 1.325260, 1.126298, 1.000000, 0.814085],
    [0.853521, 0.902817, 0.973239, 0.821127, 1.118310, 1.490141, 1.022535, 1.045070, 1.263380, 0.785915, 1.078873, 0.916901, 0.814085, 1.000000]
])

# Function to calculate Consistency Index (CI)
def calculate_consistency(matrix):
    # Calculate the eigenvalues and eigenvectors of the matrix
    eigenvalues, _ = np.linalg.eig(matrix)
    # The maximum eigenvalue (λ_max) is the largest eigenvalue
    lambda_max = max(eigenvalues)
    # CI formula: (λ_max - n) / (n - 1), where n is the size of the matrix
    n = matrix.shape[0]
    ci = (lambda_max - n) / (n - 1)
    return ci

# Function to get the Random Consistency Index (RI) based on matrix size (n)
def get_ri(n):
    # Predefined RI values for different matrix sizes
    ri_values = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45,
        10: 1.49, 11: 1.51, 12: 1.52, 13: 1.53, 14: 1.54
    }
    return ri_values.get(n, 1.54)  # Default value if n > 14

# Calculate Consistency Index (CI)
ci = calculate_consistency(comparison_matrix)
# Get the Random Consistency Index (RI) for the matrix size
ri = get_ri(len(comparison_matrix))
# Calculate Consistency Ratio (CR)
cr = ci / ri

# Check if the Consistency Ratio (CR) is acceptable
cr_message = "Consistency Ratio (CR) is acceptable." if cr < 0.10 else "Consistency Ratio (CR) is not acceptable."

# Display the results on the Streamlit interface
st.write("Consistency Check Results:")
st.write(f"Consistency Index (CI): {ci}")
st.write(f"Random Consistency Index (RI): {ri}")
st.write(f"Consistency Ratio (CR): {cr}")
st.write(cr_message)
