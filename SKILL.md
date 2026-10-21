---
name: explainer-animatic
description: Turn an idea, an article, a product, a lesson or a code change into a short explainer that is planned on the clock - one viewer line, a word budget, a spoken script, a beat sheet where every line of narration has a picture - and preview it as a playable, self-contained HTML animatic with subtitles and an optional scratch voice before anyone makes the real video. Use when the user asks for an explainer video, a 30/60/90-second script, a storyboard, a shot list, a "video version" of a doc, PR or launch, or 讲解视频 / 分镜 / 口播稿 / 动态分镜.
---

# Explainer Animatic

Plan a short explainer the way small animation studios do: settle the message, then the words, then the pictures, then watch the whole thing at real speed while changes are still cheap. The output is a beat file (`beats.json`), a playable HTML animatic, and a production sheet that any video tool, editor or person can build from.

## What this skill is for

Most "make me an explainer video" requests fail in the same three ways:

1. **Too many ideas.** The script tries to say everything in the source text, so nothing sticks.
2. **Words that do not fit the time.** A script that "reads in a minute" takes ninety seconds to speak; the video gets rushed or cut late.
3. **Pictures that only decorate.** Visuals are picked per scene in isolation, repeat the narration as text, or sit still for ten seconds.

This skill fixes the order of work. The agent writes one sentence about what the viewer will be able to do afterwards, turns the target length into a word budget, writes for the ear, gives every narration line its own picture and motion, checks the timing with a script, and builds an animatic you can watch, scrub and share. Only after the animatic passes a fresh-eyes review does anyone produce final footage.

It needs no video framework, account or API key. The final video can then be made in any tool: screen recording the animatic, a motion design tool, an HTML-to-video renderer, a video editor or a generative video service.

## When to use it

- "Make a 60-second explainer about ..." / "Turn this blog post into a short video."
- A launch, changelog or pull request that needs a "video version" for people who will not read it.
- A teacher or trainer who wants a short animated lesson on one concept.
- Any request for a storyboard, shot list, voice-over script, animatic or 分镜 / 口播稿.
- Reviewing an existing explainer script that feels too long or too flat.

Not for: long documentaries, live-action shoots with actors and locations, slide decks meant to be clicked through by a presenter, or music videos.

## Inputs to collect (ask only what is missing)

| Input | Default if the user does not say |
| --- | --- |
| Source material (text, doc, URL, PR, notes) | ask - this is required |
| Who watches, and where (feed, landing page, internal chat, class) | infer from the source, state the guess |
| Target length | 60 s (feeds: 30-45 s; tutorials: 90-120 s) |
| Format | 16:9; 9:16 for phone feeds; 1:1 or 4:5 for social posts |
| Language of narration | the user's language (`en` or `zh-CN`) |
| Voice: narration, or text-only (silent autoplay) | narration with subtitles |
| Brand colors | a calm dark palette with one accent |

## The method

### Step 1 - Write the viewer line

One sentence, written before anything else:

> After watching, **<who>** can **<do or say>** **<what>**.

It must name a person and an observable result. "Understand our platform" is not a result; "explain to a client why the first invoice is smaller" is. If the source contains three good ideas, pick one and list the other two as possible sequels. Keep the viewer line visible at the top of every artifact; every later cut is judged against it.

### Step 2 - Turn time into a word budget

Spoken narration is slower than reading. Plan with these rates, then measure with a real read if a voice exists:

| Language | Planning pace | 30 s | 60 s | 90 s |
| --- | --- | --- | --- | --- |
| English | ~2.3 words/s (130-150 wpm) | ~65 words | ~130 words | ~200 words |
| Chinese | ~4.2 characters/s (240-270 字/分) | ~125 字 | ~250 字 | ~380 字 |

Subtract about 10% for pauses, music in/out and the closing hold. Number-heavy or technical lines run slower; give them room. **If the script is over budget, cut words or beats, never speed up the voice.**

### Step 3 - Pick a spine

Choose one of these four shapes. Each part gets a rough share of the runtime.

| Spine | Parts and share | Good for |
| --- | --- | --- |
| **Snag -> Mechanism -> Proof -> Payoff -> Next** | 20 / 35 / 20 / 15 / 10 | products, habits, money, "why X works" |
| **Myth -> Twist -> Proof -> Rule** | 20 / 30 / 30 / 20 | correcting a common belief, concepts |
| **Before -> Change -> After -> Watch out** | 25 / 35 / 25 / 15 | changelogs, pull requests, process changes |
| **Count-up list** (hook + 3-5 items + wrap) | 15 / 70 / 15 | tips, mistakes, checklists |

The order of the video comes from the spine, not from the order of the source text. Reorder, merge and drop freely. The middle part (mechanism, twist, change, items) is where understanding happens; protect its time first.

### Step 4 - Write for the ear

Draft the narration as a list of lines, one idea per line.

- Short sentences: under ~20 English words or ~30 Chinese characters each.
- Concrete nouns and numbers that a listener can picture. Round numbers when the exact value does not matter ("about 280 thousand").
- Say numbers, units and acronyms the way a narrator would read them; expand an acronym on first use.
- One claim per line. If a line contains "and also", it is probably two beats.
- No warm-up ("In today's fast-moving world ..."), no logo-first intro; start inside the problem.
- One call to action at the end, phrased as a single doable step.
- Read the whole script aloud once (or have the scratch voice read it) before moving on.

### Step 5 - Build the beat sheet

Split the script into **beats**: one beat = one narration line + one picture. A 60-second explainer usually has 8-14 beats. Write them into `beats.json` (schema below). For every beat decide:

- **picture** - what the viewer sees, in one sentence a designer could draw. Choose a `kind`:
  - `type` - bold words alone on screen (for the key sentence and the call to action)
  - `diagram` - boxes, arrows, timelines, flows, before/after layouts
  - `number` - a big figure, a counter, a simple chart
  - `metaphor` - an everyday object standing in for the idea (a square splitting, a queue of cards)
  - `ui` - a simplified screen of the product or tool
- **screen** - on-screen words that *add* to the narration: the key term, the number, the label. At most ~6 English words or ~12 Chinese characters. Never paste the narration line onto the screen; subtitles already do that. Wrap a word in `*stars*` to color it with the accent.
- **motion** - one verb: `rise`, `slide`, `zoom`, `build` (parts appear one by one), `swap` (old value replaced by new), `hold` (deliberate stillness).
- **seam** - how this beat hands over to the next: `cut`, `cut on '<word>'` (the cut lands on a spoken word), `carry: <element>` (an element travels into the next beat), `hold` (a pause before the next), `end`.
- **hold** - extra seconds of stillness. Put a 0.4-0.8 s hold just before the payoff or the surprising number, and 1-2 s on the final beat.

Picture rules:

1. **Something changes about every three seconds.** A beat longer than ~8 s needs a change inside it (a build, a counter, a second label) or must be split.
2. **The eye has one place to go.** Each picture has one focal element; everything else is quieter.
3. **Keep a direction.** Pick a dominant flow (left-to-right for progress, upward for "better") and keep it; reverse only when the story reverses.
4. **Carry, don't dissolve.** When two beats share an element (a card, a number, a line), let it travel across the seam so the viewer's eye is handed over instead of reset.
5. **Visuals carry evidence.** Every number on screen must come from the source or a stated assumption; write the assumption into the narration ("assuming seven percent a year").
6. **Silent-viewer test.** Many viewers watch muted. With sound off, the screen words and pictures alone must still give the gist.

### Step 6 - Run the clock check

```bash
python3 scripts/animatic.py check beats.json
```

It counts English words or Chinese characters per beat, estimates spoken time plus a small pad, makes sure on-screen words have time to be read, adds holds, and prints a timecoded table. It flags: runtime more than 10% over target (error), beats over 8 s or under 1.2 s, missing pictures, overlong sentences, screen text that is too long or copies the narration, a missing payoff pause, and a viewer line that is still a template. Fix every error; decide consciously about each warning.

A beat may set `"seconds"` to lock its length (for example to match recorded audio); the check fails if the words need longer than the locked time.

### Step 7 - Build and watch the animatic

```bash
python3 scripts/animatic.py build beats.json -o animatic.html
```

Open the file in any browser. It plays every beat for its computed duration with the screen words, a picture description card (or your inline SVG/HTML `art`), the motion verb as a simple entrance, a progress bar, a clickable beat strip, subtitles, and an optional **scratch voice** that reads each line with the browser's built-in speech. Keys: Space play/pause, Left/Right previous/next beat, Home restart. Add `#b05` to the URL to open on a beat.

For important beats, replace the description card with a quick inline SVG in the `art` field: rough shapes are enough. The goal is to judge order, clarity and timing, not finish.

### Step 8 - Fresh-eyes review

Watch the animatic once, straight through, without pausing. Then run three tests (ideally with a person or a sub-agent that has not seen the source):

1. **Explain-back:** "In one sentence, what can you now do or say?" Compare with the viewer line. Any gap points to a missing or muddy beat.
2. **Mute test:** watch with subtitles and voice off. Is the gist still there?
3. **Blind test:** listen to the narration only (scratch voice, screen hidden). Does it still make sense as audio?

Collect all notes, fix them in one revision of `beats.json`, rerun `check` and `build`. Two rounds are normal; a third usually means the viewer line is too big.

### Step 9 - Hand off for production

```bash
python3 scripts/animatic.py sheet beats.json -o production-sheet.md
```

The production sheet is a timecoded table (narration, on-screen words, picture, motion, seam, seconds) plus any open issues. Hand it, the animatic and the final script to whoever or whatever makes the real video. When the final voice is recorded, put the real line lengths into `"seconds"` and rebuild so the picture timing follows the audio.

## beats.json schema

```json
{
  "title": "Start early or save more?",
  "lang": "en",
  "viewer_line": "After watching, <who> can <do or say> <what>.",
  "target_seconds": 60,
  "format": "16:9",
  "spine": "snag-mechanism-proof-payoff-next",
  "pace": 2.3,
  "palette": {"bg": "#0f1720", "ink": "#f3efe6", "accent": "#f5b041", "muted": "#7b8a99"},
  "beats": [
    {"id": "b01", "part": "snag", "vo": "Narration line.", "screen": "Key *term*",
     "picture": "What the viewer sees", "kind": "diagram", "motion": "build",
     "seam": "cut on 'term'", "hold": 0, "seconds": null, "art": "<svg>...</svg>"}
  ]
}
```

`lang` is `en` or `zh-CN`; `pace` is optional (words/s for English, characters/s for Chinese); `format` is `16:9`, `9:16`, `1:1` or `4:5`. `art` is optional author-written SVG or HTML and is inserted as-is, so only put your own markup there. Start a new file with `python3 scripts/animatic.py new beats.json --lang en --seconds 60`.

## Example (condensed)

Request: "Make a one-minute video that convinces new hires to start saving early."

- Viewer line: *After watching, a first-year employee can explain why ten years of saving from 25 can beat thirty years of saving from 35, and knows the one setting to change today.*
- Budget: 60 s -> ~130 words. Spine: Snag -> Mechanism -> Proof -> Payoff -> Next.
- Beats (excerpt):

| id | narration | screen | picture | motion / seam |
| --- | --- | --- | --- | --- |
| b04 | Leo puts in three times more money. So who ends up with more? | $24k vs $72k | two coin stacks, Leo's towering, a question mark lands | zoom, hold 0.6 s, cut on "more" |
| b06 | At seven percent a year, money roughly doubles every ten years. | 7% ≈ ×2 / 10 yrs | a curve with three marked doubling points | build, cut |
| b08 | ... Mia has about two hundred and eighty thousand. | Mia ≈ $281k | Mia's stack rises past the line where Leo's will stop | swap, carry Leo's stack |
| b10 | So today, switch on automatic saving, even if it is small. | Turn on auto-save today | a toggle slides to ON | slide, end, hold 1.5 s |

- `check`: 11 beats, 1:04, one warning resolved by splitting the proof into two beats.

Full files: `examples/early-start.json` (English, 60 s) and `examples/async-export.zh-CN.json` (Chinese, a pull request explained with Before -> Change -> After -> Watch out), each with its built animatic and production sheet.

## Tips

- If you cannot write the viewer line in one sentence, the video is not ready to plan. Ask the user to choose.
- Cutting a whole beat is usually better than trimming every line by a few words.
- Put the most surprising fact or number before the halfway mark; viewers leave early.
- Numbers on screen should be rounded the same way the narrator says them, or written slightly more precisely ("about 280 thousand" -> "≈ $281k"), never contradict them.
- For code changes, explain the effect on people first (what stops hurting), then the mechanism, then what others must change. Skip file names unless the audience will open those files.
- For Chinese narration, avoid long written-style clauses and stacked 的; read it aloud and split anything that makes you take a breath mid-sentence.
- Keep one accent color and use it for the single most important word or number per beat.
- When the user already has a script, still run Steps 1, 2 and 6: the viewer line and the clock check catch most problems in a pasted script.
- The animatic is a review tool. Do not polish its visuals; polish the order and the timing.
