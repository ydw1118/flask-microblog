# coding:utf8
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import login_user, logout_user, login_required, LoginManager
import models
import forms

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')
migrate = Migrate(app, db)
manage = Manager(app)
manage.add_command('db', MigrateCommand)
login_manager = LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/')
def index():
    articles = models.Entry.query.all()
    return render_template('index.html', articles=articles)

@app.route('/<id>/')
def article(id):
    article = models.Entry.query.filter_by(id=id).first()
    return render_template('article.html', article=article)



@app.route('/add_article/', methods=['GET', 'POST'])
@login_required
def add_article():
    form = forms.Add_Atricle()
    if form.validate_on_submit():
        atricle = models.Entry(title=form.title.data,
                               description=form.description.data,
                               content=form.content.data)
        db.session.add(atricle)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_article.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verity_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        flash(u'用户名或者密码错误，登录失败')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'退出成功')
    return redirect(url_for('index'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        username, password, email = form.username.data, form.password.data, form.email.data
        if models.User.query.filter_by(email=email).first():
            flash(u'邮箱已经存在，请更换邮箱')
        if username and password and email:
            new_user = models.User(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return flash(u'注册失败')
    return render_template('register.html', form=form)








if __name__ == '__main__':
    manage.run()
