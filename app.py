from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
import os



app = Flask(__name__)
FILE = "todos.json"


def load_todos():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_todos(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=2)


def urgency_score(todo):
    if not todo["due_date"]:
        return "🟢 Low"

    due = datetime.strptime(todo["due_date"], "%Y-%m-%d")
    days_left = (due - datetime.now()).days

    if todo["priority"] == "high" or days_left <= 1:
        return "🔴 High"
    elif todo["priority"] == "medium" or days_left <= 3:
        return "🟡 Medium"
    return "🟢 Low"


@app.route("/")
def index():
    todos = load_todos()

    # DAILY FOCUS MODE
    focus = request.args.get("focus")
    if focus == "today":
        today = datetime.now().date()
        todos = [
            t for t in todos
            if t["due_date"] and datetime.strptime(t["due_date"], "%Y-%m-%d").date() <= today
        ]

    # ADD URGENCY SCORE
    for t in todos:
        t["urgency"] = urgency_score(t)

    return render_template("index.html", todos=todos, focus=focus)


@app.route("/add", methods=["POST"])
def add():
    todos = load_todos()

    todos.append({
        "title": request.form["title"],
        "description": request.form["description"],
        "priority": request.form["priority"],
        "due_date": request.form["due_date"],
        "status": "todo",
        "created_at": datetime.now().isoformat()
    })

    save_todos(todos)
    return redirect(url_for("index"))


@app.route("/toggle/<int:index>")
def toggle(index):
    todos = load_todos()
    todos[index]["status"] = "done" if todos[index]["status"] == "todo" else "todo"
    save_todos(todos)
    return redirect(url_for("index"))


@app.route("/snooze/<int:index>")
def snooze(index):
    todos = load_todos()

    if todos[index]["due_date"]:
        due = datetime.strptime(todos[index]["due_date"], "%Y-%m-%d")
        todos[index]["due_date"] = (due + timedelta(days=1)).strftime("%Y-%m-%d")

    save_todos(todos)
    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete(index):
    todos = load_todos()
    todos.pop(index)
    save_todos(todos)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
