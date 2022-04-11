#!/usr/bin/env python3
from unittest import result
from flask import Flask, make_response, redirect, render_template, request, g
from flask_cors import CORS
from datetime import datetime

import config
import yacs

app = Flask(__name__)
CORS(app)

def validateToken(token):
    return token == config.allowed_token

def processToken():
    token = request.cookies.get('sToken')
    g.tokenValid = validateToken(token)
    if g.tokenValid:
        g.token = token

@app.route("/")
def helloWorld():
    processToken()
    return render_template("base.html")

@app.route("/loggedin")
def loggedin():
    processToken()
    if g.tokenValid:
        components = yacs.getComponents()
        return render_template("loggedin.html", components=components)
    return make_response(redirect("/auth/login"))

@app.route("/components/add", methods=['POST'])
def components_add():
    processToken()
    if g.tokenValid:
        component = {}
        component["name"] = request.form['cname']
        component["pull_url"] = request.form['curl']
        component["run"] = request.form['crun']
        result = yacs.addComponent(component)
        if result:
            components = yacs.getComponents()
            return render_template("loggedin.html", components=components, msg="Component Added!")
        else:
            components = yacs.getComponents()
            return render_template("loggedin.html", components=components, msg="Failed to add component.")
    return make_response(redirect("/auth/login"))

@app.route("/auth/login")
def auth_login():
    processToken()
    return render_template("auth/login.html")

@app.route("/auth/login", methods=['POST'])
def auth_login_post():
    token = request.form['token']
    if validateToken(token):
        resp = make_response(redirect("/"))
        resp.set_cookie('sToken', token)
        return resp
    else:
        resp = make_response(render_template("auth/login.html", msg="Invalid Token"))
        return resp

@app.route("/auth/logout")
def auth_logout():
    resp = make_response(render_template("auth/loggedout.html"))
    resp.delete_cookie("sToken")
    return resp

@app.route("/time")
def givetime():
    return {'time':datetime.utcnow()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')