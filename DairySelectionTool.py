import numpy as np
import pandas as pd
import streamlit as st

def calculate_weights(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvalue_index = np.argmax(eigenvalues)
    max_eigenvector = eigenvectors[:, max_eigenvalue_index].real
    weights = max_eigenvector / max_eigenvector.sum()
    return weights

def check_consistency(matrix):
    eigenvalues, _ = np.linalg.eig(matrix)
    max_eigenvalue = np.max(eigenvalues).real
    n = matrix.shape[0]
    ci = (max_eigenvalue - n) / (n - 1)
    
    ri_dict = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
    }
    ri = ri_dict.get(n, 1.49)
    cr = ci / ri if ri != 0 else 0

    if cr < 0.1:
        return f"Consistency Ratio (CR) = {cr:.3f}. The matrix is consistent."
    else:
        return f"Consistency Ratio (CR) = {cr:.3f}. The matrix is inconsistent. Please revise it."

def calculate_scores(df):
    df['Economic Score'] = df['Economic'] * criteria_weights[0]
    df['Social Score'] = df['Social'] * criteria_weights[1]
    df['Production Score'] = df['Production'] * criteria_weights[2]
    df['Total Score'] = df['Economic Score'] + df['Social Score'] + df['Production Score']
    df['Ranking'] = df['Total Score'].rank(ascending=False).astype(int)
    return df

st.title("AHP for Producer Ranking")
st.write("Analyze and rank producers based on Economic, Social, and Production criteria using AHP.")

# Step 1: Input pairwise comparison matrix
st.subheader("Pairwise Comparison Matrix")
st.write("Input the pairwise comparison matrix for the three criteria: Economic, Social, and Production.")
def input_matrix():
    comparison_matrix = np.eye(3)
    comparison_matrix[0, 1] = st.number_input("Economic vs Social:", min_value=1.0, step=0.1, value=1.0)
    comparison_matrix[1, 0] = 1 / comparison_matrix[0, 1]

    comparison_matrix[0, 2] = st.number_input("Economic vs Production:", min_value=1.0, step=0.1, value=1.0)
    comparison_matrix[2, 0] = 1 / comparison_matrix[0, 2]

    comparison_matrix[1, 2] = st.number_input("Social vs Production:", min_value=1.0, step=0.1, value=1.0)
    comparison_matrix[2, 1] = 1 / comparison_matrix[1, 2]

    return comparison_matrix

comparison_matrix = input_matrix()
criteria_weights = calculate_weights(comparison_matrix)
st.write("Criteria Weights:", dict(zip(["Economic", "Social", "Production"], criteria_weights)))

# Step 2: Input producer data
st.subheader("Producer Data")
data_input_method = st.radio("Select data input method:", ["Upload CSV", "Manual entry"])

if data_input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df_producers = pd.read_csv(uploaded_file)
        if {'Producer', 'Economic', 'Social', 'Production'}.issubset(df_producers.columns):
            df_producers = calculate_scores(df_producers)
            st.write("AHP Results:")
            st.dataframe(df_producers[['Producer', 'Economic Score', 'Social Score', 'Production Score', 'Total Score', 'Ranking']])
        else:
            st.error("CSV must contain columns: Producer, Economic, Social, Production.")

elif data_input_method == "Manual entry":
    num_producers = st.number_input("Number of producers:", min_value=1, step=1, value=1)

    producers_data = []
    for i in range(num_producers):
        st.subheader(f"Producer {i + 1}")
        producer_name = st.text_input(f"Name of Producer {i + 1}:", key=f"producer_name_{i}")
        economic = st.number_input(f"Economic Score for Producer {i + 1}:", min_value=0.0, max_value=1.0, step=0.01, key=f"economic_{i}")
        social = st.number_input(f"Social Score for Producer {i + 1}:", min_value=0.0, max_value=1.0, step=0.01, key=f"social_{i}")
        production = st.number_input(f"Production Score for Producer {i + 1}:", min_value=0.0, max_value=1.0, step=0.01, key=f"production_{i}")
        producers_data.append({
            'Producer': producer_name,
            'Economic': economic,
            'Social': social,
            'Production': production
        })

    if st.button("Calculate AHP Results"):
        if len(producers_data) == 0:
            st.error("Please enter data for at least one producer.")
        else:
            df_producers = pd.DataFrame(producers_data)
            df_producers = calculate_scores(df_producers)
            st.write("AHP Results:")
            st.dataframe(df_producers[['Producer', 'Economic Score', 'Social Score', 'Production Score', 'Total Score', 'Ranking']])

# Consistency Check
st.subheader("Consistency Check")
consistency_result = check_consistency(comparison_matrix)
st.write(consistency_result)
