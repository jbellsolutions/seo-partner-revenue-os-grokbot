# Job: list

Who belongs on which agent's list.

## Read first
- `context/owner.md` (missing: put "practice" at the top of the daily file and use made-up people in `data/practice.csv` only), `repo/playbook/PATH.md` (what makes a fit), `repo/playbook/FUNCTIONS.md`.
- `python3 repo/tools/team.py inbox cold-email`, `python3 repo/tools/people.py stats --days 7`.

## Do
1. **The owner's own people first.** For every file in `data/contacts/` not yet in `state/imported.txt`: `people.py import <file> --source "<what it is>"`, then add its name to that file.
2. **Score and place** up to 25 people with no fit or no lane: `people.py fit <id> <0-5> "<reason>"`, then `people.py lane <id> <role>`: dream-100 for the few where one yes changes everything; dream-500 for a strong fit; partners for someone whose audience is the buyers; cold-email for the rest of the fits. 0 is not a fit: `people.py stage <id> later "not a fit"`. Use what the list says and their public website. No paid data, nothing guessed.
3. **Orders** in your inbox: fill from the list first, then public pages (member directories, association boards, event speakers, community leaders), up to ten new people a day, each with the page in `--why`.
4. `team.py taken <file>` for each order filled.

## Write
`daily/<today>/list.md`: added, scored and placed by lane (counts and ids), orders filled and open.
