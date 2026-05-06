import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎮 Gaming Dashboard", layout="wide")

# -----------------------------
# 🎮 샘플 데이터
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame([
        {"Game": "Valorant", "Rank": "Gold", "Wins": 30, "Losses": 20, "PlayTime": 2},
        {"Game": "League of Legends", "Rank": "Platinum", "Wins": 50, "Losses": 40, "PlayTime": 3},
        {"Game": "Overwatch", "Rank": "Silver", "Wins": 20, "Losses": 25, "PlayTime": 1.5},
    ])

df = st.session_state.data

# 계산
df["Total Matches"] = df["Wins"] + df["Losses"]
df["Win Rate"] = (df["Wins"] / df["Total Matches"]) * 100
df["Rank Score"] = df["Wins"] * 10 - df["Losses"] * 5
df["Total PlayTime"] = df["PlayTime"] * 7

st.title("🎮 Gaming Stats Dashboard")

# Sidebar
st.sidebar.header("➕ Add Game Data")
game = st.sidebar.text_input("Game Name")
rank = st.sidebar.selectbox("Rank", ["Bronze", "Silver", "Gold", "Platinum"])
wins = st.sidebar.number_input("Wins", 0, 1000, 10)
losses = st.sidebar.number_input("Losses", 0, 1000, 5)
playtime = st.sidebar.number_input("Daily Play Time", 0.5, 24.0, 2.0)

if st.sidebar.button("Add"):
    new = pd.DataFrame([{
        "Game": game,
        "Rank": rank,
        "Wins": wins,
        "Losses": losses,
        "PlayTime": playtime
    }])
    st.session_state.data = pd.concat([df, new], ignore_index=True)
    st.rerun()

df = st.session_state.data
df["Total Matches"] = df["Wins"] + df["Losses"]
df["Win Rate"] = (df["Wins"] / df["Total Matches"]) * 100
df["Rank Score"] = df["Wins"] * 10 - df["Losses"] * 5
df["Total PlayTime"] = df["PlayTime"] * 7

# 필터
game_select = st.selectbox("🎮 Select Game", df["Game"].unique())
filtered = df[df["Game"] == game_select]

# KPI
c1,c2,c3,c4 = st.columns(4)
win_rate = filtered["Win Rate"].iloc[0]

c1.metric("Win Rate", f"{win_rate:.1f}%")
c2.metric("Matches", int(filtered["Total Matches"].iloc[0]))
c3.metric("Play Time", f"{filtered['Total PlayTime'].iloc[0]:.1f}h")
c4.metric("Rank Score", int(filtered["Rank Score"].iloc[0]))

# 색상 표시
color = "green" if win_rate > 50 else "red"
st.markdown(f"<h3 style='color:{color}'>Performance</h3>", unsafe_allow_html=True)

# 차트
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(x=["Wins","Losses"],
                  y=[filtered["Wins"].iloc[0], filtered["Losses"].iloc[0]],
                  title="Wins vs Losses")
    st.plotly_chart(fig1, width="stretch")

with col2:
    weekly = pd.DataFrame({
        "Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Hours":[filtered["PlayTime"].iloc[0]]*7
    })
    fig2 = px.line(weekly, x="Day", y="Hours", markers=True, title="Weekly Play Time")
    st.plotly_chart(fig2, width="stretch")

# 랭크 progression
progress = pd.DataFrame({
    "Match": list(range(1,11)),
    "Score":[filtered["Rank Score"].iloc[0] + i*5 for i in range(10)]
})
fig3 = px.line(progress, x="Match", y="Score", markers=True)
st.plotly_chart(fig3, width="stretch")

# 테이블
st.dataframe(df, width="stretch")
