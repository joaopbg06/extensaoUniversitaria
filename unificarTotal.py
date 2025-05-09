import pandas as pd

# 1) Carregar o DataFrame unificado com os anos de 2013 a 2020
df_unificado = pd.read_excel('tipo_residuos_total.xlsx')

# 2) Carregar os DataFrames dos anos de 2021, 2023 e 2024
df2021 = pd.read_excel('./BaseLimpo/2021_coleta_tipos_residuos.xlsx')
df2023 = pd.read_excel('./BaseLimpo/2023_coleta_tipos_residuos.xlsx')
df2024 = pd.read_excel('./BaseLimpo/2024_coleta_tipos_residuos.xlsx')

# 3) Somar os totais para os anos de 2013 a 2020
somas_2013_2020 = {
    'ano': [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    'soma_total': [
        df_unificado['total_2013'].sum(),
        df_unificado['total_2014'].sum(),
        df_unificado['total_2015'].sum(),
        df_unificado['total_2016'].sum(),
        df_unificado['total_2017'].sum(),
        df_unificado['total_2018'].sum(),
        df_unificado['total_2019'].sum(),
        df_unificado['total_2020'].sum()
    ]
}

# 4) Somar os totais para os anos de 2021, 2023 e 2024
soma_2021 = df2021['total_2021'].sum()
soma_2023 = df2023['total_2023'].sum()
soma_2024 = df2024['total_2024'].sum()

# Adicionar as somas de 2021, 2023 e 2024 à lista de somas
somas_2013_2020['ano'] += [2021, 2023, 2024]
somas_2013_2020['soma_total'] += [soma_2021, soma_2023, soma_2024]

# 5) Criar o DataFrame final com as somas
df_somas = pd.DataFrame(somas_2013_2020)

# 6) Salvar o DataFrame com as somas em um arquivo Excel
df_somas.to_excel('somas_total_2013_2024.xlsx', index=False)

print("Arquivo com as somas de 2013 a 2024 foi gerado com sucesso!")
