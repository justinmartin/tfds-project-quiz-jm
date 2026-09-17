# Quiz Explorer

[![CI](https://github.com/justinmartin/tfds-project-quiz-jm/actions/workflows/ci.yml/badge.svg)](https://github.com/justinmartin/tfds-project-quiz-jm/actions/workflows/ci.yml)

A Streamlit app to explore a dataset of French general knowledge quiz questions and play with them.

This is the final project of the *Tooling for the Data Scientist* course. It is based on one of my personal projects, [quiz-culture-generale](https://github.com/justinmartin/quiz-culture-generale), a daily quiz web app.

## Features

- Filter the questions by theme, difficulty and date
- See the most frequent answers and search the questions (case and accents are ignored)
- Play: get a random question and check your answer

## Data

`data/questions.json` contains 3,470 questions asked between January and July 2026 on the daily quiz *La Table des Savoirs*.

| Field | Description |
|---|---|
| `date` | day the question was asked |
| `difficulty` | `abordable` (easy) or `expert` |
| `theme` | one of 10 themes (Sport, Histoire, Sciences...) |
| `question` / `answer` | question and main answer |
| `valid_answers` | accepted answers |

## Project structure

```
├── app.py                  <- Streamlit app
├── quiz_explorer/data.py   <- loading, filtering and search functions
├── data/questions.json     <- dataset
├── tests/test_data.py      <- unit tests
├── requirements.txt        <- app dependencies
├── requirements-dev.txt    <- test and lint dependencies
├── Dockerfile
└── .github/workflows/ci.yml  <- CI pipeline
```

## Requirements

Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Usage

```bash
streamlit run app.py
```

Then open http://localhost:8501.

## Tests

```bash
ruff check .
ruff format --check .
python -m pytest --cov=quiz_explorer
```

## Docker

Run the image from Docker Hub:

```bash
docker run -p 8501:8501 justinmartin16/quiz-explorer
```

Or build it locally:

```bash
docker build -t quiz-explorer .
docker run -p 8501:8501 quiz-explorer
```

## CI/CD

The GitHub Actions workflow runs on every push:

1. **test**: lint, format check and unit tests with coverage
2. **docker**: build the Docker image and push it to Docker Hub (on `main` only)

The docker job needs two repository secrets in *Settings > Secrets and variables > Actions*: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.
