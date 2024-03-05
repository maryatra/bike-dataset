import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk mengimpor data
@st.cache
def load_data():
    data_df = pd.read_csv('day.csv')
    return data_df

# Fungsi untuk melakukan pembersihan data
def clean_data(data_df):
    data_df['season'] = data_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return data_df

# Fungsi untuk menjawab pertanyaan EDA
def eda_questions(data_df):
    st.subheader('Exploratory Data Analysis (EDA)')
    
    st.subheader('Pertanyaan 1')
    st.write("Bagaimana distribusi peminjaman untuk masing-masing musim dan kondisi cuaca?")
    st.write('')
    st.write("Melakukan pemetaan tabel menggunakan pivot table")
    data_df['season'] = data_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    data_musim = data_df.groupby(by=["season", "weathersit"]).agg({
        "casual": "nunique",
        "registered": "nunique"
    })
    st.write(data_musim)
    st.write('Grafik')
    data_musim['total'] = data_musim['casual'] + data_musim['registered']
    fig, ax = plt.subplots()
    sns.barplot(data=data_musim, x="season", y="total", hue="weathersit", errorbar=None, ax=ax)
    st.pyplot(fig)

    st.subheader('Pertanyaan 2')
    st.write("Pengaruh hari kerja/ akhir pekan terhadap peminjaman untuk setiap musim?")
    st.write('')
    st.write("Melakukan pemetaan tabel menggunakan pivot table")
    data_holiday = data_df.groupby(by="season").agg({
        "casual": "nunique",
        "registered": "nunique",
    })
    st.write(data_holiday)
    st.write('Grafik')
    data_holiday['total'] = data_holiday['casual'] + data_holiday['registered']
    fig, ax = plt.subplots()
    sns.scatterplot(data=data_holiday, x='season', y='casual', ax=ax)
    sns.scatterplot(data=data_holiday, x='season', y='registered', ax=ax)
    ax.set_ylim(150, 190)
    st.pyplot(fig)

    # Kesimpulan Pertanyaan 1
    st.subheader('Kesimpulan Pertanyaan 1:')
    total_rental_per_weather = data_df.groupby('weathersit')['cnt'].sum()
    st.write("Berdasarkan analisis, terlihat bahwa distribusi peminjaman berbeda-beda untuk setiap musim dan kondisi cuaca.")
    st.write("Total peminjaman untuk masing-masing kondisi cuaca:")
    st.write(total_rental_per_weather)

    # Kesimpulan Pertanyaan 2
    st.subheader('Kesimpulan Pertanyaan 2:')
    weekday_vs_weekend = data_df.groupby('weekday')['cnt'].sum()
    st.write("Berdasarkan analisis, terdapat hubungan antara hari kerja/akhir pekan dengan jumlah peminjaman untuk setiap musim.")
    st.write("Total peminjaman pada hari kerja vs akhir pekan:")
    st.write(weekday_vs_weekend)

def main():
    st.title('Analisis Data Bike Sharing')
    data_df = load_data()
    
    menu = ["Exploratory Data Analysis (EDA)"]
    choice = st.sidebar.selectbox("Pilihan Menu", menu)

    if choice == "Exploratory Data Analysis (EDA)":
        eda_questions(data_df)

if __name__ == "__main__":
    main()
