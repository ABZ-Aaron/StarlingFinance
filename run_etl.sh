#!/bin/sh

# Specify Commands
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
VENV_PATH="${SCRIPT_DIR}/venv/bin/python"
EXTRACT_STARLING="${VENV_PATH} ${SCRIPT_DIR}/extract_starling.py"
EXTRACT_STATEMENT="${VENV_PATH} ${SCRIPT_DIR}/extract_statements.py"
LOAD_STATEMENT="${VENV_PATH} ${SCRIPT_DIR}/load_statements_sqlite.py"

# Extract total effective balance and copy to Google Sheets
$EXTRACT_STARLING

# Extract monthly PDF & CSV Statements
$EXTRACT_STATEMENT

# Load CSV Statements into SQLite
$LOAD_STATEMENT