import numpy as np
import numpy_financial as npf
#import pandas as pd

def calculate_hypotheek_best(interest_percentage, interest_multiplier, payment_months, loan_amount, looptijd):
    payment_months_after = int(looptijd*12)
    interest_rate = interest_percentage / 100
    periodic_interest_rate = interest_rate / 12
    interest_percentage_after = interest_percentage+(looptijd*interest_multiplier)
    interest_rate_after = interest_percentage_after / 100
    #print('rente na rentevast',interest_percentage+(looptijd*interest_multiplier))
    periodic_interest_rate_after = interest_rate_after / 12

    principal_remaining = np.zeros(payment_months)
    interest_pay_arr = np.zeros(payment_months)
    principal_pay_arr = np.zeros(payment_months)
    monthly_pay = np.zeros(payment_months)

    monthly_installment = -1*npf.pmt(periodic_interest_rate , payment_months, loan_amount)
    #payments in rentevastperiode
    if (periodic_interest_rate_after == 0.0) or (payment_months == payment_months_after):
        for i in range(0, payment_months):

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
        for i in range(0, payment_months_after): 

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
        #print(periodic_interest_rate_after, payment_months_left, previous_principal_remaining)
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

    month_num = np.arange(payment_months)
    month_num = month_num + 1

    principal_remaining = np.around(principal_remaining, decimals=2)
    monthly_pay = np.around(monthly_pay, decimals=2)
    return(interest_percentage_after,round(np.sum(monthly_pay), 2))