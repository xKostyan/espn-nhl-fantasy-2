Repository: espn-nhl-fantasy-2 — quick reference

Purpose
- Harvest ESPN fantasy NHL league data, store per-league sqlite DBs, compute fantasy points, and export CSV/Excel for analysis.

Quick module map
- app-console.py — console UI to init or interact with leagues.
- src/init_league.py — sets up league folder, DB, scoring, saves auth.json.
- src/get_players_draft_data.py — core data fetcher/publisher; uses espn_api and writes tables.
- src/espn_api_custom.py — small extension of espn_api.League.
- src/schemas.py — DB schema + stat name mappings.
- src/player_stats_to_tables_converter.py — builds exportable data and calculates FP.
- dump_data_into_tables.py & csv_to_excel_workbook_with_sparklines.py — CSV/Excel export utilities.

Data directory
- espn-data/<league_id>/ (auth.json, league.db, dumps/)

Quick run
- Initialize: python app-console.py
- Fetch: python src/get_players_draft_data.py --league_id <id>

Security
- auth.json contains espn_s2/sw id. Never commit.

Created by Copilot CLI analysis for repository onboarding.