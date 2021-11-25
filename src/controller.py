#!/usr/bin/python3
from os import name
from flask import Flask, request
from flask.templating import render_template
import time

from model import Game


# INITIALIZATION FLASK
app = Flask("Lupus on LAN",
            static_folder='images')


# INITIALIZATION CONTROLLER
app.game = Game()


# CUSTOM FUNCTIONS
def goToLobby(userID):
    return render_template("lobby.html",
                            players  = app.game.getUsersNames(),
                            progress = app.game.getProgressLobbyStr())


# FLASK FUNCTIONS
@app.route("/")
def home():
    userIP = request.remote_addr
    if app.game.isAlreadyLogged(userIP):
        return goToLobby(userIP)
    # go to register page
    return render_template("register.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    userIP = request.remote_addr
    if app.game.isAlreadyLogged(userIP):
        return goToLobby(userIP)
    # Check if there is a message
    if request.method == 'POST':
        userName = request.form["nickname"]
        if app.game.addUser(userIP, userName):
            return goToLobby(userIP)
    return render_template("register.html")


@app.route("/lobby", methods=['GET', 'POST'])
def lobby():
    userIP = request.remote_addr
    if not app.game.isAlreadyLogged(userIP):
        return render_template("register.html")
    # Check if start
    if app.game.lobbyIsFull():
        if not app.game.isMaster(userIP):
            return render_template("player.html",
                                    name           = app.game.getNameOf(userIP),
                                    role           = app.game.getRoleDataOf(userIP),
                                    playersSimilar = app.game.getPlayersSimilarTo(userIP))
        else:
            # return render_template("master_night.html",
            #                         players     = app.game.getPlayers(),
            #                         roles       = app.game.getRolesData(),
            #                         nightPhases = app.game.getNightPhases())
            return render_template("master.html",
                                    word1   = ['a', 'b', 'c', 'd'],
                                    word2   = ['#a', '#b', '#c', '#d'],
                                    status  = app.game.getStatus(),
                                    players = app.game.getPlayers(),
                                    roles   = app.game.getRolesData())
    return goToLobby(userIP)


@app.route("/master_day", methods=['GET', 'POST'])
def masterDay():
    userIP = request.remote_addr
    if app.game.isMaster(userIP):
        # Check if there is a message
        if request.method == 'POST':
            app.game.processNightData(dict(request.form))
            return render_template("master_day.html",
                                    players     = app.game.getPlayers(),
                                    roles       = app.game.getRolesData())
    return goToLobby(userIP)
