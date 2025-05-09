import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações  iniciais
st.set_page_config(page_title="Dashboard de Vendas", page_icon="☢️", layout="wide")

# Carregar dados
df = pd.read_excel('./BaseLimpo/2013_coleta_tipos_residuos.xlsx')


# FILTROS
# Sidebar
st.sidebar.header("Selecione os Filtros")

# Filtro por loja
tipo_residuo = st.sidebar.multiselect(
    "Tipos de resíduo",
    # Opções do filto
    options=df["tipo_residuo"].unique(),
    # Opção que vem como por padrão
    default=df["tipo_residuo"].unique(),
    # Chave única
    key='tipo'
)


# Filtrar o Dataframe com as opções selecionadas
df_selecao = df.query("tipo_residuo in @tipo_residuo")

# Graficos e na função da página
def Home():
    st.title('Coletas de lixo em 2013')

    total_vendas = df_selecao['total_2013'].sum()
    media = df_selecao['total_2013'].mean()
    mediana = df_selecao['total_2013'].median()

    total1, total2, total3= st.columns(3)
    with total1:
        # Apresentrar indicadores rápidos
        st.metric('Total coletado', value=int(total_vendas))
    with total2:
        st.metric('Média de coleta ao ano', value=f"{media:.1f}")
    with total3:
        st.metric('Mediana de coleta ao ano', value=int(mediana))

    st.markdown('- - -')

df_melted = pd.melt(
    df_selecao,
    id_vars=['tipo_residuo'],   # Coluna que será mantida
    var_name='Mês',             # Nova coluna com os nomes dos meses
    value_name='Quantidade'     # Nova coluna com os valores
)


def Graficos():
    # Criar um grafico de barras
    # Mostrando a quant de produtos por lojas

    fig_barras = px.bar(
        df_melted,
        x="Mês",
        y="Quantidade",
        color="tipo_residuo",
        barmode="group",
        title="Quantidade de Resíduos por Mês"
    )
    #Grafico de linha
    # Total de vendas por Loja

    fig_linha = px.line(
        df_selecao.groupby(["tipo_residuo"]).sum(numeric_only=True).reset_index(),
        x='tipo_residuo',
        y= 'total_2013',
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

# python -m streamlit run projeto.py