import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

const CONTRACT_ADDRESS =
    "0x451cD41BB4Bf2C03239E28ED458d320795BB02Ef";

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

        resultText.textContent =
            "Preparing GenLayer transaction...";

        const client = createClient({
            chain: studionet,
            account: account,
            provider: window.ethereum
        });

        resultText.textContent =
            "Submitting verification to GenLayer...";

        const transaction = await client.writeContract({
            address: CONTRACT_ADDRESS,
            functionName: "verify_claim",
            args: [claim, source],
            value: BigInt(0)
        });

        resultText.textContent =
            "Verification submitted successfully: " + transaction;

    } catch (error) {
        console.error(error);

        resultText.textContent =
            "Error: " + (error.message || error);
    }
};