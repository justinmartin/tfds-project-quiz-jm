import json
from datetime import datetime

import pandas as pd
from pytest import fixture, raises

from quiz_explorer.data import (
    check_answer,
    filter_questions,
    load_questions,
    normalize,
    search_questions,
    top_answers,
)

SAMPLE: list[dict] = [
    {
        "date": "2026-01-02",
        "difficulty": "expert",
        "order": 1,
        "theme": "Géographie",
        "question": "Quelle est la capitale du Pérou ?",
        "answer": "Lima",
        "valid_answers": ["Lima"],
    },
    {
        "date": "2026-01-01",
        "difficulty": "abordable",
        "order": 1,
        "theme": "Classique",
        "question": "Qui a peint la Joconde ?",
        "answer": "Léonard de Vinci",
        "valid_answers": ["Léonard de Vinci", "de vinci"],
    },
    {
        "date": "2026-01-03",
        "difficulty": "abordable",
        "order": 1,
        "theme": "Sport",
        "question": "Combien de joueurs dans une équipe de football ?",
        "answer": "11",
        "valid_answers": ["11", "onze"],
    },
]


@fixture
def sample_path(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return path


@fixture
def df(sample_path):
    return load_questions(sample_path)


def test_load_questions(df):
    assert len(df) == 3
    assert df["date"].iloc[0] == datetime(2026, 1, 1)


def test_load_questions_sorted_by_date(df):
    assert df["date"].is_monotonic_increasing


def test_load_questions_missing_column(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps([{"question": "?"}]), encoding="utf-8")
    with raises(ValueError):
        load_questions(path)


def test_load_real_dataset():
    df = load_questions()
    assert len(df) > 0
    assert set(df["difficulty"]) == {"abordable", "expert"}


def test_filter_no_filter(df):
    assert len(filter_questions(df)) == 3


def test_filter_themes(df):
    result = filter_questions(df, themes=["Sport", "Classique"])
    assert set(result["theme"]) == {"Sport", "Classique"}


def test_filter_difficulty(df):
    result = filter_questions(df, difficulty="expert")
    assert list(result["answer"]) == ["Lima"]


def test_filter_dates(df):
    result = filter_questions(df, start_date="2026-01-02", end_date="2026-01-03")
    assert list(result["answer"]) == ["Lima", "11"]


def test_filter_no_match(df):
    assert filter_questions(df, themes=["Sport"], difficulty="expert").empty


def test_search_question(df):
    assert list(search_questions(df, "PEROU")["answer"]) == ["Lima"]


def test_search_answer(df):
    assert len(search_questions(df, "vinci")) == 1


def test_search_empty_keyword(df):
    assert len(search_questions(df, "  ")) == 3


def test_normalize():
    assert normalize("  Léonard   DE Vinci ") == "leonard de vinci"


def test_check_answer():
    assert check_answer(" LIMA ", ["Lima"])
    assert check_answer("onze", ["11", "onze"])


def test_check_answer_wrong():
    assert not check_answer("Paris", ["Lima"])
    assert not check_answer("", ["Lima"])


def test_top_answers(df):
    extra = df.iloc[[0]].assign(answer="lima")
    result = top_answers(pd.concat([df, extra]), n=2)
    assert list(result.columns) == ["answer", "questions"]
    assert len(result) == 2
    assert result["answer"].iloc[0] == "Lima"
    assert result["questions"].iloc[0] == 2
