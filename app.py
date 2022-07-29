import streamlit as st
import pandas as pd
import altair as alt
import datetime

#Create area for user entry
st.sidebar.header('$ Inputs')

current_dollars_in_savings = st.sidebar.number_input('Current $ in Savings', value=32000)
savings_per_month = st.sidebar.number_input('Expected $ Savings Toward House Per Month', value=2000)

expected_tax_rebate = st.sidebar.number_input('Expected $ in Tax Rebate', value=4000)
expected_tax_rebate_receive_date = st.sidebar.date_input('Expected Date to Receive Tax Rebate', value=datetime.date(2023, 4, 1))

expected_bonus = st.sidebar.number_input('Expected $ in Bonus', value=10000)
expected_bonus_receive_date = st.sidebar.date_input('Expected Date to Receive Bonus', value=datetime.date(2023, 4, 1))
bonus_allocation_to_house = st.sidebar.number_input('Expected Bonus Allocation to House', value=1, max_value=1)

minimum_necessary_left_in_savings = st.sidebar.number_input('Minimum $ Savings Required Post Transaction', value=5000)

st.sidebar.header('House Cost Inputs')
list_price = st.sidebar.number_input('List Price', value=300000)
down_payment_contribution_rate = st.sidebar.number_input('Expected % Allocation to Down Payment', value=0.10)
expected_closing_fees_as_loan_percentage = st.sidebar.number_input("Expected Closing Rate Fees as percent of Loan", value=0.05, min_value=0.02)


#Make cost calculations from user inputs
down_payment = list_price * down_payment_contribution_rate

loan_amount = list_price - down_payment

closing_fees = loan_amount * expected_closing_fees_as_loan_percentage

total_required_to_purchase = down_payment + closing_fees + minimum_necessary_left_in_savings

st.write('Total $ Required for Purchase: ', total_required_to_purchase)

#Create lists for time management by month over 15 month horizon
days_out_list = [i*30 for i in range(1,16)]
date_time_stamps = [datetime.datetime.now() + datetime.timedelta(days=day_num) for day_num in days_out_list]
date_stamps = [date_time.date() for date_time in date_time_stamps]

#Build lists for columns needed for a dataframe
#months_out
months_out_list = [i for i in range(1,16)]
#current_dollars_in_savings
current_savings_list = [current_dollars_in_savings for i in months_out_list]
#savings_per_month * months_out
savings_per_month_list = [savings_per_month * i for i in months_out_list]
#tax_rebate
tax_rebate_list = [expected_tax_rebate for i in months_out_list]
#bonus_income
bonus_income_list = [expected_bonus * bonus_allocation_to_house for i in months_out_list]
#tax_rebate_multiplier
tax_rebate_multiplier_list = [1 if expected_tax_rebate_receive_date < ds else 0 for ds in date_stamps]
#bonus_income_multiplier
bonus_income_multiplier_list = [1 if expected_bonus_receive_date < ds else 0 for ds in date_stamps]

#Build the dataframe
# dictionary of lists 
df_dict = {'months_out': months_out_list, 'current_savings': current_savings_list, 
        'expected_additional_savings': savings_per_month_list, 'tax_rebate': tax_rebate_list,
        'tax_rebate_multiplier': tax_rebate_multiplier_list, 'bonus_income': bonus_income_list, 
        'bonus_income_multiplier':bonus_income_multiplier_list, 'total_required_to_purchase':[total_required_to_purchase for i in months_out_list]} 
    
df = pd.DataFrame(df_dict)

#Calculate total savings available from other lists
df['total_savings_available_for_transaction'] = df['current_savings'] + df['expected_additional_savings'] + (df['tax_rebate']*df['tax_rebate_multiplier']) + (df['bonus_income']*df['bonus_income_multiplier'])

#boolean indicator on if you are able to purchase or not
df['able_to_purchase'] = df['total_savings_available_for_transaction'] > total_required_to_purchase
    
#Create a chart
line_chart = alt.Chart(df).mark_line().encode(x="months_out", y="total_savings_available_for_transaction")

yrule = (
    alt.Chart(df).mark_rule(strokeDash=[12, 6], size=2, color='red').encode(y=alt.Y('total_required_to_purchase', axis=alt.Axis(title=None)))
)

#output chart and dataframe to screen
st.altair_chart(line_chart + yrule, use_container_width=True)
st.write(df) 


