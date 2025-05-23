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

# Criar um filtro para retirar o total_geral para fazer somas
df_filtro = df_tipos[df_tipos['tipo_residuo'] != 'total_geral']

# Style
def aplicar_estilo():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
aplicar_estilo()

# Sidebar
st.sidebar.header("Selecione os Filtros")

# Filtro do tipo de residuo
tipo_residuo = st.sidebar.multiselect(
    "Tipos de resíduo",
    # Seleciona os 10 maiores tipos de resíduos com base em uma coluna numérica relevante
    options=df_filtro.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Define como padrão os mesmos 10 maiores tipos
    default=df_filtro.nlargest(10, 'total_anos')['tipo_residuo'],  
    # Chave única
    key='tipo'
)

# Filtro para o ano
ano = st.sidebar.slider(
    'Faixa de tempo em anos',
    min_value=min(df_soma['ano']),
    max_value=max(df_soma['ano']),
    value=(min(df_soma['ano']),max(df_soma['ano']))
)

# Lista para configuração

meses = [
    'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
meses_traducao = {
    'jan': 'jan', 'fev': 'feb', 'mar': 'mar', 'abr': 'apr',
    'mai': 'may', 'jun': 'jun', 'jul': 'jul', 'ago': 'aug',
    'set': 'sep', 'out': 'oct', 'nov': 'nov', 'dez': 'dec'
}
cores = {
    'domiciliar': '#0068C9',          
    'entulho_mecanizado': '#74B537',  
    'diversos': '#E15759',            
    'ecoponto': '#F28E2B',             
    'piscinoes': '#9467BD',            
    'esgoto': '#FFC20A',               
    'corregos': '#8C564B',            
    'varricao_manual': '#E377C2',      
    'feixa_live': '#7F7F7F',           
    'coleta_seletiva': '#17BECF',      
}

# Aplicar filtro do tipo de residuo e do ano entre colunas
colunas_ano = [f'total_{a}' for a in range(ano[0], ano[1] + 1) if a != 2022]
df_selecao_tipos = df_tipos.query(f"tipo_residuo in @tipo_residuo")[colunas_ano]
# Restaurando as colunas perdidas
df_selecao_tipos['total_anos'] = df_tipos['total_anos']
df_selecao_tipos['tipo_residuo'] = df_tipos['tipo_residuo']

# Filtrar o df da soma pelo o tempo
df_selecao_soma = df_soma.query('@ano[0] <= ano <= @ano[1]')

# Aplicar o filtro do df do grafico de setor
df_selecao_tipos_setor = df_tipos.query(f"tipo_residuo in @tipo_residuo")


# Ajustar o df da soma mensal de 2013 - 2024
colunas_meses_anos = [f'{mes}/{ i - 2000}' for i in range(ano[0], ano[1] + 1)  if i != 2022 for mes in meses ]
df_selecao_soma_mensal = df_soma_mensal[colunas_meses_anos]

df_selecao_soma_mensal_long = pd.melt(
    df_selecao_soma_mensal,
    var_name='meses/ano',   
    value_name='total_geral'    
)

df_selecao_soma_mensal_long['meses/ano'] = df_selecao_soma_mensal_long['meses/ano'].replace(meses_traducao, regex=True)
df_selecao_soma_mensal_long['meses/ano'] = pd.to_datetime(df_selecao_soma_mensal_long['meses/ano'], format='%b/%y')


# Ajustar o df da soma mensal de 2013 - 2020
colunas_meses_anos_estimativa = [f'{mes}/{ i - 2000}' for i in range(ano[0], ano[1] + 1)  if i <= 2020 for mes in meses ]
df_selecao_soma_mensal_estimativa = df_soma_mensal_estimativa[colunas_meses_anos_estimativa]

df_selecao_soma_mensal_estimativa_long = pd.melt(
    df_selecao_soma_mensal_estimativa,
    var_name='meses/ano',   
    value_name='total_geral'    
)

df_selecao_soma_mensal_estimativa_long['meses/ano'] = df_selecao_soma_mensal_estimativa_long['meses/ano'].replace(meses_traducao, regex=True)
df_selecao_soma_mensal_estimativa_long['meses/ano'] = pd.to_datetime(df_selecao_soma_mensal_estimativa_long['meses/ano'], format='%b/%y')




# Funções para exibir

# Números gerais
def Home():
    st.title('Coletas de lixo de 2013 a 2024')

    total_vendas = df_selecao_soma['soma_total'].sum()

    st.metric('Total coletado', value=f"{total_vendas:.2f}", border=True)

# Graficos do total gerado por mês com previções de 2021 - 2025. Comparando com os dados que já existem
def previsao():

    fig_linha = px.line(
        df_selecao_soma_mensal_long,
        x= 'meses/ano',
        y='total_geral',
        title='Total coletado ao longo dos anos',
    )
    
    fig_linha.update_layout(
        xaxis=dict(showgrid=True),  # Grade vertical
        yaxis=dict(showgrid=True),  # Grade horizontal
        template='plotly_white'  # Tema claro para destacar as grades
    )


    
    fig_linha_previcao = go.Figure()

    fig_linha_previcao.add_trace(go.Scatter(
        x=df_selecao_soma_mensal_estimativa_long['meses/ano'], 
        y=df_selecao_soma_mensal_estimativa_long['total_geral'], 
        mode='lines', 
        name='Histórico', 
        line=dict(color='#0068C9')
    ))
    
    fig_linha_previcao.add_trace(go.Scatter(
        x=df_previcao['ds'], 
        y=df_previcao['Previsao_ARIMA'], 
        mode='lines', 
        name='Previsão',
        line=dict(dash='dot',  color='#FF5733'),  # Define a linha como traçada
    ))
    
    fig_linha_previcao.update_layout(
        title= 'Total coletado ao longo dos anos com previsão',
        xaxis=dict(showgrid=True),  # Grade vertical
        yaxis=dict(showgrid=True),  # Grade horizontal
        template='plotly_white'  # Tema claro para destacar as grades
    )


    st.plotly_chart(fig_linha,  use_container_width=True)

    st.plotly_chart(fig_linha_previcao,  use_container_width=True)

# Grafico de barras que mostra os 10 maiores tipos de residuos coletados
def tipo_residuo_graficos():

    fig_barras = px.bar(    
        df_selecao_tipos,
        x="total_anos",
        y="tipo_residuo",
        color="tipo_residuo",
        title="Quantidade de Resíduos de todos os anos",
        color_discrete_map=(cores)
    )


    st.plotly_chart(fig_barras,  use_container_width=True)

# Gera 2 graficos de setor por um select para comparar proporções entre anos
def proporcao():

    select1, select2 = st.columns(2)
    with select1:
        ano_pie_1 = st.selectbox(
            'Selecione o Ano do gráfico Abaixo:',
            options=range(2013, 2021),
            index=0,
            key='pie1'
        )
    with select2:
        ano_pie_2 = st.selectbox(
            'Selecione o Ano do gráfico Abaixo:',
            options=[f'{x}' for x in range(2013, 2021) if x != ano_pie_1],
            index=6,
            key='pie2',
        )

    st.markdown('- - -')

    setor1, setor2 = st.columns(2)
    with setor1:

        fig_pie1 = px.pie(
            df_selecao_tipos_setor.nlargest(5, f'total_{ano_pie_1}'),
            names='tipo_residuo',
            values=f'total_{ano_pie_1}',
            color='tipo_residuo',
            color_discrete_map=(cores),
            title=f'Divição de tipos de residuo no ano de {ano_pie_1}'
        )

        st.plotly_chart(fig_pie1,  use_container_width=True)
    with setor2:


        fig_pie2 = px.pie(
            df_selecao_tipos_setor.nlargest(5, f'total_{ano_pie_2}'),
            names='tipo_residuo',
            values=f'total_{ano_pie_2}',
            color='tipo_residuo',
            color_discrete_map=(cores),
            title=f'Divição de tipos de residuo no ano de {ano_pie_2}'
        )

        st.plotly_chart(fig_pie2,  use_container_width=True)
    

Home()
previsao()
st.markdown('- - -')
proporcao()
st.markdown('- - -')
tipo_residuo_graficos()




# python -m streamlit run analise.py



