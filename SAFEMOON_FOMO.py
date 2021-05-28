import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
cg = CoinGeckoAPI()

st.write("""
# $Safemoon FOMO Calculator
Use the option below to set your parameters for:
- Date You Wish You Would Have Bought $SAFEMOON
- USD Amount You Wish You Would Have Invested
""")
st.write('---')

st.image('data/safemoon.jpeg', use_column_width=True)
st.write("[Photo by The New York Public Library](https://unsplash.com/@nypl)")
   

#Load Data
sm_current = cg.get_price(ids='safemoon', vs_currencies='usd')['safemoon']['usd']

#Giving Choices
st.write('''# Choose Date and Amount''')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2021,3,14), max_value=previous_day)
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)


#Reformat Historical Date for next function
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
sm_historic = cg.get_coin_history_by_id(id='safemoon', vs_currencies='usd', date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']

sm_historic = round(sm_historic,9)

st.write('''# Results''')
st.write('''## Historic Analysis''')
st.write("You would have originally bought: ***{:,.2f}*** $SAFEMOON".format(round(ORG_USD/sm_historic),2))
st.write("At a price of ***{:,.9f}*** per $SAFEMOON".format(sm_historic))
st.write(" ")

st.write('''## Present Effects''')
total_sm = ORG_USD/sm_historic
current_USD = total_sm * sm_current
perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
usd_diff = current_USD - ORG_USD


st.write("That is currently worth: ***${:,.2f}***".format(round(current_USD,2)))
st.write("Which is a percentage change of ***{:,.2f}%***".format(round(perc_change, 2),))

if usd_diff == 0:
   st.write('''# You Broke Even''')
elif usd_diff <= 0:
   st.write('''# You Would Have Lost''')
else:
   st.write('''# You Missed Out On''') 
st.write('***${:,.2f}!!!***'.format(abs(round(usd_diff,2)),))

now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id='safemoon', vs_currency="usd", from_timestamp=HIST_DATE_datetime.timestamp(), to_timestamp=now.timestamp())['prices']

dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')

st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))
st.write("Please consider donating some of that sweet $SAFEMOON to the wallet address below:")
st.write("0x52CB49d7dC51E214C9CC8B88c605cDbF8bc1034c")
