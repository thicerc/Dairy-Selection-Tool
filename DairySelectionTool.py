import pandas as pd 
import numpy as np
import streamlit as st

# Define the sub-criteria and normalized weights
subcriteria = {
    'Economic': [
        'Accessibility of financial resources',
        'Type and frequency of financial incentives',
        'Duration of stable pricing periods',
        'Competitiveness of exclusive price',
        'Ratio of price adjustments to quality',
        'Transparency of council-defined pricing',
        'Impact of international price fluctuations',
        'Benefit of exclusivity for long-term partnerships'
    ],
    'Social': [
        'Frequency and quality of technical visits',
        'Length and flexibility of contract terms',
        'Penalties or rewards for delivery schedules'
    ],
    'Production': [
        'Consistency in daily milk production',
        'Adherence to quality standards',
        'Economic viability of collection for different volumes'
    ]
}

normalized_weights = {
    'Accessibility of financial resources': 0.0606,
    'Type and frequency of financial incentives': 0.0641,
    'Duration of stable pricing periods': 0.0691,
    'Competitiveness of exclusive price': 0.0583,
    'Ratio of price adjustments to quality': 0.0794,
    'Transparency of council-defined pricing': 0.1058,
    'Impact of international price fluctuations': 0.0726,
    'Benefit of exclusivity for long-term partnerships': 0.0742,
    'Frequency and quality of technical visits': 0.0897,
    'Length and flexibility of contract terms': 0.0558,
    'Penalties or rewards for delivery schedules': 0.0766,
    'Consistency in daily milk production': 0.0651,
    'Adherence to quality standards': 0.0578,
    'Economic viability of collection for different volumes': 0.0710
}

import numpy as np

# Pairwise comparison matrix provided
comparison_matrix = np.array([
    [1.0, 0.94539782, 0.87698987, 1.03945111, 0.76322418, 0.57277883, 0.83471074, 0.81671159, 0.67558528, 1.08602151, 0.79112272, 0.93087558, 1.04844291, 0.85352113],
    [1.05775578, 1.0, 0.9276411, 1.09948542, 0.80730479, 0.60586011, 0.88292011, 0.8638814, 0.71460424, 1.14874552, 0.83681462, 0.98463902, 1.10899654, 0.9028169],
    [1.14026403, 1.07800312, 1.0, 1.18524871, 0.87027708, 0.65311909, 0.95179063, 0.93126685, 0.7703456, 1.23835125, 0.90208877, 1.06144393, 1.19550173, 0.97323944],
    [0.9620462, 0.90951638, 0.84370478, 1.0, 0.73425693, 0.5510397, 0.8030303, 0.78571429, 0.64994426, 1.04480287, 0.76109661, 0.89554531, 1.00865052, 0.82112676],
    [1.31023102, 1.23868955, 1.14905933, 1.3619211, 1.0, 0.75047259, 1.09366391, 1.07008086, 0.8851728, 1.42293907, 1.03655352, 1.21966206, 1.37370242, 1.11830986],
    [1.74587459, 1.65054602, 1.53111433, 1.81475129, 1.3324937, 1.0, 1.45730028, 1.42587601, 1.17948718, 1.89605735, 1.38120104, 1.62519201, 1.83044983, 1.49014085],
    [1.1980198, 1.1326053, 1.05065123, 1.24528302, 0.91435768, 0.68620038, 1.0, 0.97843666, 0.80936455, 1.30107527, 0.94778068, 1.11520737, 1.25605536, 1.02253521],
    [1.22442244, 1.1575663, 1.07380608, 1.27272727, 0.93450882, 0.70132325, 1.02203857, 1.0, 0.82720178, 1.3297491, 0.96866841, 1.13978495, 1.28373702, 1.04507042],
    [1.48019802, 1.39937598, 1.29811867, 1.53859348, 1.12972292, 0.84782609, 1.23553719, 1.20889488, 1.0, 1.60752688, 1.17101828, 1.37788018, 1.55190311, 1.26338028],
    [0.92079208, 0.87051482, 0.80752533, 0.95711835, 0.70277078, 0.52741021, 0.76859504, 0.75202156, 0.62207358, 1.0, 0.72845953, 0.85714286, 0.96539792, 0.78591549],
    [1.2640264, 1.1950078, 1.10853835, 1.31389365, 0.96473552, 0.72400756, 1.05509642, 1.03234501, 0.85395764, 1.37275986, 1.0, 1.17665131, 1.32525952, 1.07887324],
    [1.07425743, 1.01560062, 0.94211288, 1.11663808, 0.81989924, 0.61531191, 0.89669421, 0.87735849, 0.72575251, 1.16666667, 0.84986945, 1.0, 1.12629758, 0.91690141],
    [0.95379538, 0.90171607, 0.83646889, 0.99142367, 0.7279597, 0.5463138, 0.79614325, 0.77897574, 0.64437012, 1.03584229, 0.75456919, 0.88786482, 1.0, 0.81408451],
    [1.17161716, 1.10764431, 1.02749638, 1.21783877, 0.89420655, 0.6710775, 0.97796143, 0.95687332, 0.79152731, 1.27240143, 0.92689295, 1.0906298, 1.2283737, 1.0]
])

# Step 1: Calculate the largest eigenvalue (λ_max)
# To do this, we calculate the eigenvector of the matrix and then find the largest ratio between the matrix-vector multiplication and the vector itself.
eigenvalues, _ = np.linalg.eig(comparison_matrix)
lambda_max = max(eigenvalues)

# Step 2: Calculate the Consistency Index (CI)
n = comparison_matrix.shape[0]  # Number of criteria
CI = (lambda_max - n) / (n - 1)

# Step 3: Calculate the Random Consistency Index (RI) for n = 14 (matrix size)
# RI values based on AHP tables for matrices of size 14
RI_values = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.54, 13: 1.56, 14: 1.57}
RI = RI_values[n]  # For n=14, the RI is 1.57

# Step 4: Calculate the Consistency Ratio (CR)
CR = CI / RI

# Step 5: Display the results
print(f'Largest eigenvalue (λ_max): {lambda_max}')
print(f'Consistency Index (CI): {CI}')
print(f'Random Consistency Index (RI): {RI}')
print(f'Consistency Ratio (CR): {CR}')

# Check if the CR is acceptable
if CR < 0.1:
    print("The Consistency Ratio is acceptable.")
else:
    print("The Consistency Ratio is not acceptable.")


# Function to create example file
def create_example_file():
    num_producers = 100
    producers = [f"Producer {i+1}" for i in range(num_producers)]
    data = {
        'Producer': producers
    }

    for subcriterion in normalized_weights.keys():
        data[subcriterion] = np.random.randint(0, 11, size=num_producers)

    example_df = pd.DataFrame(data)
    example_df.to_csv("example_input.csv", index=False)
    return "example_input.csv"

# Function to get user input for scores
def get_user_input():
    data = []
    upload_file = st.file_uploader("Upload producer data (CSV or Excel):", type=["csv", "xlsx"])

    if upload_file:
        # Process uploaded file
        if upload_file.name.endswith('.csv'):
            uploaded_data = pd.read_csv(upload_file)
        else:
            uploaded_data = pd.read_excel(upload_file)

        for index, row in uploaded_data.iterrows():
            for subcriterion in normalized_weights.keys():
                data.append({
                    'Producer': row['Producer'],
                    'Subcriterion': subcriterion,
                    'Score': row[subcriterion]
                })
    else:
        # Manual input
        num_producers = st.number_input("Enter the number of producers (1-1000):", min_value=1, max_value=1000, value=3, step=1)
        producers = [f'Producer {i+1}' for i in range(num_producers)]

        for producer_idx, producer in enumerate(producers):
            st.header(f"Input data for {producer}")
            for criterion, subs in subcriteria.items():
                st.subheader(criterion)
                for sub_idx, sub in enumerate(subs):
                    score = st.number_input(
                        f"{sub}:",
                        min_value=0, max_value=10, value=5, step=1, format="%d",
                        key=f"{producer_idx}_{criterion}_{sub_idx}"
                    )
                    data.append({
                        'Producer': producer,
                        'Subcriterion': sub,
                        'Score': score
                    })

    return data

# Function to display the results
def display_results(data):
    scores_df = pd.DataFrame(data)
    weights_df = pd.DataFrame({
        'Subcriterion': list(normalized_weights.keys()),
        'Normalized Weight': list(normalized_weights.values())
    })

    # Calculate the weighted scores
    scores_df['Weighted Score'] = scores_df.apply(lambda row: row['Score'] * normalized_weights[row['Subcriterion']], axis=1)
    total_scores = scores_df.groupby('Producer')['Weighted Score'].sum().reset_index()
    total_scores = total_scores.sort_values(by='Weighted Score', ascending=False)

    # Rank the producers from 1 to the total number of producers
    total_scores['Ranking'] = total_scores['Weighted Score'].rank(ascending=False, method='min').astype(int)

    # Display the results
    st.write("AHP Results:")
    st.write(total_scores[['Ranking', 'Producer', 'Weighted Score']])

    # Consistency matrix example (user input should ideally provide this)
    consistency_matrix = np.random.rand(len(subcriteria), len(subcriteria))  # Placeholder for actual matrix
    ci = calculate_consistency(consistency_matrix)
    ri = get_ri(len(subcriteria))
    cr = ci / ri
    cr_message = "Consistency Ratio (CR) is acceptable." if cr < 0.10 else "Consistency Ratio (CR) is not acceptable."

    # Display consistency check results
    st.write("Consistency Check:")
    st.write(f"Consistency Index (CI): {ci}")
    st.write(f"Random Consistency Index (RI): {ri}")
    st.write(f"Consistency Ratio (CR): {cr}")
    st.write(cr_message)

def main():
    st.title("Dairy Selection Tool")

    # Provide example file download
    example_file = create_example_file()
    with open(example_file, "rb") as file:
        st.download_button(
            label="Download Example Input File",
            data=file,
            file_name="example_input.csv",
            mime="text/csv"
        )

    data = get_user_input()
    if st.button("Calculate AHP"):
        display_results(data)

if __name__ == '__main__':
    main()
