import sqlite3

conn = sqlite3.connect("company.db")
c = conn.cursor()

# Create employees table
c.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT UNIQUE,
    name TEXT,
    role TEXT,
    age INTEGER,
    email TEXT,
    salary INTEGER,
    access_level TEXT
)
""")

# Insert sample employee data
employees = [
    ("EMP001", "Amit Sharma", "Admin", 35, "amit@company.com", 120000, "HIGH"),
    ("EMP002", "Neha Verma", "HR", 30, "neha@company.com", 70000, "MEDIUM"),
    ("EMP003", "Rahul Mehta", "Developer", 28, "rahul@company.com", 90000, "MEDIUM"),
    ("EMP004", "Sneha Iyer", "Developer", 26, "sneha@company.com", 85000, "MEDIUM"),
    ("EMP005", "Rohit Singh", "Intern", 22, "rohit@company.com", 20000, "LOW")
]

c.executemany("""
INSERT INTO employees (emp_id, name, role, age, email, salary, access_level)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", employees)

conn.commit()
conn.close()

print("✅ Company employee database created successfully!")
