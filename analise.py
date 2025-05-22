import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go


# Configurações  iniciais
st.set_page_config(page_title="Dashboard de Residuos", page_icon="☢️", layout="wide")

# Carregar dados
df_soma = pd.read_excel('./DF/somas_total_2013_2024.xlsx')
df_tipos = pd.read_excel('./DF/tipo_residuos_total.xlsx')
df_soma_mensal = pd.read_excel('./DF/total_mensal_fixed.xlsx')
df_soma_mensal_estimativa = pd.read_excel('./DF/total_mensal_fixed_ESTIMATIVA.xlsx')
df_previcao = pd.read_excel('./DF/previsoes_modelos.xlsx')

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

meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
colunas_meses_anos = [f'{mes}/{ i - 2000}' for i in range(ano[0], ano[1] + 1)  if i != 2022 for mes in meses ]
colunas_meses_anos_estimativa = [f'{mes}/{ i - 2000}' for i in range(ano[0], ano[1] + 1)  if i <= 2020 for mes in meses ]


df_selecao_soma_mensal = df_soma_mensal[colunas_meses_anos]
df_selecao_soma_mensal_long = pd.melt(
    df_selecao_soma_mensal,
    var_name='meses/ano',   
    value_name='total_geral'    
)

df_selecao_soma_mensal_estimativa = df_soma_mensal_estimativa[colunas_meses_anos_estimativa]
df_selecao_soma_mensal_estimativa_long = pd.melt(
    df_selecao_soma_mensal_estimativa,
    var_name='meses/ano',   
    value_name='total_geral'    
)


meses_traducao = {
    'jan': 'jan', 'fev': 'feb', 'mar': 'mar', 'abr': 'apr',
    'mai': 'may', 'jun': 'jun', 'jul': 'jul', 'ago': 'aug',
    'set': 'sep', 'out': 'oct', 'nov': 'nov', 'dez': 'dec'
}

df_selecao_soma_mensal_long['meses/ano'] = df_selecao_soma_mensal_long['meses/ano'].replace(meses_traducao, regex=True)
df_selecao_soma_mensal_long['meses/ano'] = pd.to_datetime(df_selecao_soma_mensal_long['meses/ano'], format='%b/%y')

df_selecao_soma_mensal_estimativa_long['meses/ano'] = df_selecao_soma_mensal_estimativa_long['meses/ano'].replace(meses_traducao, regex=True)
df_selecao_soma_mensal_estimativa_long['meses/ano'] = pd.to_datetime(df_selecao_soma_mensal_estimativa_long['meses/ano'], format='%b/%y')

df_selecao_tipos = df_tipos.query(f"tipo_residuo in @tipo_residuo")[colunas_ano]
df_selecao_tipos_setor = df_tipos.query(f"tipo_residuo in @tipo_residuo")
df_selecao_soma = df_soma.query('@ano[0] <= ano <= @ano[1]')


st.write(df_selecao_soma_mensal_estimativa_long)
st.write(df_previcao)




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
            st.metric(f'A maior coleta foi de {qual_ano_1} com:', value=f"{maior_residuo:.2f}", border=True )
        with metric2:
            st.metric(f'A menor coleta foi de {qual_ano_2} com:', value=f"{menor_residuo:.2f}", border=True )

def Graficos():

    cores = {
    'domiciliar': '#0068C9',          # azul base
    'entulho_mecanizado': '#74B537',  # verde base
    'diversos': '#E15759',             # vermelho vibrante
    'ecoponto': '#F28E2B',             # laranja
    'piscinoes': '#9467BD',            # roxo
    'esgoto': '#FFC20A',               # amarelo brilhante
    'corregos': '#8C564B',             # marrom
    'varricao_manual': '#E377C2',      # rosa/magenta
    'feixa_live': '#7F7F7F',           # cinza escuro
    'coleta_seletiva': '#17BECF',      # turquesa
}

    df_selecao_tipos['total_anos'] = df_selecao_tipos.iloc[:, 1:].select_dtypes(include='number').sum(axis=1)
    df_selecao_tipos['tipo_residuo'] = df_tipos['tipo_residuo']

    df_selecao_tipos_setor['tipo_residuo'] = df_tipos['tipo_residuo']

    fig_barras = px.bar(    
        df_selecao_tipos,
        x="total_anos",
        y="tipo_residuo",
        color="tipo_residuo",
        title="Quantidade de Resíduos de todos os anos",
        color_discrete_map=(cores)
    )

    fig_linha = px.line(
        df_selecao_soma_mensal_long,
        x= 'meses/ano',
        y='total_geral',
        title='Total coletado ao longo dos anos',
        
    )   

    fig_pie1 = px.pie(
        df_selecao_tipos_setor.nlargest(5, 'total_2013'),
        names='tipo_residuo',
        values='total_2013',
        color='tipo_residuo',
        color_discrete_map=(cores),
        title='Divição de tipos de residuo no ano de 2013'
    )

    fig_pie2 = px.pie(
        df_selecao_tipos_setor.nlargest(5, 'total_2020'),
        names='tipo_residuo',
        values='total_2020',
        color='tipo_residuo',
        color_discrete_map=(cores),
        title='Divição de tipos de residuo no ano de 2020'
    )

    fig_linha_previcao = go.Figure()

    fig_linha_previcao.add_trace(go.Scatter(
        x=df_selecao_soma_mensal_estimativa_long['meses/ano'], 
        y=df_selecao_soma_mensal_estimativa_long['total_geral'], 
        mode='lines', 
        name='Série 1'
        ))
    
    fig_linha_previcao.add_trace(go.Scatter(
        x=df_previcao['ds'], 
        y=df_previcao['Previsao_ARIMA'], 
        mode='lines', 
        name='Série 2',
        line=dict(dash='dash')  # Define a linha como traçada
    ))


    setor1, setor2 = st.columns(2)
    with setor1:
        st.plotly_chart(fig_pie1,  use_container_width=True)
    with setor2:
        st.plotly_chart(fig_pie2,  use_container_width=True)

    
    # graf1, graf2= st.columns(2)
    # with graf1:
    st.plotly_chart(fig_barras,  use_container_width=True)
    # with graf2:
    st.plotly_chart(fig_linha,  use_container_width=True)

    st.plotly_chart(fig_linha_previcao,  use_container_width=True)

    
Home()
Graficos()

# python -m streamlit run analise.py



