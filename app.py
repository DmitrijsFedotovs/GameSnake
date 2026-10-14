from flask import Flask, render_template
from leaderboard import get_top_players
app = Flask(__name__)
@app.route("/")
def home():
    players = get_top_players()
    return render_template("index.html", players=players)
if __name__ == "__main__":
    app.run(debug=True)