from dataclasses import dataclass
from typing import Set

from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Position as BasketballReferencePosition
from daily_fantasy_sports_models.draft_kings.nba.models.contests.salary_cap.classic.lineup import PlayerPoolPlayer
from daily_fantasy_sports_models.draft_kings.nba.models.core.player import Player
from daily_fantasy_sports_models.draft_kings.nba.models.core.position import Position as DraftKingsPosition
from daily_fantasy_sports_scoring_calculators.draft_kings.nba.scoring.calculators.game_types.classic import \
    points_calculator
from daily_fantasy_sports_scoring_calculators.draft_kings.nba.statistics.models import Statistics

draft_kings_positions_by_basketball_reference_positions = {
    BasketballReferencePosition.POINT_GUARD: DraftKingsPosition.POINT_GUARD,
    BasketballReferencePosition.SHOOTING_GUARD: DraftKingsPosition.SHOOTING_GUARD,
    BasketballReferencePosition.SMALL_FORWARD: DraftKingsPosition.SMALL_FORWARD,
    BasketballReferencePosition.POWER_FORWARD: DraftKingsPosition.POWER_FORWARD,
    BasketballReferencePosition.CENTER: DraftKingsPosition.CENTER
}


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


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class ScoringPlayerPoolPlayer:
    player: PlayerPoolPlayer
    score: int


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=True)
class PositionPlayerScore:
    player_score: PlayerScore
    positions: Set[DraftKingsPosition]


def calculate_scores_for_date():
    box_scores = client.player_box_scores(
        day=21,
        month=4,
        year=2021
    )
    player_statistics = [
        PlayerStatistics(
            player=Player(
                id=box_score["slug"],
                name=box_score["name"]
            ),
            statistics=Statistics(
                points_scored=(1 * box_score["made_free_throws"] + (2 * (box_score["made_field_goals"] - box_score[
                    "made_three_point_field_goals"])) + (3 * box_score["made_three_point_field_goals"])),
                three_pointers_made=box_score["made_three_point_field_goals"],
                assists=box_score["assists"],
                rebounds=(box_score["offensive_rebounds"] + box_score["defensive_rebounds"]),
                steals=box_score["steals"],
                blocks=box_score["blocks"],
                turnovers=box_score["turnovers"]
            )
        ) for box_score in box_scores
    ]

    player_scores = {
        player_statistic.player.id:
            PlayerScore(
                player=player_statistic.player,
                score=points_calculator.calculate_points(value=player_statistic.statistics)
            ) for player_statistic in player_statistics
    }

    positions_by_id = {
        total["slug"]: {
            "name": total["name"],
            "positions": total["positions"]
        }
        for total in client.players_season_totals(season_end_year=2021)
    }

    player_pool = [
        ScoringPlayerPoolPlayer(
            player=PlayerPoolPlayer(
                player=player_scores.get(player_id).player,
                game_id="1",
                positions=set(
                    map(
                        lambda position: draft_kings_positions_by_basketball_reference_positions.get(position),
                        player_details["positions"]
                    )
                ),
                salary=0
            ),
            score=player_scores.get(player_id).score
        )
        for player_id, player_details in positions_by_id.items() if player_id in player_scores
    ]

    print([
        player_id
        for player_id, player_details in positions_by_id.items() if player_id not in player_scores
    ])

    print(player_pool[0])

    points_ordered_player_pool = sorted(
        player_pool,
        key=lambda player: player.score,
        reverse=True
    )

    print(
        [
            PositionPlayerScore(
                player_score=PlayerScore(
                    player=player_pool.player,
                    score=player_pool.score
                ),
                positions=player_pool.player.positions
            )
            for player_pool in points_ordered_player_pool
        ]
    )

    # get all player box scores for date (basketball reference, for example)
    # Construct player + statistics from player box scores
    # Use scoring calculators to calculate player scores based on the statistics
    # Create concept of a Candidate Lineup where not all positions need to be filled
    # However, each filled position must be valid
    # Candidate Lineups must be less than 50,000 in salary
    # Build the best candidate lineups using the knapsack problem solution
    # Candidate lineups must eventually be valid Lineups


# Select player X at position Y with salary Z
# Sub-problem where need to fill remaining positions with 50k - Z salary

# Select 1 item in each group such that the total weight is less than or equal to limit
# and maximizes total value across all groups
# Value[pg_index][sg_index][sf_index][pf_index][c_index][g_index][f_index][utility_index]
# Value[pg_index][sg_index] represents value from player at pg_index and player at sg_index
# If only 1 group, get max value of all players in group where cost < max cost
# If two groups, populate array of first group where array[cost] = maximum value of any player at the cost
# then in second group, iterate over all players and fill array[cost] = maximum value of player with cost of player +
# value at first group array at remaining cost
# For each position, array with 500 indices. The value at each index are the players that maximizes the value for a
# given cost equal to the index
def calculate_lineups(player_scores: Set[PositionPlayerScore]):


if __name__ == "__main__":
    calculate_scores_for_date()
