import pandas as pd

# 1. carregar

url_pop = 'https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/Populacao2018-2020e2024.csv' 
df_pop = pd.read_csv(url_pop, sep=';', skiprows=3, engine='python')

# Renomeando
df_pop.columns = ['Capital', 'Pop_2018', 'Pop_2019', 'Pop_2020', 'Pop_2024']
df_pop['Capital'] = df_pop['Capital'].str.strip()

lista_capitais = [
    'Rio Branco', 'Maceió', 'Macapá', 'Manaus', 'Salvador', 'Fortaleza',
    'Brasília', 'Vitória', 'Goiânia', 'São Luís', 'Cuiabá', 'Campo Grande',
    'Belo Horizonte', 'Belém', 'João Pessoa', 'Curitiba', 'Recife',
    'Teresina', 'Rio de Janeiro', 'Natal', 'Porto Alegre', 'Porto Velho',
    'Boa Vista', 'Florianópolis', 'São Paulo', 'Aracaju', 'Palmas'
]

# Filtrar e limpar os números
df_pop_capitais = df_pop[df_pop['Capital'].isin(lista_capitais)].copy()
for ano in ['Pop_2018', 'Pop_2019', 'Pop_2020', 'Pop_2024']:
    df_pop_capitais[ano] = pd.to_numeric(df_pop_capitais[ano], errors='coerce')

# o IBGE não deu 2023, usar 2024
df_pop_capitais['Pop_2023'] = df_pop_capitais['Pop_2024']


# 2. carregar os anos do datasus

url_sus_18_20 = 'https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/2018-2020.csv'
url_sus_23_24 = 'https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/2023-2024.csv'

# Lendo o arquivo de 2018 a 2020
df_sus_18_20 = pd.read_csv(url_sus_18_20, sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')
df_sus_18_20.columns = ['Capital', 'SUS_2018', 'SUS_2019', 'SUS_2020', 'Total_18_20']
df_sus_18_20['Capital'] = df_sus_18_20['Capital'].str.replace(r'^\d+\s*', '', regex=True).str.strip()

# Lendo o arquivo de 2023 a 2024
df_sus_23_24 = pd.read_csv(url_sus_23_24, sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')
df_sus_23_24.columns = ['Capital', 'SUS_2023', 'SUS_2024', 'Total_23_24']
df_sus_23_24['Capital'] = df_sus_23_24['Capital'].str.replace(r'^\d+\s*', '', regex=True).str.strip()



colunas_18_20 = ['SUS_2018', 'SUS_2019', 'SUS_2020', 'Total_18_20']
for col in colunas_18_20:
    df_sus_18_20[col] = pd.to_numeric(df_sus_18_20[col].astype(str).str.replace('-', '0', regex=False), errors='coerce')

colunas_23_24 = ['SUS_2023', 'SUS_2024', 'Total_23_24']
for col in colunas_23_24:
    df_sus_23_24[col] = pd.to_numeric(df_sus_23_24[col].astype(str).str.replace('-', '0', regex=False), errors='coerce')



# Juntando tudo na mesma tabela
df_final = pd.merge(df_pop_capitais, df_sus_18_20, on='Capital', how='inner')
df_final = pd.merge(df_final, df_sus_23_24, on='Capital', how='inner')

# Fazendo os cálculos Per Capita ano a ano (Gasto / População)
df_final['PerCapita_2018'] = (df_final['SUS_2018'] / df_final['Pop_2018']).round(2)
df_final['PerCapita_2019'] = (df_final['SUS_2019'] / df_final['Pop_2019']).round(2)
df_final['PerCapita_2020'] = (df_final['SUS_2020'] / df_final['Pop_2020']).round(2)
df_final['PerCapita_2023'] = (df_final['SUS_2023'] / df_final['Pop_2023']).round(2)
df_final['PerCapita_2024'] = (df_final['SUS_2024'] / df_final['Pop_2024']).round(2)

# 4. criar a planilha

colunas_planilha = [
    'Capital', 
    'PerCapita_2018', 'PerCapita_2019', 'PerCapita_2020', 
    'PerCapita_2023', 'PerCapita_2024'
]
df_planilha = df_final[colunas_planilha]

# ordem alfabética
df_planilha = df_planilha.sort_values(by='Capital')
# EXPORTAR PARA CSV
df_planilha.to_csv('Taxa_Per_Capita_Por_Ano.csv', sep=';', index=False, encoding='utf-8-sig')
