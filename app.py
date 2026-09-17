import random

import streamlit as st

from quiz_explorer.data import check_answer, filter_questions, load_questions, search_questions

st.title("Quiz Explorer")


@st.cache_data
def get_questions():
    return load_questions()


df = get_questions()

# Filters
theme = st.sidebar.selectbox("Theme", ["All"] + sorted(df["theme"].unique()))
difficulty = st.sidebar.selectbox("Difficulty", ["All", "abordable", "expert"])
questions = filter_questions(df, theme, difficulty)

# Explore
st.header("Questions")
st.write(f"{len(questions)} questions")
st.bar_chart(questions["answer"].value_counts().head(10))
keyword = st.text_input("Search a question")
st.dataframe(search_questions(questions, keyword)[["date", "theme", "question", "answer"]])

# Play
st.header("Play")
if st.button("New question") or st.session_state.get("index") not in questions.index:
    st.session_state.index = random.choice(questions.index)

question = df.loc[st.session_state.index]
st.write(question["question"])
answer = st.text_input("Your answer", key=str(st.session_state.index))
if answer:
    if check_answer(answer, question["valid_answers"]):
        st.success("Correct!")
    else:
        st.error(f"Wrong, the answer was {question['answer']}.")
