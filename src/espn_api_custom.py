import espn_api.hockey
from espn_api.hockey.constant import ACTIVITY_MAP, POSITION_MAP
import json
from espn_api.hockey.player import Player


class League(espn_api.hockey.League):
    def free_agents(self, week: int = None, size: int = 10000, position: str = None, position_id: int = None, players_filter: list = []) \
            -> list[espn_api.hockey.Player]:
        """
        Returns a List of players, based on filters
        Should only be used with most recent season
        :param list players_filter: allows to narrow down returned players. [] = everybody; ["FREEAGENT", "WAIVERS"]
        """
        if self.year < 2019:
            raise Exception('Cant use free agents before 2019')
        if not week:
            week = self.current_week

        slot_filter = []
        if position and position in POSITION_MAP:
            slot_filter = [POSITION_MAP[position]]
        if position_id:
            slot_filter.append(position_id)

        params = {
            'view': 'kona_player_info',
            'scoringPeriodId': week,
        }

        filters = {
            "players": {"filterStatus": {"value": players_filter}, "filterSlotIds": {"value": slot_filter},
                        "limit": size, "sortPercOwned": {"sortPriority": 1, "sortAsc": False},
                        "sortDraftRanks": {"sortPriority": 100, "sortAsc": True, "value": "STANDARD"}}}
        headers = {'x-fantasy-filter': json.dumps(filters)}

        data = self.espn_request.league_get(params=params, headers=headers)
        players = data['players']

        free_agents = [Player(player) for player in players]
        return free_agents
