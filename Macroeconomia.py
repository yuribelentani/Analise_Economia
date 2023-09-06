from bcb import sgs
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from bcb import Expectativas
import pandas as pd
import yfinance as yf


st.title('Analise Macroeconômica de Indicadores')


# buscando dados relacionados ao IPCA
#importando usando o código do BC

df_ipca = sgs.get({'IPCA': '433'}, start = '2000-01-01')
df_ipca_1 = df_ipca
df_ipca = df_ipca.iloc[-12:]
fig_ipca = go.Figure()
fig_ipca.add_trace(go.Bar(name='ipca', x=df_ipca.index, y=df_ipca.iloc[:, 0], text=round(df_ipca.iloc[:, 0], 2),
                     textposition='inside'))
fig_ipca.update_layout(title='IPCA Mensal', xaxis_title="Meses", yaxis_title='Valor Mensal (%)')

st.plotly_chart(fig_ipca, use_container_width=True, width=1600, height=600)

st.markdown('---')

#buscando dados taxa SELIC

#importando usando o código do BC

df_selic = sgs.get({'SELIC': 432}, start = '2000-01-01')

#mostrar SELIC mensal em gráfico

fig_selic = go.Figure()
fig_selic.add_trace(go.Scatter(name='Taxa SELIC BACEN', x=df_selic.index , y=df_selic.SELIC, showlegend=False ))
fig_selic.update_layout(title = 'SELIC (%)', xaxis_title="Meses", yaxis_title = 'Taxa (%)' )
fig_selic.add_trace(go.Scatter(x=[df_selic.index[-1]],
                         y=[df_selic.iloc[-1, 0]],
                         text=[df_selic.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='top center',
                         showlegend=False))
st.plotly_chart(fig_selic, use_container_width=True, width=1600, height=600)

st.markdown('---')


#importando dados da divida Bruta/ PIB

df_divida = sgs.get({'Divida': 4536}, start = '2000-01-01')

#mostrar Divida Liquida em gráfico

fig_divida = go.Figure()
fig_divida.add_trace(go.Scatter(name='Dívida Líquida', x=df_divida.index , y=df_divida.Divida, showlegend=False))
fig_divida.update_layout(title = 'Dívida Líquia', xaxis_title="Anos", yaxis_title = 'Relação Dívida Líquida/ PIB (%)' )
fig_divida.add_trace(go.Scatter(x=[df_divida.index[-1]],
                         y=[df_divida.iloc[-1, 0]],
                         text=[df_divida.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='top center',
                         showlegend=False))
st.plotly_chart(fig_divida, use_container_width=True, width=1600, height=600)

#importando usando o código do BC

st.markdown('---')

df_conf_cons = sgs.get({'Confianca_do_Consumidor': 4393}, start = '2000-01-01')
#mostrar Confiança do Consumidor mensal em gráficos de barra

fig_cons = go.Figure()
fig_cons.add_trace(go.Scatter(name='Confiança do Consumidor', x=df_conf_cons.index , y=df_conf_cons.Confianca_do_Consumidor))
fig_cons.update_layout(title = 'Confiança do Consumidor (c/ Indicador Nível Pré Pandemia)', xaxis_title="Anos", yaxis_title = 'Taxa (%)', showlegend=False)

#traçar uma linha do nível antes da pandemia

fig_cons.add_hline(y =df_conf_cons['Confianca_do_Consumidor']['2020-02-01'],line_color="red", line_dash="dash")

fig_cons.add_trace(go.Scatter(x=[df_conf_cons.index[-1]],
                         y=[df_conf_cons.iloc[-1, 0]],
                         text=[df_conf_cons.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='top center',
                         showlegend=False))

st.plotly_chart(fig_cons, use_container_width=True, width=1600, height=600)

st.markdown('---')

st.subheader('Expectativa Mercado (Pesquisa Focus - BACEN)')
# Obter a data e hora atual
now = datetime.now()
# Extrair o ano da data atual
current_year = now.year
# Extrair o ano da data atual
current_month = now.month

expec = Expectativas()
#importando usando o código do BC

ep = expec.get_endpoint('ExpectativasMercadoAnuais')

ipca_expec_atual = ( ep.query()
 .filter(ep.Indicador == 'IPCA', ep.DataReferencia == current_year)
 .filter(ep.Data >= '2022-01-01')
 .filter(ep.baseCalculo == '0')
 .select(ep.Indicador, ep.Data, ep.Media, ep.Mediana, ep.DataReferencia)
 .collect()
  )


ipca_expec_futuro = ( ep.query()
 .filter(ep.Indicador == 'IPCA', ep.DataReferencia == current_year+1)
 .filter(ep.Data >= '2022-01-01')
 .filter(ep.baseCalculo == '0')
 .select(ep.Indicador, ep.Data, ep.Media, ep.Mediana, ep.DataReferencia)
 .collect()
  )

# Formata a coluna de Data para formato datetime

ipca_expec_atual['Data'] = pd.to_datetime(ipca_expec_atual['Data'], format = '%Y-%m-%d')
ipca_expec_futuro['Data'] = pd.to_datetime(ipca_expec_atual['Data'], format = '%Y-%m-%d')


#mostrar expectativa do mercado para o IPCA 2023 e 2024 em gráfico

fig_exp_ipca = go.Figure()
fig_exp_ipca.add_trace(go.Scatter(name= ('IPCA ' +  str(current_year)), x=ipca_expec_atual.Data , y=ipca_expec_atual.Mediana))
fig_exp_ipca.add_trace(go.Scatter(name=('IPCA ' +  str(current_year+1)) , x=ipca_expec_atual.Data , y=ipca_expec_futuro.Mediana))

fig_exp_ipca.update_layout(title = ('Expectativa IPCA ' +  str(current_year) + ' e ' + str(current_year+1)), xaxis_title="Anos", yaxis_title = 'Taxa (%)')

st.plotly_chart(fig_exp_ipca, use_container_width=True, width=1600, height=600)

st.markdown('---')

pib_expec_atual = (ep.query()
             .filter(ep.Indicador == 'PIB Total', ep.DataReferencia == current_year)
             .filter(ep.Data >= '2022-01-01')
             .filter(ep.baseCalculo == '0')
             .select(ep.Indicador, ep.Data, ep.Media, ep.Mediana, ep.DataReferencia)
             .collect()
             )
pib_expec_atual['Data'] = pd.to_datetime(pib_expec_atual['Data'], format='%Y-%m-%d')


pib_expec_futuro = (ep.query()
             .filter(ep.Indicador == 'PIB Total', ep.DataReferencia == current_year+1)
             .filter(ep.Data >= '2022-01-01')
             .filter(ep.baseCalculo == '0')
             .select(ep.Indicador, ep.Data, ep.Media, ep.Mediana, ep.DataReferencia)
             .collect()
             )
pib_expec_futuro['Data'] = pd.to_datetime(pib_expec_atual['Data'], format='%Y-%m-%d')

fig_exp_pib = go.Figure()
fig_exp_pib.add_trace(go.Scatter(name= ('PIB ' +  str(current_year)), x=pib_expec_atual.Data , y=pib_expec_atual.Mediana))
fig_exp_pib.add_trace(go.Scatter(name=('PIB ' +  str(current_year+1)) , x=pib_expec_atual.Data , y=pib_expec_futuro.Mediana))

fig_exp_pib.update_layout(title = ('Expectativa PIB ' +  str(current_year) + ' e ' + str(current_year+1)), xaxis_title="Anos", yaxis_title = 'Taxa (%)')

st.plotly_chart(fig_exp_pib, use_container_width=True, width=1600, height=600)


st.subheader('Análise de Crédito Total Concedido)')


df_credito = sgs.get({'Credito': '20631'}, start = '2011-01-01')
df_credito = df_credito[-24:]

acum_passado = df_credito.loc[(df_credito.index.month <= current_month) & (df_credito.index.year == current_year -1)].cumsum()
acum_atual = df_credito.loc[(df_credito.index.month <= current_month) & (df_credito.index.year ==  current_year)].cumsum()
delta = (acum_atual.iloc[-1] - acum_passado.iloc[-1])/acum_passado.iloc[-1]

#informando dados acumulados do ano atual e ano passado
col1, col2, col3= st.columns(3)
col2.metric(str(current_year-1),acum_passado.iloc[-1] )
col1.metric(str(current_year) ,acum_atual.iloc[-1])
col3.metric('Delta Acum. até Mês Atual',acum_atual.iloc[-1] - acum_passado.iloc[-1],(str(round(delta.iloc[0]*100,2)) +' %'))


fig_credito = go.Figure()
fig_credito.add_trace(go.Scatter(name='Credito', x=df_credito.index , y=df_credito.Credito, showlegend=False ))
fig_credito.update_layout(title = 'Total Crédito', xaxis_title="Meses", yaxis_title = 'Milhões de reais' )
fig_credito.add_trace(go.Scatter(x=[df_credito.index[-1]],
                         y=[df_credito.iloc[-1, 0]],
                         text=[df_credito.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='bottom center',
                         showlegend=False))
st.plotly_chart(fig_credito, use_container_width=True, width=1600, height=600)

st.markdown('---')

st.header('Formação de Capital Bruto Fixo')
st.write('Formação bruta de capital fixo - série encadeada dos índices de base móvel (média 1995 = 100). Variação percentual em relação ao mesmo período do ano anterior.')
#importando dados do site do IPEA - webscrapping

url_invest = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38406'
tabela_invest = pd.read_html(url_invest)

#trazendo somente a tabela de interesse
df_invest = pd.DataFrame(tabela_invest[2])

#trocando nome das colunas
df_invest.rename(columns = {0: 'data', 1:'Investimento real'}, inplace = True)

#retirando as primeiras linhas
df_invest = df_invest[1:][-24:]

#deixando somente o ano e tirando os quarters
#df_invest['data'] = df_invest['data'].apply(lambda x: x.strip().split(' ')[0])

#transformando data em indice
df_invest.set_index('data', inplace = True)

#transformando em float
df_invest['Investimento real'] = df_invest['Investimento real'].astype('float')/100
fig_invest = go.Figure()

fig_invest.add_trace(go.Bar(name='Investimento Real', x=df_invest.index, y=df_invest.iloc[:, 0], text=round(df_invest.iloc[:, 0], 2)))
fig_invest.update_layout(title='Investimento Real', xaxis_title="Meses", yaxis_title='Valor Mensal (%)')
fig_invest.update_traces(textposition = 'outside', textfont_size=12)
st.plotly_chart(fig_invest, use_container_width=True, width=1600, height=600)

st.markdown('---')

st.header('Histórico de Juros - Títulos Públicos')

def busca_titulos_tesouro_direto():
  url = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
  df  = pd.read_csv(url, sep=';', decimal=',')
  df['Data Vencimento'] = pd.to_datetime(df['Data Vencimento'], dayfirst=True)
  df['Data Base']       = pd.to_datetime(df['Data Base'], dayfirst=True)
  multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
  df = df.set_index(multi_indice).iloc[: , 3:]
  return df

titulos = busca_titulos_tesouro_direto()
titulos.sort_index(inplace = True)

ipca2035 = titulos.loc[('Tesouro IPCA+', '2035-05-15')]

fig_ipca2035 = go.Figure()

fig_ipca2035.add_trace(go.Scatter(name='ipca2035', x=ipca2035.index , y=ipca2035['Taxa Compra Manha'], showlegend=False ))
fig_ipca2035.update_layout(title = 'Tesouro IPCA+ 2035', xaxis_title='Taxa (%)', yaxis_title = 'Anos' )
fig_ipca2035.add_trace(go.Scatter(x=[ipca2035.index[-1]],
                         y=[ipca2035.iloc[-1, 0]],
                         text=[ipca2035.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='bottom right',
                         showlegend=False))
st.plotly_chart(fig_ipca2035, use_container_width=True, width=1600, height=600)


#buscando tesouro pré fixado

pre2026 = titulos.loc[('Tesouro Prefixado', '2026-01-01')]

fig_pre2026 = go.Figure()

fig_pre2026.add_trace(go.Scatter(name='pre2026', x=pre2026.index , y=pre2026['Taxa Compra Manha'], showlegend=False ))
fig_pre2026.update_layout(title = 'Tesouro Pré Fixado 2026', xaxis_title='Taxa (%)', yaxis_title = 'Anos' )
fig_pre2026.add_trace(go.Scatter(x=[pre2026.index[-1]],
                         y=[pre2026.iloc[-1, 0]],
                         text=[pre2026.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='bottom right',
                         showlegend=False))
st.plotly_chart(fig_pre2026, use_container_width=True, width=1600, height=600)

st.markdown('---')

st.header('Câmbio')

df_dolar = yf.download('BRL=X', start = '2008-01-01')

fig_dolar = go.Figure()

fig_dolar.add_trace(go.Scatter(name='cambio', x=df_dolar.index , y=df_dolar['Close'], showlegend=False ))
fig_dolar.update_layout(title = 'Real/ Dolar - Câmbio', xaxis_title='R$', yaxis_title = 'Dia' )
fig_dolar.add_trace(go.Scatter(x=[df_dolar.index[-1]],
                         y=[df_dolar.iloc[-1, 0]],
                         text=[df_dolar.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='bottom right',
                         showlegend=False))
st.plotly_chart(fig_dolar, use_container_width=True, width=1600, height=600)


st.markdown('---')

df_dxy = yf.download('DX-Y.NYB', start = '2008-01-01')

fig_dxy = go.Figure()

fig_dxy.add_trace(go.Scatter(name='dxy', x=df_dxy.index , y=df_dxy['Close'], showlegend=False ))
fig_dxy.update_layout(title = 'DXY', xaxis_title='US$', yaxis_title = 'Dia' )
fig_dxy.add_trace(go.Scatter(x=[df_dxy.index[-1]],
                         y=[df_dxy.iloc[-1, 0]],
                         text=[df_dxy.iloc[-1, 0]],
                         mode='markers+text',
                         marker=dict(color='red', size=8),
                         textfont=dict(color='green', size=15),
                         textposition='bottom right',
                         showlegend=False))
st.plotly_chart(fig_dxy, use_container_width=True, width=1600, height=600)
