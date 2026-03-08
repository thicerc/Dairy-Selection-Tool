import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dairy Selection Tool | Seleção de Laticínios",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #f8fafc; }

    .hero-header {
        background: linear-gradient(135deg, #1a5276 0%, #2980b9 50%, #1abc9c 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(26,82,118,0.18);
    }
    .hero-header h1 { color: white; font-size: 2.2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
    .hero-header p  { color: rgba(255,255,255,0.85); font-size: 1rem; margin: 0.5rem 0 0; }

    .card {
        background: white;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        margin-bottom: 1.2rem;
        border: 1px solid #e8edf2;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1a5276;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .rank-1 { background: linear-gradient(135deg, #f6d365, #fda085); color: white; }
    .rank-2 { background: linear-gradient(135deg, #a8edea, #fed6e3); color: #333; }
    .rank-3 { background: linear-gradient(135deg, #d4fc79, #96e6a1); color: #333; }

    .ranking-card {
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .rank-badge {
        width: 42px; height: 42px;
        border-radius: 50%;
        background: rgba(255,255,255,0.35);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; font-weight: 700;
        flex-shrink: 0;
    }
    .rank-name { font-size: 1.05rem; font-weight: 600; flex: 1; }
    .rank-score { font-size: 1.4rem; font-weight: 700; }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid;
    }
    .metric-value { font-size: 1.8rem; font-weight: 700; }
    .metric-label { font-size: 0.8rem; color: #666; margin-top: 2px; }

    .weight-pill {
        display: inline-block;
        background: #e8f4fd;
        color: #1a5276;
        border-radius: 99px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-left: 6px;
    }

    .stSlider > div > div > div { background: #2980b9 !important; }

    .section-divider {
        border: none;
        border-top: 2px solid #e8edf2;
        margin: 1.5rem 0;
    }

    .badge-economic  { background:#dbeafe; color:#1e40af; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
    .badge-social    { background:#dcfce7; color:#166534; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }
    .badge-production{ background:#fef9c3; color:#854d0e; padding:3px 10px; border-radius:99px; font-size:0.75rem; font-weight:600; }

    div[data-testid="stExpander"] { border: 1px solid #e8edf2 !important; border-radius: 12px !important; }

    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important; }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── LANGUAGE ─────────────────────────────────────────────────────────────────
LANG = {
    'EN': {
        'title': 'Dairy Producer Selection Tool',
        'subtitle': 'AHP-based ranking system for milk producer evaluation',
        'language': 'Language / Idioma',
        'settings': '⚙️ Settings',
        'weights_title': '📊 Criterion Weights',
        'weights_info': 'Adjust the weights for each criterion. Values will be normalized to sum to 1.',
        'reset_weights': '↺ Reset to Default',
        'input_method': '📥 Data Input Method',
        'upload_csv': '📂 Upload CSV',
        'manual_entry': '✏️ Manual Entry',
        'num_producers': 'Number of Producers',
        'producer_name': 'Producer Name',
        'calc_button': '🚀 Calculate Ranking',
        'results_title': '🏆 Ranking Results',
        'ranking_tab': '🏅 Ranking',
        'charts_tab': '📊 Charts',
        'details_tab': '🔍 Details',
        'consistency_tab': '✅ Consistency',
        'export_tab': '📤 Export',
        'total_score': 'Total Score',
        'economic': 'Economic',
        'social': 'Social',
        'production': 'Production',
        'consistency_title': 'AHP Consistency Analysis',
        'cr_ok': '✅ Consistency Ratio is acceptable (CR < 0.1)',
        'cr_fail': '⚠️ Consistency Ratio is not acceptable (CR ≥ 0.1)',
        'download_excel': '📥 Download Excel Report',
        'download_csv': '📥 Download CSV',
        'upload_hint': 'Upload a CSV with columns: Producer, Economic, Social, Production',
        'download_example': '⬇️ Download Example CSV',
        'no_data': 'No data to display. Run a calculation first.',
        'producers': 'producers',
        'top_producer': 'Top Producer',
        'avg_score': 'Average Score',
        'score_range': 'Score Range',
        'economic_criteria': 'Economic Criteria',
        'social_criteria': 'Social Criteria',
        'production_criteria': 'Production Criteria',
        'subcriteria_scores': 'Sub-criteria Scores',
    },
    'PT': {
        'title': 'Ferramenta de Seleção de Produtores',
        'subtitle': 'Sistema de ranking baseado em AHP para avaliação de produtores de leite',
        'language': 'Language / Idioma',
        'settings': '⚙️ Configurações',
        'weights_title': '📊 Pesos dos Critérios',
        'weights_info': 'Ajuste os pesos de cada critério. Os valores serão normalizados para somar 1.',
        'reset_weights': '↺ Restaurar Padrão',
        'input_method': '📥 Método de Entrada de Dados',
        'upload_csv': '📂 Enviar CSV',
        'manual_entry': '✏️ Entrada Manual',
        'num_producers': 'Número de Produtores',
        'producer_name': 'Nome do Produtor',
        'calc_button': '🚀 Calcular Ranking',
        'results_title': '🏆 Resultados do Ranking',
        'ranking_tab': '🏅 Ranking',
        'charts_tab': '📊 Gráficos',
        'details_tab': '🔍 Detalhes',
        'consistency_tab': '✅ Consistência',
        'export_tab': '📤 Exportar',
        'total_score': 'Pontuação Total',
        'economic': 'Econômico',
        'social': 'Social',
        'production': 'Produção',
        'consistency_title': 'Análise de Consistência AHP',
        'cr_ok': '✅ Razão de Consistência aceitável (RC < 0,1)',
        'cr_fail': '⚠️ Razão de Consistência não aceitável (RC ≥ 0,1)',
        'download_excel': '📥 Baixar Relatório Excel',
        'download_csv': '📥 Baixar CSV',
        'upload_hint': 'Envie um CSV com as colunas: Producer, Economic, Social, Production',
        'download_example': '⬇️ Baixar CSV de Exemplo',
        'no_data': 'Sem dados para exibir. Execute um cálculo primeiro.',
        'producers': 'produtores',
        'top_producer': 'Melhor Produtor',
        'avg_score': 'Pontuação Média',
        'score_range': 'Amplitude',
        'economic_criteria': 'Critérios Econômicos',
        'social_criteria': 'Critérios Sociais',
        'production_criteria': 'Critérios de Produção',
        'subcriteria_scores': 'Pontuações por Subcritério',
    }
}

# ─── SUBCRITERIA & DEFAULT WEIGHTS ────────────────────────────────────────────
SUBCRITERIA = {
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

SUBCRITERIA_PT = {
    'Economic': [
        'Acesso a recursos financeiros',
        'Tipo e frequência de incentivos financeiros',
        'Duração dos períodos de preço estável',
        'Competitividade do preço exclusivo',
        'Relação de ajustes de preço à qualidade',
        'Transparência na precificação do conselho',
        'Impacto das flutuações internacionais de preço',
        'Benefício de exclusividade para parcerias de longo prazo'
    ],
    'Social': [
        'Frequência e qualidade das visitas técnicas',
        'Duração e flexibilidade dos termos do contrato',
        'Penalidades ou recompensas por cronogramas de entrega'
    ],
    'Production': [
        'Consistência na produção diária de leite',
        'Aderência aos padrões de qualidade',
        'Viabilidade econômica da coleta para diferentes volumes'
    ]
}

DEFAULT_WEIGHTS = {
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

COMPARISON_MATRIX = np.array([
    [1.0,0.94539782,0.87698987,1.03945111,0.76322418,0.57277883,0.83471074,0.81671159,0.67558528,1.08602151,0.79112272,0.93087558,1.04844291,0.85352113],
    [1.05775578,1.0,0.9276411,1.09948542,0.80730479,0.60586011,0.88292011,0.8638814,0.71460424,1.14874552,0.83681462,0.98463902,1.10899654,0.9028169],
    [1.14026403,1.07800312,1.0,1.18524871,0.87027708,0.65311909,0.95179063,0.93126685,0.7703456,1.23835125,0.90208877,1.06144393,1.19550173,0.97323944],
    [0.9620462,0.90951638,0.84370478,1.0,0.73425693,0.5510397,0.8030303,0.78571429,0.64994426,1.04480287,0.76109661,0.89554531,1.00865052,0.82112676],
    [1.31023102,1.23868955,1.14905933,1.3619211,1.0,0.75047259,1.09366391,1.07008086,0.8851728,1.42293907,1.03655352,1.21966206,1.37370242,1.11830986],
    [1.74587459,1.65054602,1.53111433,1.81475129,1.3324937,1.0,1.45730028,1.42587601,1.17948718,1.89605735,1.38120104,1.62519201,1.83044983,1.49014085],
    [1.1980198,1.1326053,1.05065123,1.24528302,0.91435768,0.68620038,1.0,0.97843666,0.80936455,1.30107527,0.94778068,1.11520737,1.25605536,1.02253521],
    [1.22442244,1.1575663,1.07380608,1.27272727,0.93450882,0.70132325,1.02203857,1.0,0.82720178,1.3297491,0.96866841,1.13978495,1.28373702,1.04507042],
    [1.48019802,1.39937598,1.29811867,1.53859348,1.12972292,0.84782609,1.23553719,1.20889488,1.0,1.60752688,1.17101828,1.37788018,1.55190311,1.26338028],
    [0.92079208,0.87051482,0.80752533,0.95711835,0.70277078,0.52741021,0.76859504,0.75202156,0.62207358,1.0,0.72845953,0.85714286,0.96539792,0.78591549],
    [1.2640264,1.1950078,1.10853835,1.31389365,0.96473552,0.72400756,1.05509642,1.03234501,0.85395764,1.37275986,1.0,1.17665131,1.32525952,1.07887324],
    [1.07425743,1.01560062,0.94211288,1.11663808,0.81989924,0.61531191,0.89669421,0.87735849,0.72575251,1.16666667,0.84986945,1.0,1.12629758,0.91690141],
    [0.95379538,0.90171607,0.83646889,0.99142367,0.7279597,0.5463138,0.79614325,0.77897574,0.64437012,1.03584229,0.75456919,0.88786482,1.0,0.81408451],
    [1.17161716,1.10764431,1.02749638,1.21783877,0.89420655,0.6710775,0.97796143,0.95687332,0.79152731,1.27240143,0.92689295,1.0906298,1.2283737,1.0]
])

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
def get_t(key):
    return LANG[st.session_state.get('lang', 'PT')][key]

def check_consistency(matrix):
    eigenvalues, _ = np.linalg.eig(matrix)
    lambda_max = float(np.real(max(eigenvalues)))
    n = matrix.shape[0]
    CI = (lambda_max - n) / (n - 1)
    RI_values = {1:0.0,2:0.0,3:0.58,4:0.90,5:1.12,6:1.24,7:1.32,8:1.41,9:1.45,10:1.49,11:1.51,12:1.54,13:1.56,14:1.59}
    RI = RI_values[n]
    CR = CI / RI
    return {'lambda_max': lambda_max, 'CI': CI, 'CR': CR, 'RI': RI, 'n': n}

def normalize_weights(weights_dict):
    total = sum(weights_dict.values())
    return {k: v / total for k, v in weights_dict.items()}

def calculate_scores(df, weights):
    nw = normalize_weights(weights)
    eco_w  = sum(nw[s] for s in SUBCRITERIA['Economic'])
    soc_w  = sum(nw[s] for s in SUBCRITERIA['Social'])
    prod_w = sum(nw[s] for s in SUBCRITERIA['Production'])

    df = df.copy()
    df['Economic Score']   = df['Economic']   * eco_w
    df['Social Score']     = df['Social']     * soc_w
    df['Production Score'] = df['Production'] * prod_w
    df['Total Score']      = df['Economic Score'] + df['Social Score'] + df['Production Score']
    df = df.sort_values('Total Score', ascending=False).reset_index(drop=True)
    df['Ranking'] = range(1, len(df) + 1)
    return df

def to_excel(df):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        # Main results
        df.to_excel(writer, sheet_name='Ranking', index=False)
        # Weights sheet
        weights_df = pd.DataFrame([
            {'Criterion': k, 'Category': cat, 'Weight': v}
            for cat, subs in SUBCRITERIA.items()
            for k in subs
            for v in [st.session_state.weights.get(k, DEFAULT_WEIGHTS[k])]
        ])
        weights_df.to_excel(writer, sheet_name='Weights', index=False)
    buf.seek(0)
    return buf.getvalue()

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if 'lang' not in st.session_state:
    st.session_state.lang = 'PT'
if 'weights' not in st.session_state:
    st.session_state.weights = dict(DEFAULT_WEIGHTS)
if 'results' not in st.session_state:
    st.session_state.results = None

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {get_t('language')}")
    lang_choice = st.radio("", ['PT 🇧🇷', 'EN 🇬🇧'], horizontal=True,
                           index=0 if st.session_state.lang == 'PT' else 1, label_visibility="collapsed")
    st.session_state.lang = 'PT' if lang_choice.startswith('PT') else 'EN'

    st.markdown("---")
    st.markdown(f"### {get_t('weights_title')}")
    st.caption(get_t('weights_info'))

    if st.button(get_t('reset_weights'), use_container_width=True):
        st.session_state.weights = dict(DEFAULT_WEIGHTS)
        st.rerun()

    cat_colors = {'Economic': '#dbeafe', 'Social': '#dcfce7', 'Production': '#fef9c3'}
    cat_labels_pt = {'Economic': 'Econômico', 'Social': 'Social', 'Production': 'Produção'}

    new_weights = {}
    for cat, subs in SUBCRITERIA.items():
        cat_label = cat_labels_pt[cat] if st.session_state.lang == 'PT' else cat
        subs_pt = SUBCRITERIA_PT[cat] if st.session_state.lang == 'PT' else subs
        with st.expander(f"**{cat_label}**", expanded=False):
            for sub_en, sub_label in zip(subs, subs_pt):
                default_val = st.session_state.weights.get(sub_en, DEFAULT_WEIGHTS[sub_en])
                val = st.slider(
                    sub_label,
                    min_value=0.01, max_value=0.30,
                    value=float(default_val),
                    step=0.005,
                    format="%.3f",
                    key=f"w_{sub_en}"
                )
                new_weights[sub_en] = val

    st.session_state.weights = new_weights

    # Show normalized weights summary
    nw = normalize_weights(st.session_state.weights)
    eco_total  = sum(nw[s] for s in SUBCRITERIA['Economic'])
    soc_total  = sum(nw[s] for s in SUBCRITERIA['Social'])
    prod_total = sum(nw[s] for s in SUBCRITERIA['Production'])

    st.markdown("---")
    st.markdown("**Pesos Normalizados / Normalized Weights**")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Econ.", f"{eco_total:.1%}")
    col2.metric("🤝 Social", f"{soc_total:.1%}")
    col3.metric("🐄 Prod.", f"{prod_total:.1%}")

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
    <h1>🥛 {get_t('title')}</h1>
    <p>{get_t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ─── INPUT SECTION ────────────────────────────────────────────────────────────
st.markdown(f"### {get_t('input_method')}")
method = st.radio("", [get_t('upload_csv'), get_t('manual_entry')], horizontal=True, label_visibility="collapsed")

df_result = None

# ── CSV Upload ─────────────────────────────────────────────────────────────────
if method == get_t('upload_csv'):
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader(get_t('upload_hint'), type='csv', label_visibility="collapsed")
    with col2:
        example = pd.DataFrame({
            'Producer': ['Produtor A', 'Produtor B', 'Produtor C'],
            'Economic': [0.8, 0.9, 0.7],
            'Social': [0.75, 0.85, 0.65],
            'Production': [0.9, 0.7, 0.8]
        })
        st.download_button(get_t('download_example'),
                          example.to_csv(index=False).encode('utf-8'),
                          'exemplo_produtores.csv', 'text/csv',
                          use_container_width=True)

    if uploaded:
        df_in = pd.read_csv(uploaded)
        required = ['Producer', 'Economic', 'Social', 'Production']
        if not all(c in df_in.columns for c in required):
            st.error(f"CSV deve conter: {required}")
        else:
            st.dataframe(df_in, use_container_width=True)
            if st.button(get_t('calc_button'), type='primary', use_container_width=True):
                df_result = calculate_scores(df_in, st.session_state.weights)
                st.session_state.results = df_result

# ── Manual Entry ───────────────────────────────────────────────────────────────
else:
    num = st.number_input(get_t('num_producers'), min_value=1, max_value=20, value=3, step=1)

    all_subs_en = [s for subs in SUBCRITERIA.values() for s in subs]
    all_subs_pt = [s for subs in SUBCRITERIA_PT.values() for s in subs]
    n_eco  = len(SUBCRITERIA['Economic'])
    n_soc  = len(SUBCRITERIA['Social'])

    producer_data = []
    for i in range(int(num)):
        with st.expander(f"🐄 Produtor {i+1}" if st.session_state.lang == 'PT' else f"🐄 Producer {i+1}", expanded=(i == 0)):
            pname = st.text_input(
                get_t('producer_name'),
                value=f"Produtor {i+1}" if st.session_state.lang == 'PT' else f"Producer {i+1}",
                key=f"pname_{i}"
            )

            sub_labels = all_subs_pt if st.session_state.lang == 'PT' else all_subs_en

            # Economic
            st.markdown(f'<span class="badge-economic">💰 {get_t("economic_criteria")}</span>', unsafe_allow_html=True)
            eco_scores = []
            cols = st.columns(2)
            for j, label in enumerate(sub_labels[:n_eco]):
                with cols[j % 2]:
                    val = st.slider(label, 0, 10, 5, key=f"p{i}_eco_{j}")
                    eco_scores.append(val / 10)

            # Social
            st.markdown(f'<span class="badge-social">🤝 {get_t("social_criteria")}</span>', unsafe_allow_html=True)
            soc_scores = []
            cols = st.columns(2)
            for j, label in enumerate(sub_labels[n_eco:n_eco + n_soc]):
                with cols[j % 2]:
                    val = st.slider(label, 0, 10, 5, key=f"p{i}_soc_{j}")
                    soc_scores.append(val / 10)

            # Production
            st.markdown(f'<span class="badge-production">🐄 {get_t("production_criteria")}</span>', unsafe_allow_html=True)
            prod_scores = []
            cols = st.columns(2)
            for j, label in enumerate(sub_labels[n_eco + n_soc:]):
                with cols[j % 2]:
                    val = st.slider(label, 0, 10, 5, key=f"p{i}_prod_{j}")
                    prod_scores.append(val / 10)

            producer_data.append([pname, np.mean(eco_scores), np.mean(soc_scores), np.mean(prod_scores)])

    if st.button(get_t('calc_button'), type='primary', use_container_width=True):
        df_in = pd.DataFrame(producer_data, columns=['Producer', 'Economic', 'Social', 'Production'])
        df_result = calculate_scores(df_in, st.session_state.weights)
        st.session_state.results = df_result

# ─── RESULTS ──────────────────────────────────────────────────────────────────
if st.session_state.results is not None:
    df = st.session_state.results
    st.markdown("---")
    st.markdown(f"## {get_t('results_title')}")

    # ── KPI Cards ────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpi_style = ["#dbeafe;color:#1e40af", "#dcfce7;color:#166534",
                 "#fef9c3;color:#854d0e", "#fce7f3;color:#9d174d"]
    kpis = [
        (f"{len(df)}", get_t('producers').upper()),
        (df.iloc[0]['Producer'], get_t('top_producer').upper()),
        (f"{df['Total Score'].mean():.3f}", get_t('avg_score').upper()),
        (f"{df['Total Score'].max() - df['Total Score'].min():.3f}", get_t('score_range').upper()),
    ]
    for col, (val, label), style in zip([k1, k2, k3, k4], kpis, kpi_style):
        bg, color = style.split(";")
        col.markdown(f"""
        <div class="metric-card" style="border-color:{color.split(':')[1]}; background:#{bg.split('#')[1]}">
            <div class="metric-value" style="{color}">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    t1, t2, t3, t4, t5 = st.tabs([
        get_t('ranking_tab'), get_t('charts_tab'),
        get_t('details_tab'), get_t('consistency_tab'), get_t('export_tab')
    ])

    # ── Tab 1: Ranking ────────────────────────────────────────────────────────
    with t1:
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}
        rank_colors = {
            1: "background: linear-gradient(135deg,#f6d365,#fda085); color:white",
            2: "background: linear-gradient(135deg,#a8edea,#fed6e3); color:#333",
            3: "background: linear-gradient(135deg,#d4fc79,#96e6a1); color:#333",
        }
        default_color = "background: #f8fafc; color:#333; border: 1px solid #e8edf2"

        for _, row in df.iterrows():
            rank = int(row['Ranking'])
            style = rank_colors.get(rank, default_color)
            icon = medal.get(rank, f"#{rank}")
            bar_w = (row['Total Score'] / df['Total Score'].max()) * 100

            st.markdown(f"""
            <div class="ranking-card" style="{style}">
                <div class="rank-badge">{icon}</div>
                <div style="flex:1">
                    <div class="rank-name">{row['Producer']}</div>
                    <div style="font-size:0.8rem; opacity:0.8; margin-top:2px">
                        💰 {row['Economic Score']:.3f} &nbsp;|&nbsp;
                        🤝 {row['Social Score']:.3f} &nbsp;|&nbsp;
                        🐄 {row['Production Score']:.3f}
                    </div>
                    <div style="margin-top:6px; background:rgba(255,255,255,0.3); border-radius:99px; height:6px; overflow:hidden">
                        <div style="width:{bar_w:.1f}%; height:100%; background:rgba(255,255,255,0.7); border-radius:99px"></div>
                    </div>
                </div>
                <div class="rank-score">{row['Total Score']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Charts ─────────────────────────────────────────────────────────
    with t2:
        col1, col2 = st.columns(2)

        with col1:
            # Bar chart - total scores
            fig_bar = px.bar(
                df.sort_values('Total Score'),
                x='Total Score', y='Producer', orientation='h',
                color='Total Score',
                color_continuous_scale='Blues',
                title=get_t('total_score'),
                text='Total Score'
            )
            fig_bar.update_traces(texttemplate='%{text:.4f}', textposition='outside')
            fig_bar.update_layout(
                plot_bgcolor='white', paper_bgcolor='white',
                coloraxis_showscale=False,
                height=max(300, len(df) * 50),
                margin=dict(l=0, r=40, t=40, b=0),
                font=dict(family='Inter')
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            # Stacked bar
            fig_stack = go.Figure()
            colors = ['#2980b9', '#27ae60', '#f39c12']
            cats = [
                (get_t('economic'), 'Economic Score'),
                (get_t('social'), 'Social Score'),
                (get_t('production'), 'Production Score'),
            ]
            for (cat_label, col_name), color in zip(cats, colors):
                fig_stack.add_trace(go.Bar(
                    name=cat_label, x=df['Producer'],
                    y=df[col_name], marker_color=color
                ))
            fig_stack.update_layout(
                barmode='stack', title='Score Breakdown',
                plot_bgcolor='white', paper_bgcolor='white',
                height=max(300, len(df) * 50),
                margin=dict(l=0, r=0, t=40, b=0),
                font=dict(family='Inter'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02)
            )
            st.plotly_chart(fig_stack, use_container_width=True)

        # Radar chart
        if len(df) <= 8:
            categories = [get_t('economic'), get_t('social'), get_t('production')]
            fig_radar = go.Figure()
            palette = px.colors.qualitative.Set2
            for idx, (_, row) in enumerate(df.iterrows()):
                vals = [row['Economic Score'], row['Social Score'], row['Production Score']]
                vals += [vals[0]]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals, theta=categories + [categories[0]],
                    fill='toself', name=row['Producer'],
                    line_color=palette[idx % len(palette)],
                    fillcolor=palette[idx % len(palette)],
                    opacity=0.3
                ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, df[['Economic Score','Social Score','Production Score']].max().max() * 1.1])),
                title='Radar — Score por Categoria',
                paper_bgcolor='white',
                height=400,
                font=dict(family='Inter')
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Weights donut
        nw = normalize_weights(st.session_state.weights)
        cats_w = {
            get_t('economic'): sum(nw[s] for s in SUBCRITERIA['Economic']),
            get_t('social'): sum(nw[s] for s in SUBCRITERIA['Social']),
            get_t('production'): sum(nw[s] for s in SUBCRITERIA['Production']),
        }
        fig_donut = go.Figure(go.Pie(
            labels=list(cats_w.keys()),
            values=list(cats_w.values()),
            hole=0.55,
            marker_colors=['#2980b9', '#27ae60', '#f39c12'],
        ))
        fig_donut.update_layout(
            title='Peso por Categoria / Category Weights',
            paper_bgcolor='white',
            height=320,
            font=dict(family='Inter'),
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Tab 3: Details ────────────────────────────────────────────────────────
    with t3:
        st.dataframe(
            df[['Ranking', 'Producer', 'Economic Score', 'Social Score', 'Production Score', 'Total Score']]
            .style.background_gradient(subset=['Total Score'], cmap='Blues')
            .format({'Economic Score': '{:.4f}', 'Social Score': '{:.4f}',
                     'Production Score': '{:.4f}', 'Total Score': '{:.4f}'}),
            use_container_width=True, hide_index=True
        )

        # Weights breakdown table
        st.markdown(f"#### {get_t('subcriteria_scores')}")
        nw = normalize_weights(st.session_state.weights)
        weight_rows = []
        for cat, subs in SUBCRITERIA.items():
            subs_pt = SUBCRITERIA_PT[cat]
            cat_label = cat_labels_pt[cat] if st.session_state.lang == 'PT' else cat
            for sub_en, sub_pt in zip(subs, subs_pt):
                sub_label = sub_pt if st.session_state.lang == 'PT' else sub_en
                weight_rows.append({
                    'Categoria' if st.session_state.lang == 'PT' else 'Category': cat_label,
                    'Subcritério' if st.session_state.lang == 'PT' else 'Sub-criterion': sub_label,
                    'Peso / Weight': f"{nw[sub_en]:.4f} ({nw[sub_en]:.1%})"
                })
        st.dataframe(pd.DataFrame(weight_rows), use_container_width=True, hide_index=True)

    # ── Tab 4: Consistency ────────────────────────────────────────────────────
    with t4:
        st.markdown(f"#### {get_t('consistency_title')}")
        cons = check_consistency(COMPARISON_MATRIX)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("n (critérios)", cons['n'])
        c2.metric("λ_max", f"{cons['lambda_max']:.4f}")
        c3.metric("CI", f"{cons['CI']:.4f}")
        c4.metric("CR", f"{cons['CR']:.4f}")

        if cons['CR'] < 0.1:
            st.success(get_t('cr_ok'))
        else:
            st.error(get_t('cr_fail'))

        with st.expander("📐 Matriz de Comparação / Comparison Matrix"):
            all_subs = [s for subs in SUBCRITERIA.values() for s in subs]
            df_mat = pd.DataFrame(COMPARISON_MATRIX, index=all_subs, columns=all_subs)
            st.dataframe(df_mat.style.format("{:.4f}").background_gradient(cmap='Blues'),
                        use_container_width=True)

    # ── Tab 5: Export ─────────────────────────────────────────────────────────
    with t5:
        col1, col2 = st.columns(2)
        with col1:
            excel_data = to_excel(df)
            st.download_button(
                get_t('download_excel'),
                data=excel_data,
                file_name='dairy_ranking_report.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        with col2:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                get_t('download_csv'),
                data=csv_data,
                file_name='dairy_ranking.csv',
                mime='text/csv',
                use_container_width=True
            )
        st.dataframe(df, use_container_width=True, hide_index=True)
