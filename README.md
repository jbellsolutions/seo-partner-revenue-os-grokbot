# SEO Partner Revenue OS: GrokBot pack

A Revenue OS team of ten Grok bots: a lead, and one bot for each of the nine functions. The team finds agency and web design owners whose clients need local SEO, makes them referral partners on a monthly commission, answers every reply within minutes, and books the call on the owner's calendar.

**Install or update:** one line each, in [INSTALL.md](INSTALL.md). Version 1.1.0. The pack holds no names, prices or lists: the team takes those from you.

## The team

| Agent | What it does | Thinks with |
|---|---|---|
| **SEO Partner Revenue OS** | The one the owner talks to. Plans each agent's day, keeps the owner's one queue, reports the count | Claude Code |
| **SEO Dream 100** | The hundred people where one yes changes everything: a dossier and one hand-written message each, by email and on socials | Claude Code |
| **SEO Dream 500** | The wider five hundred, in small waves, each with a true first line | Claude Code |
| **SEO Partners** | Partners, collaborators and influencers: people who already have the buyers' attention and could promote | Claude Code |
| **SEO Cold Leads** | The lists every agent orders, and cold email to the rest, ready for the sending tool | Claude Code |
| **SEO Lead Radar** | People already asking in public for what the owner offers. Reads and scores; hands them on | Codex |
| **SEO Content** | Posts and videos worth sharing, in the owner's voice | Claude Code |
| **SEO SpeakerAgent** | Podcasts, events and stages: shows scored, pitches with an angle, follow-up | Codex |
| **SEO AEO and SEO** | Found in search and named by AI answers: the questions buyers ask, and a page that answers each | Codex |
| **SEO Sales** | Every conversation after a reply: answers, calls, invitations, follow-up, and the people list as the CRM | Codex |

Each bot only orchestrates. Its routines hand their jobs to the **Claude Code** and **Codex** CLIs (`tools/job.py`), so the work runs on your own subscriptions and not on Grok usage. The team works through one set of files: one people list where each person has one agent, one queue for you, one log of every draft, send and reply.

## What is in the pack

| | |
|---|---|
| [INSTALL.md](INSTALL.md), [CHECKLIST.md](CHECKLIST.md) | The install line, the update line, everything only you can do |
| [team.json](team.json), [roles/](roles/), [MASTER-PROMPT.md](MASTER-PROMPT.md), `tools/team.py` | The ten agents, each one's memory, its set-up, hand-overs between them |
| [jobs/](jobs/) | What each routine's CLI does |
| [agents/](agents/README.md) | The nine functions: how each works, its prompts and scripts |
| [playbook/](playbook/) | What each function means here, the voice, the path, the blank owner.md |
| [tools/people.py](tools/people.py) | The people list: lanes, stages, what may go out, the export, the invitation page |
| `tools/job.py`, `skills/claude-code-cli/`, `engines/`, `agents.json` | Hands every job to its engine and counts which did it |
| `guards/`, `convlog/`, `linkedin/` | The send switch, the opt-out list, the log, the LinkedIn path |
| `tools/install.py`, `update.py`, `check.py`, `selftest.py` | The installer, the update and the checks |
