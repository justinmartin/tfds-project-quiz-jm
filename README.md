# Quiz Explorer

[![CI](https://github.com/justinmartin/tfds-project-quiz-jm/actions/workflows/ci.yml/badge.svg)](https://github.com/justinmartin/tfds-project-quiz-jm/actions/workflows/ci.yml)

A Streamlit app to explore and play with 3,470 French general knowledge quiz questions.

Final project for the *Tooling for the Data Scientist* course, based on my personal project [quiz-culture-generale](https://github.com/justinmartin/quiz-culture-generale).

- **Docker image:** [justinmartin16/quiz-explorer](https://hub.docker.com/r/justinmartin16/quiz-explorer)

## Features

- **Filters:** theme, difficulty and dates
- **Explore:** most frequent answers and a searchable table of questions
- **Play:** answer a random question

## Quick start

With Docker:

```bash
docker run -p 8501:8501 justinmartin16/quiz-explorer
```

Or with Python 3.12:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## Project structure

```
├── app.py                    Streamlit app
├── quiz_explorer/data.py     load, filter and search functions
├── tests/test_data.py        unit tests
├── data/questions.json       dataset
├── requirements.txt          app dependencies
├── requirements-dev.txt      test and lint dependencies
├── Dockerfile
└── .github/workflows/ci.yml  CI pipeline
```

## Data

Questions from the daily quiz *La Table des Savoirs* (January to July 2026). Each question has a `date`, a `difficulty` (`abordable` or `expert`), a `theme`, the `question`, its `answer` and the list of `valid_answers`.

## Tests

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
python -m pytest --cov=quiz_explorer
```

## CI/CD

On every push, GitHub Actions runs the lint and the tests. On `main`, it then builds the Docker image and pushes it to Docker Hub, using the `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets.
