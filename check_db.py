import sqlite3

conn = sqlite3.connect("company.db")
c = conn.cursor()

c.execute("SELECT emp_id, name, role, salary, access_level FROM employees")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()
