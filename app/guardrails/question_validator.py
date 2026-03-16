import re
from app.metadata.db import get_connection


SQL_WORDS = {
    "select","from","where","join","group","by",
    "avg","sum","count","min","max"
}

BLOCKED_WORDS = {
    "delete","drop","update","truncate","alter","insert"
}


def validate_question(question):

    q = question.lower()

    # block dangerous intent
    for word in BLOCKED_WORDS:
        if word in q:
            raise Exception(f"Dangerous operation '{word}' not allowed")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT table_name FROM tableDescription")
    tables = {r["table_name"].lower() for r in cursor.fetchall()}

    cursor.execute("SELECT column_name FROM columnDescription")
    columns = {r["column_name"].lower() for r in cursor.fetchall()}

    cursor.close()
    conn.close()

    tokens = re.findall(r"[a-zA-Z_\.]+", question.lower())

    for token in tokens:

        if "." in token:

            table, col = token.split(".", 1)

            if table not in tables:
                raise Exception(f"Table '{table}' not found in metadata")

            if col not in columns:
                raise Exception(f"Column '{col}' not found in metadata")

            continue

        if token in tables:
            continue

        if token in columns:
            continue

        if token in SQL_WORDS:
            continue

        if "_" in token:
            raise Exception(f"Column '{token}' not found in metadata")