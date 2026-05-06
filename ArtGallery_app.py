import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎨 Art Gallery", layout="wide")

# -----------------------------
# 🎨 초기 데이터
# -----------------------------
if "artworks" not in st.session_state:
    st.session_state.artworks = pd.DataFrame([
        {"Title": "Mona Lisa", "Artist": "Leonardo da Vinci", "Year": 1503, "Medium": "Oil", "Price": 850, "Period": "Renaissance"},
        {"Title": "Starry Night", "Artist": "Vincent van Gogh", "Year": 1889, "Medium": "Oil", "Price": 100, "Period": "Post-Impressionism"},
        {"Title": "The Scream", "Artist": "Edvard Munch", "Year": 1893, "Medium": "Oil", "Price": 120, "Period": "Expressionism"},
        {"Title": "The Persistence of Memory", "Artist": "Salvador Dalí", "Year": 1931, "Medium": "Oil", "Price": 60, "Period": "Surrealism"},
        {"Title": "Girl with a Pearl Earring", "Artist": "Johannes Vermeer", "Year": 1665, "Medium": "Oil", "Price": 200, "Period": "Baroque"},
    ])

df = st.session_state.artworks

# -----------------------------
# 🎨 UI
# -----------------------------
st.title("🎨 Art Gallery Dashboard")
st.caption("✨ Manage and explore artworks")

# Sidebar 입력
st.sidebar.header("➕ Add Artwork")

with st.sidebar.form("form"):
    title = st.text_input("Title")
    artist = st.text_input("Artist")
    year = st.number_input("Year", 1000, 2100, 2000)
    medium = st.selectbox("Medium", ["Oil", "Acrylic", "Digital"])
    price = st.number_input("Price", 1, 1000, 50)
    period = st.selectbox("Period", ["Renaissance", "Baroque", "Modern", "Other"])

    submit = st.form_submit_button("Add")

    if submit and title and artist:
        new = pd.DataFrame([{
            "Title": title,
            "Artist": artist,
            "Year": year,
            "Medium": medium,
            "Price": price,
            "Period": period
        }])
        st.session_state.artworks = pd.concat([df, new], ignore_index=True)

df = st.session_state.artworks

# 검색
search = st.text_input("🔍 Search artist")
if search:
    df = df[df["Artist"].str.contains(search, case=False)]

# 테이블
st.subheader("📋 Artworks")
st.dataframe(df, width="stretch")

# 차트
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Prices")
    fig1 = px.bar(df, x="Title", y="Price", color="Artist")
    st.plotly_chart(fig1, width="stretch")

with col2:
    st.subheader("🎭 Period")
    fig2 = px.pie(df, names="Period")
    st.plotly_chart(fig2, width="stretch")
