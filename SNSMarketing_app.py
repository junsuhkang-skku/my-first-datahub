import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 SNS Marketing Dashboard", layout="wide")

# 샘플 데이터
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"Campaign":"Summer Sale","Platform":"Instagram","Budget":5000,"Followers":10000,"Likes":1200,"Shares":200,"Comments":150},
        {"Campaign":"Product Launch","Platform":"TikTok","Budget":7000,"Followers":15000,"Likes":2500,"Shares":500,"Comments":300},
        {"Campaign":"Brand Awareness","Platform":"YouTube","Budget":6000,"Followers":20000,"Likes":1800,"Shares":350,"Comments":220}
    ])

df = st.session_state.data

# 계산
df["Engagement"] = df["Likes"] + df["Shares"] + df["Comments"]
df["Engagement Rate"] = (df["Engagement"] / df["Followers"]) * 100
df["ROI"] = (df["Engagement"] * 0.5) - df["Budget"]

st.title("📊 SNS Marketing Analytics")

# 입력
st.sidebar.header("➕ Add Campaign")
name = st.sidebar.text_input("Campaign Name")
platform = st.sidebar.selectbox("Platform", ["Instagram","TikTok","YouTube"])
budget = st.sidebar.number_input("Budget", 100,100000,5000)
followers = st.sidebar.number_input("Followers", 100,1000000,10000)
likes = st.sidebar.number_input("Likes",0,100000,1000)
shares = st.sidebar.number_input("Shares",0,50000,100)
comments = st.sidebar.number_input("Comments",0,50000,50)

if st.sidebar.button("Add"):
    new = pd.DataFrame([{
        "Campaign":name,"Platform":platform,"Budget":budget,
        "Followers":followers,"Likes":likes,"Shares":shares,"Comments":comments
    }])
    st.session_state.data = pd.concat([df,new], ignore_index=True)
    st.rerun()

df = st.session_state.data
df["Engagement"] = df["Likes"] + df["Shares"] + df["Comments"]
df["Engagement Rate"] = (df["Engagement"] / df["Followers"]) * 100
df["ROI"] = (df["Engagement"] * 0.5) - df["Budget"]

# KPI
c1,c2,c3 = st.columns(3)
c1.metric("Avg Engagement", f"{df['Engagement Rate'].mean():.2f}%")
c2.metric("Total ROI", f"${df['ROI'].sum():,.0f}")
c3.metric("Total Engagement", int(df["Engagement"].sum()))

# 색상
def color_roi(val):
    return "background-color:#d4edda" if val>0 else "background-color:#f8d7da"

st.dataframe(df.applymap(color_roi, subset=["ROI"]), width="stretch")

# 차트
st.subheader("Weekly Performance")
weekly = pd.DataFrame({
    "Week":["W1","W2","W3","W4"],
    "Summer Sale":[200,300,400,500],
    "Product Launch":[300,450,600,800],
    "Brand Awareness":[250,350,500,650]
})
fig = px.line(weekly, x="Week", y=weekly.columns[1:], markers=True)
st.plotly_chart(fig, width="stretch")
