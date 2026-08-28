# TrustVerifier

TrustVerifier is a GenLayer-powered application for verifying whether a source provides sufficient evidence to support a claim.

## How It Works

1. The user enters a claim and a source URL.
2. The frontend calls the `verify_claim` method on the GenLayer Intelligent Contract.
3. The contract retrieves the source using GenLayer's native web access.
4. Validators independently evaluate whether the source supports the claim.
5. GenLayer consensus finalizes the verification result.
6. The finalized verification is stored on-chain.
7. The frontend retrieves the stored verification using `get_verifications()` and displays the finalized verdict.

## Intelligent Contract

The Intelligent Contract source is included in this repository:

- `trust_verifier.py`

Deployed contract address:

`0x0829482B8be25A87805cE01c7488a9A48306a80E`

### Contract Methods

- `verify_claim(claim, source_url)` — submits a claim and source URL for verification.
- `get_verifications()` — retrieves stored verification records.
- `get_verification(verification_id)` — retrieves a specific verification record.

## Frontend

The frontend consists of:

- `index.html` — user interface for entering claims and source URLs.
- `app.js` — connects to the deployed Intelligent Contract, submits `verify_claim`, waits for finalized execution, retrieves the stored verdict, and displays the verification result.

## Verification Result

Each verification record contains:

- Verification ID
- Claim
- Source URL
- Result
- Status
- Verification timestamp

Possible results are:

- `SUPPORTED`
- `NOT_SUPPORTED`

## Example

Claim:

`The Earth is approximately 4.5 billion years old.`

Source:

`https://science.nasa.gov/solar-system/earth/`

The contract processes the source through GenLayer consensus and stores the finalized verification result.

## Repository Structure

```text
TrustVerifier/
├── trust_verifier.py
├── app.js
├── index.html
├── package.json
├── package-lock.json
└── .github/
    └── workflows/
        └── main.yml
