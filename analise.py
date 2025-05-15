import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações  iniciais
st.set_page_config(page_title="Dashboard de residuos coletados", page_icon="☢️", layout="wide")

# Carregar dados
df_soma = pd.read_excel('somas_total_2013_2024.xlsx')
df_tipos = pd.read_excel('tipo_residuos_total.xlsx')

def aplicar_estilo():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
aplicar_estilo()
# FILTROS
# Sidebar   
st.sidebar.header("Selecione os Filtros")

tipo_residuo = st.sidebar.multiselect(
    "Tipos de resíduo",
    # Seleciona os 10 maiores tipos de resíduos com base em uma coluna numérica relevante
    options=df_tipos.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Define como padrão os mesmos 10 maiores tipos
    default=df_tipos.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Chave única
    key='tipo'
)

ano = st.sidebar.slider(
    'Faixa de tempo em anos',
    min_value=min(df_soma['ano']),
    max_value=max(df_soma['ano']),
    value=(min(df_soma['ano']),max(df_soma['ano']))
)

df_selecao_tipos = df_tipos.query("tipo_residuo in @tipo_residuo")

colunas_ano = [f'total_{a}' for a in range(ano[0], ano[1] + 1) if a != 2022]


df_selecao_tipos = df_selecao_tipos[colunas_ano]


df_selecao_soma = df_soma.query('@ano[0] <= ano <= @ano[1]')

# Graficos e na função da página
def Home():
    st.title('Coletas de lixo de 2013 a 2024')

    total_vendas = df_soma['soma_total'].sum()
    media = df_soma['soma_total'].mean()
    mediana = df_soma['soma_total'].median()

    total1, total2, total3= st.columns(3)
    with total1:
        # Apresentrar indicadores rápidos
        st.metric('Total coletado', value=f"{total_vendas:.2f}")
    with total2:
        st.metric('Média de coleta', value=f"{media:.2f}")
    with total3:
        st.metric('Mediana de coleta', value=f"{mediana:.2f}")

    st.markdown('- - -')

def Graficos():
    # Criar um grafico de barras
    # Mostrando a quant de produtos por lojas

    fig_barras = px.bar(
        df_selecao_tipos,
        x="total_2013",
        y="tipo_residuo",
        color="tipo_residuo",
        title="Quantidade de Resíduos por ano"
    )
    #Grafico de linha
    # Total de vendas por Loja

    fig_linha = px.line(
        df_selecao_soma.groupby(["ano"]).sum(numeric_only=True).reset_index(),
        x= 'ano',
        y='soma_total',
        title='Total de Vendas Por loja'

    )

    graf1, graf2 = st.columns(2)
    with graf1:
        st.plotly_chart(fig_barras,  use_container_width=True )
    with graf2:
        st.plotly_chart(fig_linha,  use_container_width=True )


def sideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu",
            options=['Home', 'Gráficos'],
            icons=['house', 'bar-chart'],
            default_index=0
        )

    if selecionado == 'Home':
        Home()
        Graficos()
    elif selecionado == 'Gráficos':
        Graficos()

sideBar()

# python -m streamlit run analise.py



