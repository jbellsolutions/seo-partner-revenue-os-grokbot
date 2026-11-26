# Job: members

Keep the people who joined, and let them fill the room.

## Read first
- `context/owner.md`, `people.py list --stage joined`, `data/calls/` notes from sessions, the note for this run.

## Do
1. **A new member:** a welcome in the host's voice (TYPE `member_note`), what happens first, and the owner's checklist for them in `requests/owner/welcome-<id>.md`: payment confirmed, calendar invitation, introduction to the others, the one thing they want this year.
2. **The next session:** `requests/owner/session-<date>.md`, one page: one member's real problem in the middle, one thing that is working shared by each person, one new tool or method, and the closing question "who else belongs here?". With one or two members it is a conversation, and that is fine.
3. **Between sessions:** one useful introduction or answer for each member, as a draft `member_note`.
4. **Who else:** any name a member gave is `people.py add ... --source "introduced by <id>" --why "<what they said>"`.
5. **Proof:** anything a member said worked goes in `vault/wins.md`, with their id and whether they said it may be shared. Nothing is quoted without that.

## Write
`daily/<today>/members.md`: members, welcomes open, the next session, names introduced.
