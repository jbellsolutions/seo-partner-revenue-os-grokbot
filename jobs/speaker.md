# Job: speaker

Get the owner on shows and stages. You only draft.

## Read first
- `context/owner.md` (topics, host_bio), `repo/playbook/FUNCTIONS.md` (speaker), `VOICE.md`, `ITEM.md`; `repo/agents/speaker/PROCESS.md` and its `prompts/`.
- `python3 repo/tools/team.py inbox speaker`, `python3 repo/tools/people.py due --lane speaker`, `people.py list --lane speaker`.

## The daily run, for a business that set a daily number

When `context/speaker.json` exists, the day is code and this job is what is left over. The routine has already run:

`BOT_HOME=<workspace> python3 repo/agents/speaker/speaker.py day --settings context/speaker.json`

It finds shows, scores them, reads sites for an address, accepts the best that publish one and writes a pitch for each as an item, TYPE `show_pitch` (`repo/agents/speaker/PROCESS.md`, "The pace"). Then, in this job:

- Skip steps 1 and 2 below.
- Open the shows it queued in `requests/speaker/` that have a guest or booking page, best first, as far as the day allows, and write what you saw into each case.
- After the send steps send an item: `python3 repo/agents/speaker/speaker.py mark --case <the item's PERSON> sent`.
- Follow-ups: `speaker.py due --settings context/speaker.json`, then `speaker.py followup --case <id> --settings context/speaker.json` for each.
- A host's yes: `speaker.py mark --case <id> booked --date <date>`.

To set a business up for it: copy `repo/agents/speaker/speaker.example.json` to `context/speaker.json` and fill the speaker block from `context/owner.md` and the search words from FUNCTIONS.md (speaker); or, where the owner attaches a SpeakerAgent persona file, `speaker.py carry --persona <file> --out context/speaker.json`.

## Do
1. **Find** up to five shows, events or chapters the buyers listen to, active in the last two months: `people.py add --name "<host>" --company "<show>" ... --source "<page>" --why "<recent episode and the angle>" --lane speaker`, then `people.py fit`.
2. **Pitch** up to three at fit 4 or 5: a recent episode, one angle, three things the audience leaves with. TYPE `show_pitch`. A show with a form: the filled answers in `requests/owner/form-<id>.md` with the form's link.
3. **Follow-ups due:** TYPE `show_follow_up`.
4. **Booked or aired:** one line in `requests/owner/appearances.md`, and `team.py give content "<what aired>" --from speaker`.

## Write
`daily/<today>/speaker.md`: shows found, pitches with ids, forms ready, booked.
