import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import unittest

from quilt_canon_gen.gen import generate_lore, generate_lore_pack


class TestGen(unittest.TestCase):

    def test_gen_requires_zai(self):
        os.environ.pop("ZAI_TOKEN", None)
        with self.assertRaises(RuntimeError):
            generate_lore("test topic")


class TestLiveGen(unittest.TestCase):

    @unittest.skipUnless(os.environ.get("ZAI_TOKEN"), "ZAI_TOKEN not set")
    def test_generate_one_lore(self):
        result = generate_lore("the substrate walker canon", max_tokens=1000)
        self.assertGreater(len(result["lore"]), 100)
        print(f"\n  generated {result['chars']} chars on topic: {result['topic']}")
        print(f"  preview: {result['lore'][:200]}...")


if __name__ == "__main__":
    unittest.main()
