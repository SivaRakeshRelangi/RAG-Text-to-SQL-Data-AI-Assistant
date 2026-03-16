from app.guardrails.question_validator import validate_question
from app.guardrails.column_filter import filter_allowed_columns
from app.rag.retriever import retrieve_schema
from app.llm.generator import generate_sql
from app.guardrails.sanitizer import sanitize
from app.guardrails.validator import validate_columns
from app.metadata.db import get_connection
from app.llm.model import llm

def process_query(question):

    try:

        validate_question(question)

        schema = retrieve_schema(question)

        if not schema:
            raise Exception("No relevant schema found")

        sql = generate_sql(schema, question)

        sanitize(sql)

        validate_columns(sql)

        sql = filter_allowed_columns(sql)

        sql = " ".join(sql.split())

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        row_count = len(rows)

        columns = []
        if rows:
            columns = list(rows[0].keys())

        values = []
        for r in rows:
            values.append(", ".join(str(v) for v in r.values()))

        summary_prompt = f"""
You are a data assistant.

User Question:
{question}

SQL Query:
{sql}

Number of rows returned: {row_count}

Columns: {columns}

Data:
{values}

Write a short answer that directly answers the user's question.
Use simple language.
Do not mention SQL.
"""

        result = llm(
            summary_prompt,
            max_tokens=120,
            temperature=0
        )

        answer = result["choices"][0]["text"].strip()

        answer = answer.replace("- response:", "").strip()

        return {
            "question": question,
            "sql": sql,
            "data": rows,
            "answer": answer
        }

    except Exception as e:
        raise Exception(f"Query generation failed: {str(e)}")