# Job: cold-email

Cold email to the people no other agent is working. You only draft; a sending tool sends.

## Read first
- `context/owner.md`, `repo/playbook/FUNCTIONS.md` (cold-email), `VOICE.md`, `ITEM.md`; `repo/agents/cold-email/PROCESS.md` and its `prompts/`.
- `python3 repo/tools/people.py list --lane cold-email --stage listed --limit 25`, any sending numbers in `data/inbox/`.

## Do
1. **Up to ten drafts** for people with an email and fit 3 or more: one true first line, one short reason, one easy question. TYPE `cold_email`.
2. **The file:** `python3 repo/tools/people.py export --type cold_email` writes the CSV a sending tool imports.
3. **Numbers**, when there are any: sent, bounced, replied. A bounce: `people.py stage <id> later "bounced"`.

## Write
`daily/<today>/cold-email.md`: drafts with ids, the export file, the numbers or "?".
