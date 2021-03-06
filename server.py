#!/usr/bin/env python3
from flask import Flask, make_response, redirect, render_template, request, g, flash
from flask_cors import CORS
from datetime import datetime

import toml
import json 


import config
import yacs
import system

app = Flask(__name__)
app.secret_key = config.get_allowed_token()
CORS(app)

def validateToken(token):
    return token == config.get_allowed_token()

def processToken():
    token = request.cookies.get('sToken')
    g.tokenValid = validateToken(token)
    if g.tokenValid:
        g.token = token
        if len(token) < 20:
            flash(f"Current token length ({len(token)}) is below recommended length ({20})", "warn")
        if token == "UNSECUREDEFAULTTOKEN2179":
            flash(f"YOU ARE USING THE DEFAULT TOKEN, PLEASE CHANGE IT IN THE SETTINGS", "warn")

@app.route("/")
def helloWorld():
    processToken()
    return render_template("base.html")

@app.route("/components")
def components():
    processToken()
    if g.tokenValid:
        components = yacs.getComponents()
        return render_template("components.html", components=components, toml=toml)
    return make_response(redirect("/auth/login"))

@app.route("/settings")
def settings():
    processToken()
    if g.tokenValid:
        return render_template("settings.html")
    return make_response(redirect("/auth/login"))

@app.route("/components/add", methods=['POST'])
def components_add():
    processToken()
    if g.tokenValid:
        component = {}
        component["name"] = request.form['cname']
        component["pull_url"] = request.form['curl']
        component["run"] = request.form['crun']
        component["run_after_update"] = request.form['crun_after_update']
        print("crun", request.form['crun'])
        if component["run"].startswith("['") and component["run"].endswith("']"):
            component["run"] = json.loads(component["run"].replace("'", '"'))
        else:
            component["run"] = component["run"].split(";")
        if component["run_after_update"].startswith("['") and component["run_after_update"].endswith("']"):
            component["run_after_update"] = json.loads(component["run_after_update"].replace("'", '"'))
        else:
            component["run_after_update"] = component["run_after_update"].split(";")
        result = yacs.addComponent(component)
        if result:
            flash(f"Component \"{component['name']}\" Added.", "success")
            return make_response(redirect("/components"))
        else:
            flash("Failed to add component.", "err")
            return make_response(redirect("/components"))
    return make_response(redirect("/auth/login"))

@app.route("/components/remove", methods=['POST'])
def components_remove():
    processToken()
    if g.tokenValid:
        component_name = request.form['cname']
        result = yacs.removeComponent(component_name)
        if result:
            flash(f"Component \"{component_name}\" Removed.", "success")
            return make_response(redirect("/components"))
        else:
            flash("Failed to remove component.", "err")
            return make_response(redirect("/components"))
    return make_response(redirect("/auth/login"))

@app.route("/components/update", methods=['POST'])
def components_update():
    processToken()
    if g.tokenValid:
        result = yacs.updateComponents()
        if result:
            flash(f"Updated all components.", "success")
            return make_response(redirect("/components"))
        else:
            flash("Failed to update components.", "err")
            return make_response(redirect("/components"))
    return make_response(redirect("/auth/login"))

@app.route("/components/restart", methods=['POST'])
def components_restart():
    processToken()
    if g.tokenValid:
        result = yacs.restartComponents()
        if result:
            flash(f"yacs restarted.", "success")
            return make_response(redirect("/components"))
        else:
            flash("Failed to restart yacs.", "err")
            return make_response(redirect("/components"))
    return make_response(redirect("/auth/login"))

@app.route("/components/kill", methods=['POST'])
def components_kill():
    processToken()
    if g.tokenValid:
        result = yacs.killComponents()
        if result:
            flash(f"yacs killed.", "success")
            return make_response(redirect("/components"))
        else:
            flash("Failed to kill yacs.", "err")
            return make_response(redirect("/components"))
    return make_response(redirect("/auth/login"))

@app.route("/system/restart", methods=['POST'])
def system_restart():
    processToken()
    if g.tokenValid:
        result = system.restart()
        if result:
            flash(f"Reboot requested.", "success")
            return make_response(redirect("/components"))
        else:
            flash("Failed to request a reboot.", "err")
            return make_response(redirect("/components"))
    return make_response(redirect("/auth/login"))

@app.route("/auth/login")
def auth_login():
    processToken()
    return render_template("auth/login.html")

@app.route("/auth/login", methods=['POST'])
def auth_login_post():
    token = request.form['token']
    if validateToken(token):
        flash("You are now logged in.", "success")
        resp = make_response(redirect("/"))
        resp.set_cookie('sToken', token, httponly = True)
        return resp
    else:
        flash("Invalid Token", "err")
        resp = make_response(render_template("auth/login.html"))
        return resp

@app.route("/auth/logout")
def auth_logout():
    flash("You have been logged out.", "warn")
    resp = make_response(redirect("/"))
    resp.delete_cookie("sToken")
    return resp

@app.route("/auth/changepswd", methods=['POST'])
def auth_change_password():
    processToken()
    if g.tokenValid:
        token_new = request.form['token_new']
        config.setToken(token_new)
        app.secret_key = config.get_allowed_token()
        flash(f"Token Changed.", "success")
        resp = make_response(redirect("/"))
        resp.set_cookie('sToken', token_new, httponly = True)
        return resp
    return make_response(redirect("/auth/login"))

@app.route("/time")
def givetime():
    return {'time':datetime.utcnow()}

if __name__ == '__main__':
    yacs.parseData()
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc') # ssl_context='adhoc'
