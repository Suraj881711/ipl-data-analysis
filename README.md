# 🏏 IPL Data Analysis (2008–2024)

An end-to-end data analysis of the Indian Premier League — every match and
every ball from the first season in 2008 to 2024 — with a Jupyter notebook
full of charts and findings, plus a Flask dashboard that computes the same
statistics live from the CSV files.

> This project replaces an earlier version from my resume whose files were
> lost; it has been rebuilt from scratch on the full 2008–2024 dataset.

## Dataset

**IPL Complete Dataset (2008–2024)** by Patrick Bhardwaj on Kaggle
(data source: [Cricsheet](https://cricsheet.org)).

- Direct download (no login needed):
  `https://www.kaggle.com/api/v1/datasets/download/patrickb1912/ipl-complete-dataset-20082020`
- Kaggle page: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020

| File | Rows | What it is |
|---|---|---|
| `matches.csv` | 1,095 | One row per match: season, city, date, teams, toss, winner, win margin, player of the match, venue |
| `deliveries.csv` | 260,920 | One row per ball: batter, bowler, runs, extras, wickets — 260,759 rows are innings 1 & 2 (the rest are super overs) |

**Cleaning applied (in both the notebook and the app):**
season labels normalised (`2007/08` → `2008`, `2009/10` → `2010`,
`2020/21` → `2020`) and renamed franchises merged — Delhi Daredevils →
Delhi Capitals, Kings XI Punjab → Punjab Kings, Royal Challengers
Bangalore → Royal Challengers Bengaluru, Rising Pune Supergiant → Rising
Pune Supergiants. Wickets credited to bowlers exclude run outs.

## Key findings (all computed from the data in this repo)

1. **Mumbai Indians are the most successful team with 144 wins**, just ahead
   of Chennai Super Kings (138 wins), who actually have the better win
   rate — 58.0% vs MI's 55.2%.
2. **The toss is (almost) a coin flip.** The toss winner went on to win only
   **50.8%** of the 1,090 decided matches. But the decision matters: teams
   that chose to **field first won 53.9%** of the time vs **45.4%** for teams
   that chose to bat — which is why captains chose to field in 64.3% of matches.
3. **Virat Kohli is the highest run scorer in IPL history in this dataset —
   8,004 runs** (strike rate 128.43). The fastest scorer with 500+ balls
   faced is Andre Russell at a strike rate of **164.29**.
4. **Yuzvendra Chahal is the top wicket taker with 205 wickets**, ahead of
   Piyush Chawla (192) and Dwayne Bravo (183).
5. **AB de Villiers won the most Player of the Match awards — 25**, followed
   by Chris Gayle (22).
6. **The average first-innings score is 165.5 runs.** Chasing is slightly
   more common than defending: 578 matches were won by wickets vs 498 won by
   runs, and a typical successful defence is by a median of just 22 runs.
7. Recent Orange/Purple Cap winners from the data: **2024 — Virat Kohli
   (741 runs) and Harshal Patel (24 wickets)**; 2023 — Shubman Gill (890)
   and Mohammed Shami (28); 2022 — Jos Buttler (863) and Yuzvendra Chahal (27).

## What's inside

- **`ipl_analysis.ipynb`** — the full analysis notebook with markdown
  sections and charts: matches per season, most successful teams, toss
  analysis, Player of the Match leaders, venue analysis (incl. average
  first-innings scores), winning-margin distributions, season-wise team
  performance, career batting/bowling records, strike-rate leaders, and
  Orange/Purple Cap tables for the last three seasons. The notebook is
  saved **executed** — all outputs are in the file.
- **`app.py`** — Flask dashboard: summary cards (matches, seasons, teams,
  venues, toss edge), wins-by-team table + chart, matches-per-season chart,
  top players, toss analysis, and ball-by-ball batting/bowling leaderboards.
  Charts are rendered with matplotlib; `/health` returns `{"status": "ok"}`.
  If `matches.csv` is missing, the home page shows a friendly error with
  instructions instead of crashing.
- **`ipl_stats.py`** — the shared statistics module used by both the app
  and the tests, so the dashboard and the tests can never disagree.
- **`test_app.py`** — pytest suite (Flask test client). Expected values are
  computed from the CSVs inside the tests — no statistic is hardcoded.

## Tech stack

Python · pandas · matplotlib · seaborn · Flask · pytest

## How to run

```bash
pip install -r requirements.txt

# Dashboard
python app.py          # open http://127.0.0.1:5000

# Notebook
jupyter notebook ipl_analysis.ipynb   # or open it on GitHub — outputs are saved

# Tests
pytest test_app.py
```

## Files

| File | Purpose |
|---|---|
| `ipl_analysis.ipynb` | Analysis notebook (executed, with charts + findings) |
| `app.py` | Flask dashboard |
| `ipl_stats.py` | Shared statistics helpers (data loading + all computations) |
| `templates/index.html` | Dashboard page |
| `templates/error.html` | Friendly "dataset missing" page |
| `test_app.py` | pytest suite |
| `matches.csv` | Match-level dataset (1,095 rows) |
| `deliveries.csv` | Ball-by-ball dataset (260,920 rows) |
| `requirements.txt` | flask, pandas, matplotlib, seaborn |

## Author

**Suraj Dhakad** — Data Science Intern @ GRRAS Solutions, Jaipur ·
B.Tech CSE (AI), Chartered Institute of Technology (2023–2027) ·
GitHub: [Suraj881711](https://github.com/Suraj881711)
