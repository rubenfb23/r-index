from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sirope
from models import User, Paper, Post
from sirope import OID  # Import OID class

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sirope setup
s = sirope.Sirope()

@login_manager.user_loader
def load_user(user_id):
    return s.find_first(User, lambda u: u.username == user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = s.find_first(User, lambda u: u.email == email and u.password == password)
        if user:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if s.find_first(User, lambda u: u.email == email):
            flash('Email already registered')
        else:
            new_user = User(username, email, password)
            s.save(new_user)
            login_user(new_user)
            flash('Registered successfully.')
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/papers')
@login_required
def papers():
    papers = list(s.load_all(Paper))
    for paper in papers:
        paper.__oid__ = s.safe_from_oid(paper.__oid__)
    return render_template('papers.html', papers=papers)

@app.route('/paper/<paper_id>')
@login_required
def paper_detail(paper_id):
    paper_oid = s.oid_from_safe(paper_id)
    paper = s.load(paper_oid)
    print(f'Loaded Paper ID: {paper_id}, Title: {paper.title}')  # Depuración
    if paper:
        posts = list(s.load_all(Post))
        return render_template('paper_detail.html', paper=paper, posts=posts)
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))

@app.route('/add_paper', methods=['GET', 'POST'])
@login_required
def add_paper():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        url = request.form['url']
        publication_date = request.form['publication_date']
        authors = request.form['authors']
        new_paper = Paper(title, summary, url, publication_date, authors)
        saved_paper = s.save(new_paper)  # Save the object directly
        s.load(saved_paper)  # Load the last saved object
        if saved_paper:
            print(f'Paper saved: {saved_paper}')
        else:
            print('Paper not saved!')
        flash('Paper added successfully.')
        return redirect(url_for('papers'))
    return render_template('add_paper.html')

@app.route('/edit_paper/<paper_id>', methods=['GET', 'POST'])
@login_required
def edit_paper(paper_id):
    paper_oid = s.oid_from_safe(paper_id)
    paper = s.load(paper_oid)  # Load the object
    if paper:
        if request.method == 'POST':
            paper.title = request.form['title']
            paper.summary = request.form['summary']
            paper.url = request.form['url']
            paper.publication_date = request.form['publication_date']
            paper.authors = request.form['authors']
            s.save(paper)  # Save the object directly
            flash('Paper updated successfully.')
            return redirect(url_for('paper_detail', paper_id=paper_id))
        return render_template('edit_paper.html', paper=paper)
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))

@app.route('/delete_paper/<paper_id>', methods=['POST'])
@login_required
def delete_paper(paper_id):
    paper_oid = s.oid_from_safe(paper_id)
    paper = s.load(paper_oid)  # Load the object
    if paper:
        s.delete(paper)  # Delete the object directly
        posts = list(s.find_all(Post, lambda p: p.paper_id == paper_id))
        for post in posts:
            s.delete(post)  # Delete associated posts
        flash('Paper and associated reviews deleted successfully.')
        return redirect(url_for('papers'))
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))

@app.route('/add_post/<paper_id>', methods=['GET', 'POST'])
@login_required
def add_post(paper_id):
    if request.method == 'POST':
        content = request.form['content']
        user_id = current_user.username
        new_post = Post(content, user_id, paper_id)
        s.save(new_post)
        flash('Review added successfully.')
        return redirect(url_for('paper_detail', paper_id=paper_id))
    return render_template('add_post.html', paper_id=paper_id)

@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post_oid = s.oid_from_safe(post_id)
    post = s.load(post_oid)  # Load the object
    if post:
        if request.method == 'POST':
            post.content = request.form['content']
            s.save(post)  # Save the object directly
            flash('Review updated successfully.')
            return redirect(url_for('paper_detail', paper_id=post.paper_id))
        return render_template('edit_post.html', post=post)
    else:
        flash('Review not found.')
        return redirect(url_for('papers'))

@app.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post_oid = s.oid_from_safe(post_id)
    post = s.load(post_oid)  # Load the object
    if post:
        paper_id = post.paper_id
        s.delete(post)  # Delete the object directly
        flash('Review deleted successfully.')
        return redirect(url_for('paper_detail', paper_id=paper_id))
    else:
        flash('Review not found.')
        return redirect(url_for('papers'))

if __name__ == '__main__':
    app.run(debug=True)
