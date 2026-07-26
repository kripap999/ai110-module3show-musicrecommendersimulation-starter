# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0** — a content-based music recommender that matches a listener's
stated "vibe" (genre, mood, energy, acoustic preference) to songs in a small catalog.

---

## 2. Intended Use  

VibeMatch takes a short description of a listener's taste and returns a ranked list
of songs from the catalog, with a plain-language reason for each pick. It is built
for **classroom exploration**, not real end users — the goal is to understand how a
recommender turns preferences into ranked results, not to power a real music app.

It assumes the user can describe their taste in the four terms the system knows:
a favorite genre, a favorite mood, a target energy level (0.0–1.0), and whether they
prefer acoustic songs. It also assumes those preferences are honest and reasonably
consistent — the adversarial test showed it behaves oddly when they conflict.

**Non-intended use.** VibeMatch should **not** be used as a real product or to make
decisions that matter. It runs on a tiny 19-song catalog, so it is not a substitute
for a real music service. It should not be treated as an objective judge of music
quality (the scores only reflect *my* chosen weights), and it should not be used to
serve listeners with rare or underrepresented tastes, since the evaluation showed it
gives them poor, near-random results. It is a learning tool, not a shipping system.

---

## 3. How the Model Works  

Think of every song as having a few labels and dials: what genre it is, what mood it
is, how much energy it has (a dial from calm to intense), and how acoustic it is. The
listener describes their ideal song in those same terms.

To recommend, VibeMatch goes through the catalog one song at a time and gives each
song points for how well it matches the listener:

- If the **mood** matches, it earns the most points (3), because mood matters most to me.
- If the **genre** matches, it earns 2 points.
- For **energy**, a song earns up to 2 points depending on how *close* its energy is
  to what the listener wants — an exact match gets the full 2, and the further away it
  is, the fewer points it gets. (It rewards *closeness*, not just loud songs.)
- If the song's **acoustic-ness** matches the listener's acoustic preference, it earns 1 point.

Every song ends up with a total score. The system then sorts all the songs from
highest score to lowest and shows the top few. The starter code was just an empty
shell with the math left blank — I filled in the point values, the "closeness" rule
for energy, the sorting, and a short explanation printed with each recommendation.

---

## 4. Data  

The catalog is a single CSV file, `data/songs.csv`, with **19 songs**. Each song has
a genre, a mood, and four numeric attributes (energy, tempo_bpm, valence,
danceability, acousticness), plus title and artist.

It covers **13 genres** (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip
hop, edm, folk, r&b, metal, classical, blues, reggae, country) and **14 moods**
(happy, chill, intense, relaxed, moody, focused, energetic, nostalgic, romantic,
angry, dreamy, sad, uplifting, heartfelt). The starter file had 10 songs; I added
9 to widen the range of genres and moods so the scoring had more variety to work with.

What's missing: the catalog is tiny, so most genres and moods appear on only one
song. It also has no lyrics, language, release year, or popularity data, and it
carries no information about real listeners' behavior — so whole styles of music and
whole ways of describing taste simply aren't represented.

---

## 5. Strengths  

VibeMatch works well for **mainstream, internally-consistent tastes** that are well
represented in the catalog. For "High-Energy Pop" and "Chill Lofi," the top results
felt right: the pop fan got bright, upbeat pop, and the lofi fan got quiet, acoustic,
low-energy tracks.

Patterns it captures correctly:

- **Opposite tastes produce opposite lists.** The pop and lofi profiles share almost
  no songs in their top 5, which is exactly what should happen.
- **The energy "closeness" rule works.** Low-energy listeners get calm songs and
  high-energy listeners get intense ones, rather than everyone getting the loudest track.
- **The explanations are honest.** Each recommendation shows the points it earned and
  why, so it's easy to see the reasoning matched my intuition (e.g., a song ranked #1
  because it matched mood *and* genre *and* energy).

---

## 6. Limitations and Bias

The clearest weakness I found is **poor service for underrepresented moods and genres.** Many categories appear on only one song in the catalog (for example "sad" and "metal" each appear once). Because mood is my highest-weighted feature (3.0), a user who asks for a rare mood gets that single matching song forced to the top of the list even when every other preference disagrees — in my adversarial test, a "metal + sad + high energy" user was handed a slow, low-energy blues song first, purely because it was the only "sad" track. This is a fairness problem: users with mainstream tastes (pop/happy, lofi/chill) get rich, well-matched lists, while users with rare tastes get near-random results dominated by one track.

Two related limitations:

- **Filter bubble.** As a content-based system it only recommends songs similar to what the user already states they like, so it can never help a listener discover a genre or mood outside their stated profile.
- **No understanding of content.** It scores tags and numbers only — it cannot hear the audio, read lyrics, or account for language, artist, or era. It also has no notion of other users' behavior (no collaborative filtering).

**Why "Gym Hero" keeps showing up for a Happy Pop fan (plain language):** Gym Hero is tagged `pop` with very high energy. A "happy pop, high energy" listener matches its genre and its energy, so it collects points on two of the three things they asked for — even though its mood is "intense," not "happy." The system has no idea that an intense gym anthem *feels* different from a cheerful pop song; it only sees that the labels and numbers line up, so it keeps ranking it near the top.

---

## 7. Evaluation

I tested the recommender with four profiles by running `python -m src.main`, three "normal" tastes and one deliberately conflicting ("adversarial") profile.

### Profiles tested (top 5 each)

**High-Energy Pop** — `genre=pop, mood=happy, energy=0.9`
```
1. Sunrise City by Neon Echo  (Score: 6.84)  — mood happy +3.0; genre pop +2.0; energy 0.82 near 0.9 +1.84
2. Rooftop Lights by Indigo Parade  (Score: 4.72)  — mood happy +3.0; energy 0.76 near 0.9 +1.72
3. Gym Hero by Max Pulse  (Score: 3.94)  — genre pop +2.0; energy 0.93 near 0.9 +1.94
4. Storm Runner by Voltline  (Score: 1.98)  — energy 0.91 near 0.9 +1.98
5. Neon Pulse by Circuit Bloom  (Score: 1.90)  — energy 0.95 near 0.9 +1.90
```

**Chill Lofi** — `genre=lofi, mood=chill, energy=0.35, likes_acoustic=True`
```
1. Library Rain by Paper Lanterns  (Score: 8.00)  — mood chill +3.0; genre lofi +2.0; energy +2.00; acoustic +1.0
2. Midnight Coding by LoRoom  (Score: 7.86)  — mood chill +3.0; genre lofi +2.0; energy +1.86; acoustic +1.0
3. Spacewalk Thoughts by Orbit Bloom  (Score: 5.86)  — mood chill +3.0; energy +1.86; acoustic +1.0
4. Focus Flow by LoRoom  (Score: 4.90)  — genre lofi +2.0; energy +1.90; acoustic +1.0
5. Coffee Shop Stories by Slow Stereo  (Score: 2.96)  — energy +1.96; acoustic +1.0
```

**Deep Intense Rock** — `genre=rock, mood=intense, energy=0.9`
```
1. Storm Runner by Voltline  (Score: 6.98)  — mood intense +3.0; genre rock +2.0; energy +1.98
2. Gym Hero by Max Pulse  (Score: 4.94)  — mood intense +3.0; energy +1.94
3. Neon Pulse by Circuit Bloom  (Score: 1.90)  — energy +1.90
4. Iron Verdict by Ashfall  (Score: 1.84)  — energy +1.84
5. Sunrise City by Neon Echo  (Score: 1.84)  — energy +1.84
```

**Adversarial: Sad but High-Energy** — `genre=metal, mood=sad, energy=0.9`
```
1. Rainy Platform by Blue Meridian  (Score: 3.96)  — mood sad +3.0; energy 0.38 near 0.9 +0.96
2. Iron Verdict by Ashfall  (Score: 3.84)  — genre metal +2.0; energy 0.98 near 0.9 +1.84
3. Storm Runner by Voltline  (Score: 1.98)  — energy +1.98
4. Gym Hero by Max Pulse  (Score: 1.94)  — energy +1.94
5. Neon Pulse by Circuit Bloom  (Score: 1.90)  — energy +1.90
```

### What surprised me / profile comparisons

- **High-Energy Pop vs. Chill Lofi:** These are near-opposites and the outputs prove
  it — Pop returns bright, high-energy tracks (Sunrise City, energy 0.82) while Lofi
  returns quiet, acoustic ones (Library Rain, energy 0.35). The `likes_acoustic` flag
  on the Lofi profile pushed acoustic songs up, exactly as intended. This is the
  system working correctly.
- **Deep Intense Rock vs. High-Energy Pop:** Both want high energy (0.9), so their
  lower ranks overlap (Gym Hero, Neon Pulse, Storm Runner appear in both). The
  *difference* comes entirely from genre and mood — Rock's #1 is Storm Runner
  (rock/intense), Pop's #1 is Sunrise City (pop/happy). This shows energy alone
  doesn't decide the winner; the categorical matches break the tie.
- **Adversarial profile — the big surprise:** Asking for *metal + sad + high energy*
  returned a slow, sad **blues** song first, not metal. Because mood is weighted
  highest (3.0), the one "sad" track outranked the genre-matching metal track even
  though its energy (0.38) was the opposite of what was requested. This is the
  clearest evidence that, under conflict, my highest-weighted feature dominates.

### Experiment: weight shift (energy ×2, genre ÷2)

I temporarily set energy weight to 4.0 and genre to 1.0. The **#1 pick for every
profile stayed the same** (mood still led), but mid-list rankings (positions 3–5)
became energy-driven and genre matches barely mattered. Takeaway: the results got
*different*, not obviously *more accurate* — and mood is the feature that truly
controls the top result.

---

## 8. Future Work  

- **Bigger, more balanced catalog** so every genre and mood has several songs — this
  alone would fix most of the "rare taste gets one random song" problem.
- **Handle conflicting preferences** by warning the user (or lowering scores) when no
  song matches on multiple features, instead of silently forcing a single weak match.
- **Add more features** to the score, such as valence (musical positivity),
  danceability, or tempo, so it can tell apart songs that currently look identical.
- **Encourage diversity** in the top results — e.g., avoid returning three songs by
  the same artist or nearly identical tracks, so the list feels less repetitive.
- **Try collaborative filtering** — bring in (simulated) data about what similar
  listeners enjoyed, so the system can suggest songs *outside* the user's stated
  profile and escape the filter bubble.

---

## 9. Personal Reflection  

> _Draft in my own words — edit freely so it sounds like me._

**Biggest learning moment.** Building VibeMatch showed me that a recommender isn't
magic — it's just a scoring rule plus a sort. The "intelligence" lives entirely in
which features I chose and how much weight I gave each one. The clearest moment was
the adversarial test, where asking for high-energy metal returned a slow sad song,
simply because I had made mood the heaviest feature. That made the trade-offs feel
real: every weight I pick is a value judgment about what matters in music.

**How AI tools helped, and when I double-checked them.** The AI assistant was useful
for explaining concepts (like why energy should reward *closeness* instead of just
high values), scaffolding functions, and generating extra songs and test profiles
quickly. But I had to stay in control of the logic. I double-checked the scoring math
by hand on a couple of songs to make sure the totals were right, I verified the
recommendations against my own intuition, and I caught a real bug where the starter
`main.py` imported the module the wrong way — running the tests and the app was how I
confirmed things actually worked instead of just trusting the generated code.

**What surprised me.** It surprised me how a handful of simple `if` checks and one
subtraction can produce output that genuinely "feels" like a recommendation. There's
no deep learning here, yet the ranked, explained list looks a lot like what a real
app shows. It changed how I think about apps like Spotify — when a recommendation
feels "off," it's probably not broken, it's just optimizing for something different
than I expected, and it can only suggest from the data and patterns it already has.

**What I'd try next.** I'd add collaborative filtering so the system could recommend
songs *outside* my stated profile, grow the catalog so every genre and mood has
several songs, and add more features (like valence or danceability) so it can tell
apart songs that currently look identical.
