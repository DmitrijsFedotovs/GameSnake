"""Flask server for Metal Snake Solid."""
from flask import Flask, jsonify, render_template, request
from api.db import get_player_stats, get_top_scores, save_score
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)
@app.route("/scores", methods=["POST"])
def create_score():
    """Validate and save a game score."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required."}), 400
    player_name = data.get("player_name")
    score = data.get("score")
    if not isinstance(player_name, str) or not player_name.strip():
        return jsonify({"error": "Player name is required."}), 400
    player_name = player_name.strip()
    if len(player_name) > 16:
        return jsonify({"error": "Player name must be at most 16 characters."}), 400
    if isinstance(score, bool) or not isinstance(score, int) or score < 0:
        return jsonify({"error": "Score must be a non-negative integer."}), 400
    save_score(player_name, score)
    return jsonify({
        "message": "Score saved successfully.",
        "player_name": player_name,
        "score": score,
    }), 201
@app.route("/scores/top", methods=["GET"])
def top_scores():
    """Return the top ten scores."""
    return jsonify(get_top_scores()), 200
@app.route("/players/<name>/stats", methods=["GET"])
def player_stats(name: str):
    """Return statistics for a player."""
    stats = get_player_stats(name)
    if stats is None:
        return jsonify({"error": "Player not found."}), 404
    return jsonify(stats), 200
@app.route("/")
def home():
    """Display the leaderboard."""
    players = get_top_scores()
    return render_template("index.html", players=players)
@app.route("/rules")
def rules():
    """Display the game rules."""
    return render_template("rules.html")
if __name__ == "__main__":
    app.run(debug=True)