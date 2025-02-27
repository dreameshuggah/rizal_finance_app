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


vix_df = closingPricesDaily('^VIX')

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
               'SMCI', 'GFS', 'MRVL','DELL','ANF','CAT','KLAC','AMAT','ADM'
               ,'STLD','APP','CRWD'
                        #,'RKLB','SOUN'
                       ]))

df = fetchRecent(ticker_list,recent_ls)




tab1, tab2, tab3, tab4 = st.tabs(["Screener", "Comparison","VIX","Tickers"])

#================= TAB1 ===========================
with tab1:
    st.title('Stocks Screener')
  

    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('\n\n\n')

    col1, col2 = st.columns([2,1])
    
    
    col1.markdown(""" 
    Filter:
    - total debt / market cap ratio < 0.33
    - interest income ratio < 0.05
    - operating margins > 0.1
    - forward PE 
    """)

    forwardPE_cutoff = col2.slider("Forward PE cut-off < ", 10, 40, 25)
  

    #st.write('\n\n\n')
    #st.write('\n\n\n')

    
        
    buy_df = filterBuyDf(df,forwardPE_cutoff)
    qtr_df1 = financials_quarter(buy_df['ticker'].unique())
    buy_df = filterNetIncomeRatio(buy_df,latestRatios(qtr_df1))

    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('Recent Statistics')
    st.dataframe(buy_df)#,use_container_width=True)


    
    # ========================= TAB1 SCATTER PLOT =====================
    st.write('\n\n\n')
    st.write('\n\n\n')
    fig_scatter = px.scatter(buy_df[buy_df['returnOnEquity']<1]
                             , x="operatingMargins", y="returnOnEquity"
                             , color= 'market_trend'
                             , size= 'forwardPE'
                             , symbol = 'market_trend'
                             , hover_data=['ticker','shortName','revenueGrowth','currentPrice','perc_Chg_52WkHigh']
                             , title = 'Return On Equity vs Operating Margins: Size by Forward PE'
                             #, height = '700'
                            )
    st.plotly_chart(fig_scatter, key="ticker0")#, on_select="rerun")

    st.write('\n\n\n')
    st.write('\n\n\n')
    fig_scatter2 = px.scatter(buy_df[buy_df['returnOnEquity']<1]
                             , x="operatingMargins"
                             , y="revenueGrowth"
                             , color= 'market_trend'
                             , size= 'forwardPE'
                             , symbol = 'market_trend'
                             , hover_data=['ticker','shortName','revenueGrowth','currentPrice','perc_Chg_52WkHigh']
                             , title = 'Revenue Growth vs Operating Margins: Size by Forward PE'
                             #, height = '700'
                            )
    st.plotly_chart(fig_scatter2, key="ticker0b")#, on_select="rerun")
  
    

    st.markdown("##")
    
    buy_tickers=list(buy_df['ticker'].unique())

    col1a, col2a = st.columns([1,3])
    ticker_select = col1a.selectbox('Select a ticker:',buy_tickers)

    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('Ticker Recent Statistics')
    st.dataframe(buy_df[buy_df['ticker']==ticker_select])

  
    
    dailyClosePrice_df  = closingPricesDaily(ticker_select)
    longBusinessSummary = buy_df[buy_df['ticker']==ticker_select]['longBusinessSummary'].values[0]



    
    
    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('Ticker Quarterly Data')
    
    qtr_df_select = qtr_df1[qtr_df1['ticker']==ticker_select]
    cols = ['date','ticker','shortName','net_interest_income_ratio','interest_income_ratio','debt_to_ebitda'
            ,'gross_margin','npat_margin'
            ,'Total Revenue','Net Income','Accounts Receivable','Free Cash Flow','EBITDA'
            ,'Cash And Cash Equivalents','Capital Expenditure'
           ]
  
    st.dataframe(qtr_df_select[cols],use_container_width=True)



    # ======================== TAB 1 BAR CHARTS ===================  
    st.markdown("##")
    
    col1_chart, col2_chart = st.columns(2)
    
    #col1_chart.write('\nTotal Revenue')
    fig_revenue = px.bar(qtr_df_select, x="date", y="Total Revenue", color="shortName", title = 'Total Revenue' )
    col1_chart.plotly_chart(fig_revenue, key="ticker1")#, on_select="rerun")
    
    #col2_chart.write('\nNet Income')
    fig_netincome = px.bar(qtr_df_select, x="date", y="Net Income", color="shortName", title='Net Income')
    col2_chart.plotly_chart(fig_netincome, key="ticker2")#, on_select="rerun")

    
    
    col1_chart_a, col2_chart_a = st.columns(2)
    
    #col1_chart_a.write('\nFree Cash Flow')
    fig_fcf = px.bar(qtr_df_select, x="date", y="Free Cash Flow", color="shortName", title='Free Cash Flow')
    col1_chart_a.plotly_chart(fig_fcf, key="ticker4")#, on_select="rerun")

    #col2_chart_a.write('\nAccounts Receivable')
    fig_act = px.bar(qtr_df_select, x="date", y="Accounts Receivable", color="shortName", title='Accounts Receivable')
    col2_chart_a.plotly_chart(fig_act, key="ticker5")#, on_select="rerun")


  
    col1_chart_b, col2_chart_b = st.columns(2)
    
    #col1_chart_b.write('\nCash And Cash Equivalents')
    fig_cash = px.bar(qtr_df_select, x="date", y="Cash And Cash Equivalents", color="shortName", title='Cash And Cash Equivalents')
    col1_chart_b.plotly_chart(fig_cash, key="ticker3")#, on_select="rerun")
    
    #col2_chart_b.write('\nCapital Expenditure')
    fig_capex = px.bar(qtr_df_select, x="date", y="Capital Expenditure", color="shortName",title='Capital Expenditure')
    col2_chart_b.plotly_chart(fig_capex, key="ticker6")#, on_select="rerun")


    
    #dailyClosePrice_df['Ticker'] = ticker_select
    #st.write('\nDaily Close Price')
    fig_line = px.line(dailyClosePrice_df, x="Date", y="Close", title='Daily Close Price')#, color="green")
    st.plotly_chart(fig_line, key="ticker7")#, on_select="rerun")
    st.dataframe(dailyClosePrice_df)

    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('Company Profile')
    st.write(longBusinessSummary)


    #======================= END OF TAB1 =====================







# ### By Ticker only:

# In[16]:
#===================== TAB 2 =============================
with tab2:
    st.title('Stocks Comparison')
    
    ticker_ = st.multiselect('Select a ticker:',sorted(ticker_list)
                             ,['NVDA','QCOM','AMD','MU','ACLS','LRCX','DELL'
                              ,'ASML','CROX','MRK','INMD'
                              ]
                            )
    
    qtr_df2 = financials_quarter(ticker_)
    recent_df2 = df[df['ticker'].isin(ticker_)]
    price_shares_df2 = closePriceSharesCount(ticker_)
    #price_shares_df2 = closePriceDailyByList(ticker_)
    
    st.write('Recent statistics')
    st.dataframe(recent_df2)
   
    
    st.write('\n\n\n')
    st.write('\n\n\n')
    st.write('\n\n\n')

    #============ TAB2  SCATTER PLOT =================
    st.markdown("""
    Return On Equity vs Operating Margins : 
    - size by Forward PE
    """)
    fig_scatter2 = px.scatter(recent_df2
                             , x="operatingMargins", y="returnOnEquity"#,z='forwardPE'
                             , color="shortName"
                             , size= 'forwardPE'
                             , symbol = 'market_trend'
                             , hover_data=['ticker','market_trend','currentPrice','perc_Chg_52WkHigh']
                             )
    st.plotly_chart(fig_scatter2, key="ticker_b8")#, on_select="rerun")

    st.write('\nMonthly Close Price')
    #fig_line = px.line(price_shares_df2, x="Date", y="Close", color="Ticker")
    fig_line = px.line(price_shares_df2, x="date_close_price", y="close_price", color="ticker")
    st.plotly_chart(fig_line, key="ticker_b7")#, on_select="rerun")
  
    st.write('\nTotal Revenue')
    fig_revenue = px.bar(qtr_df2, x="date", y="Total Revenue", color="shortName")#,barmode='group')
    st.plotly_chart(fig_revenue, key="ticker_b1")#, on_select="rerun")
    
    st.write('\nNet Income')
    fig_netincome = px.bar(qtr_df2, x="date", y="Net Income", color="shortName")#,barmode='group')
    st.plotly_chart(fig_netincome, key="ticker_b2")#, on_select="rerun")

    st.write('\nCash And Cash Equivalents')
    fig_cash = px.bar(qtr_df2, x="date", y="Cash And Cash Equivalents", color="shortName")#,barmode='group')
    st.plotly_chart(fig_cash, key="ticker_b3")#, on_select="rerun")
  
    
    st.write('\nFree Cash Flow')
    fig_fcf = px.bar(qtr_df2, x="date", y="Free Cash Flow", color="shortName")#,barmode='group')
    st.plotly_chart(fig_fcf, key="ticker_b4")#, on_select="rerun")
    
    st.write('\nAccounts Receivable')
    fig_act_receivable = px.bar(qtr_df2, x="date", y="Accounts Receivable", color="shortName")#,barmode='group')
    st.plotly_chart(fig_act_receivable, key="ticker_b5")#, on_select="rerun")
    
    
    st.write('\nCapital Expenditure')
    fig_capex = px.bar(qtr_df2, x="date", y="Capital Expenditure", color="shortName")#,barmode='group')
    st.plotly_chart(fig_capex, key="ticker_b6")#, on_select="rerun")
    
    
    

    st.write('\n\n\n')
    st.write('Quarterly Financials')
    st.dataframe(qtr_df2[cols])
    st.write('\n\n\n')
    st.write('\nMonthly Close Price')
    st.dataframe(price_shares_df2)

    #=================== END OF TAB2 =======================




#====================== TAB3 ===========================
with tab3:
    st.title('VIX: Volatility Index')
    fig_line = px.line(vix_df, x="Date", y="Close", title='VIX: Volatility Index')#, color="green")
    st.plotly_chart(fig_line, key="ticker_c1")#, on_select="rerun")
    st.dataframe(vix_df)

with tab4:
  st.title('My Tickers:')
  st.dataframe(df)

