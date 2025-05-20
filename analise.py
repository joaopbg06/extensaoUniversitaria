import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações  iniciais
st.set_page_config(page_title="Dashboard de residuos coletados", page_icon="☢️", layout="wide")

# Carregar dados
df_soma = pd.read_excel('somas_total_2013_2024.xlsx')
df_tipos = pd.read_excel('tipo_residuos_total.xlsx')
df_filtro = df_tipos[df_tipos['tipo_residuo'] != 'total_geral']


def aplicar_estilo():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
aplicar_estilo()


st.sidebar.header("Selecione os Filtros")

tipo_residuo = st.sidebar.multiselect(
    "Tipos de resíduo",
    # Seleciona os 10 maiores tipos de resíduos com base em uma coluna numérica relevante
    options=df_filtro.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Define como padrão os mesmos 10 maiores tipos
    default=df_filtro.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Chave única
    key='tipo'
)

ano = st.sidebar.slider(
    'Faixa de tempo em anos',
    min_value=min(df_soma['ano']),
    max_value=max(df_soma['ano']),
    value=(min(df_soma['ano']),max(df_soma['ano']))
)

colunas_ano = [f'total_{a}' for a in range(ano[0], ano[1] + 1) if a != 2022]

df_selecao_tipos = df_tipos.query(f"tipo_residuo in @tipo_residuo")[colunas_ano]
df_selecao_tipos_setor = df_tipos.query(f"tipo_residuo in @tipo_residuo")
df_selecao_soma = df_soma.query('@ano[0] <= ano <= @ano[1]')


def Home():
    st.title('Coletas de lixo de 2013 a 2024')

    total_vendas = df_selecao_soma['soma_total'].sum()

    st.metric('Total coletado', value=f"{total_vendas:.2f}", border=True)
    
    maior_residuo = df_selecao_soma['soma_total'].max()
    menor_residuo = df_selecao_soma['soma_total'].min()

    if ano != (2022, 2022):
        qual_ano_1 = df_selecao_soma['ano'][df_selecao_soma['soma_total'] == maior_residuo].iloc[0]
        qual_ano_2 = df_selecao_soma['ano'][df_selecao_soma['soma_total'] == menor_residuo].iloc[0]

        metric1, metric2 = st.columns(2)
        with metric1:
            st.metric(f'De acordo com a faixa o maior número de residuo coletado é do ano {qual_ano_1} com:', value=f"{maior_residuo:.2f}", border=True )
        with metric2:
            st.metric(f'De acordo com a faixa o menor número de residuo coletado é do ano {qual_ano_2} com:', value=f"{menor_residuo:.2f}", border=True )

def Graficos():
    
    df_selecao_tipos['total_anos'] = df_selecao_tipos.iloc[:, 1:].select_dtypes(include='number').sum(axis=1)
    df_selecao_tipos['tipo_residuo'] = df_tipos['tipo_residuo']

    df_selecao_tipos_setor['tipo_residuo'] = df_tipos['tipo_residuo']

    fig_barras = px.bar(    
        df_selecao_tipos,
        x="total_anos",
        y="tipo_residuo",
        color="tipo_residuo",
        title="Quantidade de Resíduos de todos os anos"
    )

    fig_linha = px.line(
        df_selecao_soma.groupby(["ano"]).sum(numeric_only=True).reset_index(),
        x= 'ano',
        y='soma_total',
        title='Total coletado ao longo dos anos'
    )


    fig_pie1 = px.pie(
        df_selecao_tipos_setor.nlargest(5, 'total_2013'),
        names='tipo_residuo',
        values='total_2013',
        color='tipo_residuo',
        title='Divição de tipos de residuo no ano de 2013'
    )

    fig_pie2 = px.pie(
        df_selecao_tipos_setor.nlargest(5, 'total_2020'),
        names='tipo_residuo',
        values='total_2020',
        color='tipo_residuo',
        title='Divição de tipos de residuo no ano de 2020'
    )


    
    setor1, setor2 = st.columns(2)
    with setor1:
        st.plotly_chart(fig_pie1,  use_container_width=True)
    with setor2:
        st.plotly_chart(fig_pie2,  use_container_width=True)

    
    graf1, graf2= st.columns(2)
    with graf1:
        st.plotly_chart(fig_barras,  use_container_width=True)
    with graf2:
        st.plotly_chart(fig_linha,  use_container_width=True)

Home()
Graficos()

# python -m streamlit run analise.py



