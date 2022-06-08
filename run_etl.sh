#!/bin/sh
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
VENV_PATH="${SCRIPT_DIR}/venv/bin/python"
EXTRACT_STARLING="${VENV_PATH} ${SCRIPT_DIR}/extract_starling.py"
EXTRACT_STATEMENT="${VENV_PATH} ${SCRIPT_DIR}/extract_statements.py"
LOAD_STATEMENT="${VENV_PATH} ${SCRIPT_DIR}/load_statements.py"

$EXTRACT_STARLING
$EXTRACT_STATEMENT
$LOAD_STATEMENT