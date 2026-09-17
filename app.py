import random

import altair as alt
import streamlit as st

from quiz_explorer.data import (
    check_answer,
    filter_questions,
    load_questions,
    search_questions,
    top_answers,
)

st.set_page_config(page_title="Quiz Explorer", layout="wide")
st.title("Quiz Explorer")
st.write("Explore a dataset of French general knowledge questions and test yourself.")


@st.cache_data
def get_data():
    return load_questions()


df = get_data()

# Sidebar filters
st.sidebar.header("Filters")
themes = st.sidebar.multiselect("Themes", sorted(df["theme"].unique()))
difficulty = st.sidebar.radio("Difficulty", ["All", "abordable", "expert"])
min_date, max_date = df["date"].min().date(), df["date"].max().date()
dates = st.sidebar.date_input("Dates", (min_date, max_date), min_date, max_date)

start_date = dates[0] if len(dates) > 0 else None
end_date = dates[1] if len(dates) > 1 else None
filtered = filter_questions(
    df, themes, None if difficulty == "All" else difficulty, start_date, end_date
)

explore_tab, play_tab = st.tabs(["Explore", "Play"])

with explore_tab:
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions", len(filtered))
    col2.metric("Themes", filtered["theme"].nunique())
    col3.metric("Days", filtered["date"].nunique())

    st.subheader("Most frequent answers")
    chart = (
        alt.Chart(top_answers(filtered))
        .mark_bar()
        .encode(x=alt.X("questions", title="Questions"), y=alt.Y("answer", sort="-x", title=None))
    )
    st.altair_chart(chart)

    st.subheader("Questions")
    keyword = st.text_input("Search")
    results = search_questions(filtered, keyword)
    st.write(f"{len(results)} result(s)")
    st.dataframe(results[["date", "difficulty", "theme", "question", "answer"]], hide_index=True)

with play_tab:
    if filtered.empty:
        st.warning("No question matches the filters.")
    else:
        if st.button("New question") or st.session_state.get("qid") not in filtered.index:
            st.session_state.qid = random.choice(filtered.index.tolist())

        question = df.loc[st.session_state.qid]
        st.write(f"**{question['theme']}** - {question['difficulty']}")
        st.subheader(question["question"])

        with st.form("answer"):
            answer = st.text_input("Your answer")
            submitted = st.form_submit_button("Check")

        if submitted:
            if check_answer(answer, question["valid_answers"]):
                st.success(f"Correct! The answer is {question['answer']}.")
            else:
                st.error(f"Wrong, the answer was {question['answer']}.")
