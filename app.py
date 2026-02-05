from flask import Flask, render_template, request, redirect, url_for
import json
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

@app.route("/")
def index():
    todos = load_todos()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    todo = request.form.get("todo")
    todos = load_todos()
    todos.append(todo)
    save_todos(todos)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    todos = load_todos()
    todos.pop(index)
    save_todos(todos)
    return redirect(url_for("index"))

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    todos = load_todos()
    todos[index] = request.form.get("todo")
    save_todos(todos)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)