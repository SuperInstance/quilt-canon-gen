# Canon Generation Pipeline

The Quilt canon is the result of a **generation + verification** loop.
Generation proposes; verification gates. The chord hears both.

## Pipeline

```
topic → ZAI GLM-4.5 generation → lore text
lore text → multi-model JEV chord → composite score
composite ≥ 0.7 → canon-worthy (promoted)
composite < 0.7 → discarded (rejected)
```

## Why both stages?

A single model can both *generate* and *verify* — but its biases go
both ways. If a model tends to write in a certain voice, it'll tend
to score that voice highly. The chord breaks this loop.

**Generation** uses one voice (ZAI) for creativity.
**Verification** uses multiple voices (DeepInfra + ZAI + Gemini + DeepSeek)
for impartial judgment.

## Layered navigation

| Layer | Where |
|---|---|
| **CANON.md** | what this is, in 24 lines |
| **README** | quick start |
| **Gen Pipeline** | docs/GEN_PIPELINE.md (this file) |
| **Source** | quilt_canon_gen/gen.py + probe.py |
| **Tests** | tests/test_gen.py |

## License

MIT — Casey / SuperInstance, Sept 23, 2026
