import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ১. পেজ সেটআপ
st.set_page_config(page_title="Climate Prediction 1981-2060", layout="wide")

# ২. ডেটা লোড করার ফাংশন
@st.cache_data
def load_data():
    # তোমার ফাইলের নাম হুবহু এক হতে হবে
    df = pd.read_csv('Full_Climate_Dataset_1981_2060_Final.csv')
    df['ds'] = pd.to_datetime(df['ds'])
    df['Year'] = df['ds'].dt.year
    df['Month'] = df['ds'].dt.month_name()
    return df

try:
    df = load_data()

    # ৩. সাইডবার ফিল্টার
    st.sidebar.title("🌍 Search Filters")
    years = sorted(df['Year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Year", years)

    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    selected_month = st.sidebar.selectbox("Select Month", months)

    # ৪. মূল ড্যাশবোর্ড কন্টেন্ট
    st.title("📈 Future Climate Forecast Dashboard")
    st.write(f"Showing results for: **{selected_month}, {selected_year}**")

    # ডেটা ফিল্টার করা
    filtered = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]

    if not filtered.empty:
        # ম্যাট্রিক কার্ডস (বক্সের মতো দেখাবে)
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Max Temperature", f"{filtered['Max_Temp'].values[0]:.2f} °C")
        col2.metric("💧 Humidity", f"{filtered['Humidity'].values[0]:.2f} %")
        col3.metric("🌧️ Rainfall", f"{filtered['Precipitation'].values[0]:.2f} mm")

        st.divider()

        # ৫. গ্রাফ: ওই বছরের তাপমাত্রা ও বৃষ্টির ট্রেন্ড
        st.subheader(f"📊 Annual Trend for {selected_year}")
        year_df = df[df['Year'] == selected_year]
        
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=year_df, x='Month', y='Max_Temp', marker='o', color='red', label='Max Temp')
        plt.xticks(rotation=45)
        st.legend()
        st.pyplot(fig)
    else:
        st.error("Data not found for this selection!")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure your CSV file name matches exactly with 'Full_Climate_Dataset_1981_2060_Final.csv'")
