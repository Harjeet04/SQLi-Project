from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def query_db_raw(name):
    conn = sqlite3.connect('company.db')
    c = conn.cursor()

    # ❌ INTENTIONALLY VULNERABLE
    sql = f"""
    SELECT emp_id, name, role, email
    FROM employees
    WHERE name = '{name}'
    """
    c.execute(sql)

    rows = c.fetchall()
    col_names = [desc[0] for desc in c.description]

    # ⭐ UNION-based attack header handling
    if "UNION" in name.upper():
        col_names = ["emp_id", "name", "role", "email"]

    # 🔍 Detect detection / blind SQLi payloads
    detection_payload = False
    detection_keywords = [
        " AND ",
        " EXISTS",
        "1=2",
        "RANDOMBLOB",
        "/*"
    ]

    for keyword in detection_keywords:
        if keyword in name.upper():
            detection_payload = True
            break

    conn.close()
    return col_names, rows, detection_payload


# 👉 INDEX: VULNERABLE MODE ONLY
@app.route('/')
def index():
    return render_template('index.html', mode="vulnerable")


@app.route('/search_vuln', methods=['POST'])
def search_vuln():
    name = request.form.get('username', '')

    col_names, results, detection_payload = query_db_raw(name)

    # 🧠 Explanation for detection payloads
    reason = None
    if detection_payload and not results:
        reason = (
            "This is a detection / blind SQL injection payload. "
            "It is used to verify whether the application is vulnerable. "
            "The SQL query executed successfully, but the condition evaluated to FALSE, "
            "so no rows were returned."
        )

    return render_template(
        'result.html',
        endpoint='VULNERABLE',
        query=name,
        col_names=col_names,
        results=results,
        reason=reason
    )


if __name__ == '__main__':
    app.run(port=5001, debug=True)
