# Import library yang dibutuhkan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='datetime').agg({
        "user_casual": "sum",
        "user_registered": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    return daily_rent_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by='holiday').agg({
    'user_casual':'sum',
    'user_registered':'sum'
})
    return byholiday_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by='workingday').agg({
    'user_casual':'sum',
    'user_registered':'sum'
})
    return byworkingday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by='weekday').agg({
    'user_casual':'sum',
    'user_registered':'sum'
})
    return byweekday_df

def create_byhour_df(df):
    byhour_df = df.groupby(by='hour').agg({
    'user_casual':'sum',
    'user_registered':'sum'
})
    return byhour_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").count_total.sum().reset_index()
    
    return byseason_df

def create_bytemp_df(df):
    bytemp_df = df.groupby(by="temp_group").count_total.sum().reset_index()
    
    return bytemp_df

# Membaca dataset yang digunakan
day_df = pd.read_csv(r'C:\Users\ticaf\Downloads\Dicoding\Submission\dashboard\main_data.csv')

day_df["datetime"] = pd.to_datetime(day_df["datetime"])
day_df.sort_values(by="datetime", inplace=True)
day_df.reset_index(inplace=True)

# Filter data
min_date = day_df["datetime"].min()
max_date = day_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(r"C:\Users\ticaf\Downloads\Dicoding\Submission\dashboard\Logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["datetime"] >= str(start_date)) & 
                (day_df["datetime"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
holiday_rent_df = create_byholiday_df(main_df)
workingday_rent_df = create_byworkingday_df(main_df)
weekday_rent_df = create_byweekday_df(main_df)
hour_rent_df = create_byhour_df(main_df)
season_rent_df = create_byseason_df(main_df)
temp_rent_df = create_bytemp_df(main_df)

# Visualisasi untuk Penyewaan Sepeda Berdasarkan Jenis User per Bulan Tahun 2011-2012
st.header('Bike-sharing Rental Dasboard')
st.subheader('Daily Rental')

col1, col2 = st.columns(2)

with col1:
    total_casual = daily_rent_df.user_casual.sum()
    st.metric("Total rent user casual", value=total_casual)

with col2:
    total_registered = daily_rent_df.user_registered.sum()
    st.metric("Total rent user registered", value=total_registered)

fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(x='datetime', y='user_casual', data=main_df, marker='o', label='Casual', ax=ax)
sns.lineplot(x='datetime', y='user_registered', data=main_df, marker='o', label='Registered', ax=ax)
plt.xlabel('Date')
plt.ylabel('Total Count')
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda di Hari Libur(Holiday)
st.subheader("Number of Customer at Holiday")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(x=holiday_rent_df.index, 
            y='user_registered', 
            data=holiday_rent_df, 
            color='blue', label='Registered')
sns.barplot(x=holiday_rent_df.index, 
            y='user_casual', 
            data=holiday_rent_df, 
            color='orange', label='Casual')

plt.xlabel("Holiday",fontsize=25)
plt.ylabel('Total Users',fontsize=25)
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda di Hari Kerja(Workingday)
st.subheader("Number of Customer at Workingday")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(x=workingday_rent_df.index, 
            y='user_registered', 
            data=workingday_rent_df, 
            color='blue', label='Registered')
sns.barplot(x=workingday_rent_df.index, 
            y='user_casual', 
            data=workingday_rent_df, 
            color='orange', label='Casual')

plt.xlabel("Workingday",fontsize=25)
plt.ylabel('Total Users',fontsize=25)
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda Per Hari dalam Seminggu(Weekday)
st.subheader("Number of Customer at Weekday")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(x=weekday_rent_df.index, 
            y='user_registered', 
            data=weekday_rent_df, 
            color='blue', label='Registered')
sns.barplot(x=weekday_rent_df.index, 
            y='user_casual', 
            data=weekday_rent_df, 
            color='orange', label='Casual')

plt.xlabel("Weekday",fontsize=25)
plt.ylabel('Total Users',fontsize=25)
plt.xticks(range(0, 7), ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda Per Jam(Hour)
st.subheader("Number of Customer based on Hour")

fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(x='hour', y='user_casual', data=hour_rent_df, marker='o', label='Casual', ax=ax)
sns.lineplot(x='hour', y='user_registered', data=hour_rent_df, marker='o', label='Registered', ax=ax)
plt.xlabel('Hour')
plt.ylabel('Total Count')
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda berdasarkan Musim(Season)
st.subheader("Number of Customer by Season")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot( 
        x="season",
        y="count_total",
        data=season_rent_df.sort_values(by="season", ascending=False),
        palette="coolwarm",
        ax=ax
    )

plt.xlabel("Season",fontsize=25)
plt.ylabel('Total Users',fontsize=25)
plt.xticks(range(0, 4), ['Springer', 'Summer', 'Fall', 'Winter'])
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda berdasarkan Suhu(Temperature)
st.subheader("Number of Customer by Temperature")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot( 
        x="temp_group",
        y="count_total",
        data=temp_rent_df.sort_values(by="temp_group", ascending=False),
        palette="coolwarm",
        ax=ax
    )

plt.xlabel("Temperature (Celcius)",fontsize=25)
plt.ylabel('Total Users',fontsize=25)
st.pyplot(fig)

st.caption('Copyright © ASA 2023')