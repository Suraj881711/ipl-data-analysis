"""Shared statistics helpers for the IPL dashboard app and its tests.

All numbers are computed from matches.csv / deliveries.csv at runtime —
nothing is hardcoded. Season labels are normalised ('2007/08' -> '2008')
and renamed franchises are merged so the dashboard matches the notebook.
"""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MATCHES_PATH = BASE_DIR / "matches.csv"
DELIVERIES_PATH = BASE_DIR / "deliveries.csv"

SEASON_FIX = {"2007/08": "2008", "2009/10": "2010", "2020/21": "2020"}
TEAM_FIX = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}

_cache: dict = {}


def load_matches() -> pd.DataFrame:
    if "matches" not in _cache:
        df = pd.read_csv(MATCHES_PATH)
        df["season"] = df["season"].astype(str).replace(SEASON_FIX)
        for col in ("team1", "team2", "winner", "toss_winner"):
            df[col] = df[col].replace(TEAM_FIX)
        _cache["matches"] = df
    return _cache["matches"]


def load_deliveries() -> pd.DataFrame | None:
    if "deliveries" not in _cache:
        if DELIVERIES_PATH.exists():
            d = pd.read_csv(DELIVERIES_PATH)
            for col in ("batting_team", "bowling_team"):
                d[col] = d[col].replace(TEAM_FIX)
            _cache["deliveries"] = d[d["inning"].isin([1, 2])]
        else:
            _cache["deliveries"] = None
    return _cache["deliveries"]


def summary() -> dict:
    m = load_matches()
    teams = pd.unique(pd.concat([m["team1"], m["team2"]]).dropna())
    return {
        "total_matches": int(len(m)),
        "seasons": int(m["season"].nunique()),
        "season_range": f"{m['season'].min()}–{m['season'].max()}",
        "teams": int(len(teams)),
        "venues": int(m["venue"].nunique()),
        "cities": int(m["city"].nunique()),
    }


def wins_by_team() -> pd.DataFrame:
    m = load_matches()
    decided = m[m["winner"].notna()]
    wins = decided["winner"].value_counts()
    played = pd.concat([m["team1"], m["team2"]]).value_counts()
    table = pd.DataFrame({"played": played, "wins": wins}).fillna(0)
    table["wins"] = table["wins"].astype(int)
    table["win_pct"] = (100 * table["wins"] / table["played"]).round(1)
    return table.sort_values("wins", ascending=False)


def matches_per_season() -> pd.Series:
    return load_matches().groupby("season", sort=True).size()


def top_players() -> pd.Series:
    return load_matches()["player_of_match"].value_counts().head(10)


def toss_stats() -> dict:
    m = load_matches()
    decided = m[m["winner"].notna()].copy()
    decided["toss_won_match"] = decided["toss_winner"] == decided["winner"]
    by_decision = (decided.groupby("toss_decision")["toss_won_match"]
                   .mean().mul(100).round(1))
    decision_share = m["toss_decision"].value_counts(normalize=True).mul(100).round(1)
    return {
        "toss_win_pct": round(float(decided["toss_won_match"].mean() * 100), 1),
        "by_decision": {k: float(v) for k, v in by_decision.items()},
        "decision_share": {k: float(v) for k, v in decision_share.items()},
    }


def batting_leaders() -> pd.DataFrame | None:
    d = load_deliveries()
    if d is None:
        return None
    bat = d.groupby("batter").agg(runs=("batsman_runs", "sum"),
                                  balls=("ball", "count"))
    bat["strike_rate"] = (100 * bat["runs"] / bat["balls"]).round(2)
    return bat.sort_values("runs", ascending=False).head(10)


def bowling_leaders() -> pd.Series | None:
    d = load_deliveries()
    if d is None:
        return None
    wkts = d[(d["is_wicket"] == 1) & (d["dismissal_kind"] != "run out")]
    return wkts.groupby("bowler").size().sort_values(ascending=False).head(10)
