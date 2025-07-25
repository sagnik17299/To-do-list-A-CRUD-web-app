from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
from tzlocal import get_localzone
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
local_tz = get_localzone()
local_time = datetime.now(local_tz)
class todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    #completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = local_time)



    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = todo(content = current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return 'there was an error here'
    
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks=tasks)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
