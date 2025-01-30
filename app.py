import streamlit as st
import pandas as pd

# Definir estilo global com fundo azul marinho e letras cinza
st.markdown(
    """
    <style>
        body {
            background-color: #001F3F;
            color: #D3D3D3;
        }
        h1, h2 {
            color: #003366;
        }
        .stDataFrame, .stTable {
            background-color: #001F3F;
            color: #D3D3D3;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho do Dashboard
st.markdown("<h1 style='text-align: center;'>Dashboard de Movimentação Portuária</h1>", unsafe_allow_html=True)

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "dados_graficos.xlsx"
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        'Ano': 'ano',
        'Tipo de instalação': 'tipo_instalacao',
        'Perfil da Carga': 'perfil_carga',
        'Sentido': 'sentido',
        'Tipo Navegação': 'tipo_navegacao',
        'UF Origem': 'uf_origem',
        'UF Destino': 'uf_destino',
        'País Origem': 'pais_origem',
        'País Destino': 'pais_destino',
        'Total de Movimentação Portuária\nem toneladas (t)': 'movimentacao_total_t'
    })
    df["ano"] = df["ano"].astype(int).astype(str)  # Garantir formato correto de ano
    return df

df = load_data()

# Filtros ampliados
st.sidebar.header("Filtros")
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].unique()))
tipo_instalacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Instalação", df["tipo_instalacao"].unique())
perfil_carga_selecionado = st.sidebar.selectbox("Selecione o Perfil da Carga", df["perfil_carga"].unique())
sentido_selecionado = st.sidebar.selectbox("Selecione o Sentido", df["sentido"].unique())
tipo_navegacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Navegação", df["tipo_navegacao"].unique())

# Aplicar filtros
df_filtered = df[
    (df["ano"] == ano_selecionado) &
    (df["tipo_instalacao"] == tipo_instalacao_selecionado) &
    (df["perfil_carga"] == perfil_carga_selecionado) &
    (df["sentido"] == sentido_selecionado) &
    (df["tipo_navegacao"] == tipo_navegacao_selecionado)
]

# Criar título dinâmico com seleção
titulo_selecionado = f"{ano_selecionado}/{tipo_instalacao_selecionado}/{sentido_selecionado}"
st.markdown(f"<h2 style='text-align: center;'>{titulo_selecionado}</h2>", unsafe_allow_html=True)

# Agregar dados por ano
df_summary = df_filtered.groupby("ano", as_index=False)["movimentacao_total_t"].sum()

# Formatar os números para exibição
df_summary["movimentacao_total_t"] = df_summary["movimentacao_total_t"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Exibir tabela de dados agregados
st.markdown("<h2 style='text-align: center;'>Totais de Movimentação Portuária</h2>", unsafe_allow_html=True)
st.dataframe(df_summary, width=1000)
