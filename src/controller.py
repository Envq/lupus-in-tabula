"""Implementation of the controller of the game"""
from model import Game
from roles import MASTER

from flask import Flask, request
from flask.templating import render_template



# INITIALIZATION FLASK
app = Flask("virtual-lupus Game")

# INITIALIZATION CONTROLLER
app._game = Game()
app._names = list()


# FUNCTIONS
@app.route("/")
def home():
    """Home page"""
    return render_template("home.html")


@app.route("/register", methods=["POST"])
def register():
    """Register player"""
    if request.method == "POST":
        name = request.form["name"]

        if name == MASTER:
            app._game.addMaster()
            return render_template("loading.html", name=name)

        if name and not app._game.thereIs(name) and not app._game.gameFull():
            app._game.addPlayer(request.form["name"])
            return render_template("loading.html", name=name)

    return render_template("home.html")


@app.route("/lobby", methods=["POST"])
def lobby():
    """Loading player"""
    if request.method == "POST":
        name = request.form["name"]
        print(app._game.getPlayers())
        print(app._game._roles)

        if not app._game.gameFull() or not app._game.isMaster():
            return render_template("loading.html", name=name)
        else:
            app._game.initRoles()
            if name == MASTER:
                return render_template("master.html", players=app._game.getPlayers())
            else:
                role = app._game.getPlayers()[name]
                return render_template("player.html", name=name, role=role)


# MAIN
if __name__ == "__main__":
    app.run(debug=True)
    # http://localhost:5000/
