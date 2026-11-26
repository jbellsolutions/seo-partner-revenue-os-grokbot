#!/usr/bin/env python3
"""Update an older install of this pack to the team, keeping everything the owner gave it. Safe to run again.

    python3 <workspace>/repo/tools/update.py

Run it after the new pack is in repo/. It copies context/, data/people.csv and requests/owner/ to state/before-update-<time>/,
carries the old switch lines, approvals and waiting drafts over to the new names (team.json "update"), then runs install.py.
It deletes nothing the owner gave. The old routines it names are the bot's to delete in the app."""
import json, os, pathlib, re, shutil, subprocess, sys, time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import team as T


def main():
    team = T.load(); ws = pathlib.Path(T.where(team)); u = team.get("update", {}); did = []
    keep = ws / "state" / f"before-update-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}"
    keep.mkdir(parents=True, exist_ok=True); os.chmod(keep, 0o700)
    for rel in ("context", "requests/owner"):
        if (ws / rel).is_dir():
            shutil.copytree(ws / rel, keep / rel)
    if (ws / "data" / "people.csv").exists():
        shutil.copy2(ws / "data" / "people.csv", keep / "people.csv")

    f, old = ws / "context" / "routines-on.md", []
    if f.exists():
        out, seen = [], set()
        for l in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"(.+?)\s*:\s*(.*)$", l)
            if m and m.group(1) in u.get("routines", {}):
                old.append(m.group(1)); new = u["routines"][m.group(1)]
                if new and new not in seen:
                    out.append(f"{new}: {m.group(2)}"); seen.add(new)
            else:
                out.append(l)
        f.write_text("\n".join(out) + "\n", encoding="utf-8")
    f = ws / "context" / "standing-approvals.md"
    if f.exists():
        t = f.read_text(encoding="utf-8")
        for a, b in u.get("types", {}).items():
            if re.search(rf"(?m)^{a}\s*:", t):
                t = re.sub(rf"(?m)^{a}(\s*:)", rf"{b}\1", t); did.append(f"approval {a} is now {b}")
        f.write_text(t, encoding="utf-8")
    roles, n = u.get("roles", {}), 0
    for p in (ws / "requests" / "owner").glob("*.item") if (ws / "requests" / "owner").is_dir() else []:
        t = p.read_text(encoding="utf-8"); m = re.search(r"(?m)^TYPE:\s*(\S+)", t); head, sep, rest = t.partition("---PAYLOAD---")
        if m and m.group(1) in roles and re.search(rf"(?m)^ROLE:\s*{re.escape(u.get('old_role', ''))}\s*$", head):
            head = re.sub(r"(?m)^ROLE:.*$", f"ROLE: {roles[m.group(1)]}", head)
            head = re.sub(r"(?m)^TYPE:.*$", f"TYPE: {u.get('types', {}).get(m.group(1), m.group(1))}", head)
            p.write_text(head + sep + rest, encoding="utf-8"); n += 1
    for a, b in u.get("secrets", {}).items():
        s, d = ws / ".secrets" / a, ws / ".secrets" / b
        if s.exists() and not d.exists():
            shutil.copy2(s, d); os.chmod(d, 0o600)
    print(f"UPDATE to {team['name']} {team['version']}. What the owner gave is kept; a copy from before is in {keep}")
    print("\n".join(["- " + x for x in did] + [f"- waiting drafts carried to their new agent: {n}"]))
    if u.get("routines"):
        print("\nBEFORE THE STEPS BELOW: delete these old routines from yourself in the app, they are replaced: " + "; ".join(u["routines"]) + ".\n"
              "You were the only bot. You are now the lead, and the nine functions become their own bots. The two CLIs you already installed stay as they are.\n")
    sys.stdout.flush()
    return subprocess.run([sys.executable, str(REPO / "tools" / "install.py")]).returncode


if __name__ == "__main__":
    sys.exit(main())
