from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

HOME_HTML = """
<h1>Home</h1>
<nav>
  <a href="{{ url_for('login') }}">Login</a> |
  <a href="{{ url_for('form') }}">Form</a>
</nav>
"""

LOGIN_HTML = """
<h1>Login</h1>
<form method="post">
  <label>Username: <input id="username" name="username"></label><br/>
  <label>Password: <input id="password" name="password" type="password"></label><br/>
  <button id="submit" type="submit">Login</button>
</form>
{% if welcome %}
<div id="welcome">Welcome, {{ welcome }}</div>
{% endif %}
<a href="{{ url_for('home') }}">Back</a>
"""

FORM_HTML = """
<h1>Sample Form</h1>
<form method="post">
  <label>Email: <input id="email" name="email" type="email"></label><br/>
  <label>Comment: <input id="comment" name="comment" type="text"></label><br/>
  <button id="submit" type="submit">Submit</button>
</form>
{% if message %}
<div id="message">{{ message }}</div>
{% endif %}
<a href="{{ url_for('home') }}">Back</a>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/login", methods=["GET", "POST"])
def login():
    welcome = None
    if request.method == "POST":
        welcome = request.form.get("username", "")
    return render_template_string(LOGIN_HTML, welcome=welcome)

@app.route("/form", methods=["GET", "POST"])
def form():
    message = None
    if request.method == "POST":
        email = request.form.get("email", "")
        comment = request.form.get("comment", "")
        message = f"Received: {email} / {comment}"
    return render_template_string(FORM_HTML, message=message)

if __name__ == "__main__":
    app.run(debug=True)
