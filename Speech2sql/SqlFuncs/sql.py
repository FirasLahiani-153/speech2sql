import re
import mysql.connector
ALLOWED_STATEMENTS = ["select", "show", "describe"]
FORBIDDEN_STATEMENTS = [
    "insert", "update", "delete", "drop",
    "alter", "truncate", "create", "replace"
]

# --- MySQL connection ---
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="",
        database="airportdb"
    )
def execute_safe_sql(query):
    query = clean_sql(query)
    q_lower = query.lower()

    for forbidden in FORBIDDEN_STATEMENTS:
        if re.search(r"\b" + forbidden + r"\b", q_lower):
            return f"Error: '{forbidden.upper()}' queries are not allowed."

    if not any(re.search(r"\b" + allowed + r"\b", q_lower) for allowed in ALLOWED_STATEMENTS):
        return "Error: Only safe queries (SELECT, SHOW, DESCRIBE) are allowed."

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        if re.search(r"\bselect\b", q_lower) or re.search(r"\bdescribe\b", q_lower):
            rows = cursor.fetchmany(2000)
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return columns, rows
        else:
            conn.close()
            return "Query executed successfully."
    except mysql.connector.Error as e:
        return f"MySQL Error: {e}"
    finally :
        conn.close()

def clean_sql(sql_text):
    """Remove code blocks, extra whitespace, and ensure SELECT only."""
    sql_text = re.sub(r"```sql|```", "", sql_text, flags=re.IGNORECASE)
    sql_text = sql_text.strip()
    sql_text = sql_text.split(";")[0]
    return sql_text

