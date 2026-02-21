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
    # মাসগুলোকে ক্রমানুসারে সাজানো
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    
    # Temperature Range ক্যালকুলেট করা
    if 'Max_Temp' in df.columns and 'Min_Temp' in df.columns:
        df['Temp_Range'] = df['Max_Temp'] - df['Min_Temp']
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
    st.title("📈 Future Climate Forecast Dashboard (1981-2060)")
    st.markdown(f"### Results for: **{selected_month}, {selected_year}**")

    # ডেটা ফিল্টার করা
    filtered = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]

    if not filtered.empty:
        # ৫. ম্যাট্রিক কার্ডস (সব প্যারামিটার একসাথে)
        row1 = st.columns(3)
        row1[0].metric("🌡️ Max Temperature", f"{filtered['Max_Temp'].values[0]:.2f} °C")
        row1[1].metric("❄️ Min Temperature", f"{filtered['Min_Temp'].values[0]:.2f} °C")
        row1[2].metric("📊 Temp Range", f"{filtered['Temp_Range'].values[0]:.2f} °C")

        row2 = st.columns(2)
        row2[0].metric("💧 Humidity", f"{filtered['Humidity'].values[0]:.2f} %")
        row2[1].metric("🌧️ Precipitation (Rainfall)", f"{filtered['Precipitation'].values[0]:.2f} mm")

        st.divider()

        # ৬. গ্রাফ সেকশন (সব প্যারামিটারের ট্রেন্ড)
        st.subheader(f"📊 Seasonal Trends for the Year {selected_year}")
        year_df = df[df['Year'] == selected_year].sort_values('ds')
        
        # গ্রাফ ১: তাপমাত্রা (Max vs Min)
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=year_df, x='Month', y='Max_Temp', marker='o', color='red', label='Max Temp', ax=ax1)
        sns.lineplot(data=year_df, x='Month', y='Min_Temp', marker='s', color='blue', label='Min Temp', ax=ax1)
        plt.title("Temperature Variation")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        st.pyplot(fig1)

        # গ্রাফ ২: বৃষ্টিপাত এবং আর্দ্রতা (Side-by-side)
        col_left, col_right = st.columns(2)

        with col_left:
            st.write("🌧️ **Precipitation (Rainfall)**")
            fig2, ax2 = plt.subplots()
            sns.barplot(data=year_df, x='Month', y='Precipitation', color='skyblue', ax=ax2)
            plt.xticks(rotation=90)
            st.pyplot(fig2)

        with col_right:
            st.write("💧 **Humidity Levels**")
            fig3, ax3 = plt.subplots()
            sns.lineplot(data=year_df, x='Month', y='Humidity', marker='o', color='green', ax=ax3)
            plt.xticks(rotation=90)
            st.pyplot(fig3)

    # ৭. কম্পারিজন সেকশন
        st.sidebar.divider()
        compare_year = st.sidebar.checkbox("Compare with another year?")

        if compare_year:
            year_2 = st.sidebar.selectbox("Select Second Year", years, index=1, key="year2_select")
            
            st.divider()
            st.subheader(f"🔄 Comparison: {selected_year} vs {year_2}")
            
            compare_param = st.selectbox("Select Parameter to Compare", 
                                         ['Max_Temp', 'Min_Temp', 'Precipitation', 'Humidity'], 
                                         key="param_select")
            
            df_year1 = df[df['Year'] == selected_year].sort_values('ds')
            df_year2 = df[df['Year'] == year_2].sort_values('ds')
            
            fig_comp, ax_comp = plt.subplots(figsize=(12, 5))
            sns.lineplot(x=df_year1['Month'], y=df_year1[compare_param], marker='o', label=str(selected_year), ax=ax_comp)
            sns.lineplot(x=df_year2['Month'], y=df_year2[compare_param], marker='s', label=str(year_2), ax=ax_comp)
            
            plt.title(f"{compare_param} Comparison: {selected_year} vs {year_2}")
            plt.ylabel(compare_param)
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True, alpha=0.2)
            st.pyplot(fig_comp)
        
    else:
        st.error("Data not found for this selection!")

except Exception as e:
    st.error(f"Error: {e}")

