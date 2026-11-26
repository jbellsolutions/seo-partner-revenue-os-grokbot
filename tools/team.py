#!/usr/bin/env python3
"""The team (team.json): the lead, and one Grok bot for each of the nine Revenue OS functions.

    python3 tools/team.py list                       the ten agents and their routines
    python3 tools/team.py line <role>                the bot's name and the one line that sets it up
    python3 tools/team.py setup <role>               what that bot does to set itself up: memory, the CLI skill, routines
    python3 tools/team.py ready <role>               write the bot's row in context/team-registry.md and its first heartbeat
    python3 tools/team.py where                      shared or own: is this the computer the lead is on
    python3 tools/team.py solo <role>                the routines for the lead to run for an agent that has no bot here
    python3 tools/team.py missing                    agents with no row in context/team-registry.md
    python3 tools/team.py give <role> "<what>" --from <role>    work for another agent
    python3 tools/team.py inbox <role> | taken <file>           an agent's open work; mark one done
    python3 tools/team.py check                      exit 1 unless there is one lead and exactly one agent per function
"""
import json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = 50
FUNCTIONS = ["dream-100", "dream-500", "partners", "cold-email", "lead-radar", "content", "speaker", "aeo-seo", "sales-crm"]


def load():
    return json.load(open(os.path.join(ROOT, "team.json")))


def where(team):
    """The workspace: BOT_HOME, else the folder this pack's repo/ sits in, else the name in team.json."""
    return os.environ.get("BOT_HOME") or (os.path.dirname(ROOT) if os.path.basename(ROOT) == "repo" else team["workspace"])


def agent(team, role):
    return next((a for a in team["agents"] if a["role"] == role), None)


def block(path):
    m = re.search(r"```\n(.*?)\n```", open(path, encoding="utf-8").read(), re.S)
    return m.group(1) if m else ""


def memory(role):
    """The bot's whole memory section: the master prompt, then its role block. Nothing else."""
    return block(os.path.join(ROOT, "MASTER-PROMPT.md")) + "\n\n" + block(os.path.join(ROOT, "roles", role + ".md"))


def line(team, a):
    ws = team["workspace"]
    if a["kind"] == "lead":
        return (f"Install the {team['name']} team. Download {team['link']}, unpack it into {ws}/repo/, run python3 {ws}/repo/tools/install.py "
                f"and do what it prints, in order. Ask me nothing until it is all done, then send me one message that ends with the checklist. Nothing sends or posts until I say yes.")
    return (f"You are {a['bot']}, one agent on the {team['name']} team; your role is {a['role']}. If {ws}/repo/team.json is not on your computer, download {team['link']}, unpack it into {ws}/repo/ "
            f"and run python3 {ws}/repo/tools/install.py. Then run python3 {ws}/repo/tools/team.py setup {a['role']} and do what it prints, in order. "
            f"Ask nothing. Nothing sends or posts until the owner says yes. When you are done, reply with the one line the ready command prints.")


def routines(a, ws, who=""):
    out = []
    for name, cron, does in a["routines"]:
        out += [f"   - Name: {name}", f"     Schedule: {cron}", f"     Prompt: Routine: {name}. Agent: {a['role']}. {does}. Follow the run steps in your memory{who}."]
    return out


def setup(team, a):
    ws = where(team)
    out = [f"# {a['bot']}: set yourself up", "",
           "1. SAVE THIS TO YOUR MEMORY, word for word. It replaces anything an older install of this pack saved there.", "",
           "-----", memory(a["role"]), "-----", "",
           "2. SAVE THESE SKILLS, each under its own name, unless you already see them: " + "; ".join(f"{ws}/repo/skills/{k}/SKILL.md as {k}" for k in team["skills"]) + ".", ""]
    if a["kind"] != "lead":
        out += [f"3. RUN: python3 {ws}/repo/tools/team.py where", "   If it says own, you cannot see the team's files: create no routine, reply \"own computer\", and stop here. The lead runs your job.", "",
                "4. CREATE THESE ROUTINES (time zone UTC). Each runs; the switch file keeps it on test, so it only drafts:", ""]
    else:
        out += ["3. CREATE THESE ROUTINES (time zone UTC). Each runs; the switch file keeps it on test, so it only drafts:", ""]
    out += routines(a, ws)
    n = 5 if a["kind"] != "lead" else 4
    out += ["", f"{n}. RUN: python3 {ws}/repo/tools/team.py ready {a['role']}", "", "Accounts this agent uses when the owner signs them in: " + "; ".join(a.get("accounts", [])) + "."]
    return "\n".join(out)


def solo(team, a):
    ws = where(team)
    return "\n".join([f"# The lead runs {a['bot']}'s job", "", "1. ADD THIS TO YOUR MEMORY, after what is there. You keep your own role; on these routines you also act as this one:", "",
                      block(os.path.join(ROOT, "roles", a["role"] + ".md")), ""] + ["", "2. CREATE THESE ROUTINES on yourself (time zone UTC):", ""] + routines(a, ws, f" as role {a['role']}") + ["", f"3. RUN: python3 {ws}/repo/tools/team.py ready {a['role']} --by lead"])


def registered(ws):
    reg = os.path.join(ws, "context", "team-registry.md")
    return re.findall(r"^\| [^|]+ \| ([a-z0-9-]+) \|", open(reg, encoding="utf-8").read(), re.M) if os.path.exists(reg) else []


def problems():
    team, bad = load(), []
    roles = sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, "roles")) if f.endswith(".md"))
    have = [a["role"] for a in team["agents"]]
    bad += [f"roles/{r}.md has no agent in team.json" for r in roles if r not in have]
    bad += [f"agent '{r}' has no roles/{r}.md" for r in have if r not in roles]
    leads = [a["role"] for a in team["agents"] if a["kind"] == "lead"]
    if leads != ["lead"]:
        bad.append("there is not exactly one lead")
    fns = [a["role"] for a in team["agents"] if a["kind"] == "function"]
    bad += [f"function '{f}' has {fns.count(f)} agents, not one" for f in FUNCTIONS if fns.count(f) != 1]
    bad += [f"agent '{a['role']}' has no engine (claude or codex)" for a in team["agents"] if a.get("engine") not in ("claude", "codex")]
    bots = [a["bot"] for a in team["agents"]]
    bad += [f"two bots are named '{n}'" for n in sorted(set(bots)) if bots.count(n) > 1]
    names = [r[0] for a in team["agents"] for r in a["routines"]]
    bad += [f"two routines are named '{n}'" for n in sorted(set(names)) if names.count(n) > 1]
    bad += [f"agent '{a['role']}' has more than the {CAP} routines one bot allows" for a in team["agents"] if len(a["routines"]) > CAP]
    jobs = sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, "jobs")) if f.endswith(".md"))
    used = set()
    for a in team["agents"]:
        if a["role"] in roles:
            b = block(os.path.join(ROOT, "roles", a["role"] + ".md"))
            if f"Role: {a['role']}." not in b:
                bad.append(f"roles/{a['role']}.md has no memory block that starts 'Role: {a['role']}.'")
            bad += [f"routine '{n}' is not named in roles/{a['role']}.md" for n, _, _ in a["routines"] if f'"{n}"' not in b]
        for n, _, does in a["routines"]:
            m = re.search(r"job\.py run ([a-z0-9-]+)", does)
            if not m:
                bad.append(f"routine '{n}' does not hand a job to tools/job.py")
            elif m.group(1) not in jobs:
                bad.append(f"routine '{n}' runs job '{m.group(1)}', which has no file in jobs/")
            else:
                used.add(m.group(1))
    bad += [f"jobs/{j}.md is run by no routine" for j in jobs if j not in used]
    if "job.py" not in block(os.path.join(ROOT, "MASTER-PROMPT.md")):
        bad.append("MASTER-PROMPT.md does not carry the rule that every task goes through tools/job.py")
    return bad, team


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    arg = sys.argv[2:]
    bad, team = problems()
    ws = where(team)
    if cmd == "check":
        n = sum(len(x["routines"]) for x in team["agents"])
        print("\n".join(bad) if bad else f"ok: {len(team['agents'])} agents, the lead and {len(team['agents']) - 1} functions; {n} routines, each hands a job to a CLI")
        return 1 if bad else 0
    if cmd == "list":
        for x in team["agents"]:
            print(f"{x['bot']} | role {x['role']} | thinks with {x['engine']}")
            for n, c, d in x["routines"]:
                print(f"  {n} ({c})")
        return 0
    if cmd == "missing":
        have = registered(ws)
        print("\n".join(x["role"] for x in team["agents"] if x["role"] not in have) or "none: every agent is set up"); return 0
    if cmd == "where":
        print("shared" if "lead" in registered(ws) else "own"); return 0
    if cmd == "taken" and arg:
        f = os.path.abspath(arg[0])
        if os.path.dirname(os.path.dirname(f)) != os.path.join(os.path.abspath(ws), "requests") or not os.path.isfile(f):
            print("that is not an open item in requests/<role>/"); return 1
        d = os.path.join(os.path.dirname(f), "done"); os.makedirs(d, exist_ok=True); os.replace(f, os.path.join(d, os.path.basename(f))); print("ok"); return 0
    a = agent(team, arg[0]) if arg else (team["agents"][0] if cmd in ("line", "setup", "ready") else None)
    if not a:
        print("no such role. Roles: " + ", ".join(x["role"] for x in team["agents"])); return 1
    if cmd == "line":
        print(f"Name: {a['bot']}\nLine: {line(team, a)}"); return 0
    if cmd == "setup":
        print(setup(team, a)); return 0
    if cmd == "solo":
        print(solo(team, a)); return 0
    if cmd == "give" and len(arg) >= 2:
        d = os.path.join(ws, "requests", a["role"]); os.makedirs(d, exist_ok=True)
        frm = arg[arg.index("--from") + 1] if "--from" in arg and len(arg) > arg.index("--from") + 1 else "owner"
        p = os.path.join(d, f"{time.strftime('%Y-%m-%d-%H%M%S', time.gmtime())}-{os.getpid()}.md")
        open(p, "w", encoding="utf-8").write(f"From: {frm}\n\n{arg[1]}\n"); print(p); return 0
    if cmd == "inbox":
        d = os.path.join(ws, "requests", a["role"])
        fs = sorted(f for f in (os.listdir(d) if os.path.isdir(d) else []) if f.endswith(".md"))
        for f in fs:
            print(f"== {os.path.join(d, f)}\n" + open(os.path.join(d, f), encoding="utf-8").read().strip())
        print(f"{len(fs)} open"); return 0
    if cmd == "ready":
        reg = os.path.join(ws, "context", "team-registry.md")
        os.makedirs(os.path.dirname(reg), exist_ok=True)
        rows = open(reg, encoding="utf-8").read().splitlines() if os.path.exists(reg) else ["# The team, as set up", "", "| Bot | Role | Routines | Set up (UTC) |", "|---|---|---|---|"]
        rows = [r for r in rows if f"| {a['role']} |" not in r]
        by = " (run by the lead)" if "--by" in arg else ""
        rows.append(f"| {a['bot']}{by} | {a['role']} | " + "; ".join(f"{n} `{c}`" for n, c, _ in a["routines"]) + f" | {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} |")
        open(reg, "w", encoding="utf-8").write("\n".join(rows) + "\n")
        subprocess.run([sys.executable, os.path.join(ROOT, "guards", "scripts", "beat.py"), "write", a["role"], "set up", "found=0", "drafted=0", "sent=0"],
                       env=dict(os.environ, BOT_HOME=ws), capture_output=True)
        print(f"ready: {a['bot']}{by}, {len(a['routines'])} routines, all on test")
        return 0
    print(__doc__); return 1


if __name__ == "__main__":
    sys.exit(main())
