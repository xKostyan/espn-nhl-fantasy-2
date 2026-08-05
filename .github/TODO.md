# Draft Assistant — TODO

Stack: 

Purpose: Replace Excel workflow with a snappy multi-window desktop app for draft helper. Persist available/not-available flags and "my team" using SQLite. UI must be fast (virtualized tables, sparklines), multi-monitor (separate windows), and sortable by projected avg fantasy points.

Features (high level):

- Screen 1: Players table (tabs: F, D, G)
  - Columns: <available> <name> <points -4y> <points -3y> <points -2y> <points -1y> <sparkline 4y> <projected avg pts/game upcoming>
  - For G: use avg pts/game for last 4 years instead of totals
  - Search-as-you-type within current tab; select centers/highlights row
  - Click name to highlight (alternate to search)
  - Checkbox in first column for available/not available; unavailable rows are grayed out but remain visible
  - Table sorted by projected avg fantasy points by default

- Screen 2: Player detail
  - Shows charts and numbers for selected player; placeholder shows name
  - Button: "Add to my team"

- Screen 3: My team
  - Shows added players grouped by F, D, G
  - Enforce league roster limits (from league rules)
  - Persistent storage for available flags and my team
  - Future: show projected totals, goalie gamestarts, etc.

Non-functional requirements:
- Snappy UI (virtualized lists, minimal re-renders)
- Sparklines in table rows
- Multi-window support (3 resizable windows)
- SQLite for persistence (local file in app data or project dir)
- Commit between each feature implementation (git commits required)
- Keep an iterative TODO table below for tracking

TODO table:

| id | task | status | notes |
|---|---|---|---|
| create-todo | Create this TODO.md and record choices | pending |  |
| screen1-table | Implement Screen 1 table UI with virtualization & sparklines | pending | single-tab first, then tabs |
| search | Implement search-as-you-type and row centering | pending | keyboard + mouse selection |
| screen2 | Implement Screen 2 player detail placeholder + "Add to my team" | pending | basic charts placeholder |
| screen3 | Implement My Team with roster enforcement and persistence | pending | store in SQLite |
| persist | Implement save/load of available flags and team | pending | migrations and DB schema |
| multiwindow | Support separate OS windows for each screen | pending | draggable/resizable |
| tests | Add basic integration tests for key flows | pending | minimal smoke tests |

Notes:
- Store any additional user instructions and new feature ideas in this file under "Changelog".
- Commits must include Co-authored-by trailer per repo policy when making git commits.
