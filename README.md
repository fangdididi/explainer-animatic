**English** | [简体中文](README.zh-CN.md)

# Explainer Animatic

> An agent skill that plans a short explainer video on the clock and lets you watch it before it exists: one viewer line, a word budget, a script written for the ear, a beat sheet where every narration line has its own picture, a timing check, and a playable HTML animatic with subtitles and a scratch voice.

Ask an AI agent for "a 60-second video about X" and you usually get a script that is too long to speak in 60 seconds, tries to say everything in the source, and comes with a scene list that repeats the narration as on-screen text. You only find out when the video is already made.

**Explainer Animatic** gives the agent the order of work small animation studios use. It pins down what the viewer will be able to do afterwards, turns the length into a word budget, picks a story spine, writes short spoken lines, gives each line a picture, a motion and a hand-off to the next beat, then checks the timing with a script and builds a single HTML file you can play, scrub and share. Fix the order and the timing there, while it costs minutes; then make the real video in whatever tool you like.

It works for product and feature explainers, concept lessons, changelogs and pull requests, tips lists and internal announcements, in English and Chinese.

## Features

- **Viewer line first.** "After watching, <who> can <do or say> <what>." Every later cut is judged against it.
- **Word budget from length.** About 2.3 words/s for English and 4.2 characters/s for Chinese, with room for pauses. Over budget means cut, never speed up.
- **Four story spines.** Snag -> Mechanism -> Proof -> Payoff -> Next; Myth -> Twist -> Proof -> Rule; Before -> Change -> After -> Watch out; Count-up list. Each with runtime shares.
- **Ear-first script rules.** One idea per line, short sentences, numbers said the way a narrator reads them, one call to action.
- **Beat sheet with intent.** Each beat has narration, on-screen words that add rather than repeat, a picture of one of five kinds (type, diagram, number, metaphor, UI), a motion verb, a seam (cut, cut on a word, carry an element, hold) and optional stillness before the payoff.
- **Clock check.** `animatic.py check` estimates spoken and reading time per beat, prints a timecoded table, and flags overruns, beats that sit too long or flash by, missing pictures, overlong sentences and screen text that copies the narration.
- **Playable animatic.** `animatic.py build` writes one self-contained HTML file: timed beats, simple entrances per motion verb, subtitles, a clickable beat strip, keyboard controls, deep links to a beat, and an optional scratch voice using the browser's own speech. Drop inline SVG into any beat to sketch it.
- **Fresh-eyes review.** Explain-back, mute and blind-listen tests before anything is produced.
- **Production sheet.** `animatic.py sheet` writes a timecoded Markdown shot list for editors, motion designers, HTML-to-video renderers or generative video tools.
- **Zero dependencies.** One Python 3.8+ script, standard library only. No account, no API key.
- **Bilingual.** Beat files, timing and the player UI in English or Chinese (`"lang": "zh-CN"`).

## Installation

Clone the repository into your agent's skills folder. The folder name should be `explainer-animatic`.

**Claude Code**

```bash
# personal (all projects)
git clone https://github.com/fangdididi/explainer-animatic ~/.claude/skills/explainer-animatic
# or for one project
git clone https://github.com/fangdididi/explainer-animatic .claude/skills/explainer-animatic
```

**OpenAI Codex CLI**

```bash
git clone https://github.com/fangdididi/explainer-animatic ~/.codex/skills/explainer-animatic
```

**Cursor**

```bash
git clone https://github.com/fangdididi/explainer-animatic .cursor/skills/explainer-animatic
```

**Gemini CLI, OpenCode, Windsurf and other agents**

Clone into the agent's skills directory if it has one (for example `.agents/skills/`). If your agent has no skill system, add a line to `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or your rules file:

```text
When I ask for an explainer video, a short video script or a storyboard, follow ./explainer-animatic/SKILL.md and keep the beats in beats.json.
```

Requirement: Python 3.8 or newer for the helper script, and any modern browser to watch the animatic. The method itself works without them.

## Usage

Just ask in plain words:

- "Make a 60-second explainer that convinces new hires to start saving early."
- "Turn this pull request into a 45-second video for the support team."
- "Here is my blog post. I need a 30-second vertical video script with a storyboard."
- "把这篇产品介绍做成 60 秒的讲解视频分镜。"

The agent will write the viewer line, propose the spine and budget, draft the script, fill `beats.json`, and run the helper:

```bash
python3 scripts/animatic.py new beats.json --lang en --seconds 60   # starter file
python3 scripts/animatic.py check beats.json                        # timing + lint, exit 1 on errors
python3 scripts/animatic.py build beats.json -o animatic.html       # playable animatic
python3 scripts/animatic.py sheet beats.json -o production-sheet.md # shot list for production
```

Open `animatic.html` in a browser. Space plays and pauses, Left/Right step between beats, Home restarts, and `animatic.html#b05` opens on beat `b05`. Tick **scratch voice** to hear each line read aloud.

## Example

From `examples/early-start.json` (English, 60 s, "start saving early"):

```text
Start early or save more?  (en, pace 2.3 words/s)
id    start   part           vo screen    dur  picture
b01   0:00.0  snag         2.6s   1.1s   3.0s  Two simple figures side by side, identical name
b02   0:03.0  snag         5.2s   1.4s   5.6s  Mia's card grows a short bar labelled 10 years
...
b06   0:27.9  mechanism    4.8s   1.6s   5.2s  A curve with three marked doubling steps
...
b10   0:57.6  next         4.8s   1.6s   6.7s  A toggle in a banking app slides to ON
total 1:04.3  |  11 beats  |  131 spoken words  |  target 60
OK
```

The first draft had the proof as one 8.9-second beat; the check flagged it, so it became two beats with a carry between them.

`examples/async-export.zh-CN.json` shows the Before -> Change -> After -> Watch out spine on a code change, in Chinese, with an inline SVG diagram in one beat. Both examples include the built `.html` animatic and `.sheet.md` production sheet.

## File structure

```text
explainer-animatic/
├── SKILL.md                    # the skill (English)
├── SKILL.zh-CN.md              # the skill (Chinese)
├── README.md
├── README.zh-CN.md
├── LICENSE
├── scripts/
│   └── animatic.py             # new / check / build / sheet
└── examples/
    ├── early-start.json        # English, 60 s, money explainer
    ├── early-start.html        # built animatic
    ├── early-start.sheet.md    # production sheet
    ├── async-export.zh-CN.json # Chinese, 45 s, pull request explainer
    ├── async-export.zh-CN.html
    └── async-export.zh-CN.sheet.md
```

## License

MIT © fangdididi
