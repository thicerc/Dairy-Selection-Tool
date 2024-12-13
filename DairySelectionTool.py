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
    'Accessibility of financial resources': 0.096,
    'Type and frequency of financial incentives': 0.166,
    'Duration of stable pricing periods': 0.267,
    'Competitiveness of exclusive price': 0.050,
    'Ratio of price adjustments to quality': 0.039,
    'Transparency of council-defined pricing': 0.304,
    'Impact of international price fluctuations': 0.000,
    'Benefit of exclusivity for long-term partnerships': 1.000,
    'Frequency and quality of technical visits': 0.337,
    'Length and flexibility of contract terms': 0.368,
    'Penalties or rewards for delivery schedules': 0.678,
    'Consistency in daily milk production': 0.000,
    'Adherence to quality standards': 0.416,
    'Economic viability of collection for different volumes': 0.186
}

# Function to calculate Consistency Index (CI)
def calculate_consistency(matrix):
    n = len(matrix)
    eigenvalue = np.mean(np.sum(matrix, axis=1) / np.sum(matrix, axis=0))
    ci = (eigenvalue - n) / (n - 1)
    return ci

# Function to calculate Random Consistency Index (RI)
def get_ri(n):
    ri_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    return ri_dict.get(n, 1.49)  # Default for 10 criteria or more

# Function to get user input for scores (manual entry)
def get_user_input_manual():
    num_producers = st.number_input("Enter the number of producers (1-1000):", min_value=1, max_value=1000, value=3, step=1)
    producers = [f'Producer {i+1}' for i in range(num_producers)]

    data = []
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

# Function to get user input for scores (CSV upload)
def get_user_input_csv():
    uploaded_file = st.file_uploader("Upload producer data (CSV)", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Assuming CSV has columns 'Producer', 'Subcriterion', 'Score'
            if all(col in df.columns for col in ['Producer', 'Subcriterion', 'Score']):
                return df.to_dict('records')
            else:
                st.error("CSV file must contain columns: 'Producer', 'Subcriterion', 'Score'")
                return None
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return None
    else:
        return None

# Function to display the results
def display_results(data):
    # ... (rest of the display_results function remains the same) ...

def main():
    st.title("Dairy Selection Tool")

    # Choose data input method
    data_input_method = st.radio("Select data input method:", ("Manual entry", "Upload CSV file"))

    if data_input_method == "Manual entry":
        data = get_user_input_manual()
    elif data_input_method == "Upload CSV file":
        data = get_user_input_csv()

    if data:
        if st.button("Calculate AHP"):
            display_results(data)

if __name__ == '__main__':
    main()
