import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_cnt_by_hr_df(hr_df):
    hr_cnt_df = hr_df.groupby(by="hr").agg({"cnt": ["sum"]})
    return hr_cnt_df

def cnt_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({"registered": "sum"})
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({"casual": ["sum"]})
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season(day_df):
    season_df = day_df.groupby(by="season").cnt.sum().reset_index()
    return season_df

days_df = pd.read_csv("day_fix.csv")
hours_df = pd.read_csv("hour_fix.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://media.istockphoto.com/id/1452109378/id/vektor/layanan-datar-penyewaan-sepeda-ilustrasi-vektor-halaman-web-gaya-hidup-sepeda-kartun-naik.jpg?s=612x612&w=0&k=20&c=rS9C_4te1MN2V_yKmZjoYBKNttEUtFV-Xv58HdH_y2w=")
    
    # Mengambil start_date & end_date dari date_input
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date_days,
    max_value=max_date_days,
    value=[min_date_days, max_date_days])

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_cnt_by_hr_df(main_df_hour)
day_df_count_2011 = cnt_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)


# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Pada musim apa permintaan untuk menyewa sepeda paling tinggi?")
# Membuat subplot dengan 1 baris dan 1 kolom, dengan ukuran (15, 6)
fig, ax = plt.subplots(figsize=(15, 6))

# Membuat barplot untuk y="cnt" dan x="season", menggunakan data=day_df
sns.barplot(
    y="cnt", 
    x="season",
    data=days_df,
    hue="season",
    palette={"Spring": "#00FF00", "Summer": "#ff69b4", "Fall": "#FFA500", "Winter": "#87CEEB"}, 
    ax=ax,
    order=["Spring", "Summer", "Fall", "Winter"],  
)

# Mengatur judul, label y dan x
ax.set_title("Grafik Antar Musim", loc="center", fontsize=20)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=15)
ax.set_xlabel("Musim", fontsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Menampilkan plot di Streamlit
st.pyplot(fig)

st.subheader("Pengaruh cuaca terhadap orang yang menyewa sepeda")
# Menghitung rata-rata 'cnt' untuk setiap kategori 'weathersit'
avg_weather = days_df.groupby('weathersit')['cnt'].mean().reset_index().sort_values("cnt")

# Membuat barplot untuk menampilkan jumlah rata-rata 'cnt' untuk setiap kategori 'weathersit'
plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=avg_weather, hue='weathersit', palette='coolwarm')

# Mengatur judul, label sumbu x dan y
plt.title('Hubungan antara Cuaca dan Jumlah Sewa Sepeda')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Sewa Sepeda')

# Menampilkan plot di Streamlit
st.pyplot(plt)

st.subheader("Pada jam berapakah biasanya orang paling banyak menyewa sepeda")

# Menghitung rata-rata penyewaan sepeda berdasarkan jam
avg_hour = hours_df.groupby('hr')['cnt'].mean().reset_index()

# Mencari jam dengan rata-rata penyewaan sepeda tertinggi
max_avg_hour = avg_hour['hr'].iloc[avg_hour['cnt'].idxmax()]

# Membuat barplot untuk menampilkan rata-rata penyewaan sepeda berdasarkan jam
plt.figure(figsize=(12, 6))
sns.barplot(x='hr', y='cnt', data=avg_hour, hue='hr', palette='coolwarm')

# Menandai jam dengan rata-rata penyewaan sepeda tertinggi
plt.axvline(x=max_avg_hour, color='red', linestyle='--')

# Mengatur judul, label sumbu x dan y
plt.title('Rata - Rata Penyewaan Sepeda berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Rata - Rata Penyewaan')

# Menampilkan plot di Streamlit
st.pyplot(plt)
