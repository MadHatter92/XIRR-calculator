#Works with Streamlit and is run on a local server
#Currently only operates with ICICI Direct Brokerage Statement
#Need to add

import streamlit as st
import streamlit_analytics
import pandas as pd
from datetime import date
from datetime import datetime
from pyxirr import xirr
import pandas as pd

st.title('XIRR Calculator', anchor=None)
st.text("(Currently only works for ICICI Direct brokerage statement)")

with st.form("xirr_form"):
    
	uploaded_file = st.file_uploader("Upload CSV statement", type=['csv'], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)

	current_NAV = st.number_input(label="Enter current portfolio value", min_value=None, max_value=None, value=0.0, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

	if uploaded_file is not None and current_NAV != 0:

		df = pd.read_csv(uploaded_file)

		amount = []
		date = []

		# Calculate amount of Transaction
		# If buy transaction, add negative against amount

		for index, row in df.iterrows():
		    if row['Action'] == 'Buy':
		        sign = -1
		    else:
		        sign = 1
		    amount.append(row['Transaction Price']*row['Quantity']*sign)
		    date.append(datetime.strptime(row['Transaction Date'], '%d-%b-%Y').date())

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
	streamlit_analytics.stop_tracking()

st.subheader('How to Use:', anchor=None)
# st.image('https://i.postimg.cc/bY1KVM11/Screenshot-2021-12-12-at-10-15-19-ICICI-Direct.png', caption='Log in to your ICICI Direct Account', width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.text("1. Log into your ICICI Direct Account")
st.text("2. Go to \"Portfolio\" tab under the \"Equity\" tab")
st.text("3. Select Holding Duration as \"All\" and click on \"View\"")
st.text("4. Click on \"Download\", with the \"All Transactions: CSV\" option")
st.text("5. Upload the CSV file here")
st.text("6. Enter current portfolio value to calculate XIRR")

st.write("[Created by MadHatter92](https://github.com/MadHatter92)")
