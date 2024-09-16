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
    st.title('Potential Buys')
    
    forwardPE_cutoff = st.slider("forwardPE_cutoff (lower = more undervalued)", 10, 50, 26)
    #price_percChg_52WkLow_cutoff = st.slider('price_percChg_52WkLow_cutoff',10,15,10)
    #price_percChg_52WkHigh_cutoff = st.slider('price_percChg_52WkHigh_cutoff',-50,-15,-25)
        
    buy_df = filterBuyDf(df,forwardPE_cutoff)
    qtr_df1 = financials_quarter(buy_df['ticker'].unique())
    buy_df = filterNetIncomeRatio(buy_df,latestRatios(qtr_df1))

    st.dataframe(buy_df)#,use_container_width=True)
    

    
    
    
    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('Ticker Quarterly Data')
    buy_tickers=list(buy_df['ticker'].unique())
    ticker_select = st.selectbox('Select a ticker:',buy_tickers)
    
    qtr_df_select = qtr_df1[qtr_df1['ticker']==ticker_select]
    cols = ['date','ticker','shortName','net_interest_income_ratio','interest_income_ratio','debt_to_ebitda'
            ,'gross_margin','npat_margin'
            ,'Total Revenue','Net Income','Free Cash Flow','EBITDA'
            ,'Cash And Cash Equivalents'
           ]
    
    st.dataframe(qtr_df_select[cols],use_container_width=True)
    
    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('\n\n\n')
    
    st.write('\nTotal Revenue')
    fig_revenue = px.bar(qtr_df_select, x="date", y="Total Revenue", color="shortName")
    st.plotly_chart(fig_revenue, key="ticker1", on_select="rerun")
    
    st.write('\nNet Income')
    fig_netincome = px.bar(qtr_df_select, x="date", y="Net Income", color="shortName")
    st.plotly_chart(fig_netincome, key="ticker2", on_select="rerun")
    
    st.write('\nFree Cash Flow')
    fig_netincome = px.bar(qtr_df_select, x="date", y="Free Cash Flow", color="shortName")
    st.plotly_chart(fig_netincome, key="ticker3", on_select="rerun")
    







# ### By Ticker only:

# In[16]:

with tab2:
    st.title('Ticker Analytics')
    
    ticker_ = st.multiselect('Select a ticker:',sorted(ticker_list),['NVDA','TSM','QCOM','AMD'])
    
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
    
    st.write('\nFree Cash Flow')
    fig_netincome = px.bar(qtr_df2, x="date", y="Free Cash Flow", color="shortName")
    st.plotly_chart(fig_netincome, key="ticker_b3", on_select="rerun")
    
    st.write('\nAccounts Receivable')
    fig_act_receivable = px.bar(qtr_df2, x="date", y="Accounts Receivable", color="shortName")
    st.plotly_chart(fig_act_receivable, key="ticker_b4", on_select="rerun")
    
    
    st.write('\nCapital Expenditure')
    fig_capex = px.bar(qtr_df2, x="date", y="Capital Expenditure", color="shortName")
    st.plotly_chart(fig_capex, key="ticker_b5", on_select="rerun")
    
    
    st.write('\nMonthly Close Price')
    fig_line = px.line(price_shares_df2, x="date_close_price", y="close_price", color="ticker")
    st.plotly_chart(fig_line, key="ticker_b6", on_select="rerun")
    st.dataframe(price_shares_df2)

