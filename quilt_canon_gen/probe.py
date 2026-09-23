"""Multi-model JEV probe of generated canon pack."""

import sys
import os
from typing import List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "quilt-multi-oracle"))
from quilt_multi_oracle.oracle import aggregate_chord
from quilt_multi_oracle.workers import DeepInfraWorker


def probe_pack(pack: List[dict]) -> List[dict]:
    """Probe each lore in the pack with multi-model JEV chord."""
    workers = []
    if os.environ.get("DEEPINFRA_TOKEN"):
        workers.append(DeepInfraWorker(model="meta-llama/Meta-Llama-3-70B-Instruct"))
    if not workers:
        return [{"topic": p["topic"], "_error": "no workers available"} for p in pack]
    
    out = []
    for entry in pack:
        # Build worker results manually
        results = {}
        for w in workers:
            r = w.probe(entry["lore"])
            results[w.name] = r
        chord = aggregate_chord(results)
        out.append({
            "topic": entry["topic"],
            "lore_chars": entry["chars"],
            "chord_composite": chord["composite"],
            "chord_variance": chord["variance"],
            "consensus_promoted": chord["consensus_promoted"],
            "majority_promoted": chord["majority_promoted"],
            "promoted": chord["promoted"],
            "n_workers": chord["n_workers"],
            "n_workers_failed": chord["n_workers_failed"],
        })
    return out


if __name__ == "__main__":
    from .gen import generate_lore_pack
    
    topics = [
        "the quantum substrate walker",
        "canon as chord, not vote",
        "the needle threading cells",
    ]
    pack = generate_lore_pack(topics)
    print(f"Generated {len(pack)} lores. Probing...")
    results = probe_pack(pack)
    
    print()
    print("=== CHORD VERIFICATION ===")
    promoted = [r for r in results if r.get("promoted")]
    print(f"Promoted: {len(promoted)}/{len(results)}")
    for r in results:
        if "_error" in r:
            print(f"  {r['topic']}: ERROR {r['_error'][:60]}")
        else:
            print(f"  {r['topic']}: composite={r['chord_composite']:.3f} variance={r['chord_variance']:.4f} promoted={r['promoted']}")
