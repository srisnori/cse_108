import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "healthcare_analytics.sqlite"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT doctor_id, password FROM Doctor")

for doctor_id, password in cur.fetchall():
    if password.startswith("pbkdf2:"):
        continue  # already hashed

    hashed = generate_password_hash(password, method="pbkdf2:sha256")

    cur.execute(
        "UPDATE Doctor SET password = ? WHERE doctor_id = ?",
        (hashed, doctor_id),
    )

conn.commit()
conn.close()

print("All doctor passwords hashed.")

