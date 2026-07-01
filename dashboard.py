import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

st.set_page_config(page_title="경희대 우울증 게시판 분석", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_excel("everytime_posts_2024_2026.xlsx")
    df["parsed_time"] = df["time"].apply(parse_time)
    df = df.dropna(subset=["parsed_time"])
    df["year"] = df["parsed_time"].dt.year
    df["month"] = df["parsed_time"].dt.month
    df["hour"] = df["parsed_time"].dt.hour
    df["weekday"] = df["parsed_time"].dt.weekday  # 0=월, 6=일
    df["year_month"] = df["parsed_time"].dt.to_period("M").astype(str)
    return df


def parse_time(t):
    t = str(t).strip()
    try:
        # YY/MM/DD 형식 (예: 24/03/15, 25/06/20)
        if t.count("/") == 2:
            parts = t.split("/")
            yy = int(parts[0])
            mm = int(parts[1])
            dd_hm = parts[2].split()
            dd = int(dd_hm[0])
            hour, minute = (int(x) for x in dd_hm[1].split(":")) if len(dd_hm) > 1 else (0, 0)
            return pd.Timestamp(2000 + yy, mm, dd, hour, minute)
        # MM/DD HH:MM 형식 (현재 연도 2026)
        if t.count("/") == 1:
            date_part, time_part = t.split()
            mm, dd = (int(x) for x in date_part.split("/"))
            hour, minute = (int(x) for x in time_part.split(":"))
            return pd.Timestamp(2026, mm, dd, hour, minute)
    except Exception:
        return None


STOPWORDS = {"것", "수", "이", "가", "을", "를", "은", "는", "에", "의", "도", "로", "으로",
             "그", "저", "제", "다", "고", "에서", "와", "과", "하", "합니다", "해요", "있어요",
             "있는", "있는데", "없어요", "없는데", "어요", "아요", "네요", "했어요", "같아요",
             "그냥", "진짜", "너무", "정말", "좀", "더", "또", "이제", "그래도", "근데",
             "싶어요", "싶은데", "아닌", "않아요", "않는", "같은데", "거", "거요", "건"}


def get_keywords(texts, top_n=30):
    words = []
    for text in texts:
        if not isinstance(text, str):
            continue
        tokens = re.findall(r"[가-힣]{2,}", text)
        words.extend([w for w in tokens if w not in STOPWORDS])
    return Counter(words).most_common(top_n)


df = load_data()

# 사이드바
st.sidebar.title("필터")
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("연도", years, default=years)
df_filtered = df[df["year"].isin(selected_years)]

# 헤더
st.title("경희대학교 우울증 게시판 패턴 분석")
st.caption(f"데이터: 에브리타임 경희대 우울증 게시판 | {df_filtered['parsed_time'].min().date()} ~ {df_filtered['parsed_time'].max().date()}")

# 요약 지표
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 게시글", f"{len(df_filtered):,}개")
col2.metric("평균 좋아요", f"{df_filtered['likes'].mean():.1f}")
col3.metric("평균 댓글", f"{df_filtered['comments'].mean():.1f}")
col4.metric("가장 활발한 시간", f"{df_filtered['hour'].mode()[0]}시")

st.divider()

# 월별 추이
st.subheader("월별 게시글 수 추이")
monthly = df_filtered.groupby("year_month").size().reset_index(name="count")
fig_monthly = px.line(monthly, x="year_month", y="count", markers=True,
                      labels={"year_month": "월", "count": "게시글 수"})
fig_monthly.update_layout(height=350, xaxis_tickangle=-45)
st.plotly_chart(fig_monthly, width='stretch')

st.divider()

col_a, col_b = st.columns(2)

# 시간대별
with col_a:
    st.subheader("시간대별 활동")
    hourly = df_filtered.groupby("hour").size().reset_index(name="count")
    fig_hour = px.bar(hourly, x="hour", y="count",
                      labels={"hour": "시간", "count": "게시글 수"},
                      color="count", color_continuous_scale="Blues")
    fig_hour.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_hour, width='stretch')

# 요일별
with col_b:
    st.subheader("요일별 활동")
    day_names = ["월", "화", "수", "목", "금", "토", "일"]
    weekly = df_filtered.groupby("weekday").size().reset_index(name="count")
    weekly["day_name"] = weekly["weekday"].map(lambda x: day_names[x])
    fig_week = px.bar(weekly, x="day_name", y="count",
                      labels={"day_name": "요일", "count": "게시글 수"},
                      color="count", color_continuous_scale="Purples",
                      category_orders={"day_name": day_names})
    fig_week.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_week, width='stretch')

st.divider()

# 키워드
st.subheader("주요 키워드 TOP 30")
keywords = get_keywords(df_filtered["content"])
if keywords:
    kw_df = pd.DataFrame(keywords, columns=["키워드", "빈도"])
    fig_kw = px.bar(kw_df, x="빈도", y="키워드", orientation="h",
                    color="빈도", color_continuous_scale="Reds")
    fig_kw.update_layout(height=600, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_kw, width='stretch')

st.divider()

# 반응 TOP 게시글
st.subheader("반응 많은 게시글 TOP 10")
top_posts = df_filtered.nlargest(10, "likes")[["time", "title", "content", "likes", "comments", "scraps"]]
top_posts["content"] = top_posts["content"].str[:80] + "..."
st.dataframe(top_posts.reset_index(drop=True), width='stretch')
