import json

from pytest import fixture, raises

from quiz_explorer.data import check_answer, filter_questions, load_questions

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
        "theme": "Sport",
        "question": "Combien de joueurs dans une équipe de football ?",
        "answer": "11",
        "valid_answers": ["11", "onze"],
    },
]


@fixture
def df(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(QUESTIONS))
    return load_questions(path)


def test_load_questions(df):
    assert len(df) == 2
    assert list(df["answer"]) == ["11", "Lima"]


def test_load_questions_bad_file(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps([{"date": "2026-01-01"}]))
    with raises(ValueError):
        load_questions(path)


def test_load_real_data():
    assert len(load_questions()) > 0


def test_filter_all(df):
    assert len(filter_questions(df, "All", "All")) == 2


def test_filter_theme(df):
    assert list(filter_questions(df, "Sport", "All")["answer"]) == ["11"]


def test_filter_difficulty(df):
    assert list(filter_questions(df, "All", "expert")["answer"]) == ["Lima"]


def test_check_answer():
    assert check_answer(" LIMA ", ["Lima"])
    assert check_answer("onze", ["11", "onze"])
    assert not check_answer("Paris", ["Lima"])
