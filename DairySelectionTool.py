import numpy as np

# Função para calcular Consistency Index (CI)
def calculate_consistency(matrix):
    # Calcular os autovalores e autovetores
    eigenvalues, _ = np.linalg.eig(matrix)
    
    # O maior autovalor (lambda_max)
    lambda_max = max(eigenvalues)
    
    # Número de critérios
    n = matrix.shape[0]
    
    # Calcular o Consistency Index (CI)
    ci = (lambda_max - n) / (n - 1)
    return ci

# Função para calcular o Random Consistency Index (RI)
def get_ri(n):
    ri_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 14: 1.49}
    return ri_dict.get(n, 1.49)  # Padrão para 10 critérios ou mais

# Função para exibir os resultados da consistência
def display_consistency_results(matrix):
    # Calcular Consistency Index (CI)
    ci = calculate_consistency(matrix)
    
    # Número de critérios (subcritérios)
    n = matrix.shape[0]
    
    # Obter o Random Consistency Index (RI) para o número de critérios
    ri = get_ri(n)
    
    # Calcular o Consistency Ratio (CR)
    cr = ci / ri
    
    # Exibir os resultados da consistência
    print(f"Consistency Index (CI): {ci}")
    print(f"Random Consistency Index (RI): {ri}")
    print(f"Consistency Ratio (CR): {cr}")
    
    # Verificar se a consistência é aceitável
    if cr < 0.10:
        print("Consistency Ratio (CR) is acceptable.")
    else:
        print("Consistency Ratio (CR) is not acceptable.")

# Exemplo de uso
# Exemplo de matriz de comparação (isso deve ser feito de acordo com as ponderações normalizadas)
n = 8  # Exemplo com 8 critérios (subcritérios)
comparison_matrix = np.random.rand(n, n)
comparison_matrix = (comparison_matrix + comparison_matrix.T) / 2  # Matriz simétrica para garantir consistência
np.fill_diagonal(comparison_matrix, 1)  # A diagonal principal é 1 (autocomparação)

# Exibir os resultados da consistência
display_consistency_results(comparison_matrix)
