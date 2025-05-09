import pandas as pd

# Carregar os DataFrames
df2013 = pd.read_excel('./BaseLimpo/2013_coleta_tipos_residuos.xlsx')
df2014 = pd.read_excel('./BaseLimpo/2014_coleta_tipos_residuos.xlsx')
df2015 = pd.read_excel('./BaseLimpo/2015_coleta_tipos_residuos.xlsx')
df2016 = pd.read_excel('./BaseLimpo/2016_coleta_tipos_residuos.xlsx')
df2017 = pd.read_excel('./BaseLimpo/2017_coleta_tipos_residuos.xlsx')
df2018 = pd.read_excel('./BaseLimpo/2018_coleta_tipos_residuos.xlsx')
df2019 = pd.read_excel('./BaseLimpo/2019_coleta_tipos_residuos.xlsx')
df2020 = pd.read_excel('./BaseLimpo/2020_coleta_tipos_residuos.xlsx')
df2021 = pd.read_excel('./BaseLimpo/2021_coleta_tipos_residuos.xlsx')
df2023 = pd.read_excel('./BaseLimpo/2023_coleta_tipos_residuos.xlsx')
df2024 = pd.read_excel('./BaseLimpo/2024_coleta_tipos_residuos.xlsx')

# Criar uma lista com os DataFrames, excluindo o de 2022
dfs = [df2013, df2014, df2015, df2016, df2017, df2018, df2019, df2020,]

# Inicializar o DataFrame final com o primeiro DataFrame (df2013)
df_final = df2013[['tipo_residuo', 'total_2013']]

# Realizar a junção com os outros DataFrames, exceto o de 2022
for i, df in enumerate(dfs[1:], start=2014):
    if i < 2022:
        coluna_nome = f'total_{i}'
        
        # Realizar o merge (junção) com base na coluna 'tipo_residuo'
        df_final = pd.merge(df_final, df[['tipo_residuo', coluna_nome]], on='tipo_residuo', how='outer')


# Salvar o DataFrame final em um arquivo Excel
df_final.to_excel('tipo_residuos_total.xlsx', index=False)

print("Arquivo Excel com as colunas unificadas foi gerado com sucesso!")
