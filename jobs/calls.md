# Job: calls

Before and after each conversation.

## Read first
- `data/calls/*.md` from the last three days, `context/owner.md`, `repo/playbook/PATH.md`, `python3 repo/tools/people.py due`.

## Before
For each call today or tomorrow: `requests/owner/brief-<date>-<id>.md`, half a page. Who they are and what they run (public facts with the page), how they came in, what they said so far (`python3 repo/convlog/convlog.py thread "<email>"`), the one thing they would bring to the room, three questions to ask, and what a good end to the call looks like. If it feels like selling, it has gone off track.

## After
For each call with new notes: `people.py stage <id> talked "<one line>"`, then exactly one next step:
- a fit: a personal invitation, TYPE `invitation`, from PATH.md's words plus what they said on the call;
- wants more: a second call, TYPE `reply`;
- not there yet: mentorship, if owner.md has it, TYPE `reply`;
- no: `people.py stage <id> no`.
Files and logging as in `repo/playbook/ITEM.md`. A promise the host made on the call is one line in `requests/owner/promises.md`.

Offered and quiet for three days: one kind "are you in?" note, TYPE `reply`.

## Write
`daily/<today>/calls.md`: calls ahead, calls held, next step for each, promises open.
