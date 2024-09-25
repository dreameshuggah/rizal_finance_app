#!/usr/bin/env python
# coding: utf-8

# In[1]:

# cd /Users/norrizal/Documents/Rizal_Analytics/Financial_Stock_Analysis/Rizal_Finance_App
# streamlit run streamlit_tickers.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

#from IPython.display import display
#pd.options.display.max_columns = None
#pd.options.display.max_rows = 30
#pd.get_option("display.max_rows")
#pd.set_option('display.max_rows', 100)
from pandasql import sqldf
import yfinance as yf
import plotly.express as px
from ticker_funcs import *

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)


tab1, tab2 = st.tabs(["Screener", "Tickers Analysis"])




ticker_list = list(set(['ADSK', 'CRM', 'MMM', 'ADBE', 'AMD', 'APD', 'ABNB', 'AMR', 'GOOG',
               'AMZN', 'AXP', 'AAPL', 'ANET', 'ARM', 'ASML', 'ACLS', 'BCC',
               'BKNG', 'BOOT', 'AVGO', 'CP', 'CF', 'CVX', 'CTAS', 'CL',
               'CPRT', 'CROX', 'DG', 'ELF', 'DAVA', 'ENPH', 'EXPE', 'XOM', 'FSLR',
               'FTNT', 'INMD', 'INTC', 'ISRG', 'JNJ', 'LRCX', 'LULU', 'CART',
               'MA', 'MRK', 'META', 'MU', 'MSFT', 'MRNA', 'MDLZ', 'NFLX',
               'NKE', 'NVO', 'NVDA', 'OXY', 'OKTA', 'ORCL', 'OTIS', 'PANW',
               'PYPL', 'PEP', 'PFE', 'PUBM', 'QCOM', 'QLYS', 'RVLV',
               'NOW', 'SHOP', 'SWKS', 'SFM', 'TSM', 'TGLS', 'TSLA', 'TXRH', 'KO',
               'EL', 'HSY', 'HD', 'KHC', 'PG', 'TTD', 'ULTA', 'VEEV', 'VICI', 'V',
               'SMCI', 'GFS', 'MRVL','DELL']))


df = fetchRecent(ticker_list,recent_ls)


with tab1:
    st.title('Stock Screener')

    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('\n\n\n')

    st.markdown(""" 
    Filter:
    - total debt / market cap ratio < 0.33
    - interest income ratio < 0.05
    - operating margins > 0.1
    """)

    st.write('\n\n\n')
    st.write('\n\n\n')
    forwardPE_cutoff = st.slider("Forward PE cut-off", 10, 40, 25)
        
    buy_df = filterBuyDf(df,forwardPE_cutoff)
    qtr_df1 = financials_quarter(buy_df['ticker'].unique())
    buy_df = filterNetIncomeRatio(buy_df,latestRatios(qtr_df1))

    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('Recent Statistics')
    st.dataframe(buy_df)#,use_container_width=True)
    

    st.markdown("##")
    st.write('Ticker Quarterly Data')
    buy_tickers=list(buy_df['ticker'].unique())
    ticker_select = st.selectbox('Select a ticker:',buy_tickers)

    

  
    
    qtr_df_select = qtr_df1[qtr_df1['ticker']==ticker_select]
    cols = ['date','ticker','shortName','net_interest_income_ratio','interest_income_ratio','debt_to_ebitda'
            ,'gross_margin','npat_margin'
            ,'Total Revenue','Net Income','Accounts Receivable','Free Cash Flow','EBITDA'
            ,'Cash And Cash Equivalents','Capital Expenditure'
           ]
    
    st.dataframe(qtr_df_select[cols],use_container_width=True)
    
    st.markdown("##")
    
    st.write('\nTotal Revenue')
    fig_revenue = px.bar(qtr_df_select, x="date", y="Total Revenue", color="shortName")
    st.plotly_chart(fig_revenue, key="ticker1", on_select="rerun")
    
    st.write('\nNet Income')
    fig_netincome = px.bar(qtr_df_select, x="date", y="Net Income", color="shortName")
    st.plotly_chart(fig_netincome, key="ticker2", on_select="rerun")

    st.write('\nCash And Cash Equivalents')
    fig_cash = px.bar(qtr_df_select, x="date", y="Cash And Cash Equivalents", color="shortName")
    st.plotly_chart(fig_cash, key="ticker3", on_select="rerun")
    
    st.write('\nFree Cash Flow')
    fig_fcf = px.bar(qtr_df_select, x="date", y="Free Cash Flow", color="shortName")
    st.plotly_chart(fig_fcf, key="ticker4", on_select="rerun")

    st.write('\nAccounts Receivable')
    fig_act = px.bar(qtr_df_select, x="date", y="Accounts Receivable", color="shortName")
    st.plotly_chart(fig_act, key="ticker5", on_select="rerun")

    st.write('\nCapital Expenditure')
    fig_capex = px.bar(qtr_df_select, x="date", y="Capital Expenditure", color="shortName")
    st.plotly_chart(fig_capex, key="ticker6", on_select="rerun")


    dailyClosePrice_df  = closingPricesDaily(ticker_select)
    dailyClosePrice_df['Ticker'] = ticker_select[0]
    st.write('\nDaily Close Price')
    fig_line = px.line(dailyClosePrice_df, x="Date", y="Close")#, color="green")
    st.plotly_chart(fig_line, key="ticker7", on_select="rerun")
    st.dataframe(dailyClosePrice_df)







# ### By Ticker only:

# In[16]:

with tab2:
    st.title('Ticker Analytics')
    
    ticker_ = st.multiselect('Select a ticker:',sorted(ticker_list),['NVDA','QCOM','AMD','MU'])
    
    qtr_df2 = financials_quarter(ticker_)
    recent_df2 = df[df['ticker'].isin(ticker_)]
    price_shares_df2 = closePriceSharesCount(ticker_)
    
    st.write('Recent statistics')
    st.dataframe(recent_df2)
   
    st.write('\n\n\n')
    st.write('Quarterly Financials')
    st.dataframe(qtr_df2[cols])
    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('\n\n\n')
  
    st.write('\nTotal Revenue')
    fig_revenue = px.bar(qtr_df2, x="date", y="Total Revenue", color="shortName")
    st.plotly_chart(fig_revenue, key="ticker_b1", on_select="rerun")
    
    st.write('\nNet Income')
    fig_netincome = px.bar(qtr_df2, x="date", y="Net Income", color="shortName")
    st.plotly_chart(fig_netincome, key="ticker_b2", on_select="rerun")

    st.write('\nCash And Cash Equivalents')
    fig_cash = px.bar(qtr_df2, x="date", y="Cash And Cash Equivalents", color="shortName")
    st.plotly_chart(fig_cash, key="ticker_b3", on_select="rerun")
  
    
    st.write('\nFree Cash Flow')
    fig_fcf = px.bar(qtr_df2, x="date", y="Free Cash Flow", color="shortName")
    st.plotly_chart(fig_fcf, key="ticker_b4", on_select="rerun")
    
    st.write('\nAccounts Receivable')
    fig_act_receivable = px.bar(qtr_df2, x="date", y="Accounts Receivable", color="shortName")
    st.plotly_chart(fig_act_receivable, key="ticker_b5", on_select="rerun")
    
    
    st.write('\nCapital Expenditure')
    fig_capex = px.bar(qtr_df2, x="date", y="Capital Expenditure", color="shortName")
    st.plotly_chart(fig_capex, key="ticker_b6", on_select="rerun")
    
    
    st.write('\nMonthly Close Price')
    fig_line = px.line(price_shares_df2, x="date_close_price", y="close_price", color="ticker")
    st.plotly_chart(fig_line, key="ticker_b7", on_select="rerun")
    st.dataframe(price_shares_df2)


