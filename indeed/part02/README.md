# Project/Video Documentation
## Prerequisites 

## Registering an Indeed App
You'll need to register an app with Indeed if you would like to use their API. Go to `developer.indeed.com` and create an account and sign in. From there you should be able to navigate to this address `https://secure.indeed.com/account/apikeys` where you will see an option to register a new application.

Provide the following:
* Application name
* Application description
* Credential type: __OAuth 2.0__
* Allow grant types: __Authorization code__
* Redirect URL: __http://localhost:8000/callback__
* __Do not have the application reviewed__

I don't think anything else is strictly required, but it won't affect the program if you do fill out the rest.

## Protecting credentials
Now that we have a registered app with Indeed they have provided us some credentials. These credentials are sensitive and if exposed to the public, would make your app very vulenerable to malicious actors. So to protect our selves we will store this information in a `.env` file which won't be tracked by git and when we run the program we will pull in those values as necessary.

* Make sure `.env` in included in the `.gitignore` file.
* Create `.env` file.

Add your credentials to the file in key/value format. And while we're here lets add some of the necessary endpoints we're going to use in this program, since they are sort of constants. The other information can be found in Indeeds super good documentation: https://developer.indeed.com/docs/authorization/3-legged-oauth. The callback URL has to be one of our routes in the application which will kick off our logic to handle extracting the auth code and exchanging it for an oauth token.

```
CLIENT_ID=get-from-indeed
CLIENT_SECRET=get-from-indeed
AUTHORIZATION_ENDPOINT=https://secure.indeed.com/oauth/v2/authorize
TOKEN_ENDPOINT=https://apis.indeed.com/oauth/v2/tokens
GET_USER_INFO_ENDPOINT=https://secure.indeed.com/v2/api/userinfo
SCOPE=email
CALLBACK_URL=http://localhost:8000/callback
SECRET_KEY=some-long-random-secret-string
```

## Setting up the environment
Before we should really start coding we should get our environment set up and sync'd with our IDE. To create a virtual environment directory run this command:

`python3 -m venv venv` 

This will create a virtual env directory, which we will point our system to look for any installed dependencies instead of trying to use whatever is in our PATH or globally installed.

Before we can install anything onto our virtual environment we need to activate it. This is done by running the activate script.

`source venv/bin/activate`

If everything went as planned your terminal prompt should be prepended with the virtual environment directory, in our case `venv`

So it should look something like this: `$ (venv) user@host %`

Now we can install our dependencies:

`pip3 install flask requests requests-oauthlib python-dotenv`

Also a neat pip trick is to print the library list to a file so that we can install all the dependencies at once without having to remember the individual libraries. This process becomes very helpfuly when it comes time to deploy or implement an automated pipeline for your project. So first we call the pip command to list all the installed dependencies and than pipe that output to a file.

`pip3 freeze > requirements.txt`

Now in the future when we start with a fresh environment we can reference the `requirements.txt` file to install everything we need with this command:

`pip3 install -r requirements.txt`

That easy!

## Coding the application
