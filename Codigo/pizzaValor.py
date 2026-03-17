import pandas as pd
import plotly.graph_objects as go

# 1. carregamento dos dados.

# Dados Financeiros 2018-2020
df_valor = pd.read_csv('ValoresRegiao2018-2020.csv', sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')
# Dados Financeiros 2023-2024
df_valor2 = pd.read_csv('ValoresRegiao2023-2024.csv', sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')

df_valor.rename(columns={df_valor.columns[0]: 'Regiao/UF'}, inplace=True)
df_valor2.rename(columns={df_valor2.columns[0]: 'Regiao/UF'}, inplace=True)

# 2. limpeza

def LimpezaDaColDinheiro(col):
    if col.dtype == 'object':
        return col.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.replace('-', '0', regex=False).astype(float)
    return col

# Aplicar limpeza
df_valor['Total'] = LimpezaDaColDinheiro(df_valor['Total'])
df_valor2['Total'] = LimpezaDaColDinheiro(df_valor2['Total'])

# Dividimos os valores por 1 bilhão
df_valor['Total_Bi'] = df_valor['Total'] / 1_000_000_000
df_valor2['Total_Bi'] = df_valor2['Total'] / 1_000_000_000

# Filtrar para pegar apenas as regiões
df_valor_regioes = df_valor[df_valor['Regiao/UF'].str.startswith('Regi')].copy()
df_valor_regioes['Regiao/UF'] = df_valor_regioes['Regiao/UF'].str.replace('Região ', '').str.replace('RegiÃ£o ', '')

df_valor_regioes2 = df_valor2[df_valor2['Regiao/UF'].str.startswith('Regi')].copy()
df_valor_regioes2['Regiao/UF'] = df_valor_regioes2['Regiao/UF'].str.replace('Região ', '').str.replace('RegiÃ£o ', '')

# Paleta de cores
cores_plotly = ['#EF553B', "#87CEEB", '#00CC96', '#AB63FA', '#FFA15A']


# 3. gráficos plotly

# Gráfico para 2018-2020
fig = go.Figure(data=[go.Pie(
labels=df_valor_regioes['Regiao/UF'], 
values=df_valor_regioes['Total_Bi'], 
textinfo='percent', 

# "Bi"
hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:.2f} Bilhões<br>Percentual: %{percent}<extra></extra>",
 marker=dict(colors=cores_plotly, line=dict(color='#FFFFFF', width=1))
)])

fig.update_layout(
title_text='Distribuição Financeira dos Valores aprovados por Região - (2018-2020)',
title_x=0.5, 
template='plotly_dark' 
)
fig.show()

# Gráfico para 2023-2024
fig2 = go.Figure(data=[go.Pie(
labels=df_valor_regioes2['Regiao/UF'], 
values=df_valor_regioes2['Total_Bi'], 
textinfo='percent', 
hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:.2f} Bilhões<br>Percentual: %{percent}<extra></extra>",
marker=dict(colors=cores_plotly, line=dict(color='#FFFFFF', width=1))
)])

fig2.update_layout(
title_text='Distribuição Financeira dos Valores aprovados por Região - (2023-2024)',
title_x=0.5,
template='plotly_dark'
)
fig2.show()
