from flask import Flask, redirect, request, render_template, url_for, session
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load the configuration variables from the .env file
load_dotenv()

# Encrypt the session object
app.secret_key = os.getenv("SECRET_KEY")

def create_oauth_session():
    """Creates an OAuth2Session object with the application's credentials."""
    return OAuth2Session(
        client_id=os.getenv("CLIENT_ID"),
        redirect_uri=os.getenv("CALLBACK_URL"),
        scope=os.getenv("SCOPE"),
    )

@app.route("/")
def home():
    token = session.get("token")
    user_info = session.get("user_info")
    return render_template("home.html", token=token, user_info=user_info)


@app.route("/login")
def login():
    # Create an OAuth2Session object with your credentials
    oauth_session = OAuth2Session(
        client_id=os.getenv("CLIENT_ID"),
        redirect_uri=os.getenv("CALLBACK_URL"),
        scope=os.getenv("SCOPE"),
    )

    # Generate the authorization URL and redirect the user to it
    authorization_url = oauth_session.authorization_url(os.getenv("AUTHORIZATION_ENDPOINT"))[0]
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    # Get the identity server auth code
    code = request.args.get("code")

    # Exchange the code for a token
    oauth_session = OAuth2Session(
        client_id=os.getenv("CLIENT_ID"),
        redirect_uri=os.getenv("CALLBACK_URL"),
    )

    # Fetch the access token using the authorization code
    token = oauth_session.fetch_token(
        client_secret=os.getenv("CLIENT_SECRET"),
        token_url=os.getenv("TOKEN_ENDPOINT"),
        code=code,
    )

    # Store the token in the session object
    session["token"] = token

    # Send the user back to the home page
    return redirect(url_for("home"))

@app.route("/getUserInfo")
def get_user_info():
    # Get token from session
    token = session.get("token")
    if not token:
        return redirect(url_for("login"))

    # Create OAuth2Session object and call protected resource
    oauth_session = OAuth2Session(
        client_id=os.getenv("CLIENT_ID"),
        token=token
    )
    session["user_info"] = oauth_session.get(os.getenv("GET_USER_INFO_ENDPOINT")).json()
    return redirect(url_for("home"))

if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(port=8000, debug=True)
