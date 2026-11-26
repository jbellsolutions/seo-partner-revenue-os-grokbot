# Job: dream-100

The hundred people where one yes changes everything. Quality over number; you only draft.

## Read first
- `context/owner.md`, `repo/playbook/FUNCTIONS.md` (dream-100), `VOICE.md`, `PATH.md`, `ITEM.md`; `repo/agents/dream-100/PROCESS.md` and its `prompts/`.
- `python3 repo/tools/team.py inbox dream-100`, any note for this run, `python3 repo/tools/people.py due --lane dream-100`, `people.py list --lane dream-100 --stage listed`.

## Do
1. **People the owner named come first**, then the best fits. Fewer than ten listed at 4 or 5: find up to three new candidates from public pages and `people.py add --name ... --company ... --linkedin ... --source "<page>" --why "<reason>" --lane dream-100`, then `people.py fit`.
2. **Dossier** for the next three without one, in `vault/People/<id>.md`: what they do, who listens to them, what they care about now, the warm path to them, each with its page.
3. **First message** for the next three with a dossier: TYPE `dream100_first_touch`, written for that one person.
4. **Follow-ups due**: TYPE `dream100_follow_up`, each brings something new. Three messages sent: `people.py stage <id> later`.
5. `team.py taken <file>` for each inbox item done.

## Write
`daily/<today>/dream-100.md`: candidates, dossiers, drafts with ids, who was skipped and why.
