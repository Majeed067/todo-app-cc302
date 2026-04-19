from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    priority = db.Column(db.String(10))

HTML = """
<form method="get">
<input name="q" placeholder="Search">
<button>Search</button>
</form>

<form action="/add" method="post">
<input name="title">
<input name="description">
<select name="priority">
<option>low</option>
<option>medium</option>
<option>high</option>
</select>
<button>Add</button>
</form>

<ul>
{% for t in tasks %}
<li>{{t.title}} ({{t.priority}})</li>
{% endfor %}
</ul>
"""

@app.route("/")
def index():
    q = request.args.get("q")
    if q:
        tasks = Todo.query.filter(Todo.title.contains(q)).all()
    else:
        priority = request.args.get("priority")
    if priority:
        tasks = Todo.query.filter_by(priority=priority).all()
    else:
        tasks = Todo.query.all()
    return render_template_string(HTML, tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    t = Todo(
        title=request.form["title"],
        description=request.form["description"],
        priority=request.form["priority"]
    )
    db.session.add(t)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
