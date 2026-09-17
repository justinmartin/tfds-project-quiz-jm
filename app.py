import random

import streamlit as st

from quiz_explorer.data import (
    check_answer,
    filter_questions,
    load_questions,
    search_questions,
    top_answers,
)

st.title("Quiz Explorer")
st.write("Explore and play with French general knowledge quiz questions.")


@st.cache_data
def get_data():
    return load_questions()


df = get_data()

# Filters
st.sidebar.header("Filters")
themes = st.sidebar.multiselect("Themes", sorted(df["theme"].unique()))
difficulty = st.sidebar.selectbox("Difficulty", ["All", "abordable", "expert"])
start = st.sidebar.date_input("From", df["date"].min().date())
end = st.sidebar.date_input("To", df["date"].max().date())

if difficulty == "All":
    difficulty = None
questions = filter_questions(df, themes, difficulty, start, end)

st.write(f"{len(questions)} questions selected")

# Explore
st.header("Explore")
st.subheader("Most frequent answers")
st.bar_chart(top_answers(questions))

st.subheader("Search")
keyword = st.text_input("Keyword")
st.dataframe(search_questions(questions, keyword)[["date", "theme", "question", "answer"]])

# Play
st.header("Play")
if questions.empty:
    st.write("No question for these filters.")
else:
    if st.button("New question") or st.session_state.get("index") not in questions.index:
        st.session_state.index = random.choice(questions.index)

    question = df.loc[st.session_state.index]
    st.write(f"**{question['theme']}** ({question['difficulty']})")
    st.write(question["question"])
    answer = st.text_input("Your answer", key=f"answer_{st.session_state.index}")

    if answer:
        if check_answer(answer, question["valid_answers"]):
            st.success("Correct!")
        else:
            st.error(f"Wrong, the answer was {question['answer']}.")
