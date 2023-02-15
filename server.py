from flask import *
import os
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

app  = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"]



# 👆 We're continuing from the steps above. Append this to your server.py file.

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

#https://dev-nu48fjmkn57b1wuq.us.auth0.com/authorize?response_type=code&client_id=v1rFGukUNg0qnMBio96SGrzizZBBdR9L&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback&scope=openid+profile+email&state=5q4Cqj7eygRx9zHNma16uje8Ac9i1x&nonce=iHkiyaV23Jc7gS8QCvxU
# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    #session['uid'] = token['userinfo']['sid']
    #session['email']=token['userinfo']['email']
    #session['picture']=token['userinfo']['pitcure']
    return redirect("/")



# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("hello_world", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# @app.route('/api/fact', methods=['GET'])
# def hi():
#   return jsonify({"id": 15, "source": "brain", "content": "flaming hot cheetos"})

# @app.route("/api/fact", method=["POST"])
# def fact():
#   print(request.json)
#   return jsonify("ok")