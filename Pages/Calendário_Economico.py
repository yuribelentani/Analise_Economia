import investpy
import streamlit as st
import pandas as pd


st.title('Calendário Econômico 📆')

options = st.multiselect(
    'Selecione Países/ Regiões',
    ['Brazil', 'United States', 'Germany', 'France', 'Euro Zone', 'China', 'Australia', 'Japan','Mexico', 'Argentina'])

options1 = st.multiselect('Escolha a Relevância',
                          ['low', 'medium', 'high'])

try:
    data = investpy.economic_calendar(countries=options, importances = options1)
    data.drop(columns=['id'], inplace=True)
    st.write(data)
except:
    st.error('Sem Dados para essa Relevância!', icon="🚨")

