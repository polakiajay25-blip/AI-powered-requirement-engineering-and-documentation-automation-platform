import sqlite3


def create_db():

    conn = sqlite3.connect("projects.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        analysis TEXT,
        requirements TEXT,
        srs TEXT,
        architecture TEXT,
        tests TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_project(
        project_name,
        analysis,
        requirements,
        srs,
        architecture,
        tests
):

    conn = sqlite3.connect("projects.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO projects(
        project_name,
        analysis,
        requirements,
        srs,
        architecture,
        tests
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        project_name,
        analysis,
        requirements,
        srs,
        architecture,
        tests
    ))

    conn.commit()
    conn.close()


def get_projects():

    conn = sqlite3.connect("projects.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM projects
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# Ensure the database and tables exist when the module is imported
create_db()