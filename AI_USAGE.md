# AI Usage and Development Report

## 1. Project Overview

The AI Business Intelligence Assistant answers natural-language questions about sales data. It uses Python, FastAPI, SQLite, and a web-based interface to return calculated results from the sales database.

## 2. AI Tools and Techniques

An AI-assisted development approach was used to help design the application structure, implement features, debug errors, and create automated tests.

The application uses a local intent interpreter to identify supported question types. It also includes optional OpenAI integration for interpreting questions when an API key is configured.

## 3. Application Architecture

- **Frontend:** HTML, CSS, and JavaScript interface for entering questions and displaying answers.
- **Backend:** FastAPI receives requests and coordinates question interpretation and analytics.
- **Question interpreter:** Maps natural-language questions to supported analytics intents.
- **Database:** SQLite stores the sales data imported from the CSV file.
- **Analytics:** Predefined database queries calculate revenue, top product, monthly trends, top region, and monthly comparisons.
- **Tests:** Pytest verifies important analytics and question-handling behavior.

## 4. Supported Questions

The application supports:
- Total sales revenue
- Product with the highest revenue
- Monthly revenue trend
- Region with the highest revenue
- Revenue comparison between two months

## 5. Testing and Debugging

Automated tests were executed using:

`python -m pytest -q`

The latest test run completed successfully with **7 passed**.

Manual tests verified the five main analytics features. An initial pytest import issue was resolved by adding `pytest.ini` with the project root in the Python path.

## 6. Error Handling and Reliability

Unsupported questions return a helpful message listing supported question types. Month comparisons require months in `YYYY-MM` format. Analytics calculations are performed by predefined database queries rather than allowing the language model to generate arbitrary SQL.

## 7. Limitations

The local interpreter supports a limited set of question patterns. More flexible natural-language understanding depends on the optional OpenAI integration. The application currently focuses on the provided sales dataset and predefined analytics.

## 8. Future Improvements

- Add more natural-language question patterns.
- Improve the interface with charts and downloadable reports.
- Add more automated tests for API validation and unusual data.
- Support additional datasets and analytics.
- Add stronger logging and deployment configuration.

## 9. Responsible AI Use

AI assistance was used during development, and the implementation was tested locally. The developer should review and understand the source code, verify calculation results, and be able to explain the design decisions before submission.
