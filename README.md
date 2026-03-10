# AI Lead Qualification API

This project is an API that analyzes inbound lead messages and determines whether the lead should be shown a Calendly scheduling link.

The system extracts structured intent signals from free-form text, evaluates purchase probability, detects disqualifiers, and produces a final qualification decision.

The goal is to automate the early stages of B2B lead qualification and filter out low-quality leads before a sales call.

## Features

- Lead intent signal extraction from raw text
- Purchase probability estimation
- Detection of sales disqualifiers (budget, authority, timing, etc.)
- Deterministic lead scoring system
- Final policy decision for whether to show a scheduling link
- Explanation of the final decision
- REST API built with FastAPI

## How It Works

The system processes lead messages through several stages:

1. **Intent Extraction**
   - Extracts structured signals such as budget, timeline, authority, and commitment.

2. **Probability Estimation**
   - Estimates the likelihood that the lead will purchase.

3. **Disqualifier Detection**
   - Detects signals such as lack of authority, no budget, wrong segment, or competitor lock-in.

4. **Lead Scoring**
   - Generates a lead score and classification (Reject, Qualified, Priority).

5. **Decision Policy**
   - Determines whether the lead should be shown a Calendly scheduling link.

6. **Decision Explanation**
   - Generates a short explanation describing why the decision was made.

The system uses the Mistral API to perform structured reasoning tasks such as signal extraction and decision evaluation.
