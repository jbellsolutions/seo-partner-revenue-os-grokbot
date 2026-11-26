#!/usr/bin/env python3
"""The team's one people list: which agent works each person, and how far that person has got. Plain files, no network.

    people.py import <file.csv> --source "<where it came from>" [--lane <role>]   add people from any CSV (name, email, company, linkedin, city, phone)
    people.py add --name N [--email E] [--company C] [--linkedin L] [--city C] [--source S] [--why W] [--lane <role>]
    people.py list [--stage S] [--lane <role>] [--limit N]
    people.py show <id>
    people.py fit <id> <0-5> "<why, from something public or known>"
    people.py stage <id> <stage> ["<note>"]
    people.py lane <id> <role>                                       give a person to one agent; one agent works one person
    people.py due [--lane <role>]                                   who needs a next step today
    people.py stats [--days N]                                      counts by stage, and what moved in the last N days
    people.py outbox --routine "<NAME>"                             that agent's items that may go out now (type approved, routine on, not opted out)
    people.py done <item file> [--failed]                           after the sending app confirms: log it, file it, move the person on
    people.py export --type cold_email [--out FILE]                drafts as a CSV a cold-email tool imports
    people.py page                                                  write content/invitation.html from context/owner.md

Stages: listed, invited, replied, booked, talked, offered, joined, mentorship, later, no.
A lane is the role id of the agent working the person. "no" also goes on the opt-out list. Everything is in data/people.csv and state/people.jsonl under the workspace."""
import contextlib, csv, datetime, fcntl, html, json, os, pathlib, re, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
WS = pathlib.Path(os.environ.get("BOT_HOME") or (REPO.parent if REPO.name == "repo" else REPO))
PEOPLE, LOG = WS / "data" / "people.csv", WS / "state" / "people.jsonl"
COLS = ["id", "name", "email", "company", "linkedin", "city", "phone", "source", "fit", "why", "stage", "touches", "last", "note", "lane"]
STAGES = ["listed", "invited", "replied", "booked", "talked", "offered", "joined", "mentorship", "later", "no"]
HEAD = {"name": ["name", "full name", "contact", "contact name"], "email": ["email", "email address", "work email", "e-mail"],
        "company": ["company", "company name", "business", "organization", "account"], "linkedin": ["linkedin", "linkedin url", "person linkedin url", "profile url"],
        "city": ["city", "location", "town"], "phone": ["phone", "mobile", "phone number", "cell"], "why": ["why", "notes", "title", "job title"]}


TEAM = json.loads((REPO / "team.json").read_text(encoding="utf-8"))
LANES = [a["role"] for a in TEAM["agents"]]
FIRST = {"dream100_first_touch", "dream500_first_touch", "partner_outreach", "cold_email", "radar_opener", "show_pitch"}


@contextlib.contextmanager
def lock():
    """Ten bots share one list: one command at a time."""
    PEOPLE.parent.mkdir(parents=True, exist_ok=True)
    with (PEOPLE.parent / ".lock").open("w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def today():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def load():
    if not PEOPLE.exists():
        return []
    with PEOPLE.open(newline="", encoding="utf-8") as f:
        return [{c: r.get(c, "") or "" for c in COLS} for r in csv.DictReader(f)]


def save(rows):
    PEOPLE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PEOPLE.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)
    os.chmod(tmp, 0o600); tmp.replace(PEOPLE)


def event(pid, what, **kw):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"d": today(), "id": pid, "what": what, **kw}) + "\n")


def key(r):
    li = re.sub(r"^https?://(www\.)?", "", r["linkedin"].lower()).rstrip("/")
    return [k for k in (r["email"].lower().strip(), li, (r["name"] + "|" + r["company"]).lower().strip("| ") if r["name"] and r["company"] else "") if k]


def guard(script, *args):
    r = subprocess.run([sys.executable, str(REPO / "guards" / "scripts" / script), *args], capture_output=True, text=True, env=dict(os.environ, BOT_HOME=str(WS)))
    return r.returncode, r.stdout.strip()


def insert(rows, seen, new, source):
    r = {c: "" for c in COLS}
    r.update({k: (v or "").strip() for k, v in new.items() if k in COLS})
    r["source"] = r["source"] or source
    ks = key(r)
    if not ks or any(k in seen for k in ks):
        return None
    r.update(id=f"p{max([int(x['id'][1:]) for x in rows] or [0]) + 1:04d}", stage="listed", touches="0", last=today())
    rows.append(r); seen.update(ks); event(r["id"], "listed", source=r["source"])
    return r


def person(rows, pid):
    r = next((x for x in rows if x["id"] == pid), None)
    if not r:
        raise SystemExit(f"no person {pid}")
    return r


def owner():
    """context/owner.md as a dict: `key: value` lines."""
    f, out = WS / "context" / "owner.md", {}
    if f.exists():
        for l in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*[-*]?\s*([a-z_]+):\s*(.+?)\s*$", l)
            if m:
                out[m.group(1)] = m.group(2)
    return out


def item(path):
    t = pathlib.Path(path).read_text(encoding="utf-8")
    g = lambda k: (re.search(rf"^{k}:\s*(.+)$", t, re.M) or [None, ""])[1].strip()
    body = re.search(r"^TEXT:\n(.*?)^---END---$", t, re.S | re.M)
    return {"role": g("ROLE"), "type": g("TYPE"), "person": g("PERSON"), "to": g("TO"), "subject": g("SUBJECT"), "text": (body.group(1) if body else "").strip()}


def move(rows, r, stage, note=""):
    r["stage"], r["last"] = stage, today()
    if note:
        r["note"] = note
    event(r["id"], stage, note=note)
    if stage == "no":
        for who in (r["email"], r["linkedin"], r["name"] if not r["email"] and not r["linkedin"] else ""):
            if who:
                guard("suppression.py", "add", who, note or "said no")


def outbox(routine):
    ok, held = [], []
    role = next((x["role"] for x in TEAM["agents"] if routine in [r[0] for r in x["routines"]]), None)
    for f in sorted((WS / "requests" / "owner").glob("*.item")):
        i = item(f)
        if i["role"] != role:
            continue
        rc, why = guard("send_guard.py", i["type"] or "unknown", "--routine", routine)
        if rc:
            held.append((f, why)); continue
        if not i["to"] or guard("suppression.py", "check", i["to"])[0]:
            held.append((f, "opted out or no address")); continue
        ok.append(f)
    return ok, held


PAGE = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title>
<style>body{{font:17px/1.6 system-ui,sans-serif;max-width:40rem;margin:0 auto;padding:3rem 1.2rem;color:#17262e;background:#fff}}h1{{font-size:2.2rem;line-height:1.15;margin:0 0 .6rem}}h2{{margin:2.2rem 0 .4rem;font-size:1.25rem}}a.b{{display:inline-block;margin-top:1.4rem;padding:.8rem 1.2rem;background:#0a6470;color:#fff;text-decoration:none}}li{{margin:.3rem 0}}.m{{color:#546670}}@media(prefers-color-scheme:dark){{body{{background:#10191e;color:#e4edf0}}.m{{color:#9db0b8}}}}</style>
<h1>{name}</h1><p>{promise}</p>{who}{get}{how}{price}{cta}<p class="m">{host}</p></html>
"""


def page():
    o, e = owner(), html.escape
    if not o.get("name"):
        print("context/owner.md has no `name:` line yet. Copy context/owner.example.md to context/owner.md and fill it in."); return 1
    sec = lambda h, k: f"<h2>{h}</h2><ul>" + "".join(f"<li>{e(x.strip())}</li>" for x in o[k].split(";") if x.strip()) + "</ul>" if o.get(k) else ""
    price = f"<h2>Price</h2><p>{e(o['price'])}" + (f". {e(o['payment'])}" if o.get("payment") else "") + "</p>" if o.get("price") and o.get("show_price", "no").lower() == "yes" else ""
    link = o.get("booking_link", "")
    cta = f'<a class="b" href="{e(link, quote=True)}">Book a conversation</a>' if re.match(r"https://", link) else ""
    seats = f"<h2>Seats</h2><p>{e(o['seats'])}</p>" if o.get("seats") else ""
    f = WS / "content" / "invitation.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(PAGE.format(name=e(o["name"]), promise=e(o.get("promise", "")), who=sec("Who it is for", "who"), get=sec("What you get", "members_get"),
                             how=sec("How it runs", "format") + seats, price=price, cta=cta, host=e("Hosted by " + o["host"]) if o.get("host") else ""), encoding="utf-8")
    print(f"wrote {f}" + ("" if cta else " (no button: booking_link is not an https link yet)")); return 0


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 2
    opt = lambda k, d="": a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else d
    cmd, rows = a[0], load()
    seen = {k for r in rows for k in key(r)}
    if cmd == "import" and len(a) >= 2:
        if opt("--lane") and opt("--lane") not in LANES:
            print("lanes: " + ", ".join(LANES)); return 2
        n = skip = 0
        with open(a[1], newline="", encoding="utf-8-sig", errors="ignore") as f:
            for raw in csv.DictReader(f):
                low = {(k or "").strip().lower(): v for k, v in raw.items() if isinstance(v, str)}
                new = {c: next((low[h] for h in hs if low.get(h)), "") for c, hs in HEAD.items()}
                if not new["name"]:
                    new["name"] = " ".join(x for x in (low.get("first name", ""), low.get("last name", "")) if x)
                new["lane"] = opt("--lane")
                held = any(guard("suppression.py", "check", v)[0] for v in (new["email"], new["linkedin"]) if v)
                if held or not insert(rows, seen, new, opt("--source", os.path.basename(a[1]))):
                    skip += 1
                else:
                    n += 1
        save(rows); print(f"added {n}, skipped {skip} (already listed, opted out or no way to tell who)"); return 0
    if cmd == "add":
        if opt("--lane") and opt("--lane") not in LANES:
            print("lanes: " + ", ".join(LANES)); return 2
        if any(guard("suppression.py", "check", v)[0] for v in (opt("--email"), opt("--linkedin")) if v):
            print("opted out"); return 1
        r = insert(rows, seen, {c: opt("--" + c) for c in COLS if c not in ("id", "stage", "touches", "last", "fit")}, opt("--source", "added by hand"))
        if not r:
            print("already listed, or no name with company, email or linkedin"); return 1
        save(rows); print(r["id"]); return 0
    if cmd == "list":
        out = [r for r in rows if (not opt("--stage") or r["stage"] == opt("--stage")) and (not opt("--lane") or r["lane"] == opt("--lane"))]
        out.sort(key=lambda r: (-int(r["fit"] or 0), r["id"]))
        for r in out[:int(opt("--limit", "50"))]:
            print(f"{r['id']} | {r['stage']} | {r['lane'] or 'no lane'} | fit {r['fit'] or '?'} | {r['name']} | {r['company']} | {r['source']}")
        return 0
    if cmd == "show" and len(a) >= 2:
        print("\n".join(f"{k}: {v}" for k, v in person(rows, a[1]).items())); return 0
    if cmd == "fit" and len(a) >= 4:
        r = person(rows, a[1])
        if not re.fullmatch("[0-5]", a[2]):
            print("fit is 0 to 5"); return 2
        r["fit"], r["why"] = a[2], a[3]; save(rows); event(r["id"], "fit", fit=a[2]); print("ok"); return 0
    if cmd == "lane" and len(a) >= 3:
        if a[2] not in LANES:
            print("lanes: " + ", ".join(LANES)); return 2
        r = person(rows, a[1]); r["lane"] = a[2]; save(rows); event(r["id"], "lane", lane=a[2]); print("ok"); return 0
    if cmd == "stage" and len(a) >= 3:
        if a[2] not in STAGES:
            print("stages: " + ", ".join(STAGES)); return 2
        move(rows, person(rows, a[1]), a[2], a[3] if len(a) > 3 else ""); save(rows); print("ok"); return 0
    if cmd == "due":
        wait, now = {"invited": 4, "replied": 1, "booked": 1, "talked": 2, "offered": 3, "later": 30}, datetime.date.fromisoformat(today())
        n = 0
        for r in rows:
            age = (now - datetime.date.fromisoformat(r["last"])).days
            if r["stage"] not in wait or age < wait[r["stage"]] or (opt("--lane") and r["lane"] != opt("--lane")):
                continue
            step = {"invited": "one more short note" if int(r["touches"] or 0) < 3 else "move to later", "replied": "answer and offer the call", "booked": "prepare, or mark talked",
                    "talked": "invite, offer mentorship, or say not now", "offered": "ask if they are in", "later": "a friendly hello"}[r["stage"]]
            print(f"{r['id']} | {r['stage']} {age}d | {r['name']}, {r['company']} | {step}"); n += 1
        print(f"{n} due"); return 0
    if cmd == "stats":
        by = {s: sum(r["stage"] == s for r in rows) for s in STAGES}
        print("lanes: " + (", ".join(f"{l or 'none'} {sum(r['lane'] == l for r in rows)}" for l in sorted({r["lane"] for r in rows})) or "nobody yet"))
        print(f"people {len(rows)}: " + ", ".join(f"{s} {n}" for s, n in by.items() if n))
        since = (datetime.date.fromisoformat(today()) - datetime.timedelta(days=int(opt("--days", "1")) - 1)).isoformat()
        moved = {}
        for l in (LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []):
            e = json.loads(l)
            if e["d"] >= since:
                moved[e["what"]] = moved.get(e["what"], 0) + 1
        print(f"last {opt('--days', '1')} day(s): " + (", ".join(f"{k} {v}" for k, v in moved.items()) or "nothing moved")); return 0
    if cmd == "outbox":
        ok, held = outbox(opt("--routine", "unknown"))
        print("\n".join(str(f) for f in ok)); print(f"{len(ok)} may go now; {len(held)} wait for the owner", file=sys.stderr); return 0
    if cmd == "done" and len(a) >= 2:
        f, i = pathlib.Path(a[1]), item(a[1])
        failed = "--failed" in a
        subprocess.run([sys.executable, str(REPO / "convlog" / "gate.py"), "failed" if failed else "sent", str(f), "--agent", i["role"] or "unknown"], env=dict(os.environ, BOT_HOME=str(WS)), capture_output=True)
        r = next((x for x in rows if x["id"] == i["person"]), None)
        if r and not failed:
            r["touches"] = str(int(r["touches"] or 0) + 1)
            move(rows, r, "offered" if i["type"] == "invitation" else "invited" if i["type"] in FIRST and r["stage"] == "listed" else r["stage"]); save(rows)
        d = WS / "requests" / ("failed" if failed else "sent"); d.mkdir(parents=True, exist_ok=True)
        f.rename(d / f.name); print("filed"); return 0
    if cmd == "export":
        kind, out = opt("--type", "cold_email"), pathlib.Path(opt("--out") or WS / "data" / "out" / f"{opt('--type', 'cold_email')}-{today()}.csv")
        n = 0; out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as h:
            w = csv.writer(h); w.writerow(["email", "first_name", "company", "subject", "message"])
            for f in sorted((WS / "requests" / "owner").glob("*.item")):
                i = item(f); r = next((x for x in rows if x["id"] == i["person"]), None)
                if i["type"] == kind and r and "@" in i["to"] and not guard("suppression.py", "check", i["to"])[0]:
                    w.writerow([i["to"], (r["name"].split() or [""])[0], r["company"], i["subject"], i["text"]]); n += 1
        os.chmod(out, 0o600); print(f"{n} rows in {out}"); return 0
    if cmd == "page":
        return page()
    print(__doc__); return 2


if __name__ == "__main__":
    with lock():
        sys.exit(main(sys.argv[1:]))
