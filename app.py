from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

# ------------------------
# Routes
# ------------------------
@app.route("/")
def index():
    tasks = Todo.query.all()
    task_list = "<ul>" + "".join([f"<li>{t.title}</li>" for t in tasks]) + "</ul>"
    return f"<h1>My ToDo List</h1>{task_list}"

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if not title:
        return "Bad Request", 400
    new_task = Todo(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    task.title = request.form.get("title")
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

# ------------------------
# Ensure tables exist for tests
# ------------------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)