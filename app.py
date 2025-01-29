import streamlit as st
import pandas as pd

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
    return df

df = load_data()

# Configuração do layout do Streamlit
st.title("Dashboard de Movimentação Portuária")

# Filtros
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].unique()))
tipo_instalacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Instalação", ["Todos"] + sorted(df["tipo_instalacao"].unique()))
perfil_carga_selecionado = st.sidebar.selectbox("Selecione o Perfil da Carga", ["Todos"] + sorted(df["perfil_carga"].unique()))
sentido_selecionado = st.sidebar.selectbox("Selecione o Sentido", ["Todos"] + sorted(df["sentido"].unique()))
tipo_navegacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Navegação", ["Todos"] + sorted(df["tipo_navegacao"].unique()))
uf_origem_selecionado = st.sidebar.selectbox("Selecione a UF de Origem", ["Todos"] + sorted(df["uf_origem"].unique()))

# Aplicar filtros
df_filtered = df[df["ano"] == ano_selecionado]
if tipo_instalacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_instalacao"] == tipo_instalacao_selecionado]
if perfil_carga_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["perfil_carga"] == perfil_carga_selecionado]
if sentido_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["sentido"] == sentido_selecionado]
if tipo_navegacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_navegacao"] == tipo_navegacao_selecionado]
if uf_origem_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["uf_origem"] == uf_origem_selecionado]

# Agregar dados por ano
df_summary = df_filtered.groupby("ano", as_index=False)["movimentacao_total_t"].sum()

# Exibir tabela de dados agregados
st.subheader("Totais de Movimentação Portuária")
st.dataframe(df_summary)
