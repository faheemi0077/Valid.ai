from fastapi import FastAPI
from pydantic import BaseModel
import utils

app = FastAPI()

class LeadInput(BaseModel):
    text: str

@app.post("/analyze-lead")
def analyze_lead(data: LeadInput):
    signals = utils.extract_intent_signals(data.text)
    probability = utils.estimate_buy_probability(signals)
    disqualifiers = utils.detect_disqualifiers(data.text, signals)
    score = utils.score_lead(signals, probability, disqualifiers)
    decision = utils.make_decision(score)
    explanation = utils.explain_decision(score)

    return {
        "signals": signals,
        "probability": probability,
        "disqualifiers": disqualifiers,
        "score": score,
        "decision": decision,
        "explanation": explanation
    }