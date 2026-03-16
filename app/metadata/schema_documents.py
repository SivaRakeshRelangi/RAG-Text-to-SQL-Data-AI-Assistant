def build_schema_docs(rows):

    tables = {}

    for r in rows:

        table = r["table_name"]
        column = r["column_name"]

        if table not in tables:
            tables[table] = []

        tables[table].append(column)

    docs = []

    for table, cols in tables.items():

        doc = f"""
        Table: {table}

        Columns:
        {", ".join(cols)}
        """

        docs.append(doc)

    return docs