#Works with Streamlit and hosted on Streamlit cloud

import streamlit as st
import streamlit_analytics
import pandas as pd
from datetime import date
from datetime import datetime
from pyxirr import xirr
import pandas as pd

st.title('XIRR Calculator', anchor=None)

with st.form("xirr_form"):

	option = st.selectbox(
	     'Select your broker',
	     ('ICICI Direct', 'Zerodha'))

	#TBD: Calculate for Zerodha, the time field will need a bit of manipulation
    
	uploaded_file = st.file_uploader("Upload CSV statement", type=['csv'], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)

	current_NAV = st.number_input(label="Enter current portfolio value", min_value=None, max_value=None, value=0.0, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

	if uploaded_file is not None and current_NAV != 0:

		df = pd.read_csv(uploaded_file)

		amount = []
		date = []
		portfolio = []

		if option == 'ICICI Direct':
			action = 'Action'
			buy = 'Buy'
			sell = 'Sell'
			price = 'Transaction Price'
			quantity = 'Quantity'
			transaction_date = 'Transaction Date'

		elif option == 'Zerodha':
			action = 'trade_type'
			buy = 'buy'
			sell = 'sell'
			price = 'price'
			quantity = 'quantity'
			transaction_date = 'trade_date'
			
		# Calculate amount of Transaction
		# If buy transaction, add negative against amount

		for index, row in df.iterrows():
		    if row[action] == buy:
		        sign = -1
		    else:
		        sign = 1
		    value = row[price]*row[quantity]*sign
		    amount.append(value)
		    if option == 'ICICI Direct':
			    date.append(datetime.strptime(row[transaction_date],'%d-%b-%Y').date())
		    elif option == 'Zerodha':
			    date.append(datetime.strptime(row[transaction_date],'%d-%m-%Y').date())
		

		df = pd.DataFrame(zip(date, amount), columns =['Date', 'Amount']).sort_values(by="Date")

		#An elegant way to aggregate amounts by date
		df = df.groupby(['Date']).sum()
		aggregated_amount_list = df['Amount'].tolist()

		# #Calculation of net portfolio value on each date by summing buys and subtracting sells
		for item in aggregated_amount_list:
			if portfolio == []:
				portfolio.append(-1*item)
			else:
				portfolio.append(portfolio[-1]+(-1*item))
		
		df['Book Value of Portfolio'] = portfolio

		# Add last data points as current date and NAV as of current date
		# Calculate XIRR

		# print(xirr(date+[datetime.today()], amount+current_NAV))

	submitted = st.form_submit_button("Calculate")

	streamlit_analytics.start_tracking()
	if submitted:
		if uploaded_file is not None:

			if current_NAV > 0:
				try: 
					xirr = round(xirr(date+[datetime.today()], amount+[current_NAV])*100,2)
					st.metric(label='XIRR', value=str(xirr)+"%", delta=None, delta_color="normal")
				except:
					st.error("Something went wrong, please check the values entered")
			else: st.error("Please enter current portfolio value")
		else: st.error("Please upload broker statement as shown in Instructions")
		
		#Charts need a little more polish

		# st.metric(label='Book value of portfolio', value="", delta=None, delta_color="normal")
		# st.area_chart(df.drop(['Amount'], axis=1))
		
		st.metric(label='Buy/Sell History', value="", delta=None, delta_color="normal")
		st.bar_chart(df.drop(['Book Value of Portfolio'], axis=1))
	
	streamlit_analytics.stop_tracking()

st.subheader('How to Use:', anchor=None)
# st.image('https://i.postimg.cc/bY1KVM11/Screenshot-2021-12-12-at-10-15-19-ICICI-Direct.png', caption='Log in to your ICICI Direct Account', width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.text("1. Log into your broker account")
st.text("4. Download the brokerage statement showing all buy and sell transactions")
st.text("5. Upload the CSV file here")
st.text("6. Enter current portfolio value to calculate XIRR")

st.write("[Created by MadHatter92](https://github.com/MadHatter92)")
