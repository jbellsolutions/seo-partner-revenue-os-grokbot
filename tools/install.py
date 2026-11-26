#!/usr/bin/env python3
"""Set up the team's workspace. One command, no questions, safe to run again.

    python3 <workspace>/repo/tools/install.py

It makes the folders and the switch files, writes each agent's setup page and the list of bots to create, runs the pack's checks, and prints what the bot does next. It uses no network, installs nothing, asks
nothing and never overwrites a file it wrote before: the owner's answers in context/ survive a second run and a new version.
What it makes is all read from team.json.
"""
import json, os, shutil, subprocess, sys, time, uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import team as T


def main():
    team = T.load()
    ws, agents = T.where(team), team["agents"]
    made, kept = [], []

    def d(rel, mode=None):
        p = os.path.join(ws, *rel.split("/"))
        os.makedirs(p, exist_ok=True)
        if mode:
            os.chmod(p, mode)
        return p

    def w(rel, text, mode=None, fresh=False):
        p = os.path.join(ws, rel)
        if os.path.exists(p) and not fresh:
            kept.append(rel); return
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
        if mode:
            os.chmod(p, mode)
        made.append(rel)

    for x in team["folders"]:
        d(x)
    for a in agents:
        d("requests/" + a["role"])
    for x in team["private_folders"]:
        d(x, 0o700)

    routines = [n for a in agents for n, _, _ in a["routines"]]
    w("context/routines-on.md", "# Routines: on, test or off\n\ntest means the routine runs and only drafts. The owner changes a line by saying it in any agent's chat.\n\n"
      + "".join(f"{n}: test\n" for n in routines) + "".join(s + "\n" for s in team.get("switches", [])))
    rf = os.path.join(ws, "context", "routines-on.md")
    have = open(rf, encoding="utf-8").read()
    miss = [f"{n}: test" for n in routines if not __import__("re").search(rf"(?m)^{__import__('re').escape(n)}\s*:", have)] + \
           [s for s in team.get("switches", []) if not __import__("re").search(rf"(?m)^{__import__('re').escape(s.split(':')[0])}\s*:", have)]
    if miss:
        open(rf, "a", encoding="utf-8").write(("" if have.endswith("\n") else "\n") + "\n".join(miss) + "\n")
        made.append("context/routines-on.md (added: " + ", ".join(m.split(":")[0] for m in miss) + ")")
    w("context/standing-approvals.md", "# Message types the owner has approved\n\nOne line per type: `<type>: auto` with the date and the owner's words. Empty means every message is a draft.\n")
    w("context/suppression.csv", "# People who said no, one per line: who,why,date\n")
    shutil.copyfile(os.path.join(REPO, "playbook", "owner.example.md"), os.path.join(ws, "context", "owner.example.md"))
    w("context/computer.md", f"The team's computer. Written by install.py at {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC. id {uuid.uuid4().hex[:12]}\n")
    w("vault/Decisions.md", "# Decisions\n\nOne line per decision: the date, what was decided, the number behind it.\n")
    w(f".secrets/{team['secrets']}", f"BOT_HOME={ws}\nCONVLOG_TZ=America/New_York\n" + "".join(f"{k}={v}\n" for k, v in team.get("env", {}).items()), mode=0o600)

    # always rewritten: these come from the pack, not from the owner
    for a in agents:
        w(f"team/{a['role']}.md", T.setup(team, a) + "\n", fresh=True)
    w("requests/owner/create-the-team.md", "# If the lead cannot create the other bots\n\nFor each one that does not exist yet: create a bot with this name, set its time zone to UTC, and paste its line. Nothing else.\n\n"
      + "".join(f"## {a['bot']}\n\n{T.line(team, a)}\n\n" for a in agents if a["kind"] != "lead"), fresh=True)
    shutil.copyfile(os.path.join(REPO, "CHECKLIST.md"), os.path.join(ws, "requests", "owner", "CHECKLIST.md"))

    def run(*cmd):
        r = subprocess.run([sys.executable, *cmd], cwd=REPO, capture_output=True, text=True, env=dict(os.environ, BOT_HOME=ws))
        return r.returncode, (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["(no output)"])[-1]

    checks = [("pack check", run("tools/check.py")), ("team", run("tools/team.py", "check")), *[(c[0], run(*c[1:])) for c in team.get("checks", [])]]
    clis = {n: bool(shutil.which(n)) for n in ("claude", "codex")}
    ok = all(rc == 0 for _, (rc, _) in checks)
    log = [f"## install.py, {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC", "", f"workspace: {ws}", f"files written: {len(made)}; kept as they were: {len(kept)}", ""]
    log += [f"- {n}: {'ok' if rc == 0 else 'FAILED'} ({last})" for n, (rc, last) in checks]
    log += [f"- Claude Code CLI on this computer: {'yes' if clis['claude'] else 'no'}", f"- Codex CLI on this computer: {'yes' if clis['codex'] else 'no'}", ""]
    os.makedirs(os.path.join(ws, "log"), exist_ok=True)
    with open(os.path.join(ws, "log", "setup.md"), "a", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")

    print("\n".join(log))
    print("INSTALLED" if ok else "INSTALLED, WITH A FAILED CHECK ABOVE: go on, and put the failed line in your report")
    fns = [a for a in agents if a["kind"] != "lead"]
    print(f"""
WHAT YOU DO NOW, in order, without asking the owner anything. (Only if your line gave you another role: skip all of this and run the setup command your line names.)

1. You are the lead, {agents[0]['bot']}. Run: python3 {ws}/repo/tools/team.py setup lead
   and do what it prints (memory, the skill, your {len(agents[0]['routines'])} routines, the ready command).
2. Create the other {len(fns)} bots, one at a time, in this order: {', '.join(a['role'] for a in fns)}.
   For each: python3 {ws}/repo/tools/team.py line <role> prints its name and the one line to give it. Time zone UTC.
   If you cannot create a bot or message it, stop trying after the first failure: the names and lines for the owner to paste are in
   {ws}/requests/owner/create-the-team.md. Until a bot exists, or if one answers "own computer", run its job yourself:
   python3 {ws}/repo/tools/team.py solo <role>, and create the routines it prints.
3. Install the two CLIs if the lines above say no:
     npm install -g @anthropic-ai/claude-code
     npm install -g @openai/codex
   Then run: python3 {ws}/repo/tools/job.py status
   "not answering" is expected until the owner signs them in. Go on either way.
4. If one answered, prove it now: python3 {ws}/repo/tools/job.py run {team.get('first_job', 'plan')}
5. Run python3 {ws}/repo/tools/team.py missing. Every agent should be set up, by its own bot or by you.
6. Send the owner ONE message: each agent and whether it is its own bot or run by you (context/team-registry.md), what job.py status said,
   any failed check above, and then the whole of {ws}/requests/owner/CHECKLIST.md, starting with the line NEEDS YOU:
   Then stop. Do not ask the checklist's questions one at a time.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
