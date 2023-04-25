from flask import Flask, redirect, request, render_template, url_for, session
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load the configuration variables from the .env file
load_dotenv()

# Encrypt the session object
app.secret_key = os.getenv("SECRET_KEY")


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

    # # Get the authorization code from the query parameters
    # code = request.args.get('code')

    # # Replace the values with your own OAuth2 credentials and API endpoint
    # client_id = 'your_client_id'
    # client_secret = 'your_client_secret'
    # callback_uri = 'http://localhost:8000/callback'
    # token_endpoint = 'https://example.com/token'

    # # Exchange the authorization code for an access token
    # data = {
    #     'grant_type': 'authorization_code',
    #     'code': code,
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    #     'callback_uri': callback_uri
    # }
    # response = requests.post(token_endpoint, data=data)
    # access_token = response.json()['access_token']

    # # Use the access token to make a request to the API
    # api_endpoint = 'https://example.com/api'
    # headers = {'Authorization': f'Bearer {access_token}'}
    # response = requests.get(api_endpoint, headers=headers)
    # return response.json()


# @app.route('/login')
# def login():
#     # Create an OAuth2Session object with your credentials
#     oauth = OAuth2Session(
#         os.getenv('CLIENT_ID'),
#         callback_uri=os.getenv['callback_URI'],
#         scope=os.getenv['SCOPE']
#     )

#     # Generate the authorization URL and callback the user to it
#     authorization_url, state = oauth.authorization_url(os.getenv('AUTH_ENDPOINT'))
#     return redirect(authorization_url)

# @app.route('/callback')
# def callback():
#     # Create an OAuth2Session object with your credentials
#     oauth = OAuth2Session(
#         os.getenv('CLIENT_ID'),
#         callback_uri=os.getenv['callback_URI']
#     )

#     # Fetch the access token using the authorization code
#     token = oauth.fetch_token(
#         os.getenv('TOKEN_ENDPOINT'),
#         authorization_response=request.url,
#         client_secret=os.getenv('CLIENT_SECRET')
#     )

#     # Use the access token to make a request to the API
#     api_endpoint = os.getenv('API_ENDPOINT')
#     headers = {'Authorization': f'Bearer {token["access_token"]}'}
#     response = oauth.get(api_endpoint, headers=headers)
#     return response.json()

if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run(port=8000, debug=True)
