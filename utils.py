import requests
import json
import prompts
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.getenv("MISTRAL_API_KEY")



def extract_intent_signals(raw_text):
    #url of api
    base_url = "https://api.mistral.ai/v1/chat/completions"
    #headers needed
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    #payload of model
    payload = {
        "model": "mistral-small-latest",
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": prompts.prompt_intent
            },
            {
                "role": "user",
                "content": raw_text
            }
        ]
    }
    #the request
    response = requests.post(base_url, headers=headers, json=payload)
    #the content we have
    content = response.json()["choices"][0]["message"]["content"]
    #raise the exception if the response is unsuccessful
    response.raise_for_status()
    #CONTENT CLEANUP
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()
    #RETURNING POST CLEANUP
    return json.loads(content)

def estimate_buy_probability(signals):
    #url of api
    base_url = "https://api.mistral.ai/v1/chat/completions"
    #headers needed
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    #payload of model
    payload = {
        "model": "mistral-small-latest",
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": prompts.probability_prompt
            },
            {
                "role": "user",
                "content": json.dumps(signals)
            }
        ]
    }
    #the request
    response = requests.post(base_url, headers=headers, json=payload)
    #raise the exception if the response is unsuccessful
    response.raise_for_status()
    #the content we have
    content = response.json()["choices"][0]["message"]["content"]
    #CONTENT CLEANUP
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()
    #RETURNING POST CLEANUP
    return json.loads(content)

def detect_disqualifiers(raw_text, signals):
    disqualifiers = {
        "authority": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Lead lacks decision-making authority or is explicitly not the buyer",
        },
        "budget": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Lead has no budget or explicitly rejects paying for software",
        },
        "segment_fit": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Lead does not belong to the target customer segment",
        },
        "intent": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Lead explicitly states non-buying or purely informational intent",
        },
        "timing": {
            "present": False,
            "severity": "soft",
            "confidence": 0.0,
            "evidence": None,
            "description": "Buying timeline is too far out or undefined",
        },
        "competitive_lock": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Lead is locked into a competitor or cannot switch vendors",
        },
        "use_case_fit": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Requested use case is incompatible with product capabilities",
        },
        "signal_quality": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Input is low-quality, nonsensical, or bot-generated",
        },
        "compliance_or_policy": {
            "present": False,
            "severity": "hard",
            "confidence": 0.0,
            "evidence": None,
            "description": "Company policy, legal, or compliance rules prevent purchase",
        },
        "churn_risk": {
            "present": False,
            "severity": "soft",
            "confidence": 0.0,
            "evidence": None,
            "description": "High likelihood of short-term churn even if conversion occurs",
        },
    }

    base_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-small-latest",
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": prompts.disqualifier_prompt
            },
            {
                "role": "user",
                "content": json.dumps({
                    "raw_text": raw_text,
                    "signals": signals,
                    "schema": disqualifiers
                })
            }
        ]
    }
    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()
    return json.loads(content)

def score_lead(signals, buy_probability, disqualifiers):
    base_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-small-latest",
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": prompts.scoring_prompt
            },
            {
                "role": "user",
                "content": json.dumps({
                    "signals": signals,
                    "buy_probability": buy_probability,
                    "disqualifiers": disqualifiers
                })
            }
        ]
    }
    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()
    return json.loads(content)
    
def make_decision(score):
    base_url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small-latest",
        "temperature": 0.0,
        "messages": [
            {
                "role": "system",
                "content": prompts.decision_prompt
            },
            {
                "role": "user",
                "content": json.dumps(score)
            }
        ]
    }

    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    # CONTENT CLEANUP (same pattern as everywhere else)
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return json.loads(content)

def explain_decision(score):
    base_url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small-latest",
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": prompts.explain_decision_prompt
            },
            {
                "role": "user",
                "content": json.dumps(score)
            }
        ]
    }

    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    # CONTENT CLEANUP (same pattern as everywhere else)
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return json.loads(content)
