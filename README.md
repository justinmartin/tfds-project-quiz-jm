# Tools for Data Science - Final Project

[![CI](https://github.com/justinmartin/tfds-project-quiz-jm/actions/workflows/ci.yml/badge.svg)](https://github.com/justinmartin/tfds-project-quiz-jm/actions/workflows/ci.yml)

This is a Streamlit app of a personal project with more than 3000 general knowledge quiz questions (in French) I created last year for me. Here is my repo [quiz-culture-generale](https://github.com/justinmartin/quiz-culture-generale).

The Docker image is here: [justinmartin16/quiz-explorer](https://hub.docker.com/r/justinmartin16/quiz-explorer)

## Features

- **Filters:** by theme and difficulty
- **Explore:** most frequent answers and the list of questions
- **Play:** answer a random question

## Quick start

Requirements: [Docker](https://www.docker.com/), or [uv](https://docs.astral.sh/uv/) with Python 3.12.

With the image from Docker Hub:

```bash
docker run -p 8501:8501 justinmartin16/quiz-explorer
```

Or build the image yourself:

```bash
docker build -t quiz-explorer .
docker run -p 8501:8501 quiz-explorer
```

Or with uv:

```bash
uv sync
uv run streamlit run app.py
```

Then open http://localhost:8501.

## Project structure

```
├── app.py                    Streamlit app
├── quiz_explorer/data.py     functions to load, filter and check the questions
├── tests/test_data.py        unit tests
├── data/questions.json       dataset
├── pyproject.toml            dependencies and tool settings
├── uv.lock                   exact dependency versions
├── Dockerfile
└── .github/workflows/ci.yml  CI pipeline
```

## Tests

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=quiz_explorer
```

## CI/CD

On every push, GitHub Actions installs the dependencies with uv and runs the lint and the tests. On `main`, it then builds the Docker image and pushes it to Docker Hub, using the `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets.

## Data

Questions were extracted from the daily quiz *La Table des Savoirs*. Each question has a `date`, a `difficulty` (`abordable` or `expert`), a `theme`, the `question`, its `answer` and the list of `valid_answers`.
