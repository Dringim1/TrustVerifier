# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing
import json
from dataclasses import dataclass


@allow_storage
@dataclass
class Verification:
    id: u256
    claim: str
    source_url: str
    result: str
    status: str
    verified_at: str


class TrustVerifier(gl.Contract):
    verifications: DynArray[Verification]
    next_id: u256

    def __init__(self):
        self.next_id = u256(1)

    @gl.public.write
    def verify_claim(self, claim: str, source_url: str) -> typing.Any:
        verification_id = self.next_id
        self.next_id += u256(1)

        def evaluate_claim() -> str:
            response = gl.nondet.web.get(source_url)
            source_text = response.body.decode("utf-8")

            prompt = f"""
You are a reliable source verification system.

CLAIM:
{claim}

SOURCE URL:
{source_url}

SOURCE CONTENT:
{source_text}

Determine whether the source content provides sufficient evidence
to support the claim.

Return JSON only:
{{
  "result": "SUPPORTED"
}}

or

{{
  "result": "NOT_SUPPORTED"
}}

Rules:
- Use SUPPORTED only when the source clearly supports the claim.
- Use NOT_SUPPORTED when the source does not provide sufficient evidence.
- Do not use any other result.
"""

            response = gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

            if isinstance(response, dict):
                result = response.get("result", "NOT_SUPPORTED")
            else:
                try:
                    parsed = json.loads(response)
                    result = parsed.get("result", "NOT_SUPPORTED")
                except Exception:
                    result = "NOT_SUPPORTED"

            result = str(result).strip().upper()

            if result != "SUPPORTED":
                result = "NOT_SUPPORTED"

            return result

        result = gl.eq_principle.prompt_comparative(
            evaluate_claim,
            principle="""
The verification result must be exactly one of:
SUPPORTED
NOT_SUPPORTED

The validators must agree on the result.

SUPPORTED means the source provides sufficient evidence
to support the claim.

NOT_SUPPORTED means the source does not provide sufficient
evidence to support the claim.
"""
        )

        result = str(result).strip().upper()

        if result != "SUPPORTED":
            result = "NOT_SUPPORTED"

        verification = Verification(
            id=verification_id,
            claim=claim,
            source_url=source_url,
            result=result,
            status=result,
            verified_at=gl.message_raw["datetime"],
        )

        self.verifications.append(verification)

        return {
            "id": verification_id,
            "result": result,
            "status": result,
        }

    @gl.public.view
    def get_verifications(self) -> list:
        return list(self.verifications)

    @gl.public.view
    def get_verification(self, verification_id: u256) -> typing.Any:
        for verification in self.verifications:
            if verification.id == verification_id:
                return verification

        return {
            "error": "Verification not found"
        }
