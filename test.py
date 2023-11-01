from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime as dt


print("starting test.py")

app=Flask(__name__)
CORS(app)

#--------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>'% self.id

#--------------------------------------------------------------------
@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':

        task_content=request.form['content']

        new_task=Todo(content=task_content)

        if task_content=="":
            return redirect('/empty')
        else:
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return "There was some error in adding into DB."
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)
    
#--------------------------------------------------------------------
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was some error in deleting task."


#--------------------------------------------------------------------
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)

    if request.method=='POST':
        task.content=request.form['content']
        if task.content=="":
            return redirect('/empty')
        else:
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "there was some error in updating task."
        
    else:
        return render_template('update.html',task=task)

#--------------------------------------------------------------------
@app.route('/empty')
def empty():
    return render_template('empty.html')
    
    
#--------------------------------------------------------------------
if __name__=="__main__":
    app.run(debug=True)

