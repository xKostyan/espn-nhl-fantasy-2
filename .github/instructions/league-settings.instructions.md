League rules and draft settings (personal fantasy league)

Purpose
- Documented rules and constraints for the personal NHL fantasy league so Copilot CLI agents auto-load them on start.

General
- Auction draft with a shared salary cap and per-team cap space used to assign player values on draft day.
- Keeper league: each team receives a table from manager with keeper $$ values (based on actual auction price or public ESPN projection adjusted to our cap, whichever is higher).
- Keeper spend limit: teams must spend between $250 and $550 total on keeper players.
- Only one goalie may be kept per team.
- Keeper rules, roster rules, and scoring weights are stored in the league.db (scoring table) created by init_league.py.

Roster composition (active)
- 9 Forwards (F)
- 5 Defensemen (D)
- 2 Skater (Utility; can be F or D)
- 2 Goalies (G)

Bench and shared
- 2 Skater bench slots
- 1 Goalie bench slot
- 1 Shared slot (Skater OR Goalie)

Game limits per season (active appearance limits)
- Forwards: 9 x 84 games
- Defensemen: 5 x 84 games
- Utility: 2 x 84 games
- Goalies: total 140 games across goalie slots

Scoring and storage
- Fantasy points are calculated using league scoring weights provided at initialisation and saved in espn-data/<league_id>/league.db in the scoring table.
- Points accumulate only while a player occupies an active slot.

Waivers and pickup budgets
- Weekly blind-bid waiver pickups using a separate waiver budget.

Notes for agents and developers
- Do NOT commit espn-data/*/auth.json (contains espn_s2 & swid). These are secrets and must remain local.
- init_league.py uses sqlite3.connect to create/initialize the league DB and scoring table; ensure scoring weights schema matches these documented fields.

TODO (user requests)
- Maintain this file to include any in-house rule changes so agents always have up-to-date rules on start.
- Add sample keeper table format and CSV template if desired.
