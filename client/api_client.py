"""HTTP client for the Metal Snake Solid API."""
import requests
API_URL = "http://127.0.0.1:5000"
def send_score(player_name: str, score: int) -> bool:
    """Send a score to the server.
    Return True if the server saved the score, otherwise False.
    """
    try:
        response = requests.post(
            f"{API_URL}/scores",
            json={
                "player_name": player_name,
                "score": score,
            },
            timeout=3,
        )
        response.raise_for_status()
        return response.status_code == 201
    except requests.RequestException:
        return False