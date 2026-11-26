# Install

The team is ten Grok bots: the lead you talk to, and one for each of the nine Revenue OS functions. You paste one line into one bot; it sets up the rest.

## New install

> Install the SEO Partner Revenue OS team. Download https://github.com/jbellsolutions/seo-partner-revenue-os-grokbot/releases/latest/download/seo-partner-revenue-os.zip, unpack it into /workspace/seo-partner-revenue-os/repo/, run python3 /workspace/seo-partner-revenue-os/repo/tools/install.py and do what it prints, in order. Ask me nothing until it is all done, then send me one message that ends with the checklist. Nothing sends or posts until I say yes.

## Update: the bot that already has an older install

> Update to the SEO Partner Revenue OS team. Download https://github.com/jbellsolutions/seo-partner-revenue-os-grokbot/releases/latest/download/seo-partner-revenue-os.zip, move /workspace/seo-partner-revenue-os/repo/ to /workspace/seo-partner-revenue-os/repo-old/, unpack the download into /workspace/seo-partner-revenue-os/repo/, run python3 /workspace/seo-partner-revenue-os/repo/tools/update.py and do what it prints, in order. You become the lead, and you create the other nine bots. Ask me nothing until it is all done, then send me one message that ends with the checklist. Nothing sends or posts until I say yes.

`update.py` keeps everything in `context/`, `data/`, `requests/` and `.secrets/`, the sign-ins and the CLIs.

**Already have an owner.md?** Attach it to the same message. The lead saves it as `/workspace/seo-partner-revenue-os/context/owner.md`.

## What the lead does

1. Runs the installer (or the update). It asks nothing and can be run again.
2. Sets itself up: memory, the skill, its routines.
3. Creates the other nine bots and gives each its one line. Each sets itself up the same way.
4. Installs the two CLIs if they are missing and runs `job.py status`.
5. Sends the owner one message: each agent and whether it is its own bot, what `job.py status` said, any failed check, then the checklist, starting `NEEDS YOU:`. Then stops.

## What can go wrong, and what to do

| If | Then |
|---|---|
| The download fails | Ask the owner once to attach `seo-partner-revenue-os.zip` from the release, then carry on |
| The lead cannot create a bot | `requests/owner/create-the-team.md` has each name and line for the owner to paste. Until a bot exists the lead runs its job: `team.py solo <role>` |
| A new bot answers "own computer" | It cannot see the team's files, so the lead runs its job: `team.py solo <role>` |
| A CLI does not answer | Carry on. Each job falls to the bot itself and is recorded, until the owner signs it in |
| A check fails | Carry on, and put the failed line in the one message |

## What is on after the install

Every routine runs on **test**: its job runs and makes drafts. A message goes out only when its type says auto and its routine is on, and never to someone who opted out. The owner changes a switch by saying it in any agent's chat.
