import json

import pandas as pd

DATA_PATH = "data/questions.json"


def load_questions(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load the questions from a JSON file.

    :param path: path to the JSON file
    :return: questions sorted by date
    """
    with open(path, encoding="utf-8") as f:
        df = pd.DataFrame(json.load(f))
    if "question" not in df.columns or "answer" not in df.columns:
        raise ValueError("The file must contain questions and answers.")
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")


def filter_questions(df: pd.DataFrame, theme: str, difficulty: str) -> pd.DataFrame:
    """
    Keep the questions of the chosen theme and difficulty ("All" keeps everything).

    :param df: questions
    :param theme: theme to keep
    :param difficulty: difficulty to keep
    :return: filtered questions
    """
    if theme != "All":
        df = df[df["theme"] == theme]
    if difficulty != "All":
        df = df[df["difficulty"] == difficulty]
    return df


def search_questions(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Keep the questions containing the keyword.

    :param df: questions
    :param keyword: word to look for
    :return: matching questions
    """
    return df[df["question"].str.lower().str.contains(keyword.lower(), regex=False)]


def check_answer(answer: str, valid_answers: list) -> bool:
    """
    Check if the answer is correct.

    :param answer: answer given by the user
    :param valid_answers: accepted answers
    :return: True if the answer is correct
    """
    return answer.lower().strip() in [a.lower() for a in valid_answers]
