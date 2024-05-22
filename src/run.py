from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sirope
from models import User, Paper, Post

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sirope setup
s = sirope.Sirope()

# User loader
@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database based on the provided user_id.

    Args:
        user_id (str): The username of the user to load.

    Returns:
        User: The loaded User object.

    """
    return s.find_first(User, lambda u: u.username == user_id)

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.

    If the request method is POST, it retrieves the email and password from the form data.
    It then searches for a user with the provided email and password in the database.
    If a user is found, it logs in the user, flashes a success message, and redirects to the index page.
    If no user is found, it flashes an error message.
    If the request method is GET, it renders the login template.

    Returns:
        If the request method is POST and a user is found, it redirects to the index page.
        Otherwise, it renders the login template.
    """
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
    """
    Register a new user.

    This function handles the registration process for a new user. It accepts both GET and POST requests.
    If a POST request is received, it retrieves the username, email, and password from the request form.
    It checks if the email is already registered in the database. If it is, it displays a flash message indicating that the email is already registered.
    If the email is not registered, it creates a new User object with the provided username, email, and password.
    It saves the new user to the database, logs in the user, displays a flash message indicating successful registration, and redirects to the index page.
    If a GET request is received, it renders the register.html template.

    Returns:
        If a POST request is received and the registration is successful, it redirects to the index page.
        If a GET request is received, it renders the register.html template.
    """
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
    """
    Logs out the current user and redirects to the index page.

    Returns:
        A redirect response to the index page.
    """
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    """
    Renders the index.html template with a list of papers and their corresponding reviews.

    Returns:
        The rendered index.html template with the paper reviews.
    """
    papers = list(s.load_all(Paper))
    paper_reviews = []

    for paper in papers:
        paper.__oid__ = s.safe_from_oid(paper.__oid__)
        reviews = list(s.filter(Post, lambda p: p.paper_id == paper.__oid__))

        if reviews:
            avg_score = round(sum([review.score for review in reviews]) / len(reviews), 2)
        else:
            avg_score = 0

        paper_reviews.append({
            'paper': paper,
            'avg_score': avg_score,
            'reviews': reviews,
            'num_reviews': len(reviews)
        })

    return render_template('index.html', paper_reviews=paper_reviews)


@app.route('/papers')
@login_required
def papers():
    """
    Retrieves the papers associated with the current user and renders them on the 'papers.html' template.

    Returns:
        The rendered 'papers.html' template with the retrieved papers.
    """
    user_id = current_user.get_id()
    papers = list(s.filter(Paper, lambda p: p.authors == user_id))
    for paper in papers:
        paper.__oid__ = s.safe_from_oid(paper.__oid__)
    return render_template('papers.html', papers=papers)


@app.route('/paper/<paper_id>')
@login_required
def paper_detail(paper_id):
    """
    Display the details of a paper.

    Args:
        paper_id (str): The ID of the paper.

    Returns:
        A rendered template with the paper details, posts, user information, and flags indicating if the user has reviewed the paper or if the user is an author.
        If the paper is not found, it flashes a message and redirects to the papers page.
    """
    paper_oid = s.oid_from_safe(paper_id)
    paper = s.load(paper_oid)
    user = current_user
    user_has_reviewed = False
    is_author = False

    if paper:
        is_author = user.get_id() in paper.authors.split(", ")
        posts = list(s.filter(Post, lambda p: p.paper_id == paper_id))       
        for post in posts:
            post.__oid__ = s.safe_from_oid(post.__oid__)
            if post.user_id == user.get_id():
                user_has_reviewed = True
                break
        paper.__oid__ = s.safe_from_oid(paper.__oid__)
        return render_template('paper_detail.html', paper=paper, posts=posts, user=user, user_has_reviewed=user_has_reviewed, is_author=is_author)
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))


@app.route('/add_paper', methods=['GET', 'POST'])
@login_required
def add_paper():
    """
    Add a new paper to the system.

    This function handles both GET and POST requests. If the request method is POST,
    it retrieves the paper details from the form data and creates a new Paper object.
    The Paper object is then saved to the system using the `save` method of the `s` object.
    If the paper is successfully saved, a success message is printed and the user is redirected
    to the 'papers' page. Otherwise, an error message is printed.

    If the request method is GET, the function renders the 'add_paper.html' template.

    Returns:
        If the request method is POST, it redirects the user to the 'papers' page.
        If the request method is GET, it renders the 'add_paper.html' template.
    """
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        url = request.form['url']
        publication_date = request.form['publication_date']
        authors = request.form['authors']
        new_paper = Paper(title, summary, url, publication_date, authors)
        saved_paper = s.save(new_paper)
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
    """
    Edit a paper with the given paper_id.

    Args:
        paper_id (str): The unique identifier of the paper.

    Returns:
        If the paper is found:
            If the request method is POST:
                - Updates the paper with the provided form data.
                - Flashes a success message.
                - Redirects to the paper detail page.
            If the request method is GET:
                - Renders the edit_paper.html template with the paper data.
        If the paper is not found:
            - Flashes an error message.
            - Redirects to the papers page.
    """
    paper_oid = s.oid_from_safe(paper_id)
    paper = s.load(paper_oid)
    if paper:
        if request.method == 'POST':
            paper.title = request.form['title']
            paper.summary = request.form['summary']
            paper.url = request.form['url']
            paper.publication_date = request.form['publication_date']
            paper.authors = request.form['authors']
            s.save(paper)
            flash('Paper updated successfully.')
            return redirect(url_for('paper_detail', paper_id=paper_id))
        return render_template('edit_paper.html', paper=paper)
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))


@app.route('/delete_paper/<paper_id>', methods=['POST'])
@login_required
def delete_paper(paper_id):
    """
    Delete a paper and its associated reviews.

    Args:
        paper_id (str): The ID of the paper to be deleted.

    Returns:
        flask.Response: A redirect response to the 'papers' route.

    """
    paper_oid = s.oid_from_safe(paper_id)
    paper = s.load(paper_oid)
    if paper:
        s.delete(paper_oid)
        posts = list(s.filter(Post, lambda p: p.paper_id == paper_oid))
        for post in posts:
            s.delete(post)
        flash('Paper and associated reviews deleted successfully.')
        return redirect(url_for('papers'))
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))


@app.route('/add_post/<paper_id>', methods=['GET', 'POST'])
@login_required
def add_post(paper_id):
    """
    Add a new post to a paper.

    Args:
        paper_id (str): The ID of the paper.

    Returns:
        If the paper exists:
            If the request method is POST:
                - If the post is added successfully, redirect to the paper detail page.
            If the request method is GET:
                - Render the 'add_post.html' template.
        If the paper does not exist:
            - Redirect to the papers page.

    """
    paper_oid = s.oid_from_safe(paper_id)
    if s.exists(paper_oid):
        if request.method == 'POST':
            content = request.form['content']
            score = float(request.form['score'])
            new_post = Post(content, current_user.username, paper_id, score)
            s.save(new_post)
            flash('Review added successfully.')
            return redirect(url_for('paper_detail', paper_id=paper_id))
        return render_template('add_post.html')
    else:
        flash('Paper not found.')
        return redirect(url_for('papers'))


@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edit a post.

    Args:
        post_id (str): The ID of the post to be edited.

    Returns:
        If the post is found:
            If the request method is POST:
                - Updates the content of the post.
                - Saves the updated post.
                - Flashes a success message.
                - Redirects to the paper detail page.
            If the request method is GET:
                - Renders the edit_post.html template with the post data.
        If the post is not found:
            - Flashes an error message.
            - Redirects to the papers page.
    """
    post_oid = s.oid_from_safe(post_id)
    post = s.load(post_oid)
    if post:
        if request.method == 'POST':
            post.content = request.form['content']
            s.save(post)
            flash('Review updated successfully.')
            return redirect(url_for('paper_detail', paper_id=post.paper_id))
        return render_template('edit_post.html', post=post)
    else:
        flash('Review not found.')
        return redirect(url_for('papers'))


@app.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Delete a post with the given post_id.

    Args:
        post_id (str): The ID of the post to be deleted.

    Returns:
        redirect: A redirect to the paper_detail page of the deleted post's paper_id if the post is found and deleted successfully.
        redirect: A redirect to the papers page if the post is not found.

    """
    post_oid = s.oid_from_safe(post_id)
    post = s.load(post_oid)
    if post:
        paper_id = post.paper_id
        s.delete(post_oid)
        flash('Review deleted successfully.')
        return redirect(url_for('paper_detail', paper_id=paper_id))
    else:
        flash('Review not found.')
        return redirect(url_for('papers'))


if __name__ == '__main__':
    app.run(debug=True)
