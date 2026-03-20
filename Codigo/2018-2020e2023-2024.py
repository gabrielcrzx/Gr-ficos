import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 1. Carregar os dados (ignorando as 4 primeiras linhas e o total no final)
# 2018-2020
df_valor = pd.read_csv('https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/ValoresRegiao2018-2020.csv', sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')
df_qtd = pd.read_csv('https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/ComplexidadeRegiao2018-2020.csv', sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')
# 2023-2024
df_valor2 = pd.read_csv('https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/ValoresRegiao2023-2024.csv', sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')
df_qtd2 = pd.read_csv('https://raw.githubusercontent.com/gabrielcrzx/Gr-ficos/main/arquivos_csv/ComplexidadeRegiao2023-2024.csv', sep=';', skiprows=4, skipfooter=1, engine='python', encoding='latin1')

# 2. Limpar os dados
def LimpezaDaColDinheiro(col):
    if col.dtype == 'object':
        return col.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.replace('-', '0', regex=False).astype(float)
    return col

def LimpezaDaQtd(col):
    if col.dtype == 'object':
        return col.str.replace('-', '0', regex=False).astype(float)
    return col

colunas_interesse = ['Atenção Básica', 'Média complexidade', 'Alta complexidade']

for col in colunas_interesse + ['Total']:
    if col not in df_valor.columns: df_valor[col] = 0.0
    if col not in df_valor2.columns: df_valor2[col] = 0.0
    if col not in df_qtd.columns: df_qtd[col] = 0.0
    if col not in df_qtd2.columns: df_qtd2[col] = 0.0

# limpeza
for col in colunas_interesse + ['Total']:
    df_valor[col] = LimpezaDaColDinheiro(df_valor[col])
    df_qtd[col] = LimpezaDaQtd(df_qtd[col])
    
    df_valor2[col] = LimpezaDaColDinheiro(df_valor2[col])
    df_qtd2[col] = LimpezaDaQtd(df_qtd2[col])

# 3. Filtrar apenas as linhas de Região
df_valor_regioes = df_valor[df_valor['Região/UF'].str.startswith('Região')].copy()
df_qtd_regioes = df_qtd[df_qtd['Região/UF'].str.startswith('Região')].copy()

df_valor_regioes2 = df_valor2[df_valor2['Região/UF'].str.startswith('Região')].copy()
df_qtd_regioes2 = df_qtd2[df_qtd2['Região/UF'].str.startswith('Região')].copy()

df_valor_regioes['Região/UF'] = df_valor_regioes['Região/UF'].str.replace('Região ', '')
df_qtd_regioes['Região/UF'] = df_qtd_regioes['Região/UF'].str.replace('Região ', '')

df_valor_regioes2['Região/UF'] = df_valor_regioes2['Região/UF'].str.replace('Região ', '')
df_qtd_regioes2['Região/UF'] = df_qtd_regioes2['Região/UF'].str.replace('Região ', '')

# 4. Calcular as Médias por Complexidade (Valor / Quantidade)
df_media = df_valor_regioes.copy()
df_media2 = df_valor_regioes2.copy()

# Médias 2018-2020
df_media['Média Baixa'] = np.where(df_qtd_regioes['Atenção Básica'] > 0, df_valor_regioes['Atenção Básica'] / df_qtd_regioes['Atenção Básica'], 0)
df_media['Média Média'] = np.where(df_qtd_regioes['Média complexidade'] > 0, df_valor_regioes['Média complexidade'] / df_qtd_regioes['Média complexidade'], 0)
df_media['Média Alta'] = np.where(df_qtd_regioes['Alta complexidade'] > 0, df_valor_regioes['Alta complexidade'] / df_qtd_regioes['Alta complexidade'], 0)

# Médias 2023-2024
df_media2['Média Baixa'] = np.where(df_qtd_regioes2['Atenção Básica'] > 0, df_valor_regioes2['Atenção Básica'] / df_qtd_regioes2['Atenção Básica'], 0)
df_media2['Média Média'] = np.where(df_qtd_regioes2['Média complexidade'] > 0, df_valor_regioes2['Média complexidade'] / df_qtd_regioes2['Média complexidade'], 0)
df_media2['Média Alta'] = np.where(df_qtd_regioes2['Alta complexidade'] > 0, df_valor_regioes2['Alta complexidade'] / df_qtd_regioes2['Alta complexidade'], 0)

# A divisão/fator de (1 milhão).
fator = 1000000


# Gráfico (Matplotlib) - 2018-2020

plt.style.use('ggplot')
plt.figure(figsize=(10, 6))


plt.plot(df_qtd_regioes['Região/UF'], df_qtd_regioes['Atenção Básica'] / fator, marker='o', markersize=10, linewidth=3, label='Baixa Complexidade (Atenção Básica)')
plt.plot(df_qtd_regioes['Região/UF'], df_qtd_regioes['Média complexidade'] / fator, marker='o', markersize=10, linewidth=3, label='Média Complexidade')
#plt.plot(df_qtd_regioes['Região/UF'], df_qtd_regioes['Alta complexidade'] / fator, marker='o', markersize=10, linewidth=3, label='Alta Complexidade')

plt.title('Quantidade de Procedimentos por Região e Complexidade - (2018-2020)', fontsize=14)
plt.ylabel('Quantidade de Procedimento (milhões)')
plt.xlabel('Região')
plt.legend()
plt.tight_layout()
plt.show()


# Gráfico A (Plotly): Quantidade de Procedimentos - (2018-2020)

fig_linhas = go.Figure()


fig_linhas.add_trace(go.Scatter(x=df_qtd_regioes['Região/UF'], y=df_qtd_regioes['Atenção Básica'] / fator, 
mode='lines+markers', name='Baixa Complexidade', 
marker=dict(size=12), line=dict(width=3)))

fig_linhas.add_trace(go.Scatter(x=df_qtd_regioes['Região/UF'], y=df_qtd_regioes['Média complexidade'] / fator, 
mode='lines+markers', name='Média Complexidade',
marker=dict(size=12), line=dict(width=3)))

#fig_linhas.add_trace(go.Scatter(x=df_qtd_regioes['Região/UF'], y=df_qtd_regioes['Alta complexidade'] / fator, 
#mode='lines+markers', name='Alta Complexidade',
#marker=dict(size=12), line=dict(width=3)))

fig_linhas.update_layout(
title='Quantidade de Procedimentos por Região e Complexidade - (2018-2020)',
xaxis_title='Região',
yaxis_title='Quantidade Aprovada (milhões)',
template='plotly_white')
fig_linhas.show()


# Gráfico B (Plotly) - Valor Médio por Complexidade (2018-2020)
fig_barras = go.Figure()

fig_barras.add_trace(go.Bar(name='Baixa Complexidade', x=df_media['Região/UF'], y=df_media['Média Baixa'], text=df_media['Média Baixa'].round(2), textposition='auto'))
fig_barras.add_trace(go.Bar(name='Média Complexidade', x=df_media['Região/UF'], y=df_media['Média Média'], text=df_media['Média Média'].round(2), textposition='auto'))
#fig_barras.add_trace(go.Bar(name='Alta Complexidade', x=df_media['Região/UF'], y=df_media['Média Alta'], text=df_media['Média Alta'].round(2), textposition='auto'))

fig_barras.update_layout(
title='Custo Médio por Procedimento e Complexidade - (2018-2020)',
xaxis_title='Região',
yaxis_title='Valor Médio (R$)',
barmode='group', # Agrupa as barras lado a lado
template='plotly_white'
)
fig_barras.show()


# Gráfico (Matplotlib) - (2023-2024)

plt.figure(figsize=(10, 6))


plt.plot(df_qtd_regioes2['Região/UF'], df_qtd_regioes2['Atenção Básica'] / fator, marker='o', markersize=10, linewidth=3, label='Baixa Complexidade (Atenção Básica)')
plt.plot(df_qtd_regioes2['Região/UF'], df_qtd_regioes2['Média complexidade'] / fator, marker='o', markersize=10, linewidth=3, label='Média Complexidade')
#plt.plot(df_qtd_regioes2['Região/UF'], df_qtd_regioes2['Alta complexidade'] / fator, marker='o', markersize=10, linewidth=3, label='Alta Complexidade')

plt.title('Quantidade de Procedimentos por Região e Complexidade - (2023-2024)', fontsize=14)
plt.ylabel('Quantidade de Procedimento (milhões)')
plt.xlabel('Região')
plt.legend()
plt.tight_layout()
plt.show()


# Gráfico A (Plotly): Quantidade de Procedimentos - (2023-2024)

fig_linhas2 = go.Figure()


fig_linhas2.add_trace(go.Scatter(x=df_qtd_regioes2['Região/UF'], y=df_qtd_regioes2['Atenção Básica'] / fator, 
mode='lines+markers', name='Baixa Complexidade', 
marker=dict(size=12), line=dict(width=3)))

fig_linhas2.add_trace(go.Scatter(x=df_qtd_regioes2['Região/UF'], y=df_qtd_regioes2['Média complexidade'] / fator, 
mode='lines+markers', name='Média Complexidade',
marker=dict(size=12), line=dict(width=3)))

#fig_linhas2.add_trace(go.Scatter(x=df_qtd_regioes2['Região/UF'], y=df_qtd_regioes2['Alta complexidade'] / fator, 
#mode='lines+markers', name='Alta Complexidade',
#marker=dict(size=12), line=dict(width=3)))

fig_linhas2.update_layout(
title='Quantidade de Procedimentos por Região e Complexidade - (2023-2024)',
xaxis_title='Região',
yaxis_title='Quantidade Aprovada (milhões)',
template='plotly_white')
fig_linhas2.show()



# Gráfico B (Plotly) - Valor Médio por Complexidade (2023-2024)
fig_barras2 = go.Figure()

fig_barras2.add_trace(go.Bar(name='Baixa Complexidade', x=df_media2['Região/UF'], y=df_media2['Média Baixa'], text=df_media2['Média Baixa'].round(2), textposition='auto'))
fig_barras2.add_trace(go.Bar(name='Média Complexidade', x=df_media2['Região/UF'], y=df_media2['Média Média'], text=df_media2['Média Média'].round(2), textposition='auto'))
#fig_barras2.add_trace(go.Bar(name='Alta Complexidade', x=df_media2['Região/UF'], y=df_media2['Média Alta'], text=df_media2['Média Alta'].round(2), textposition='auto'))

fig_barras2.update_layout(
title='Custo Médio por Procedimento e Complexidade - (2023-2024)',
xaxis_title='Região',
yaxis_title='Valor Médio (R$)',
barmode='group', 
template='plotly_white'
)
fig_barras2.show()