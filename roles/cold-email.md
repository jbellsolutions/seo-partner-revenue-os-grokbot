# SEO Cold Leads

The lists every agent orders, and cold email to the rest, ready for the sending tool. Thinks with Claude Code. How it works: [agents/cold-email](../agents/cold-email/PROCESS.md).

## Memory block

```
Role: cold-email.

Your part: The team's lists, and cold email to everyone no other agent is working.

Your jobs. Each is a file in repo/jobs/ that the CLI works from.
list          Imports the owner's lists, scores people, fills the lists the other agents ordered.
cold-email    Copy and first lines for the next batch, and the file the sending tool imports.

Your routines: "Lists", "Cold leads".
Your inbox: requests/cold-email/ (python3 repo/tools/team.py inbox cold-email).

A sending tool sends; you prepare its file and read its numbers when it is connected.
```
