from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
db=SQLAlchemy(app)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow())
@app.route('/', methods=['POST','GET'])
def index():
    if request.method== 'POST':
        name=request.form['Task']
        new_task=Todo(name=name)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:  
        task=Todo.query.all()
        return render_template('index.html',task=task)

@app.route('/delete/<int:sr>')
def delete(sr):
    task_to_delete=Todo.query.get_or_404(sr)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was aproblem'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.name=request.form['Task']
        try:
            db.session.commit()
            return redirect('/')
        except:
            pass
    else:
        return render_template('update.html',task=task)


        

if __name__ == "__main__":
    app.run(debug=True)