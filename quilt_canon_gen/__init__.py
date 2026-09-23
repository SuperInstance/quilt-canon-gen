"""quilt-canon-gen — creative canon generation + multi-model JEV verification."""
from .gen import generate_lore, generate_lore_pack
from .probe import probe_pack

__version__ = "0.1.0"
__all__ = ["generate_lore", "generate_lore_pack", "probe_pack"]
