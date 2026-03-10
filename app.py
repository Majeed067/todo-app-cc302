import os
import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()

    task = {
        "title": request.form["title"],
        "priority": request.form["priority"]
    }

    tasks.append(task)
    save_tasks(tasks)

    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()

    if index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)