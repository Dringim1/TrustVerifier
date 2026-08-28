import unittest
from pathlib import Path


CONTRACT = (
    Path(__file__).resolve().parent.parent / "trust_verifier.py"
).read_text(encoding="utf-8")


class TrustVerifierContractTest(unittest.TestCase):

    def test_contract_class_exists(self):
        self.assertIn("class TrustVerifier(gl.Contract):", CONTRACT)

    def test_verification_storage_exists(self):
        self.assertIn("verifications: DynArray[Verification]", CONTRACT)
        self.assertIn("next_id: u256", CONTRACT)

    def test_verify_claim_exists(self):
        self.assertIn(
            "def verify_claim(self, claim: str, source_url: str)",
            CONTRACT,
        )

    def test_web_source_retrieval_exists(self):
        self.assertIn("gl.nondet.web.get(source_url)", CONTRACT)

    def test_consensus_verification_exists(self):
        self.assertIn(
            "gl.eq_principle.prompt_comparative",
            CONTRACT,
        )

    def test_result_values_are_restricted(self):
        self.assertIn('"SUPPORTED"', CONTRACT)
        self.assertIn('"NOT_SUPPORTED"', CONTRACT)

    def test_verification_retrieval_methods_exist(self):
        self.assertIn("def get_verifications(self)", CONTRACT)
        self.assertIn(
            "def get_verification(self, verification_id: u256)",
            CONTRACT,
        )


if __name__ == "__main__":
    unittest.main()
