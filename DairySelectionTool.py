import pandas as pd
import numpy as np
import streamlit as st

# Define os subcritérios e os pesos normalizados
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

# Matriz de comparação par-a-par fornecida
comparison_matrix = np.array([
    # [Adicione aqui a matriz]
])

# Função para calcular a consistência da matriz
def check_consistency(matrix):
    eigenvalues, _ = np.linalg.eig(matrix)
    lambda_max = max(eigenvalues).real  # Usa apenas a parte real
    n = matrix.shape[0]
    CI = (lambda_max - n) / (n - 1)
    RI_values = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.54, 13: 1.56, 14: 1.59}
    RI = RI_values.get(n, 1.59)  # Usa 1.59 como padrão para n >= 14
    CR = CI / RI if RI != 0 else 0
    return f"The Consistency Ratio is {'acceptable' if CR < 0.1 else 'not acceptable'}: {CR:.4f}"

# Função para calcular a pontuação total dos produtores
def calculate_scores(df):
    df['Economic Score'] = df['Economic'] * sum([normalized_weights[sub] for sub in subcriteria['Economic']])
    df['Social Score'] = df['Social'] * sum([normalized_weights[sub] for sub in subcriteria['Social']])
    df['Production Score'] = df['Production'] * sum([normalized_weights[sub] for sub in subcriteria['Production']])
    df['Total Score'] = df['Economic Score'] + df['Social Score'] + df['Production Score']
    df['Ranking'] = df['Total Score'].rank(ascending=False)
    return df

# Interface Streamlit
st.title("AHP for Milk Producer Evaluation")

# Opções para inserir dados: upload de arquivo ou entrada manual
data_input_method = st.radio("Select data input method:", ("Upload CSV file", "Manual entry"))

if data_input_method == "Upload CSV file":
    uploaded_file = st.file_uploader("Upload producer data (CSV)", type="csv")

    if uploaded_file is not None:
        df_producers = pd.read_csv(uploaded_file)

        required_columns = ['Producer', 'Economic', 'Social', 'Production']
        if not all(col in df_producers.columns for col in required_columns):
            st.error(f"CSV file must contain these columns: {required_columns}")
        else:
            df_producers = calculate_scores(df_producers)
            st.write("AHP Results:")
            st.dataframe(df_producers)
else:
    st.write("Manual entry is not yet implemented.")
