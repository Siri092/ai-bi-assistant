# AI Usage and Development Report

## 1. Project Overview

The Mini AI Business Intelligence Assistant answers natural-language questions about sales data. It uses Python, FastAPI, SQLite, SQL, and a browser-based interface to return answers calculated from the sales database.

The purpose of the project is to demonstrate the development of a small business analytics application that combines question interpretation with deterministic database queries.

## 2. AI Tools Used

ChatGPT was used as an AI-assisted development tool for guidance, code explanations, debugging assistance, and documentation preparation.

The development process involved reviewing requirements, planning the application structure, understanding the database-backed analytics approach, troubleshooting errors, and preparing project documentation.

The application also includes optional OpenAI integration for question interpretation when configured. The local interpreter provides an alternative for supported question patterns.

## 3. How AI Was Used During Development

AI assistance supported the following activities:

- Understanding the assignment requirements and breaking them into implementation tasks.
- Planning the application architecture and separation of responsibilities between the frontend, backend, database, interpreter, and analytics modules.
- Understanding how to load CSV data into SQLite and calculate business metrics using SQL.
- Explaining FastAPI endpoints and structured request and response handling.
- Troubleshooting development and test execution issues.
- Reviewing the supported analytics questions and documenting data-quality assumptions.
- Preparing setup instructions, architecture documentation, and this development report.

AI-generated suggestions were reviewed and tested during development. The final implementation should be understood and explained by the developer.

## 4. Application Architecture

The application consists of the following components:

- **Frontend:** HTML, CSS, and JavaScript interface for entering questions and displaying answers.
- **Backend:** FastAPI application that accepts questions and coordinates the processing flow.
- **Question interpreter:** Maps supported natural-language questions to predefined analytics intents.
- **Database:** SQLite stores transaction data imported from the supplied CSV.
- **Analytics:** Predefined database queries calculate revenue, top product, monthly trends, top region, and comparisons between months.
- **Automated tests:** Pytest checks important analytics and question-handling behavior.

The processing flow is:

Browser interface → FastAPI → Question interpreter → Supported analytics operation → SQL query → SQLite → Structured answer

## 5. AI Integration and Responsible Query Handling

The application supports local question interpretation and optional OpenAI-powered intent classification.

The intended role of the optional language model is to help identify a supported analytics intent and its required parameters. Database calculations are performed by predefined analytics queries.

The language model is not permitted to supply arbitrary SQL for execution. Restricting execution to predefined analytics operations helps reduce the risk of unsupported queries and destructive database operations.

The system's answers remain limited to the analytics it implements and the data available in the database.

## 6. Supported Analytics

The application supports five main questions:

1. What is the total revenue?
2. Which product generated the highest revenue?
3. What is the monthly revenue trend?
4. Which region generated the highest sales?
5. How did revenue change between two months?

The application also provides helpful handling for unsupported questions and month comparisons that do not follow the expected `YYYY-MM` format.

## 7. Testing and Debugging

Automated tests were run using:

```powershell
python -m pytest -q
```

The latest recorded test run completed successfully with **7 passed**.

Manual testing was also performed for the five main analytics features through the application interface.

One development issue involved pytest being unable to locate the `database` module. This was addressed by adding a `pytest.ini` configuration that places the project root on the Python path. The tests were then rerun successfully.

The test results apply to the version tested at that time. Tests should be rerun after further code changes.

## 8. Data Quality and Calculation Rules

Revenue is calculated as:

```text
(quantity * unit_price) - discount_amount
```

For revenue analytics, the application includes completed transactions with positive quantities and valid, non-missing, non-negative numeric values for unit price and discount.

Returned transactions are excluded from revenue metrics. Records with missing unit prices remain in the database for traceability but are excluded from the revenue calculations.

These rules were selected for the assessment and documented in the project README. In a production application, the treatment of incomplete or inconsistent financial records should be confirmed with the data owner.

## 9. Problems Encountered

The following development challenges were encountered:

- Pytest initially had difficulty locating the database module.
- The local interpreter did not recognize every possible natural-language phrasing.
- The application needed clear rules for handling missing prices, returned transactions, and invalid month-comparison inputs.
- Documentation needed to explain how AI-assisted interpretation could be combined with controlled database operations.

## 10. How the Problems Were Addressed

- Added pytest configuration to make the project root available during test execution.
- Tested the supported question examples manually through the web interface.
- Used predefined analytics operations instead of allowing arbitrary model-generated SQL to execute.
- Documented the revenue formula, data-quality rules, supported questions, and known limitations.
- Reran the automated tests and recorded the successful test result.

## 11. Known Limitations

- Local question interpretation supports a limited set of patterns.
- The application focuses on the supplied dataset and five predefined analytics tasks.
- Additional tests would improve coverage of API validation, unusual data, and edge cases.
- The current application is a local assessment prototype rather than a production-hardened service.
- Optional OpenAI interpretation depends on correct configuration and service availability.

The actual fallback behavior when the OpenAI integration is unavailable should be verified against the implementation.

## 12. Future Improvements

With more development time, the following improvements could be considered:

- Expand natural-language question recognition.
- Add further analytics and support for additional datasets.
- Add charts and downloadable reports.
- Increase automated test coverage for API validation and unusual data.
- Improve logging and configuration management.
- Prepare the application for secure deployment and production monitoring.

## 13. Responsible AI Use

AI was used as a development aid rather than as a substitute for validating the application.

The implementation should be reviewed and understood by the developer. Calculations should be verified against the database, tests should be rerun after changes, and the developer should be able to explain the architecture, query-handling approach, assumptions, and limitations.

## 14. Conclusion

This project demonstrates an AI-assisted approach to building a small business analytics application. It combines natural-language interpretation with predefined database queries, automated tests, and documented data-quality rules.

The development process highlights the importance of validating AI-assisted code, testing application behavior, controlling database operations, and clearly documenting technical decisions and limitations.
