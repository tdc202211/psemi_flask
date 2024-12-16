from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

# Model Definition
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    details = db.Column(db.String(100))

# Routes
@app.route("/")
def index():
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get(id)
    db.session.delete(delete_task)
    db.session.commit()
    return redirect('/')

@app.route("/create", methods=["POST"])
def create():
    title = request.form.get("title")
    details = request.form.get("details")
    new_task = Todo(title=title, details=details)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    task = Todo.query.get(id)
    if request.method == "POST":
        task.title = request.form.get("title")
        task.details = request.form.get("details")
        db.session.commit()
        return redirect('/')
    return render_template("update.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
