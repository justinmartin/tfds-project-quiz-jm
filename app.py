import random

import streamlit as st

from quiz_explorer.data import check_answer, filter_questions, load_questions

st.title("Tools for Data Science - Project")


@st.cache_data
def get_questions():
    return load_questions()


df = get_questions()

st.header("French General Knowledge Quiz")
st.subheader(
    "This project is an extract of a personal project I created to play with friends. "
    "Here is a small extract of the questions, in French, that I used to create the streamlit app."
)

theme = st.selectbox("Theme", ["All"] + sorted(df["theme"].unique()))
difficulty = st.selectbox("Difficulty", ["All", "abordable", "expert"])
questions = filter_questions(df, theme, difficulty)

st.write(f"{len(questions)} questions")
st.bar_chart(questions["answer"].value_counts().head(10))


st.header("Play")
if st.button("New question") or "index" not in st.session_state:
    st.session_state.index = random.choice(questions.index)

question = df.loc[st.session_state.index]
st.write(question["question"])
with st.form("answer", clear_on_submit=True):
    answer = st.text_input("Your answer")
    submitted = st.form_submit_button("Check")

if submitted:
    if check_answer(answer, question["valid_answers"]):
        st.success("Correct!")
    else:
        st.error(f"Wrong, the answer was {question['answer']}.")


st.subheader("List of questions")
st.dataframe(questions[["date", "theme", "difficulty", "question", "answer"]])
