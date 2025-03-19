from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Function to fetch playing XI from Cricbuzz
def get_playing_xi(match_id):
    url = f"https://www.cricbuzz.com/match-api/{match_id}.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    data = response.json()
    teams = data.get("team", {})
    playing_xi = {}

    for team_id, team_info in teams.items():
        team_name = team_info.get("name")
        players = team_info.get("player", [])
        playing_xi[team_name] = [
            {"name": player["name"], "image": f"https://www.cricbuzz.com/a/img/v1/152x152/i1/c{player['id']}.jpg"}
            for player in players if player.get("id")
        ]

    return playing_xi

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-playing-xi", methods=["POST"])
def get_xi():
    match_id = request.json.get("match_id")
    playing_xi = get_playing_xi(match_id)

    if playing_xi:
        return jsonify({"status": "success", "data": playing_xi})
    return jsonify({"status": "error", "message": "Invalid match ID or data not found"})

if __name__ == "__main__":
    app.run(debug=True)
