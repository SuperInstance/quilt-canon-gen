# quilt-canon-gen

> **Generation + verification in one substrate.**
> ZAI GLM-4.5 generates canon lore. Multi-model JEV verifies.

## TL;DR

```python
from quilt_canon_gen.gen import generate_lore_pack
from quilt_canon_gen.probe import probe_pack

# Step 1: generate
pack = generate_lore_pack([
    "the quantum substrate walker",
    "canon as chord, not vote",
])

# Step 2: verify with multi-model JEV
results = probe_pack(pack)
for r in results:
    print(f"{r['topic']}: composite={r['chord_composite']:.3f}, promoted={r['promoted']}")
```

## What this is

Canon needs both *production* (generation) and *gate* (verification).
This repo joins them in one pipeline:
1. **Generation**: ZAI GLM-4.5 generates canon-aligned lore
2. **Verification**: Multi-model JEV chord (DeepInfra etc.) probes each lore
3. **Promotion**: Lores with composite ≥ 0.7 are canon-worthy

## Architecture

```
topics → ZAI GLM-4.5 (gen.py)
            ↓
       lore texts (200-500 chars)
            ↓
       multi-model JEV chord (probe.py)
            ↓
       {composite, variance, promoted}
```

## License

MIT — Casey / SuperInstance, Sept 23, 2026
