---
name: claude-code-cli
description: Use for every task. The bot orchestrates; the Claude Code CLI does the work, with the Codex CLI as the second engine. Covers how to hand over a job or any task, how to install and sign in both CLIs, what to do when one does not answer, and how the daily report proves the rule was kept.
---

# The Claude Code CLI: every task goes through it

Every agent on the team is an orchestrator. The owner signs in Claude Code and Codex once, and every task runs on those subscriptions instead of Grok usage.

## Hand over a task

```
python3 repo/tools/job.py run <job>                     a job with a file in repo/jobs/
python3 repo/tools/job.py run <job> --note "<words>"    the same, with what the owner asked for
python3 repo/tools/job.py ask "<any task>"              anything else
python3 repo/tools/job.py list                          the jobs
```

`job.py` starts the job's engine headless (team.json: Claude Code or Codex, the other one if it gives no answer) in the workspace with the job's brief. It reads and writes the workspace's files, searches and reads the public web, and runs the pack's Python scripts. The CLI's last message is printed and saved in `log/jobs/`. Wait for it; a job can take several minutes.

## What is the bot's own

Only what a CLI cannot reach:

- the browser the owner signed in (the mailbox, the calendar, LinkedIn, a member directory): read it, save the text to a file, then hand the job over;
- connected apps: send an item `people.py outbox` allows, and post the report file the job wrote, as it is;
- creating and changing routines;
- talking with the owner, and writing the owner's yes into a switch file.

## When the CLI does not answer

`job.py` exits 3 and says so. Then, and only then, do the job yourself from `repo/jobs/<job>.md` and record it:

```
python3 repo/tools/job.py grok <job> "no CLI answered"
```

Tell the owner once that a CLI needs signing in. Do not say it again until it has answered and failed again.

## Install and sign in

```
npm install -g @anthropic-ai/claude-code
npm install -g @openai/codex
python3 repo/tools/job.py status
```

If `npm` is missing, Claude Code's own installer is `curl -fsSL https://claude.ai/install.sh | bash`.

Sign-in is the owner's. Claude Code: they run `claude setup-token` on their own computer and give the token by hidden prompt; it is saved as `CLAUDE_CODE_OAUTH_TOKEN` in `.secrets/team.env`, where `job.py` reads it. Or they open the bot's terminal, run `claude` and sign in there. Codex: they run `codex login` in the bot's terminal and approve the sign-in it shows. `job.py status` makes one tiny real call to each and says which answer.

## Proof

Every hand-over is one line in `log/engine-<month>.jsonl`. `python3 repo/tools/job.py audit` counts the day's jobs by engine and exits 1 if the bot carried one without a recorded reason. The nightly report prints that count.
