from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','postgresql://postgres.ifhbgrmlpgiorbbiflhz:GDa5gURNcbBuyhLW@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)



class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(50))  
    schedule_time = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)  # Track completion
    updated = db.Column(db.Boolean, default=False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        time = request.form['time']
        schedule_time = request.form['tododate']
        
        todo = Todo(title=title, desc=desc,time=time,schedule_time=schedule_time)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all() 
    xy= datetime.now() 
    current_date = xy.strftime("%d-%m-%Y %H:%M:%p")
    return render_template('index.html', allTodo=allTodo,current_date=current_date )





# Completed Todos
@app.route('/completed')
def completed_tasks():
    completed_todos = Todo.query.filter_by(completed=True).all()  # Query for completed tasks
    return render_template('completed.html', completed_todos=completed_todos)

@app.route('/complete/<int:sno>')
def complete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        todo.completed = True  # Mark as completed
        db.session.commit()
    return redirect('/')


@app.route('/About')
def about():
    return render_template('About.html')

   
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'




@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title'] 
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.updated = True # Mark Updated
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()

    return render_template('update.html', todo=todo)


@app.route('/updated')
def updated_todos():
    updated_todos = Todo.query.filter_by(updated=True).all()  # Query for updated tasks
    return render_template('updated.html', updated_todos=updated_todos)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
