# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing


class TrustVerifier(gl.Contract):
    claim: str
    source_url: str
    result: str
    status: str
    verified_at: str

    def __init__(self):
        self.claim = ""
        self.source_url = ""
        self.result = ""
        self.status = "NOT_VERIFIED"
        self.verified_at = ""

    @gl.public.write
    def verify_claim(self, claim: str, source_url: str) -> typing.Any:
        self.claim = claim
        self.source_url = source_url
        self.status = "VERIFYING"
        self.result = ""

        def evaluate_claim() -> str:
            response = gl.nondet.web.get(source_url)
            source_text = response.body.decode("utf-8")

            prompt = f"""
You are a claim verification system.

CLAIM:
{claim}

SOURCE:
{source_text}

Determine whether the source supports the claim.

Return exactly one word:
SUPPORTED
or
NOT_SUPPORTED
"""

            return gl.nondet.exec_prompt(prompt).strip()

        self.result = gl.eq_principle.prompt_comparative(
            evaluate_claim,
            principle="""
The verification result must be exactly SUPPORTED or NOT_SUPPORTED.

SUPPORTED means the source provides sufficient evidence supporting
the claim.

NOT_SUPPORTED means the source does not provide sufficient evidence
supporting the claim.
"""
        )

        self.status = self.result
        self.verified_at = gl.message_raw["datetime"]

        return self.result

    @gl.public.view
    def get_verification(self) -> dict:
        return {
            "claim": self.claim,
            "source_url": self.source_url,
            "result": self.result,
            "status": self.status,
            "verified_at": self.verified_at,
        }
