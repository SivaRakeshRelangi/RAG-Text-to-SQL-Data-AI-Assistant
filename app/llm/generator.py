from app.llm.model import llm
from app.llm.prompt import build_prompt
import re

def generate_sql(schema, question):

    prompt = build_prompt(schema, question)

    result = llm(
        prompt,
        max_tokens=200,
        temperature=0
    )

    text = result["choices"][0]["text"].strip()

    text = text.replace("```sql", "").replace("```", "")

    match = re.search(r"(SELECT[\s\S]*?;)", text, re.IGNORECASE)

    if not match:
        raise Exception("Model did not generate a valid SQL query")

    sql = match.group(1).strip()

    return sql