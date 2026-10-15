import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database: a local SQLite file called todo.db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "todo.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# A "model" = one table in the database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


# Create the table if it doesn't exist yet
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        db.session.add(Task(title=title))
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    task = db.get_or_404(Task, task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)