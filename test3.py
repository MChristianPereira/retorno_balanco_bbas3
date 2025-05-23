import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.style.use('dark_background')

df = pd.read_parquet('LucroLiquido.parquet')
df = df[(df['ticker'] == 'BBAS3')]
df = df.drop_duplicates(subset = ['valor'])
df['data'] = pd.to_datetime(df['data'])
datas_divulgacao_balancos = df['data']
# print(datas_divulgacao_balancos)

cotacoes = pd.read_parquet('cotacoes.parquet')
cotacoes = cotacoes[(cotacoes['ticker'] == 'BBAS3')]
cotacoes = cotacoes[['data', 'preco_fechamento_ajustado']].reset_index(drop = True)
cotacoes['data'] = pd.to_datetime(cotacoes['data'])
# print(cotacoes)

cotacoes_filtrado = []

for data in datas_divulgacao_balancos:
    dados_do_dia = cotacoes[(cotacoes['data'] == data)]
    cotacoes_filtrado.append(dados_do_dia)
    index_dados_o_dia = dados_do_dia.index

    dados_do_dia = cotacoes.iloc[index_dados_o_dia + 1]
    cotacoes_filtrado.append(dados_do_dia)

cotacoes = pd.concat(cotacoes_filtrado).reset_index(drop = True)
cotacoes['Retornos BBAS3'] = cotacoes['preco_fechamento_ajustado'].pct_change()

remove_rows = []

for linha in cotacoes.iterrows():
    if linha[0] %2 == 0:
        remove_rows.append(linha[0])

cotacoes = cotacoes[(~cotacoes.index.isin(remove_rows))].reset_index(drop = True)
cotacoes['Retornos BBAS3'] *= 100
cotacoes['Retornos BBAS3'] = cotacoes['Retornos BBAS3'].round(2)
print(cotacoes)

cores = []

for index, linha in cotacoes.iterrows():
    if linha['Retornos BBAS3'] >= 0:
        cores.append('#19C819')
    if linha['Retornos BBAS3'] < 0:
        cores.append('#E50000')

fig, ax = plt.subplots()
ax.tick_params(axis = 'x', labelsize = 18)
ax.tick_params(axis = 'y', labelsize = 18)
ax.yaxis.set_major_formatter(PercentFormatter())
ax.set_title('Retorno de BBAS3 após os resultados trimestrais', fontsize = 22, color = 'white')
ax.bar(cotacoes['data'], cotacoes['Retornos BBAS3'], color = cores, width = 80)
ax.set_facecolor('none')
ax.grid(True, color = 'gray', linestyle = '--', linewidth = 0.5)

plt.show()