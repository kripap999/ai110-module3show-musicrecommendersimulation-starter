"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# A set of taste profiles used to stress-test the recommender.
# The last one is "adversarial": high energy paired with a sad mood, which
# almost never occur together in real music, to see how scoring copes.
PROFILES = [
    ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.9}),
    ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.9}),
    ("Adversarial: Sad but High-Energy", {"genre": "metal", "mood": "sad", "energy": 0.9}),
]


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one named profile."""
    print(f"\n=== {name} ===")
    print(f"User profile: {user_prefs}\n")
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  (Score: {score:.2f})")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES:
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
