from flask import Flask
import os
import psycopg2

app = Flask(__name__)


@app.route("/")
def hello():
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "db"),
        dbname=os.environ.get("POSTGRES_DB", "postgres"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
    )
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            count INTEGER NOT NULL
        )
        """
    )
    conn.commit()

    cur.execute("SELECT count(*) FROM visits")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO visits (count) VALUES (0)")
        conn.commit()

    cur.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
    conn.commit()

    cur.execute("SELECT count FROM visits WHERE id = 1")
    visit_count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return f"Du er besøgende nr. {visit_count}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
