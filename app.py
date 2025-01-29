import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
@st.cache
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
anos = st.sidebar.multiselect("Selecione o Ano", df["ano"].unique(), default=df["ano"].unique())
tipo_instalacao = st.sidebar.multiselect("Tipo de Instalação", df["tipo_instalacao"].unique(), default=df["tipo_instalacao"].unique())
perfil_carga = st.sidebar.multiselect("Perfil da Carga", df["perfil_carga"].unique(), default=df["perfil_carga"].unique())

# Aplicar filtros
df_filtered = df[df["ano"].isin(anos) & df["tipo_instalacao"].isin(tipo_instalacao) & df["perfil_carga"].isin(perfil_carga)]

# Gráficos
fig_movimentacao = px.bar(df_filtered, x="ano", y="movimentacao_total_t", color="tipo_instalacao", title="Movimentação Portuária por Ano")
st.plotly_chart(fig_movimentacao)

fig_perfil = px.pie(df_filtered, names="perfil_carga", values="movimentacao_total_t", title="Distribuição da Carga")
st.plotly_chart(fig_perfil)

# Tabela de dados
st.subheader("Dados Filtrados")
st.dataframe(df_filtered)

# Exportar dados como TXT
st.subheader("Exportar Dados Filtrados")
df_txt = df_filtered.to_csv(sep='\t', index=False)
st.download_button(label="Baixar Dados como TXT", data=df_txt, file_name="dados_filtrados.txt", mime="text/plain")

