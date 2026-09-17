"""
Functions to load and filter the quiz questions.
"""

import json
import unicodedata

import pandas as pd

DATA_PATH = "data/questions.json"
COLUMNS = ["date", "difficulty", "theme", "question", "answer", "valid_answers"]


def load_questions(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load the questions from a JSON file.

    :param path: path to the JSON file
    :return: questions sorted by date
    """
    with open(path, encoding="utf-8") as f:
        df = pd.DataFrame(json.load(f))

    for column in COLUMNS:
        if column not in df.columns:
            raise ValueError(f"Column {column} is missing in {path}")

    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def filter_questions(df: pd.DataFrame, themes=None, difficulty=None, start=None, end=None):
    """
    Keep the questions matching the filters. Empty filters are ignored.

    :param df: questions
    :param themes: list of themes
    :param difficulty: "abordable" or "expert"
    :param start: first date (included)
    :param end: last date (included)
    :return: filtered questions
    """
    if themes:
        df = df[df["theme"].isin(themes)]
    if difficulty:
        df = df[df["difficulty"] == difficulty]
    if start:
        df = df[df["date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["date"] <= pd.Timestamp(end)]
    return df


def search_questions(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Keep the questions containing the keyword (not case sensitive).

    :param df: questions
    :param keyword: word to look for
    :return: matching questions
    """
    return df[df["question"].str.contains(keyword, case=False, regex=False)]


def top_answers(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """
    Count the most frequent answers.

    :param df: questions
    :param n: number of answers to keep
    :return: number of questions for each answer
    """
    return df["answer"].value_counts().head(n)


def remove_accents(text: str) -> str:
    """
    Lowercase the text and remove its accents.

    :param text: text to clean
    :return: cleaned text
    """
    text = unicodedata.normalize("NFD", text.lower().strip())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def check_answer(answer: str, valid_answers: list[str]) -> bool:
    """
    Check if the answer is one of the valid answers (ignoring case and accents).

    :param answer: answer given by the user
    :param valid_answers: accepted answers
    :return: True if the answer is correct
    """
    valid = [remove_accents(v) for v in valid_answers]
    return remove_accents(answer) in valid
