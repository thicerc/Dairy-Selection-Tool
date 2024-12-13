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

# Função para calcular a consistência da matriz
def check_consistency(matrix):
    eigenvalues, _ = np.linalg.eig(matrix)
    lambda_max = max(eigenvalues)
    n = matrix.shape[0]
    CI = (lambda_max - n) / (n - 1)
    RI_values = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.54, 13: 1.56, 14: 1.59}
    RI = RI_values[n]
    CR = CI / RI
    if CR < 0.1:
        return f"The Consistency Ratio is acceptable: {CR:.4f}"
    else:
        return f"The Consistency Ratio is not acceptable: {CR:.4f}"

# Função para calcular a pontuação total dos produtores
def calculate_scores(df):
    df['Economic Score'] = df['Economic'] * sum([normalized_weights[subcriteria_group] for subcriteria_group in subcriteria['Economic']])
    df['Social Score'] = df['Social'] * sum([normalized_weights[subcriteria_group] for subcriteria_group in subcriteria['Social']])
    df['Production Score'] = df['Production'] * sum([normalized_weights[subcriteria_group] for subcriteria_group in subcriteria['Production']])
    df['Total Score'] = df['Economic Score'] + df['Social Score'] + df['Production Score']
    df['Ranking'] = df['Total Score'].rank(ascending=False)
    return df

# Interface Streamlit
st.title("AHP for Milk Producer Evaluation")

# Opções para inserir dados: upload de arquivo ou entrada manual
data_input_method = st.radio("Select data input method:", ("Upload CSV file", "Manual entry"))

if data_input_method == "Upload CSV file":
    # Upload de arquivo CSV
    uploaded_file = st.file_uploader("Upload producer data (CSV)", type="csv")

    if uploaded_file is not None:
        df_producers = pd.read_csv(uploaded_file)

        # Verificar se as colunas necessárias existem no DataFrame
        required_columns = ['Producer', 'Economic', 'Social', 'Production']
        if not all(col in df_producers.columns for col in required_columns):
            st.error(f"CSV file must contain these columns: {required_columns}")
        else:
            # Calcular e exibir resultados
            df_producers = calculate_scores(df_producers)
            st.write("AHP Results:")
            st.dataframe(df_producers[['Producer', 'Total Score', 'Ranking']])

            # Exibir o resultado da verificação de consistência
            consistency_result = check_consistency(comparison_matrix)
            st.write(consistency_result)
    else:
        st.info("Upload a CSV file to get started.")

elif data_input_method == "Manual entry":
    # Entrada manual de dados
    st.subheader("Enter Producer Data:")
    num_producers = st.number_input("Number of producers:", min_value=1, value=1, step=1)

    producer_data = []
    for i in range(num_producers):
        st.write(f"**Producer {i+1}**")
        producer_name = st.text_input(f"Producer Name {i+1}:", value=f"Producer {i+1}")
        
        # Entrada de dados com a nova hierarquia
        st.write("**Economics**")
        economic_score = st.number_input(f"Overall Economic Score {i+1}:", min_value=0, max_value=10, value=5, step=1)
        for subcriterion in subcriteria['Economic']:
            st.number_input(f"{subcriterion} {i+1}:", min_value=0, max_value=10, value=5, step=1)
        
        st.write("**Social**")
        social_score = st.number_input(f"Overall Social Score {i+1}:", min_value=0, max_value=10, value=5, step=1)
        for subcriterion in subcriteria['Social']:
            st.number_input(f"{subcriterion} {i+1}:", min_value=0, max_value=10, value=5, step=1)

        st.write("**Production**")
        production_score = st.number_input(f"Overall Production Score {i+1}:", min_value=0, max_value=10, value=5, step=1)
        for subcriterion in subcriteria['Production']:
            st.number_input(f"{subcriterion} {i+1}:", min_value=0, max_value=10, value=5, step=1)

        producer_data.append([producer_name, economic_score/10, social_score/10, production_score/10])

    if st.button("Calculate"):
        df_producers = pd.DataFrame(producer_data, columns=['Producer', 'Economic', 'Social', 'Production'])
        df_producers = calculate_scores(df_producers)
        st.write("AHP Results:")
        st.dataframe(df_producers[['Producer', 'Total Score', 'Ranking']])

        # Exibir o resultado da verificação de consistência
        consistency_result = check_consistency(comparison_matrix)
        st.write(consistency_result)
