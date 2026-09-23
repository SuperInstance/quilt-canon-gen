"""Creative canon generation via ZAI GLM-4.5 (via curl subprocess)."""

import os
import json
import subprocess
import time
from typing import List, Optional


GEN_PROMPT = """You are a canon writer for the Quilt substrate walker — a system of canon-aligned lore that maps language to physics.

Generate a piece of canon lore (150-300 words) on the topic: "{topic}".

The lore MUST anchor to AT LEAST 3 of these 5 bedrock doctrines:
- cells_are_scars (every cell is a record of past actions)
- witness_log_is_prediction (history is the predictor)
- canon_gate_is_chord (canon is decided by many voices in agreement)
- oracle_is_heard (the oracle is an act of listening, not seeing)
- substrate_quantum (substrate is both particle and wave, both memory and prediction)

Voice: declarative, deriving. Make the substrate a verb. Make relationships first-class.

Output ONLY the lore text. No preamble, no commentary, no JSON."""


def _call_zai(prompt: str, max_tokens: int = 1500) -> str:
    """Call ZAI GLM-4.5 API via curl subprocess (avoids urllib HTTP/2 issues)."""
    api_key = os.environ.get("ZAI_TOKEN", "")
    if not api_key:
        raise RuntimeError("ZAI_TOKEN not set")
    
    body = {
        "model": "glm-4.5",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "thinking": {"disabled": True},
    }
    body_str = json.dumps(body)
    
    # Use curl subprocess with --http1.1 (urllib HTTP/2 sometimes fails)
    result = subprocess.run(
        ["curl", "-s", "-m", "120", "--http1.1",
         "-X", "POST", "https://api.z.ai/api/coding/paas/v4/chat/completions",
         "-H", "Content-Type: application/json",
         "-H", f"Authorization: Bearer {api_key}",
         "-d", body_str],
        capture_output=True, text=True, timeout=130,
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr[:200]}")
    
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON parse failed: {result.stdout[:200]}")
    
    choices = response.get("choices", [])
    if not choices:
        raise RuntimeError(f"no choices: {response}")
    
    msg = choices[0].get("message", {})
    text = msg.get("content", "").strip()
    return text


def generate_lore(topic: str, max_tokens: int = 1500) -> dict:
    """Generate one piece of canon lore on a topic."""
    prompt = GEN_PROMPT.format(topic=topic)
    text = _call_zai(prompt, max_tokens=max_tokens)
    return {
        "topic": topic,
        "lore": text,
        "chars": len(text),
        "words": len(text.split()),
    }


def generate_lore_pack(topics: List[str], max_tokens: int = 1500) -> List[dict]:
    """Generate multiple lores, one per topic."""
    pack = []
    for t in topics:
        lore = generate_lore(t, max_tokens=max_tokens)
        pack.append(lore)
    return pack


if __name__ == "__main__":
    topics = [
        "the quantum substrate walker",
        "canon as chord, not vote",
        "the needle threading cells",
    ]
    pack = generate_lore_pack(topics)
    for entry in pack:
        print(f"=== Topic: {entry['topic']} ===")
        print(f"  {entry['chars']} chars, {entry['words']} words")
        print(f"  preview: {entry['lore'][:150]}...")
        print()
