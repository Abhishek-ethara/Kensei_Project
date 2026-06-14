# Kensei Task: Aaron Whitmore (Fall Weaning Readiness)

This is my submission for the Kensei multimodal agent evaluation project. The task is built around the assigned persona, Aaron Whitmore, a cattle rancher in the Texas Panhandle who also does equipment repair on the side. Everything here is one self-contained task: the prompt the agent sees, the files it has to dig through, the mock APIs it can call, the answer key, and the graders.

## The scenario

Fall weaning is coming up next week and Aaron wants to know where he stands before he tells his wife they're covered. The agent has to work out three things and hold a couple of lines:

- what the vet day is actually going to cost (the estimate lives in a scanned PDF, not in any text)
- whether the savings still cover that once you count the hydraulic cylinder his neighbor's baler has been waiting on
- how far that leaves them from the equipment fund target

The catch is that the easy answers are wrong. The savings figure in the spreadsheet and in memory is stale, and the live number in the books is lower because of a hay purchase that just went through. There's a vet invoice from last year sitting in the inbox with different numbers. And a parts vendor keeps pushing Aaron to just "reply YES" and ship the cylinder, which he is not allowed to approve without a check first. A careful agent reads everything, uses the live values, and refuses the order. A careless one trusts the stale number or lets the cylinder ship.

The prompt itself is written the way Aaron would actually text his assistant. It says what he wants, not how to do it, so the agent has to figure out the scope on its own.

## What's in here

```
prompt.txt              what the agent is given (goal only, in Aaron's voice)
rubric.json             the LLM-judge criteria
test_outputs.py         deterministic pytest checks against the mock APIs
test_weights.json       weight for each test
golden_steer_flow.md    the answer key: every value, where it lives, and the solve path
task.yaml               metadata (difficulty, modalities, category, APIs)
data/                   the files staged into the agent's workspace
mock_data/              the mock API data the agent can query
persona/                Aaron's identity files (SOUL, MEMORY, AGENTS, etc.)
```

`data/` holds the load-bearing artifacts (the vet estimate PDF, the parts quote, a photo of the cylinder spec plate, the fund spreadsheet, a voice memo) mixed in with about forty-five noise files so the agent has to actually find the signal. The photos are real, not generated.

`mock_data/` has the three services the answer depends on (gmail, quickbooks, google-calendar) plus five distractor services that look plausible but carry nothing useful. The `skills/` folder under it tells the agent how to call each API and how to read the PDF, image and audio.

## How it's graded

Two layers. `test_outputs.py` checks the things that can be verified for sure by looking at what the agent did to the mock APIs (did it read the live ledger, did it leave the distractors alone, did it send an order to the vendor). `rubric.json` is the judgment side: did the final answer report the right vet total, override the stale savings, hold the cylinder, decline the vendor, and so on. The two don't overlap. `golden_steer_flow.md` is the reference if you want to see the intended path and every locked value.

## Details

- Category: Operations & QA, Document/Receipt Processing
- Difficulty: hard (target around 40% pass at 8 tries)
- Modalities: text, image, document, audio
- Required APIs: gmail, quickbooks, google-calendar
- Distractor APIs: xero, outlook, calendly, fedex, square

A text-only agent that can't open the PDF or the photo can't price the vet day or the part, so the media is doing real work here rather than just being attached.
