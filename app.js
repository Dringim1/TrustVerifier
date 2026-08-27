import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionStatus, ExecutionResult } from "genlayer-js/types";

const CONTRACT_ADDRESS =
    "0x0829482B8be25A87805cE01c7488a9A48306a80E";

window.verifyClaim = async function () {
    const claim = document.getElementById("claim").value.trim();
    const source = document.getElementById("source").value.trim();

    const resultBox = document.getElementById("result");
    const resultText = document.getElementById("resultText");

    resultBox.style.display = "block";

    if (!claim || !source) {
        resultText.textContent =
            "Please enter both a claim and a source URL.";
        return;
    }

    try {
        if (!window.ethereum) {
            throw new Error("MetaMask was not detected.");
        }

        resultText.textContent = "Connecting to MetaMask...";

        const accounts = await window.ethereum.request({
            method: "eth_requestAccounts"
        });

        const account = accounts[0];

        const client = createClient({
            chain: studionet,
            account: account,
            provider: window.ethereum
        });

        resultText.textContent =
            "Submitting verification to GenLayer...";

        const transactionHash = await client.writeContract({
            address: CONTRACT_ADDRESS,
            functionName: "verify_claim",
            args: [claim, source],
            value: BigInt(0)
        });

        resultText.textContent =
            "Verification submitted. Waiting for finalized consensus...";

        const receipt = await client.waitForTransactionReceipt({
            hash: transactionHash,
            status: TransactionStatus.FINALIZED,
            interval: 5000,
            retries: 60
        });

        if (
            receipt.txExecutionResultName !==
            ExecutionResult.FINISHED_WITH_RETURN
        ) {
            throw new Error(
                "Verification transaction did not finish successfully."
            );
        }

        resultText.textContent =
            "Verification finalized. Retrieving the finalized verdict...";

        const verifications = await client.readContract({
            address: CONTRACT_ADDRESS,
            functionName: "get_verifications",
            args: []
        });

        if (!verifications || verifications.length === 0) {
            throw new Error(
                "No verification record was found."
            );
        }

        const verification =
            verifications[verifications.length - 1];

        resultText.innerHTML = `
            <strong>Verification Finalized</strong><br><br>
            <strong>Result:</strong> ${verification.result}<br>
            <strong>Status:</strong> ${verification.status}<br>
            <strong>Claim:</strong> ${verification.claim}<br>
            <strong>Source:</strong>
            <a href="${verification.source_url}" target="_blank">
                ${verification.source_url}
            </a><br>
            <strong>Verification ID:</strong> ${verification.id}<br>
            <strong>Verified At:</strong> ${verification.verified_at}<br><br>
            <strong>Transaction:</strong> ${transactionHash}
        `;

    } catch (error) {
        console.error(error);

        resultText.textContent =
            "Error: " + (error.message || error);
    }
};
