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

# Function to calculate Consistency Index (CI)
def calculate_consistency(matrix):
    n = len(matrix)
    eigenvalue = np.mean(np.sum(matrix, axis=1) / np.sum(matrix, axis=0))
    ci = (eigenvalue - n) / (n - 1)
    return ci

# Function to calculate Random Consistency Index (RI)
def get_ri(n):
    ri_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 14: 1.49}
    return ri_dict.get(n, 1.49)  # Default for 10 criteria or more

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

    # Create and display the consistency matrix
    n = len(normalized_weights)
    comparison_matrix = np.ones((n, n))

    # Populate the matrix using the normalized weights
    for i in range(n):
        for j in range(n):
            if i != j:
                comparison_matrix[i, j] = normalized_weights[list(normalized_weights.keys())[i]] / normalized_weights[list(normalized_weights.keys())[j]]

    # Calculate consistency
    ci = calculate_consistency(comparison_matrix)
    ri = get_ri(len(normalized_weights))
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
