from flask import Flask, render_template , redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
Scss(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ontidatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db=SQLAlchemy(app)



class MyTask(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    contents=db.Column(db.String[150], nullable= False)
    complete=db.Column(db.Integer ,default=0)
    created=db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task: {self.id}" 
    
with app.app_context():
    db.create_all()


 
@app.route("/" , methods=["POST","GET"]) 
def index():


    if request.method == "POST":
         current_task = request.form["content"]
         new_task=MyTask(contents=current_task)         
         try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
         except Exception as e:

              return f"Error: {e}"
    else:

        tasks=MyTask.query.order_by(MyTask.created).all()
        return  render_template("index.html", tasks=tasks)


@app.route("/delete/<id>", methods=["POST","GET"])
def delete(id):
   delete_task=MyTask.query.get_or_404(id)
   try:
       db.session.delete(delete_task)

       db.session.commit()
       return redirect ("/")
   
   except Exception as e:
       return f"Error: {e}"

@app.route("/update/<id>", methods=["POST","GET"]  )
def update(id):
    update_task=MyTask.query.get_or_404(id)
    if request.method== "POST":
        #from our model       #from the index.htm file
        update_task.contents=request.form["content"]
        try:
            db.session.commit()
            return redirect ("/")
        except Exception as e:
            return f"error: {e}"
        
    else:
        return render_template("edit.html" , task=update_task)
            
            
        
    















if __name__ == "__main__":
    app.run(debug=True)
    
    
