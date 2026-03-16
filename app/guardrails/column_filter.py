import re
from app.metadata.db import get_connection


def filter_allowed_columns(sql):

    if "*" not in sql:
        return sql

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    match = re.search(r"FROM\s+([a-zA-Z_]+)", sql, re.IGNORECASE)

    if not match:
        return sql

    table = match.group(1)

    cursor.execute("""
        SELECT c.column_name
        FROM columnDescription c
        JOIN tableDescription t
        ON t.id = c.table_ref
        WHERE t.table_name = %s
    """, (table,))

    cols = [r["column_name"] for r in cursor.fetchall()]

    cursor.close()
    conn.close()

    if not cols:
        return sql

    column_string = ", ".join(cols)

    sql = re.sub(
        r"SELECT\s+\*",
        f"SELECT {column_string}",
        sql,
        flags=re.IGNORECASE
    )

    return sql