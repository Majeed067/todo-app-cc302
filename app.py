from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

HTML_PAGE = """
<!doctype html>
<title>Todo App</title>
<h1>Todo List</h1>
<form action="/add" method="post">
  <input type="text" name="title">
  <input type="submit" value="Add">
</form>
<ul>
{% for task in tasks %}
  <li>{{ task.title }} <a href="/delete/{{ task.id }}">Delete</a></li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET"])
def index():
    tasks = Todo.query.all()
    return render_template_string(HTML_PAGE, tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    task = Todo(title=title)
    db.session.add(task)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

# Only create the database when running app directly
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)