from flask import Flask,url_for,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)#Заголовок
    into=db.Column(db.String(300), nullable=False)#Вступительный текст
    text=db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>'% self.id
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/posts')
def posts():
    articles=Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html",articles=articles)

@app.route('/posts/<int:id>')
def posts_det(id):
    article=Article.query.get(id)
    return render_template("posts_det.html",article=article)

@app.route('/posts/<int:id>/delete')
def posts_del(id):
    article=Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Ошибочка при удалении'

@app.route('/create', methods=['POST','GET'])
def create():
    if request.method=="POST":
        title = request.form['title']
        into = request.form['into']
        text = request.form['text']

        article=Article(title=title, into=into, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Ошибочки получились'

    else:
        return render_template("create.html")

@app.route('/posts/<int:id>/up',methods=['POST','GET'])
def update(id):
    article=Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.into = request.form['into']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            pass
    else:
        article = Article.query.get(id)
        return render_template('post_up.html',article=article)






if __name__ == "__main__":
    app.run(debug=True)