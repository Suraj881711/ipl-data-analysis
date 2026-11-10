"""Tests for the IPL dashboard.

Expected values are computed from the CSVs inside the tests themselves —
no statistic is hardcoded.
"""
from pathlib import Path

import pandas as pd
import pytest

import ipl_stats as stats
from app import app

BASE = Path(__file__).resolve().parent
SEASON_FIX = {"2007/08": "2008", "2009/10": "2010", "2020/21": "2020"}
TEAM_FIX = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}


@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="module")
def raw_matches():
    df = pd.read_csv(BASE / "matches.csv")
    df["season"] = df["season"].astype(str).replace(SEASON_FIX)
    for col in ("team1", "team2", "winner", "toss_winner"):
        df[col] = df[col].replace(TEAM_FIX)
    return df


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_home_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"IPL Data Analysis" in resp.data


def test_total_matches_matches_csv(client, raw_matches):
    assert stats.summary()["total_matches"] == len(raw_matches)
    resp = client.get("/")
    assert str(len(raw_matches)).encode() in resp.data


def test_seasons_match_csv(raw_matches):
    s = stats.summary()
    assert s["seasons"] == raw_matches["season"].nunique()
    assert s["season_range"] == f"{raw_matches['season'].min()}–{raw_matches['season'].max()}"


def test_top_team_by_wins(raw_matches):
    expected = raw_matches["winner"].value_counts()
    table = stats.wins_by_team()
    assert table.index[0] == expected.index[0]
    assert table["wins"].iloc[0] == int(expected.iloc[0])
    # wins can never exceed matches played
    assert (table["wins"] <= table["played"]).all()


def test_matches_per_season_sums_to_total(raw_matches):
    per_season = stats.matches_per_season()
    assert int(per_season.sum()) == len(raw_matches)
    assert set(per_season.index) == set(raw_matches["season"].unique())


def test_toss_percentage_is_sane(raw_matches):
    decided = raw_matches[raw_matches["winner"].notna()]
    expected = round(float((decided["toss_winner"] == decided["winner"]).mean() * 100), 1)
    toss = stats.toss_stats()
    assert toss["toss_win_pct"] == expected
    assert 0 < toss["toss_win_pct"] < 100


def test_top_player_matches_csv(raw_matches):
    expected = raw_matches["player_of_match"].value_counts().head(10)
    players = stats.top_players()
    assert players.index[0] == expected.index[0]
    assert int(players.iloc[0]) == int(expected.iloc[0])


def test_batting_leader_matches_deliveries():
    path = BASE / "deliveries.csv"
    if not path.exists():
        pytest.skip("deliveries.csv not present")
    d = pd.read_csv(path, usecols=["inning", "batter", "batsman_runs"])
    d = d[d["inning"].isin([1, 2])]
    expected = d.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False)
    leaders = stats.batting_leaders()
    assert leaders.index[0] == expected.index[0]
    assert int(leaders["runs"].iloc[0]) == int(expected.iloc[0])
