# Podcast SpeakerAgent

Shows and stages: SpeakerAgent research cycles, fit scoring with an episode angle, pitches, follow-up on day 4 and day 10, and attribution for every appearance.

| | |
|---|---|
| Engine | codex; falls back to claude |
| Tier | not a partner tier |
| Channels | email, forms |
| Message types | podcast_pitch, podcast_follow_up |

## What it is built from

Adapted from the Speaker Agent pack of the owner's self-hosted agent app, where it already runs: its charter and three skills (podcast research, pitch writing, booking follow-up) became [PROCESS.md](PROCESS.md), and its runtime is in `runtime/`, unchanged.

Also in the `revenue-os-max` kit (the product's base, in the same factory), for a pack that already carries them:

- Roles: `roles/speaker.md`
- Skills: `speakeragent`, `speakeragent-podcasts`, `speakeragent-pitches`, `show-rss-research`, `charm-podcast-pitch`, `podcast-follow-up-and-attribution`
- Worker jobs: `show-research`, `show-score`

## Files here

| File | What |
|---|---|
| [PROCESS.md](PROCESS.md) | The process: what changed in the move to a Grok bot, the pace, the fifteen steps, the rules and whose each one is |
| [speaker.example.json](speaker.example.json) | One business's settings: the speaker, topics and approved claims, leave-outs, sources and search words, the daily pace, the route order, follow-up days, attribution |
| [speaker.py](speaker.py) | The whole day in one run (`day`): find shows (Apple's search, free; Listen Notes with a key), score them on Codex, read sites for an address, accept the best shows that publish one, draft a pitch for each on Codex. Also a follow-up, track every show to a booking, report against the daily pace, carry an existing SpeakerAgent persona and cases over |
| [prompts/](prompts/) | `show-fit.md` (the four judgments), `pitch.md` (three parts, every claim with its support), `follow-up.md` |
| [runtime/](runtime/) | From the source pack, unchanged: `research.py` (scorer, case validator), `speaker_cases.py` (case repair), the case contract, the scoring anchors, example files with made-up values |
| [LISTEN-NOTES.md](LISTEN-NOTES.md) | Listen Notes as a second source of shows: built over its API with a key, switched off in the example; the plans, the requests a day, its terms, what is the owner's |
| [STATUS.md](STATUS.md) | Where the function stands and what the owner still needs to say |
