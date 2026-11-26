# Job: plan

Each agent's work for today.

## Read first
- `context/owner.md` (goal), yesterday's `daily/<date>/*.md`, `repo/playbook/FUNCTIONS.md`.
- `python3 repo/tools/people.py stats --days 7`, `people.py due`, `python3 repo/tools/team.py inbox lead`, `python3 repo/guards/scripts/beat.py status`.
- `requests/owner/` (oldest first), `context/routines-on.md`.

## Do
1. Pick the one thing most likely to move the goal today, and the agent it belongs to.
2. For each agent whose routine runs today, only when there is something particular to do: `python3 repo/tools/team.py give <role> "<one or two sentences>" --from lead`. An agent with nothing particular does its usual job.
3. Two agents on one person: `people.py lane <id> <role>` gives the person to one.
4. An agent silent past its schedule, or a draft older than three days: one line for the owner in the daily file.
5. Mark each inbox item you handled: `team.py taken <file>`.

## Write
`daily/<today>/plan.md`, under 150 words: the one thing, one line per agent given work, what waits on the owner.
