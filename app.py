from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
FILE = "todos.json"


# ---------- Helpers ----------
def load_todos():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_todos(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=2)


# ---------- Routes ----------
@app.route("/")
def index():
    todos = load_todos()

    # SEARCH
    q = request.args.get("q", "").lower()
    if q:
        todos = [
            t for t in todos
            if q in t["title"].lower() or q in t["description"].lower()
        ]

    # FILTER
    priority = request.args.get("priority")
    status = request.args.get("status")

    if priority:
        todos = [t for t in todos if t["priority"] == priority]

    if status:
        todos = [t for t in todos if t["status"] == status]

    # SORT
    sort = request.args.get("sort")
    if sort == "due_date":
        todos.sort(key=lambda t: t["due_date"] or "9999-99-99")
    elif sort == "priority":
        priority_order = {"low": 1, "medium": 2, "high": 3}
        todos.sort(key=lambda t: priority_order[t["priority"]])

    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    todos = load_todos()

    new_todo = {
        "title": request.form["title"],
        "description": request.form["description"],
        "priority": request.form["priority"],
        "due_date": request.form["due_date"],
        "status": "todo",
        "created_at": datetime.now().isoformat()
    }

    todos.append(new_todo)
    save_todos(todos)
    return redirect(url_for("index"))


@app.route("/toggle/<int:index>")
def toggle(index):
    todos = load_todos()
    todos[index]["status"] = "done" if todos[index]["status"] == "todo" else "todo"
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
