"""
Loading, filtering and search functions for the quiz questions dataset.
"""

import json
import unicodedata
from pathlib import Path

import pandas as pd

DATA_PATH: Path = Path(__file__).parent.parent / "data" / "questions.json"
REQUIRED_COLUMNS: list[str] = ["date", "difficulty", "theme", "question", "answer", "valid_answers"]


def load_questions(path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Load the questions from a JSON file.

    :param path: path to the JSON file
    :return: questions sorted by date, with a datetime ``date`` column
    """
    with open(path, encoding="utf-8") as f:
        df = pd.DataFrame(json.load(f))

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing column(s) in {path}: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["date", "difficulty", "order"]).reset_index(drop=True)


def filter_questions(
    df: pd.DataFrame,
    themes: list[str] | None = None,
    difficulty: str | None = None,
    start_date=None,
    end_date=None,
) -> pd.DataFrame:
    """
    Filter the questions. Filters left empty are ignored.

    :param df: questions
    :param themes: themes to keep
    :param difficulty: difficulty to keep ("abordable" or "expert")
    :param start_date: first date to keep (included)
    :param end_date: last date to keep (included)
    :return: filtered questions
    """
    if themes:
        df = df[df["theme"].isin(themes)]
    if difficulty:
        df = df[df["difficulty"] == difficulty]
    if start_date is not None:
        df = df[df["date"] >= pd.Timestamp(start_date)]
    if end_date is not None:
        df = df[df["date"] <= pd.Timestamp(end_date)]
    return df


def normalize(text: str) -> str:
    """
    Lowercase the text and remove accents and extra spaces.

    :param text: text to normalize
    :return: normalized text
    """
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.lower().split())


def search_questions(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Keep the questions whose text or answer contains the keyword.

    :param df: questions
    :param keyword: word to look for (case and accents are ignored)
    :return: matching questions
    """
    keyword = normalize(keyword)
    if not keyword:
        return df
    in_question = df["question"].map(normalize).str.contains(keyword, regex=False)
    in_answer = df["answer"].map(normalize).str.contains(keyword, regex=False)
    return df[in_question | in_answer]


def check_answer(user_answer: str, valid_answers: list[str]) -> bool:
    """
    Check the user's answer against the accepted answers.

    :param user_answer: answer typed by the user
    :param valid_answers: accepted answers
    :return: True if the answer is accepted
    """
    guess = normalize(user_answer)
    return bool(guess) and any(guess == normalize(answer) for answer in valid_answers)


def top_answers(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Find the answers that come up most often.

    Answers are grouped after normalization, so "Brésil" and "bresil" count as one.

    :param df: questions
    :param n: number of answers to keep
    :return: table with ``answer`` and ``questions`` columns, most common first
    """
    counts = (
        df.assign(key=df["answer"].map(normalize))
        .groupby("key")
        .agg(answer=("answer", "first"), questions=("answer", "size"))
    )
    counts = counts.sort_values("questions", ascending=False, kind="stable")
    return counts.head(n).reset_index(drop=True)
