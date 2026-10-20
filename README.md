# Soccer Stats Pipeline + API

A project that turns soccer match and goal-event CSV files into a SQLite database, exposes the data through a FastAPI REST API, and answers questions with SQL. The project uses Python for the ETL pipeline and does not use machine learning.

## Development roadmap

1. **Set up the repository and Python environment (complete).** Organize folders for raw data, source code, tests, and SQL. Create a virtual environment and ignore it in Git so dependencies stay local.
2. **Explore the source CSV files (complete).** Choose and document the data source. Inspect columns and sample rows, then identify missing values, inconsistent formats, and duplicates before designing the database.
3. **Design the SQLite schema (in progress).** Define tables, primary keys, foreign keys, and relationships based on the data. Explain why each table and constraint exists.
4. **Build the ETL pipeline.** Read the CSV files, clean and transform records, and load them into SQLite. Make the process repeatable and understandable.
5. **Check data quality.** Verify required fields, relationships, row counts, and important transformations. Add tests for failures that could change the results.
6. **Build the REST API.** Use FastAPI to expose basic endpoints for the stored data. Check response formats and error cases.
7. **Write SQL analysis queries.** Calculate goals by team, averages, and rankings. Verify the queries against known examples.
8. **Finish the documentation and review.** Explain setup, data sources, how to run the ETL and API, example queries, design decisions, and limitations. Review whether the project is ready to discuss in interviews and include on a CV.

At each stage, the workflow is to explain the approach, make a small change, verify the result, and explain the tradeoffs.

## Data source and initial profile

The raw files come from [International football results](https://github.com/martj42/international_results) by martj42, which is published under [CC0-1.0](https://github.com/martj42/international_results/blob/master/LICENSE). `results.csv` contains international match results; `goalscorers.csv` contains goal events and named scorers where available. It is not a complete roster of every player in those matches.

| File | Data rows | Columns | Blank or `NA` cells found |
| --- | ---: | ---: | --- |
| `results.csv` | 49,945 | 9 | 0 |
| `goalscorers.csv` | 47,914 | 9 | 44 missing scorers, 254 missing minutes, 45,838 missing assists |

The counts above treat only empty strings and `NA` as missing. A goal with an unknown scorer or assist still represents a goal and must not be discarded automatically. The CSV files do not provide database IDs, so the schema design must determine how to link each goal to its match.
