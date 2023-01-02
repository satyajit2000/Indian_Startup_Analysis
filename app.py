import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('startup_cleandata.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def overall_analysis():
    #total amount
    total = round(df['amount'].sum())
    #max amount
    max_amount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #average funding
    avg_amount = round(df.groupby('startup')['amount'].sum().mean())

    #total funded
    total_fund = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_amount) + ' Cr')
    with col3:
        st.metric('Average', str(avg_amount) + ' Cr')
    with col4:
        st.metric('Total Fund', str(total_fund))

    st.header('Month to Month Graph')
    temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig5)






def investor_details(investor):
    st.title(investor)
    last_df = df[df['investors'].str.contains(investor)].head()[['date','startup','verticle','city','round','amount']]
    st.subheader('Recent Investment')
    st.dataframe(last_df)

    col1, col2 = st.columns(2)
    with col1:
        #biggest Investment
        big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_df.index, big_df.values)
        st.pyplot(fig)

    with col2:
        pie_chart = df[df['investors'].str.contains(investor)].groupby('verticle')['amount'].sum()

        st.subheader('Sector Investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(pie_chart,labels=pie_chart.index,autopct = "%0.01f%%")
        st.pyplot(fig1)
    col3, col4 = st.columns(2)

    with col3:
        stage_chart = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Stage Investment')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_chart, labels=stage_chart.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        city_chart = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('City Wise Investment')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_chart, labels=city_chart.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    year_chart = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year to Year Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_chart.index, year_chart.values)
    st.pyplot(fig4)







st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
    btn_overall = st.sidebar.button('Show Overall Analysis')
    if btn_overall:
        overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn_startup = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    investor_selected = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn_investor = st.sidebar.button('Find Investor Details')
    if btn_investor:
        investor_details(investor_selected)

