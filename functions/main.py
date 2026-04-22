import json
import base64
from google.cloud import firestore
import vertexai
from vertexai.preview.generative_models import GenerativeModel

def analyze_shipment(event, context):
    raw = base64.b64decode(event['data']).decode()
    data = json.loads(raw)
    vertexai.init(project="supply-chain-491404", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash")
    prompt = (
        "You are a supply chain risk analyst. "
        "Analyze this shipment and return ONLY a JSON object with no extra text. "
        "Shipment: " + json.dumps(data) + " "
        'Return exactly: {"risk_score": 75, "risk_reason": "reason", "recommended_action": "action"}'
    )
    resp = model.generate_content(prompt)
    txt = resp.text.strip()
    if "```" in txt:
        txt = txt.split("```")[1]
        if txt.startswith("json"):
            txt = txt[4:]
    result = json.loads(txt.strip())
    db = firestore.Client()
    db.collection("shipments").document(data["shipment_id"]).set({**data, **result})
    print(f"Done: {data['shipment_id']} risk={result['risk_score']}")
