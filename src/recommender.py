import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a Song object against a UserProfile, reusing the shared recipe."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }
        return score_song(prefs, song_dict)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Songs for this user, ranked highest score first."""
        return sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining a song's score."""
        score, reasons = self._score(user, song)
        detail = "; ".join(reasons) if reasons else "no strong matches"
        return f"Score {score:.2f} — {detail}"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numeric columns to numbers."""
    numeric_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            song["id"] = int(song["id"])          # id is a whole number
            for field in numeric_fields:
                if field in song:
                    song[field] = float(song[field])  # convert text -> number for math
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs, returning (score, list of human-readable reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Categorical matches: exact match earns fixed points.
    if "mood" in user_prefs and song.get("mood") == user_prefs["mood"]:
        score += 3.0
        reasons.append(f"mood match: {song['mood']} (+3.0)")
    if "genre" in user_prefs and song.get("genre") == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Numeric closeness: reward songs whose energy is NEAR the target, not just high.
    if "energy" in user_prefs:
        closeness = 1 - abs(song["energy"] - user_prefs["energy"])
        points = 2.0 * closeness
        score += points
        reasons.append(f"energy {song['energy']} near target {user_prefs['energy']} (+{points:.2f})")

    # Optional acoustic preference (True/False).
    if "likes_acoustic" in user_prefs:
        is_acoustic = song.get("acousticness", 0.0) > 0.5
        if is_acoustic == user_prefs["likes_acoustic"]:
            score += 1.0
            reasons.append(f"acoustic preference match (+1.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation) sorted high to low."""
    scored = []
    for song in songs:                                    # the loop: judge every song
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # sorted() returns a NEW list (leaves `songs` untouched); reverse=True = highest first.
    scored.sort(key=lambda item: item[1], reverse=True)   # item[1] is the score
    return scored[:k]                                     # top k only
