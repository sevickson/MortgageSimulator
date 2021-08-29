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
import numpy_financial as npf
import hypotheekrentetarieven

st.set_page_config(
    page_title="Hypotheek Betaling Simulator")

st.title("Hypotheek Betaling Simulator")

st.header("**Hypotheekgegevens**")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Totaal Hypotheekbedrag")
    total_mortgage = st.number_input("Vul in totale hypotheekbedrag (€): ", min_value=0.0, format='%f')
    
    st.subheader("Hypotheekrente per jaar")
    interest_rate = st.number_input("Vul in je hypotheekrente in rentevast periode (%): ", min_value=0.0, format='%f')

    st.subheader("Rentevastperiode")
    interest_rate_period = st.number_input("Vul in je rentevast periode (jaren): ", min_value=0.0, format='%f')

with col2:
    #st.subheader("Waarde woning")
    #home_value = st.number_input("Waarde van de woning(€): ", min_value=0.0, format='%f')
    
    st.subheader("Looptijd hypotheek (jaren)")
    payment_years = st.number_input("Vul in totale looptijd van hypotheek (jaren): ", min_value=30, format='%d')

    st.subheader("Stijging na rentevastperiode")
    interest_rate_after = st.number_input("Vul in mogelijke stijging na rentevastperiode (%): ", min_value=0.0, format='%f')
    

#down_payment = home_value* (down_payment_percent / 100)
loan_amount = total_mortgage #- down_payment
payment_months = int(payment_years*12)
payment_months_after = int(interest_rate_period*12)

interest_rate = interest_rate / 100
periodic_interest_rate = interest_rate / 12

interest_rate_after = interest_rate_after / 100
periodic_interest_rate_after = interest_rate_after / 12
#previous_principal_remaining = ''

monthly_installment = -1*npf.pmt(periodic_interest_rate , payment_months, loan_amount)

#st.subheader("**Hypotheekbedrag:** €" + str(round(loan_amount, 2)))
#st.subheader("**Bruto maandelijks bedrag:** €" + str(round(monthly_installment, 2)))
#st.subheader("**Bruto totaal bedrag gedurene looptijd:** €" + str(round(monthly_installment*payment_months, 2)))

st.markdown("---")

st.header("**Annuïteitenhypotheek afschrijvingen**")
principal_remaining = np.zeros(payment_months)
interest_pay_arr = np.zeros(payment_months)
principal_pay_arr = np.zeros(payment_months)
monthly_pay = np.zeros(payment_months)

#payments in rentevastperiode
if periodic_interest_rate_after == 0.0:
    for i in range(0, payment_months): #payment_months):

        if i == 0:
            previous_principal_remaining = loan_amount
        else:
            previous_principal_remaining = principal_remaining[i-1]
            
        interest_payment = round(previous_principal_remaining*periodic_interest_rate, 2)
        principal_payment = round(monthly_installment - interest_payment, 2)
        
        if previous_principal_remaining - principal_payment < 0:
            principal_payment = previous_principal_remaining
        
        interest_pay_arr[i] = interest_payment 
        principal_pay_arr[i] = principal_payment
        principal_remaining[i] = previous_principal_remaining - principal_payment
        monthly_pay[i] = monthly_installment

#if periodic_interest_rate_after is not None:
else:
    for i in range(0, payment_months_after): #payment_months):

        if i == 0:
            previous_principal_remaining = loan_amount
        else:
            previous_principal_remaining = principal_remaining[i-1]
            
        interest_payment = round(previous_principal_remaining*periodic_interest_rate, 2)
        principal_payment = round(monthly_installment - interest_payment, 2)
        
        if previous_principal_remaining - principal_payment < 0:
            principal_payment = previous_principal_remaining
        
        interest_pay_arr[i] = interest_payment 
        principal_pay_arr[i] = principal_payment
        principal_remaining[i] = previous_principal_remaining - principal_payment
        monthly_pay[i] = monthly_installment

    payment_months_left = payment_months-payment_months_after
    #calculate after rentevastperiode
    previous_principal_remaining = principal_remaining[payment_months_after-1]
    monthly_installment_after = -1*npf.pmt(periodic_interest_rate_after, payment_months_left, previous_principal_remaining)

    #payments after rentevastperiode
    for i in range(payment_months_after, payment_months):
        previous_principal_remaining = principal_remaining[i-1]
 
        interest_payment_after = round(previous_principal_remaining*periodic_interest_rate_after, 2)
        principal_payment = round(monthly_installment_after - interest_payment_after, 2)
        
        if previous_principal_remaining - principal_payment < 0:
            principal_payment = previous_principal_remaining
        
        interest_pay_arr[i] = interest_payment_after 
        principal_pay_arr[i] = principal_payment
        principal_remaining[i] = previous_principal_remaining - principal_payment
        monthly_pay[i] = monthly_installment_after

#else:
#    for i in range(payment_months_after, payment_months):
#
#        if i == 0:
#            previous_principal_remaining = loan_amount
#        else:
#            previous_principal_remaining = principal_remaining[i-1]
#            
#        interest_payment = round(previous_principal_remaining*periodic_interest_rate, 2)
#        principal_payment = round(monthly_installment - interest_payment, 2)
#        
#        if previous_principal_remaining - principal_payment < 0:
#            principal_payment = previous_principal_remaining
#        
#        interest_pay_arr[i] = interest_payment 
#        principal_pay_arr[i] = principal_payment
#        principal_remaining[i] = previous_principal_remaining - principal_payment
#        monthly_pay[i] = monthly_installment

#test hypotheekrente
#df_rentes = hypotheekrentetarieven.scrape_hypotheekrentetarieven()
#print(df_rentes)

month_num = np.arange(payment_months)
month_num = month_num + 1

principal_remaining = np.around(principal_remaining, decimals=2)
monthly_pay = np.around(monthly_pay, decimals=2)

st.subheader("**Hypotheekbedrag:** €" + str(round(loan_amount, 2)))
st.subheader("**Bruto maandelijks bedrag:** €" + str(round(monthly_installment, 2)))
#st.subheader("**Bruto totaal bedrag gedurene looptijd:** €" + str(round(monthly_installment*payment_months, 2)))
st.subheader("**Bruto totaal bedrag gedurende looptijd:** €" + str(round(np.sum(monthly_pay), 2)))

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