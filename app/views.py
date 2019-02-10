import os
from flask import render_template,url_for,flash,request,redirect,abort
from flask_login import login_user,login_required,current_user,logout_user
from app import app,bcrypt,db
from form import RegisterForm,LoginForm,PostTweetForm
from app.models import User,Post
from werkzeug.utils import secure_filename


@app.route('/',methods=['GET','POST'])
@login_required
def index():
    form = PostTweetForm()
    if form.validate_on_submit():
        body = form.text.data
        f = form.img.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('app', 'static', filename))
        img = '/static/' + filename
        post = Post(body=body,img=img)
        current_user.posts.append(post)
        db.session.commit()
        flash('你发表了新的说说', category='success')
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 5, False)
    return render_template('index.html', form=form, posts=posts)

@app.route('/user_page/<username>', methods=['GET', 'POST'])
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page,10,False)
        return render_template('user_page.html',user=user,posts=posts)
    else:
        return '404'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('成功登入', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('login'))
        flash('亲，输入有误噢！', category='danger')
    return render_template('login.html', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # print(request.form['username'])
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        # print(username,password,email)
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你，注册成功。', category='success')
        return redirect(url_for('login'))
    return render_template('register.html',form = form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

