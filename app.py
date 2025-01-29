import streamlit as st
import pandas as pd
import plotly.express as px

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

# Seleção de Ano
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].unique()))

# Filtrar dados com base no ano selecionado
df_filtered = df[df["ano"] == ano_selecionado]

# Exibir tabela de dados
st.subheader(f"Dados para o ano {ano_selecionado}")
st.dataframe(df_filtered)


