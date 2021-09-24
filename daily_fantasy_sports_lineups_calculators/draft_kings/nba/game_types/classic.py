from dataclasses import dataclass

from basketball_reference_web_scraper import client
from daily_fantasy_sports_models.draft_kings.nba.models.core.player import Player
from daily_fantasy_sports_scoring_calculators.draft_kings.nba.scoring.calculators.game_types.classic import \
    points_calculator
from daily_fantasy_sports_scoring_calculators.draft_kings.nba.statistics.models import Statistics


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class PlayerStatistics:
    player: Player
    statistics: Statistics


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class PlayerScore:
    player: Player
    score: int


def calculate_scores_for_date(date):
    box_scores = client.player_box_scores(
        day=21,
        month=4,
        year=2021
    )
    player_statistics = [
        PlayerStatistics(
            player=Player(
                id=box_score["player_id"],
                name=box_score["name"]
            ),
            statistics=Statistics(
                points_scored=box_score["points_scored"],
                three_pointers_made=box_score["made_three_pointers"],
                assists=box_score["assists"],
                rebounds=box_score["rebounds"],
                steals=box_score["steals"],
                blocks=box_score["blocks"],
                turnovers=box_score["turnovers"]
            )
        ) for box_score in box_scores
    ]

    player_scores = [
        PlayerScore(
            player=player_statistic.player,
            score=points_calculator.calculate_points(value=player_statistic.statistics)
        ) for player_statistic in player_statistics
    ]
    # get all player box scores for date (basketball reference, for example)
    # Construct player + statistics from player box scores
    # Use scoring calculators to calculate player scores based on the statistics
    # Create concept of a Candidate Lineup where not all positions need to be filled
    # However, each filled position must be valid
    # Candidate Lineups must be less than 50,000 in salary
    # Build the best candidate lineups using the knapsack problem solution
    # Candidate lineups must eventually be valid Lineups
    raise NotImplementedError("not implemented")
