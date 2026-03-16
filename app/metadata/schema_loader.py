import json
import os
from app.metadata.db import get_connection

SCHEMA_JSON_PATH = "app/metadata/schema_cache.json"

def load_schema():
    query = """
    SELECT
        t.table_name,
        t.Description,
        c.column_name,
        c.column_description
    FROM tableDescription t
    JOIN columnDescription c
    ON t.id = c.table_ref
    ORDER BY t.table_name, c.column_name
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def save_schema_to_json():
    rows = load_schema()
    os.makedirs(os.path.dirname(SCHEMA_JSON_PATH), exist_ok=True)
    with open(SCHEMA_JSON_PATH, 'w') as f:
        json.dump(rows, f, indent=2)
    return rows

def load_schema_from_json():
    if os.path.exists(SCHEMA_JSON_PATH):
        with open(SCHEMA_JSON_PATH, 'r') as f:
            return json.load(f)
    return []