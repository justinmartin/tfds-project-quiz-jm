import json

from pytest import fixture, raises

from quiz_explorer.data import (
    check_answer,
    filter_questions,
    load_questions,
    remove_accents,
    search_questions,
    top_answers,
)

QUESTIONS = [
    {
        "date": "2026-01-02",
        "difficulty": "expert",
        "theme": "Géographie",
        "question": "Quelle est la capitale du Pérou ?",
        "answer": "Lima",
        "valid_answers": ["Lima"],
    },
    {
        "date": "2026-01-01",
        "difficulty": "abordable",
        "theme": "Classique",
        "question": "Qui a peint la Joconde ?",
        "answer": "Léonard de Vinci",
        "valid_answers": ["Léonard de Vinci", "Vinci"],
    },
    {
        "date": "2026-01-03",
        "difficulty": "abordable",
        "theme": "Sport",
        "question": "Dans quel pays se trouve Lima ?",
        "answer": "Pérou",
        "valid_answers": ["Pérou"],
    },
]


@fixture
def df(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(QUESTIONS))
    return load_questions(path)


def test_load_questions(df):
    assert len(df) == 3
    assert list(df["answer"]) == ["Léonard de Vinci", "Lima", "Pérou"]


def test_load_questions_missing_column(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps([{"question": "?"}]))
    with raises(ValueError):
        load_questions(path)


def test_load_real_data():
    df = load_questions()
    assert len(df) > 0


def test_filter_no_filter(df):
    assert len(filter_questions(df)) == 3


def test_filter_themes(df):
    result = filter_questions(df, themes=["Sport", "Classique"])
    assert list(result["answer"]) == ["Léonard de Vinci", "Pérou"]


def test_filter_difficulty(df):
    result = filter_questions(df, difficulty="expert")
    assert list(result["answer"]) == ["Lima"]


def test_filter_dates(df):
    result = filter_questions(df, start="2026-01-02", end="2026-01-02")
    assert list(result["answer"]) == ["Lima"]


def test_search_questions(df):
    result = search_questions(df, "LIMA")
    assert list(result["answer"]) == ["Pérou"]


def test_top_answers(df):
    assert top_answers(df, n=2).tolist() == [1, 1]


def test_remove_accents():
    assert remove_accents(" Pérou ") == "perou"


def test_check_answer():
    assert check_answer("perou", ["Pérou"])
    assert check_answer("VINCI", ["Léonard de Vinci", "Vinci"])
    assert not check_answer("Paris", ["Lima"])
