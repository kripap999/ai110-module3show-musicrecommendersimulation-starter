# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

**How real systems do it.** Big platforms like Spotify and YouTube predict what you'll love next using two main ideas. *Collaborative filtering* looks at other users' behavior — likes, skips, plays, and playlists — and recommends what people with similar taste enjoyed, even if it can't "hear" the song. *Content-based filtering* looks at the attributes of the songs themselves — genre, mood, energy, tempo — and recommends songs that are similar to what you already like. Real systems blend both (a *hybrid*) so they can handle brand-new songs and still surprise you.

**What my version prioritizes.** My recommender is **content-based**. It compares a user's stated taste profile against each song's attributes and scores how well they match. I prioritize **mood** most, because that's what most defines a song's "vibe" for me, followed by genre, then how close the song's energy is to what the user wants, and finally whether it's acoustic.

**How scoring works.** For each song I compute a single score:

- **mood** matches favorite mood → **+3.0** (weighted highest, on purpose)
- **genre** matches favorite genre → **+2.0**
- **energy** closeness → **+2.0 × (1 − |song energy − target energy|)**
  (rewards songs *close* to the target, not just high-energy ones)
- **acoustic** preference matches → **+1.0**

**How I choose what to recommend.** Scoring rates one song at a time, so the score only becomes meaningful when compared to others. The **ranking rule** sorts all songs by score (highest first) and returns the top `k`. Scoring is like grading each song; ranking is the "honor roll" I actually show the user.

### Features used

**`Song`** stores: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`,
`danceability`, `acousticness` (plus `id`, `title`, `artist`). My scoring uses
**genre, mood, energy, and acousticness**.

**`UserProfile`** stores: `favorite_genre`, `favorite_mood`, `target_energy`, and
`likes_acoustic` (a yes/no preference for acoustic songs).

**Example profile I test with:** `genre=jazz`, `mood=dreamy`, `target_energy=0.3`,
`likes_acoustic=True`.

### Potential biases I expect

- **Mood can override genre.** Because mood is weighted highest (3.0 > 2.0), the
  top pick for a jazz-loving user can actually be a *classical* song that matches
  the mood. This is intended, but it means "favorite genre" is a weaker signal
  than a user might assume.
- **Sparse categories do little work.** Genres/moods that appear on only one song
  (e.g. jazz) can only ever reward that single song, so the feature barely
  discriminates across the catalog.
- **Small catalog.** With only 19 songs, a single strong match can dominate, and
  whole genres are represented by one example.
- **No understanding of content.** It scores tags and numbers only — it can't hear
  the music, read lyrics, or know language or artist.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Sample output from `python -m src.main` for the default pop/happy profile:

```
Loaded songs: 19

User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

Top recommendations:

1. Sunrise City by Neon Echo  (Score: 6.96)
   Because: mood match: happy (+3.0); genre match: pop (+2.0); energy 0.82 near target 0.8 (+1.96)

2. Rooftop Lights by Indigo Parade  (Score: 4.92)
   Because: mood match: happy (+3.0); energy 0.76 near target 0.8 (+1.92)

3. Gym Hero by Max Pulse  (Score: 3.74)
   Because: genre match: pop (+2.0); energy 0.93 near target 0.8 (+1.74)

4. Night Drive Loop by Neon Echo  (Score: 1.90)
   Because: energy 0.75 near target 0.8 (+1.90)

5. Concrete Jungle by Rhyme Theory  (Score: 1.80)
   Because: energy 0.7 near target 0.8 (+1.80)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



