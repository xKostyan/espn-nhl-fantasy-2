# Copilot repo instructions

This repository includes preloaded agent instructions and repository analysis for Copilot CLI.

Files to load on agent start:
- .github/instructions/repo-insights.instructions.md  — primary repo analysis and module summaries

Purpose for Copilot agents:
- Use the above file(s) as authoritative context about project purpose, runtime layout, and module responsibilities when making suggestions, code changes, or running agents.

Notes:
- Do NOT attempt to read or commit `espn-data/*/auth.json` (contains secrets).
- If more context is needed, read src/*.py and espn-data layout referenced in repo-insights.instructions.md.