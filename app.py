from flask import Flask, redirect, request, flash, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'benji'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_db'
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)


@app.route('/')
def homepage():
    return redirect('/register')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password,
                                 email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    return render_template('signup.html', form=form)

@app.route('/users/<string:username>')
def secret(username):
    if session['user_id'] != username:
        flash("Not Authenticated")
        return redirect('/login')
    else:
        selected_user = User.query.filter_by(username=username).first()
        return render_template('secret.html', user=selected_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        selected_user = User.login(username, password)
        print(selected_user)
        if selected_user:
            flash(f"Welcome back, {selected_user.first_name}!")
            session['user_id'] = selected_user.username
            return redirect(f'/users/{selected_user.username}')
            
    return render_template('login.html', form=form)
        
@app.route('/logout', methods =['GET','POST'])
def logout():
    session['user_id'] = None
    flash("logged out!")
    return redirect('/register')

@app.route('/users/<int:user_id>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(user_id):
    selected_user = User.query.get(user_id)
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=selected_user.username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{selected_user.username}')
    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    selected_feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=selected_feedback)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        selected_feedback.title = title
        selected_feedback.content = content
        db.session.add(selected_feedback)
        db.session.commit()
        return redirect(f'/users/{selected_feedback.username}')
    return render_template('update_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    selected_feedback = Feedback.query.get(feedback_id)
    username = selected_feedback.user.username
    if session['user_id'] != username:
        flash("Sorry, you can't delete someone elses feedback")
        return redirect(f'users/{username}')
    else:
        Feedback.query.filter_by(id=feedback_id).delete()
        db.session.commit()
        return redirect(f'/users/{username}')

@app.route('/users/<string:username>/delete', methods = ['POST'])
def delete_user(username):
    goner = User.query.filter_by(username = username).first()
    db.session.delete(goner)
    db.session.commit()
    session['user_id'] = None
    return redirect('/register')
