import os
from flask import render_template, redirect, flash, url_for, request
from image_repo import app, db, bcrypt
from image_repo.forms import RegistrationForm, LoginForm, PostForm
from image_repo.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
	if current_user.is_authenticated:
		# Display All public images and the user's private images
		private_posts = Post.query.filter_by(private=True, author=current_user).all() # Specific User private
		public_posts = Post.query.filter_by(private=False).all()
		return render_template('home.html', title="Home", public_posts=public_posts, private_posts=private_posts)
	else: # Only display public images
		public_posts = Post.query.filter_by(private=False).all()
		return render_template('home.html', title="Home", public_posts=public_posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You can now log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():	
	if current_user.is_authenticated:
		return redirect(url_for('home'))	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
	user_posts = Post.query.filter_by(author=current_user).all() # Specific User private
	return render_template('account.html', title="Account", posts=user_posts)

@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add():
	form = PostForm()
	if form.validate_on_submit():
		files = form.files.data
		for file in files:
			print(files)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)

				temp = app.config['UPLOAD_FOLDER']

				print(temp)
				print(filename)

				path = os.path.join(temp, filename)
				print(path)
				file.save(path)

				image = Post(path=str(path), name=filename, private=form.private.data, author=current_user)
		
				db.session.add(image)
		db.session.commit()
		privacy = "private" if form.private.data else "public"
		flash('Your photo has been uploaded! The upload was made ' + privacy + '.', 'success')
		return redirect(url_for('home'))
	return render_template('add.html', title="Add", form=form)