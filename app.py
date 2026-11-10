"""IPL Data Analysis — Flask dashboard.

Reads matches.csv (and deliveries.csv when present) from the project folder
and renders summary cards, team/season/player tables and matplotlib charts.

Run:  pip install -r requirements.txt && python app.py
Then open http://127.0.0.1:5000
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template

import ipl_stats as stats

app = Flask(__name__)
CHART_DIR = Path(__file__).resolve().parent / "static" / "charts"


def _save_bar(series, filename, title, xlabel, horizontal=True, color="#1f77b4"):
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.6))
    if horizontal:
        series.sort_values().plot(kind="barh", ax=ax, color=color)
        ax.set_xlabel(xlabel)
    else:
        series.plot(kind="bar", ax=ax, color=color)
        ax.set_ylabel(xlabel)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=110)
    plt.close(fig)


def build_charts():
    _save_bar(stats.wins_by_team()["wins"], "wins_by_team.png",
              "Wins by team (all seasons)", "Wins", color="#2ca02c")
    _save_bar(stats.matches_per_season(), "matches_per_season.png",
              "Matches per season", "Matches", horizontal=False, color="#ff7f0e")
    _save_bar(stats.top_players(), "top_players.png",
              "Top 10 Player of the Match awards", "Awards", color="#d62728")
    leaders = stats.batting_leaders()
    if leaders is not None:
        _save_bar(leaders["runs"], "top_scorers.png",
                  "Top 10 run scorers (all seasons)", "Runs", color="#9467bd")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/")
def home():
    if not stats.MATCHES_PATH.exists():
        return render_template("error.html"), 500
    build_charts()
    toss = stats.toss_stats()
    return render_template(
        "index.html",
        summary=stats.summary(),
        wins=stats.wins_by_team(),
        season_counts=stats.matches_per_season(),
        players=stats.top_players(),
        toss=toss,
        batting=stats.batting_leaders(),
        bowling=stats.bowling_leaders(),
        has_deliveries=stats.DELIVERIES_PATH.exists(),
    )


if __name__ == "__main__":
    app.run(debug=True)
