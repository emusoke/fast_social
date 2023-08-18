from fastapi import FastAPI, Depends, Header
from fastapi.security import HTTPBearer
from typing import Annotated, Any
from routers import users, posts
import logging
logging.basicConfig(level=logging.DEBUG)


import json
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode
from authlib.integrations.starlette_client import OAuth,OAuthError
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

config = Config('.env')

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key = env.get("APP_SECRET_KEY")
                   )

oauth = OAuth()
oauth.register(
        name='auth0',
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
        client_kwargs={
        "scope": "openid profile email"},
        )

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def home(request: Request):
    return 'hello world'


@app.get("/login")
async def end_point_to_redirect_user_to_login(request: Request):
    redirect_uri = request.url_for('auth')
    print(f'redirect uri is {redirect_uri}')
    return await oauth.auth0.authorize_redirect(request,redirect_uri)


@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.auth0.authorize_access_token(request)
    except OAuthError as error:
        return "Error occured"
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    logging.debug(f"The token is {token} and the user is {user}")
    return RedirectResponse(url='/docs')

@app.get('/logout')
def logout(request: Request):
    request.session.pop('user',None)
    request.session.clear()
    print("Logging the used out")
    logout_redirect = ("https://"
        + env.get("AUTH0_DOMAIN") + "/v2/logout?"
        + urlencode(
            {
                "returnTo": 'http://localhost:8000/docs',
                "client_id": env.get("AUTH0_CLIENT_ID"),
            })
        )
    print(logout_redirect)
    return RedirectResponse(logout_redirect)
