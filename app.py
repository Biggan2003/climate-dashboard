import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ১. পেজ সেটআপ
st.set_page_config(page_title="Climate Prediction 1981-2060", layout="wide")

# ২. ডেটা লোড করার ফাংশন
@st.cache_data
def load_data():
    df = pd.read_csv('Full_Climate_Dataset_1981_2060_Final.csv')
    df['ds'] = pd.to_datetime(df['ds'])
    df['Year'] = df['ds'].dt.year
    df['Month'] = df['ds'].dt.month_name()
    # মাসগুলোকে ক্রমানুসারে সাজানোর জন্য
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    return df

try:
    df = load_data()

    # ৩. সাইডবার ফিল্টার
    st.sidebar.title("🌍 Search Filters")
    years = sorted(df['Year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Year", years)

    # ৪. মূল ড্যাশবোর্ড কন্টেন্ট
    st.title("📈 Future Climate Forecast Dashboard")
    st.markdown(f"### Yearly Overview for: **{selected_year}**")

    # ৫. ওই বছরের তাপমাত্রা ও বৃষ্টির ট্রেন্ড (পুরো বছরের গ্রাফ)
    year_df = df[df['Year'] == selected_year].sort_values('ds')
    
    if not year_df.empty:
        # ম্যাট্রিক কার্ডস (বছরের গড় ভ্যালু দেখাবে)
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Avg Max Temp", f"{year_df['Max_Temp'].mean():.2f} °C")
        col2.metric("💧 Avg Humidity", f"{year_df['Humidity'].mean():.2f} %")
        col3.metric("🌧️ Total Rainfall (Avg)", f"{year_df['Precipitation'].mean():.2f} mm")

        st.divider()

        # গ্রাফ তৈরি
        st.subheader(f"📊 Monthly Temperature Trend for {selected_year}")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=year_df, x='Month', y='Max_Temp', marker='o', color='red', label='Max Temp', ax=ax)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend() # এটি গ্রাফের ভেতর লেজেন্ড দেখাবে
        st.pyplot(fig)
        
        # বৃষ্টির গ্রাফ
        st.subheader(f"🌧️ Monthly Rainfall Trend for {selected_year}")
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        sns.barplot(data=year_df, x='Month', y='Precipitation', color='skyblue', ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    else:
        st.error("Data not found for this year!")

except Exception as e:
    st.error(f"Error: {e}")
