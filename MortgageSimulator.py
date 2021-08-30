# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:12:17 2021

@author: Sevickson Kwidama
@based on work from: Teo Bee Guan
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
#import numpy_financial as npf
import hypotheekrentetarieven
import hypotheekberekening

#get all hypotheekrentes
df_rentes = hypotheekrentetarieven.scrape_hypotheekrentetarieven()
#only use providers that have all the interest data available
df_rentes_filter = df_rentes[(df_rentes['100%'] != '–') & (df_rentes['nhg'] != '–')]
#change types to use groupby
df_rentes_filter[["nhg","60%","80%","90%","100%","looptijd"]] = df_rentes_filter[["nhg","60%","80%","90%","100%","looptijd"]].apply(pd.to_numeric)
#drop 'nhg' and mean without 'nhg' as this is only 23% of all mortgages (source:https://www.hdn.nl/marktcijfers/)
df_rentes_filter.drop('nhg', axis=1,inplace=True)
df_rentes_filter = df_rentes_filter.assign(gemiddelde=df_rentes_filter.iloc[:, 1:4].mean(axis=1).round(2))
#use mean based on 'looptijd' to use this for the calculations
df_rentes_filter = df_rentes_filter.groupby('looptijd').agg({'gemiddelde': ['mean','min']}).round(2)

st.set_page_config(
    page_title="Hypotheek Betaling Simulator")

st.title("Hypotheek Betaling Simulator")

st.header("**Hypotheekgegevens**")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Totaal Hypotheekbedrag")
    total_mortgage = st.number_input("Vul in totale hypotheekbedrag (€): ", min_value=0.0, format='%f')
    
    #st.subheader("Hypotheekrente per jaar")
    #interest_rate = st.number_input("Vul in je hypotheekrente in rentevast periode (%): ", min_value=0.0, format='%f')

    #st.subheader("Rentevastperiode")
    #interest_rate_period = st.number_input("Vul in je rentevast periode (jaren): ", min_value=0.0, format='%f')

with col2:    
    st.subheader("Rente vermenigvuldiger")
    interest_multiplier = st.number_input("Vul in verwachte rente groei per jaar: ", min_value=0.0, format='%f')

    st.subheader("Looptijd hypotheek (jaren)")
    payment_years = st.number_input("Vul in totale looptijd van hypotheek (jaren): ", min_value=30, format='%d')

    #st.subheader("Stijging na rentevastperiode")
    #interest_rate_after = st.number_input("Vul in mogelijke stijging na rentevastperiode (%): ", min_value=0.0, format='%f')
    

loan_amount = total_mortgage #- down_payment
payment_months = int(payment_years*12)
#payment_months_after = int(interest_rate_period*12)

#interest_rate = interest_rate / 100
#periodic_interest_rate = interest_rate / 12

#interest_rate_after = interest_rate_after / 100
#periodic_interest_rate_after = interest_rate_after / 12

#monthly_installment = -1*npf.pmt(periodic_interest_rate , payment_months, loan_amount)

st.markdown("---")

st.header("**Annuïteitenhypotheek afschrijvingen**")

#loan_amount = 200000 
#payment_months = int(30*12)
#looptijd = 5
#interest_percentage = 2
#interest_multiplier = 0.2

for index,row in df_rentes_filter.iterrows():
    print('looptijd',index)
    print('rente gemiddelde',row[0])
    looptijd = index
    interest_percentage = row[0]
    results = hypotheekberekening.calculate_hypotheek_best(interest_percentage, interest_multiplier, payment_months, loan_amount, looptijd)
    print(results)

st.subheader("**Hypotheekbedrag:** €" + str(round(loan_amount, 2)))
#st.subheader("**Bruto maandelijks bedrag:** €" + str(round(monthly_installment, 2)))
#st.subheader("**Bruto totaal bedrag gedurende looptijd:** €" + str(round(np.sum(monthly_pay), 2)))

st.write(results)

fig = make_subplots(
    rows=2, cols=1,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "scatter"}]
          ]
)

fig.add_trace(
        go.Table(
            header=dict(
                    values=['Maand', 'Maandbedrag','Aflossing(€)', 'Rente(€)', 'Restschuld(€)']
                ),
            cells = dict(
                    values =[month_num, monthly_pay, principal_pay_arr, interest_pay_arr, principal_remaining]
                )
            ),
        row=1, col=1
    )

fig.add_trace(
        go.Scatter(
                x=month_num,
                y=principal_pay_arr,
                name= "Aflossing betaling(€)"
            ),
        row=2, col=1
    )

fig.append_trace(
        go.Scatter(
            x=month_num, 
            y=interest_pay_arr,
            name="Rente betaling(€)"
        ),
        row=2, col=1
    )

fig.update_layout(title='Annuïteitenhypotheek afschrijvingen per maand',
                   xaxis_title='Month',
                   yaxis_title='Amount(€)',
                   height= 800,
                   width = 1200,
                   legend= dict(
                           orientation="h",
                           yanchor='top',
                           y=0.47,
                           xanchor= 'left',
                           x= 0.01
                       )
                  )

st.plotly_chart(fig, use_container_width=True)