import sqlglot
from sqlglot import exp
from app.metadata.db import get_connection


def validate_columns(sql):

    try:
        tree = sqlglot.parse_one(sql)
    except Exception:
        raise Exception("Invalid SQL syntax")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT table_name FROM tableDescription")
    allowed_tables = {r["table_name"].lower() for r in cursor.fetchall()}

    cursor.execute("SELECT column_name FROM columnDescription")
    allowed_columns = {r["column_name"].lower() for r in cursor.fetchall()}

    cursor.close()
    conn.close()

    tables = {t.name.lower() for t in tree.find_all(exp.Table)}

    for table in tables:
        if table not in allowed_tables:
            raise Exception(f"Table '{table}' not found in metadata")

    columns = {c.name.lower() for c in tree.find_all(exp.Column)}

    for column in columns:
        if column not in allowed_columns:
            raise Exception(f"Column '{column}' not found in metadata")

    return True