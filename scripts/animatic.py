#!/usr/bin/env python3
"""animatic.py - helper for the explainer-animatic skill.

Subcommands
  new    <beats.json> [--lang en|zh-CN] [--seconds N] [--title T]   write a starter beat file
  check  <beats.json>                                                 clock check + lint, exit 1 on errors
  build  <beats.json> [-o out.html]                                   write a playable, self-contained HTML animatic
  sheet  <beats.json> [-o out.md]                                     write a Markdown production sheet

Python 3.8+, standard library only.
"""
import argparse
import html
import json
import re
import sys

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
LATIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9'%.\-]*")

DEFAULT_PACE = {"en": 2.3, "zh-CN": 4.2}   # spoken units per second: words (en) or characters (zh)
SCREEN_READ = {"en": 3.5, "zh-CN": 6.0}    # on-screen units a viewer reads per second
KINDS = ["type", "diagram", "number", "metaphor", "ui"]
MOTIONS = ["rise", "slide", "zoom", "build", "swap", "hold"]
PARTS_HINT = "snag, mechanism, proof, payoff, next, myth, twist, before, change, after, item"
MIN_BEAT, MAX_BEAT = 1.2, 8.0
PAD = 0.4


def units(text, lang):
    """Spoken/read units: CJK characters count one each, latin tokens count one each."""
    text = text or ""
    cjk = len(CJK.findall(text))
    lat = len(LATIN.findall(CJK.sub(" ", text)))
    if lang == "zh-CN":
        return cjk + lat * 2  # a latin word in Chinese narration takes about two characters of time
    return lat + cjk


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        sys.exit("cannot read %s: %s" % (path, e))


def timing(doc):
    lang = doc.get("lang", "en")
    pace = float(doc.get("pace") or DEFAULT_PACE.get(lang, 2.3))
    read = SCREEN_READ.get(lang, 3.5)
    out, t = [], 0.0
    for b in doc.get("beats", []):
        vo_u = units(b.get("vo", ""), lang)
        scr_u = units(b.get("screen", ""), lang)
        vo_s = vo_u / pace if vo_u else 0.0
        scr_s = (scr_u / read + 0.5) if scr_u else 0.0
        need = max(vo_s + PAD if vo_u else 0.0, scr_s, MIN_BEAT if not vo_u else 0.0)
        dur = float(b["seconds"]) if b.get("seconds") else round(need + float(b.get("hold", 0) or 0), 1)
        out.append({"beat": b, "start": round(t, 1), "dur": dur, "vo_units": vo_u,
                    "scr_units": scr_u, "vo_s": round(vo_s, 1), "scr_s": round(scr_s, 1), "need": round(need, 1)})
        t += dur
    return out, round(t, 1), pace


def tc(s):
    return "%d:%04.1f" % (int(s // 60), s % 60)


def cmd_new(a):
    zh = a.lang == "zh-CN"
    doc = {
        "title": a.title or ("新的讲解短片" if zh else "New explainer"),
        "lang": a.lang,
        "viewer_line": "看完之后，<谁> 能 <做到/说出> <什么>。" if zh else "After watching, <who> can <do or say> <what>.",
        "target_seconds": a.seconds,
        "format": "16:9",
        "spine": "snag-mechanism-payoff",
        "palette": {"bg": "#101418", "ink": "#f4f1ea", "accent": "#ffb347", "muted": "#7d8794"},
        "beats": [
            {"id": "b01", "part": "snag", "vo": "", "screen": "", "picture": "", "kind": "type", "motion": "rise", "seam": "cut"},
            {"id": "b02", "part": "mechanism", "vo": "", "screen": "", "picture": "", "kind": "diagram", "motion": "build", "seam": "carry"},
            {"id": "b03", "part": "payoff", "vo": "", "screen": "", "picture": "", "kind": "number", "motion": "zoom", "seam": "cut", "hold": 0.5},
            {"id": "b04", "part": "next", "vo": "", "screen": "", "picture": "", "kind": "type", "motion": "hold", "seam": "end", "hold": 1.5},
        ],
    }
    with open(a.file, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("wrote", a.file)


def lint(doc):
    errs, warns = [], []
    lang = doc.get("lang", "en")
    if lang not in DEFAULT_PACE:
        warns.append("lang %r unknown, timing uses English pace" % lang)
    vl = (doc.get("viewer_line") or "").strip()
    if not vl or "<" in vl:
        errs.append("viewer_line is missing or still a template")
    beats = doc.get("beats") or []
    if not beats:
        errs.append("no beats")
    ids = set()
    rows, total, pace = timing(doc)
    screen_cap = 12 if lang == "zh-CN" else 7
    for r in rows:
        b = r["beat"]
        bid = b.get("id") or "?"
        if bid in ids:
            errs.append("%s: duplicate id" % bid)
        ids.add(bid)
        if not (b.get("vo") or b.get("screen")):
            errs.append("%s: empty beat (no vo and no screen words)" % bid)
        if not (b.get("picture") or b.get("art")):
            errs.append("%s: no picture - say what the viewer sees" % bid)
        if b.get("kind") and b["kind"] not in KINDS:
            warns.append("%s: kind %r not in %s" % (bid, b["kind"], "/".join(KINDS)))
        if b.get("motion") and b["motion"] not in MOTIONS:
            warns.append("%s: motion %r not in %s" % (bid, b["motion"], "/".join(MOTIONS)))
        if r["dur"] > MAX_BEAT:
            warns.append("%s: %.1fs on one picture - split it or add a change inside the beat" % (bid, r["dur"]))
        if r["dur"] < MIN_BEAT:
            warns.append("%s: %.1fs is too short to register" % (bid, r["dur"]))
        if b.get("seconds") and float(b["seconds"]) + 0.05 < r["need"]:
            errs.append("%s: fixed %.1fs but the words need %.1fs" % (bid, float(b["seconds"]), r["need"]))
        if r["scr_units"] > screen_cap:
            warns.append("%s: %d on-screen units - keep screen words short (<= %d)" % (bid, r["scr_units"], screen_cap))
        vo, scr = (b.get("vo") or "").strip().lower(), (b.get("screen") or "").strip().lower()
        if vo and scr and len(scr) > 12 and scr.rstrip(".。") in vo:
            warns.append("%s: screen words repeat the narration verbatim - show the key term or number instead" % bid)
        if lang == "en":
            for s in re.split(r"[.!?]+", b.get("vo") or ""):
                if len(LATIN.findall(s)) > 22:
                    warns.append("%s: a narration sentence has %d words - split it for the ear" % (bid, len(LATIN.findall(s))))
        else:
            for s in re.split(r"[。！？!?]+", b.get("vo") or ""):
                if len(CJK.findall(s)) > 35:
                    warns.append("%s: 一句旁白 %d 字，太长，拆开" % (bid, len(CJK.findall(s))))
    tgt = doc.get("target_seconds")
    if tgt:
        tgt = float(tgt)
        if total > tgt * 1.1:
            errs.append("runtime %.1fs is over target %.0fs by %.0f%% - cut words, not pace" % (total, tgt, (total / tgt - 1) * 100))
        elif total < tgt * 0.7:
            warns.append("runtime %.1fs is well under target %.0fs - fine if the idea is complete" % (total, tgt))
    seams = [b.get("seam", "") for b in beats]
    if seams and seams[-1] not in ("end", ""):
        warns.append("last beat seam should be 'end'")
    holds = [b for b in beats if float(b.get("hold", 0) or 0) > 0]
    if len(beats) >= 5 and not holds:
        warns.append("no beat has a hold - give the payoff a short pause before it lands")
    return errs, warns, rows, total, pace


def cmd_check(a):
    doc = load(a.file)
    errs, warns, rows, total, pace = lint(doc)
    lang = doc.get("lang", "en")
    unit = "chars" if lang == "zh-CN" else "words"
    print("%s  (%s, pace %.1f %s/s)" % (doc.get("title", a.file), lang, pace, unit))
    print("%-5s %-7s %-10s %6s %6s %6s  %s" % ("id", "start", "part", "vo", "screen", "dur", "picture"))
    for r in rows:
        b = r["beat"]
        print("%-5s %-7s %-10s %5.1fs %5.1fs %5.1fs  %s" % (
            b.get("id", "?"), tc(r["start"]), (b.get("part") or "")[:10], r["vo_s"], r["scr_s"], r["dur"],
            (b.get("picture") or ("(art)" if b.get("art") else "-"))[:48]))
    vo_total = sum(r["vo_units"] for r in rows)
    print("total %s  |  %d beats  |  %d spoken %s  |  target %s" % (
        tc(total), len(rows), vo_total, unit, doc.get("target_seconds", "-")))
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print("OK" if not errs else "%d error(s)" % len(errs))
    sys.exit(1 if errs else 0)


CSS = r"""
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#000;color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
#wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100%;gap:12px;padding:12px}
#stage{container-type:inline-size;position:relative;width:min(96vw,calc((100vh - 190px)*var(--ar)));aspect-ratio:var(--arc);background:var(--bg);overflow:hidden;border-radius:6px}
.beat{position:absolute;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;padding:6%;text-align:center}
.beat.on{display:flex}
.screen{font-size:clamp(20px,6.2cqw,96px);font-weight:800;line-height:1.1;letter-spacing:-.01em}
.screen em{font-style:normal;color:var(--accent)}
.pic{margin-top:3cqw;font-size:clamp(11px,1.7cqw,22px);color:var(--muted);max-width:80%;border:1px dashed var(--muted);padding:.6em 1em;border-radius:6px}
.kind{position:absolute;top:3%;left:3%;font-size:clamp(9px,1.2cqw,14px);color:var(--muted);text-transform:uppercase;letter-spacing:.12em}
.art{width:100%;display:flex;align-items:center;justify-content:center}
.art svg{max-width:100%;max-height:34cqw}
#sub{position:absolute;left:5%;right:5%;bottom:4%;font-size:clamp(11px,2cqw,26px);line-height:1.35;color:var(--ink);background:rgba(0,0,0,.55);padding:.3em .6em;border-radius:4px;display:none}
#sub.show{display:block}
#bar{position:absolute;left:0;bottom:0;height:4px;background:var(--accent);width:0}
.m-rise.go>*{animation:rise .7s cubic-bezier(.2,.8,.2,1) both}
.m-slide.go>*{animation:slide .6s cubic-bezier(.2,.8,.2,1) both}
.m-zoom.go>*{animation:zoom .8s cubic-bezier(.2,.8,.2,1) both}
.m-swap.go>*{animation:swap .5s ease-out both}
.m-build.go>*{animation:rise .6s cubic-bezier(.2,.8,.2,1) both}
.m-build.go>*:nth-child(2){animation-delay:.35s}.m-build.go>*:nth-child(3){animation-delay:.7s}.m-build.go>*:nth-child(4){animation-delay:1.05s}
@keyframes rise{from{opacity:0;transform:translateY(4cqw)}to{opacity:1;transform:none}}
@keyframes slide{from{opacity:0;transform:translateX(12cqw)}to{opacity:1;transform:none}}
@keyframes zoom{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:none}}
@keyframes swap{from{opacity:0;filter:blur(8px)}to{opacity:1;filter:none}}
#ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;color:#ccc;font-size:14px}
#ctl button{background:#222;color:#eee;border:1px solid #444;border-radius:4px;padding:6px 12px;cursor:pointer;font:inherit}
#ctl label{display:flex;gap:4px;align-items:center}
#strip{display:flex;gap:3px;width:min(96vw,1200px)}
#strip div{flex:var(--d);height:22px;background:#2a2f36;border-radius:2px;cursor:pointer;font-size:10px;color:#9aa;display:flex;align-items:center;justify-content:center;overflow:hidden;white-space:nowrap}
#strip div.on{background:var(--accent);color:#000}
#time{font-variant-numeric:tabular-nums;min-width:110px;text-align:center}
"""

JS = r"""
const B=window.BEATS, total=B.reduce((s,b)=>s+b.dur,0);
let t=0, playing=false, last=null, cur=-1, voice=false;
const st=document.getElementById('stage'), sub=document.getElementById('sub'), bar=document.getElementById('bar');
const els=[...document.querySelectorAll('.beat')], strip=[...document.querySelectorAll('#strip div')];
function fmt(s){const m=Math.floor(s/60);return m+':'+(s%60).toFixed(1).padStart(4,'0')}
function idx(at){let a=0;for(let i=0;i<B.length;i++){a+=B[i].dur;if(at<a)return i}return B.length-1}
function show(i){if(i===cur)return;cur=i;els.forEach((e,k)=>{e.classList.toggle('on',k===i);e.classList.remove('go')});
 strip.forEach((e,k)=>e.classList.toggle('on',k===i));void els[i].offsetWidth;els[i].classList.add('go');
 sub.textContent=B[i].vo||'';if(voice&&playing)speak(B[i].vo)}
function speak(txt){if(!('speechSynthesis' in window)||!txt)return;speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(txt);u.lang=window.LANG==='zh-CN'?'zh-CN':'en-US';u.rate=window.RATE;speechSynthesis.speak(u)}
function render(){const i=idx(t);show(i);bar.style.width=(100*t/total)+'%';document.getElementById('time').textContent=fmt(t)+' / '+fmt(total)}
function tick(now){if(!playing)return;if(last!==null)t+=(now-last)/1000;last=now;if(t>=total){t=total-0.001;playing=false;btn.textContent='▶ Play';render();return}render();requestAnimationFrame(tick)}
const btn=document.getElementById('play');
function toggle(){playing=!playing;btn.textContent=playing?'❚❚ Pause':'▶ Play';if(playing){if(t>=total-0.01)t=0;last=null;cur=-1;render();requestAnimationFrame(tick)}else if('speechSynthesis' in window)speechSynthesis.cancel()}
function jump(i){i=Math.max(0,Math.min(B.length-1,i));t=B.slice(0,i).reduce((s,b)=>s+b.dur,0);cur=-1;last=null;render()}
btn.onclick=toggle;document.getElementById('prev').onclick=()=>jump(cur-1);document.getElementById('next').onclick=()=>jump(cur+1);
strip.forEach((e,k)=>e.onclick=()=>jump(k));
document.getElementById('subs').onchange=e=>sub.classList.toggle('show',e.target.checked);
document.getElementById('voice').onchange=e=>{voice=e.target.checked;if(!voice&&'speechSynthesis' in window)speechSynthesis.cancel()};
document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();toggle()}if(e.key==='ArrowRight')jump(cur+1);if(e.key==='ArrowLeft')jump(cur-1);if(e.key==='Home')jump(0)});
sub.classList.add('show');render();
const h=decodeURIComponent(location.hash.slice(1));const hi=B.findIndex(b=>b.id===h);if(hi>=0)jump(hi);
"""


def mark(text):
    """Escape, then turn *word* into an accent span."""
    s = html.escape(text or "")
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def cmd_build(a):
    doc = load(a.file)
    errs, warns, rows, total, pace = lint(doc)
    for e in errs:
        print("ERROR", e, file=sys.stderr)
    lang = doc.get("lang", "en")
    pal = {"bg": "#101418", "ink": "#f4f1ea", "accent": "#ffb347", "muted": "#7d8794"}
    pal.update(doc.get("palette") or {})
    fmt = doc.get("format", "16:9")
    w, h = {"16:9": (16, 9), "9:16": (9, 16), "1:1": (1, 1), "4:5": (4, 5)}.get(fmt, (16, 9))
    zh = lang == "zh-CN"
    parts = []
    for r in rows:
        b = r["beat"]
        inner = []
        if b.get("art"):
            inner.append('<div class="art">%s</div>' % b["art"])  # trusted, author-supplied SVG/HTML
        if b.get("screen"):
            inner.append('<div class="screen">%s</div>' % mark(b["screen"]))
        if b.get("picture") and not b.get("art"):
            inner.append('<div class="pic">%s</div>' % html.escape(b["picture"]))
        parts.append('<section class="beat m-%s"><span class="kind">%s · %s</span>%s</section>' % (
            html.escape(b.get("motion", "rise")), html.escape(b.get("id", "")),
            html.escape(b.get("part", "")), "".join(inner)))
    strip = "".join('<div style="--d:%s" title="%s %s">%s</div>' % (
        r["dur"], html.escape(r["beat"].get("id", "")), tc(r["start"]), html.escape(r["beat"].get("id", ""))) for r in rows)
    beats_js = json.dumps([{"id": r["beat"].get("id"), "dur": r["dur"], "vo": r["beat"].get("vo", "")} for r in rows],
                          ensure_ascii=False).replace("</", "<\\/")
    rate = max(0.6, min(1.6, pace / DEFAULT_PACE.get(lang, 2.3)))
    page = """<!doctype html>
<html lang="%(lang)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s - animatic</title>
<style>:root{--bg:%(bg)s;--ink:%(ink)s;--accent:%(accent)s;--muted:%(muted)s;--ar:%(ar)s;--arc:%(w)d/%(h)d}%(css)s</style></head>
<body><div id="wrap">
<div id="stage">%(beats)s<div id="sub"></div><div id="bar"></div></div>
<div id="strip">%(strip)s</div>
<div id="ctl"><button id="prev">◀</button><button id="play">▶ Play</button><button id="next">▶|</button>
<span id="time"></span><label><input type="checkbox" id="subs" checked> %(l_sub)s</label>
<label><input type="checkbox" id="voice"> %(l_voice)s</label></div>
</div>
<script>window.BEATS=%(bjs)s;window.LANG=%(langjs)s;window.RATE=%(rate).2f;%(js)s</script>
</body></html>
""" % {"lang": html.escape(lang), "title": html.escape(doc.get("title", "animatic")), "css": CSS, "js": JS,
       "bg": pal["bg"], "ink": pal["ink"], "accent": pal["accent"], "muted": pal["muted"],
       "ar": "%.4f" % (w / h), "w": w, "h": h, "beats": "\n".join(parts), "strip": strip, "bjs": beats_js,
       "langjs": json.dumps(lang), "rate": rate,
       "l_sub": "字幕" if zh else "subtitles", "l_voice": "草稿配音" if zh else "scratch voice"}
    out = a.o or re.sub(r"\.json$", "", a.file) + ".html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote %s  (%d beats, %s)%s" % (out, len(rows), tc(total), "  - fix the errors above" if errs else ""))


def cmd_sheet(a):
    doc = load(a.file)
    errs, warns, rows, total, pace = lint(doc)
    zh = doc.get("lang") == "zh-CN"
    L = (lambda en, cn: cn if zh else en)
    out = ["# %s" % doc.get("title", ""), "",
           "**%s** %s  " % (L("Viewer line:", "观众收获："), doc.get("viewer_line", "")),
           "**%s** %s · %s · %s %s" % (L("Format:", "画幅："), doc.get("format", "16:9"), tc(total),
                                      len(rows), L("beats", "拍")), ""]
    out.append("| # | %s | %s | %s | %s | %s | %s |" % (
        L("time", "时间"), L("narration", "旁白"), L("on screen", "屏幕文字"), L("picture", "画面"),
        L("motion / seam", "动作 / 衔接"), L("sec", "秒")))
    out.append("|---|---|---|---|---|---|---|")
    for r in rows:
        b = r["beat"]
        cell = lambda s: (s or "").replace("|", "\\|").replace("\n", " ")
        out.append("| %s | %s | %s | %s | %s | %s · %s | %.1f |" % (
            cell(b.get("id")), tc(r["start"]), cell(b.get("vo")), cell(b.get("screen")),
            cell(b.get("picture") or ("(art)" if b.get("art") else "-")), cell(b.get("motion")), cell(b.get("seam")), r["dur"]))
    if warns or errs:
        out += ["", "## %s" % L("Open issues", "待处理"), ""] + ["- %s" % x for x in errs + warns]
    path = a.o or re.sub(r"\.json$", "", a.file) + ".sheet.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote", path)


def main():
    p = argparse.ArgumentParser(description="explainer-animatic helper")
    s = p.add_subparsers(dest="cmd", required=True)
    n = s.add_parser("new"); n.add_argument("file"); n.add_argument("--lang", default="en", choices=["en", "zh-CN"])
    n.add_argument("--seconds", type=int, default=60); n.add_argument("--title")
    c = s.add_parser("check"); c.add_argument("file")
    b = s.add_parser("build"); b.add_argument("file"); b.add_argument("-o")
    h = s.add_parser("sheet"); h.add_argument("file"); h.add_argument("-o")
    a = p.parse_args()
    {"new": cmd_new, "check": cmd_check, "build": cmd_build, "sheet": cmd_sheet}[a.cmd](a)


if __name__ == "__main__":
    main()
