import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
from datetime import datetime
cg = CoinGeckoAPI()

st.write("""
# Doge FOMO Calculator
Use the option below to set your parameters for:
- Date You Wished You Would Have Bought $Doge
- USD Amount You Wish You Would Have Invested
""")
st.write('---')

st.image('data/doge.jpg', use_column_width=True)
st.write("[Photo by Minh Pham](https://unsplash.com/@minhphamdesign?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)")
#Photo by <a href="https://unsplash.com/@minhphamdesign?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Minh Pham</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
   

#Load Data
doge_current = cg.get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']

#Giving Choices
st.write('''# Choose Date and Amount''')
HIST_DATE = st.date_input("Date: ", min_value=datetime(2014,1,1), max_value=datetime.now())
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)


#Reformat Historical Date for next function
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
doge_historic = cg.get_coin_history_by_id(id='dogecoin', vs_currencies='usd', date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']

doge_historic = round(doge_historic, 5)

st.write('''# Results''')
st.write('''## Historic Analysis''')
st.write("You would have originally bought: ", round((ORG_USD/doge_historic),5), " DOGE")
st.write("At a price of ", doge_historic,' per DOGE')
st.write(" ")

st.write('''## Present Affects''')
total_doge = ORG_USD/doge_historic
current_USD = total_doge * doge_current
perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
usd_diff = current_USD - ORG_USD

st.write("That is currently worth: $", round(current_USD,2))
st.write("Which is a percentage change of ", round(perc_change, 2), "%")
st.write('''# You Lost Out On''')
st.write('$', round(usd_diff,2),"!!!")

now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id='dogecoin', vs_currency="usd", from_timestamp=HIST_DATE_datetime.timestamp(), to_timestamp=now.timestamp())['prices']

dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')

st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))
