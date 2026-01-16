from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    return sqlite3.connect("todo.db")

# Create table
conn = get_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
)
""")
conn.commit()
conn.close()

@app.get("/todos")
def get_todos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    data = cursor.fetchall()
    conn.close()
    return [{"id": d[0], "title": d[1]} for d in data]

@app.post("/todos")
def add_todo(todo: dict):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos(title) VALUES(?)", (todo["title"],))
    conn.commit()
    conn.close()
    return {"message": "Todo added"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return {"message": "Todo deleted"}
