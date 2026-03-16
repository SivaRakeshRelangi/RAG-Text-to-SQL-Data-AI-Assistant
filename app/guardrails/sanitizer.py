import re
from app.config import BLOCKED_SQL

def sanitize(query):

    q = query.upper()

    for word in BLOCKED_SQL:
        if word in q:
            raise Exception("Unsafe SQL detected")

    if not re.match(r"^\s*SELECT", q):
        raise Exception("Only SELECT allowed")

    return query