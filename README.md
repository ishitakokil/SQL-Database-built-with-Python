# SQL-Database-built-with-Python

## Project Overview
SQL-Database-built-with-Python is a Python project that provides tools for creating, managing, and interacting with SQL databases. It includes two key scripts: SQL_DB.py for database operations and cli.py for testing and interacting with the database via a command-line interface (CLI). This project is ideal for database management tasks and can be extended for various use cases. 

## Features
- **Database Operations:**
  - Create, update, query, and delete tables.
  - Manage database connections and transactions.

- **Command-Line Interface:**
  - Test database functionalities via commands.
  - Interactive CLI for executing predefined operations.

- **Extensibility:**
  - Modular design allows easy addition of new database functionalities and CLI commands.

## Scripts Overview
### `SQL_DB.py`
This script provides core database functionalities:
- **Database Connection:** Establishes a connection to an SQLite database.
- **Table Management:** Create, modify, and delete tables.
- **Data Manipulation:** Insert, update, delete, and retrieve records.
- **Error Handling:** Ensures robust operations with meaningful error messages.

### `cli.py`
This script enables interaction with the database via a command-line interface:
- Provides predefined commands for testing SQL operations.
- Accepts arguments to customize operations (e.g., specifying table names or query parameters).
- Extensible for additional CLI commands.

## How to Use `cli.py`
### Prerequisites
- Python 3.8+
- SQLite (built-in with Python)

### Running the Script
1. **Prepare a Test SQL File:**
   Save SQL commands in a file, e.g., `test.create_database.01.sql`. Example content:

   ```sql
   FILENAME: test.db
   1: CREATE TABLE student_123 (name TEXT, grade REAL, piazza INTEGER);
   1: INSERT INTO student_123 VALUES ('James', 4.0, 1);
   1: INSERT INTO student_123 VALUES ('Yaxin', 4.0, 2);
   1: INSERT INTO student_123 VALUES ('Li', 3.2, 2);
   1: SELECT * FROM student_123 ORDER BY piazza, grade;
   1: CLOSE

2. **Run cli.py: Execute the script with the test file:**
   ``` python cli.py test.create_database.01.sql ```

There are some test files you can run here. 
