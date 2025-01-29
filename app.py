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
tipo_instalacao = st.sidebar.multiselect("Tipo de Instalação", df["tipo_instalacao"].unique(), default=df["tipo_instalacao"].unique())
perfil_carga = st.sidebar.multiselect("Perfil da Carga", df["perfil_carga"].unique(), default=df["perfil_carga"].unique())
sentido = st.sidebar.multiselect("Sentido", df["sentido"].unique(), default=df["sentido"].unique())
tipo_navegacao = st.sidebar.multiselect("Tipo de Navegação", df["tipo_navegacao"].unique(), default=df["tipo_navegacao"].unique())
uf_origem = st.sidebar.multiselect("UF Origem", df["uf_origem"].unique(), default=df["uf_origem"].unique())

# Filtrar dados com base nos filtros selecionados
df_filtered = df[
    (df["ano"] == ano_selecionado) &
    (df["tipo_instalacao"].isin(tipo_instalacao)) &
    (df["perfil_carga"].isin(perfil_carga)) &
    (df["sentido"].isin(sentido)) &
    (df["tipo_navegacao"].isin(tipo_navegacao)) &
    (df["uf_origem"].isin(uf_origem))
]

# Agregar dados
df_summary = df_filtered.groupby(["ano", "tipo_instalacao", "perfil_carga", "sentido", "tipo_navegacao", "uf_origem"], as_index=False)["movimentacao_total_t"].sum()

# Exibir tabela de dados agregados
st.subheader("Resumo dos Dados Filtrados")
st.dataframe(df_summary)
