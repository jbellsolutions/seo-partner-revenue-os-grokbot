# Job: report

The night's count and tomorrow's one thing.

## Run and read
- `python3 repo/tools/people.py stats --days 1`, `people.py stats --days 7`, `people.py due`.
- `python3 repo/tools/job.py audit --days 1`, `python3 repo/convlog/gate.py day`, `python3 repo/guards/scripts/beat.py status`.
- `context/owner.md` (goal), today's `daily/<today>/*.md`, `requests/owner/` (oldest first), `context/routines-on.md`, `context/standing-approvals.md`.

## Write `daily/<today>/report.md`, under 220 words

```
<name from owner.md>, <date>
Goal: <goal line>. Joined: N<of seats, when owner.md has seats>.
Today: N messages sent, N replies, N calls booked, N held, N invited in, N joined. Ready and waiting on you: N.
Week: the same numbers.
By agent: one short line for each that did something today.
Waiting on you: the three oldest, one line each, with the file
Tomorrow: the one thing most likely to move the goal
Engines: Claude Code N jobs, Codex N, the bots themselves N
```

Sent means an app confirmed it. No owner.md: the first line of "Waiting on you" is to fill it in. Nothing goes out until a type is approved and its routine is on: say which switch is next, once.

## Also write
`vault/Daily/<today>.md`: the report. Fridays, one line in `vault/Decisions.md`: which agent brought the most replies and calls, and what to do more of.
