import os
from flask import Flask, render_template_string
from google.cloud import firestore

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html>
<head>
<title>LogiSense AI Dashboard</title>
<meta http-equiv="refresh" content="20">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Google Sans, sans-serif; background: #f1f3f4; }
.nav { background: #1a73e8; padding: 16px 24px; color: white; }
.nav h1 { font-size: 20px; font-weight: 500; }
.nav p { font-size: 12px; opacity: 0.85; margin-top: 4px; }
.container { padding: 24px; }
table { width: 100%; border-collapse: collapse; background: white;
        border-radius: 8px; overflow: hidden;
        box-shadow: 0 1px 6px rgba(0,0,0,0.1); }
th { background: #1a73e8; color: white; padding: 12px 16px;
     text-align: left; font-size: 13px; font-weight: 500; }
td { padding: 12px 16px; border-bottom: 1px solid #f0f0f0; font-size: 13px; color: #202124; }
tr:last-child td { border: none; }
tr:hover td { background: #f8f9fa; }
.hi { color: #c5221f; font-weight: 600; }
.md { color: #b06000; font-weight: 600; }
.lo { color: #188038; font-weight: 600; }
.empty { text-align: center; padding: 80px; color: #999; font-size: 15px; }
.badge { display: inline-block; padding: 2px 10px; border-radius: 99px; font-size: 11px; font-weight: 600; }
.badge-hi { background: #fce8e6; color: #c5221f; }
.badge-md { background: #fef7e0; color: #b06000; }
.badge-lo { background: #e6f4ea; color: #188038; }
</style>
</head>
<body>
<div class="nav">
  <h1>LogiSense AI — Supply Chain Dashboard</h1>
  <p>Powered by Gemini 1.5 Flash on Google Cloud · Auto-refreshes every 20s</p>
</div>
<div class="container">
{% if shipments %}
<table>
  <tr>
    <th>Shipment ID</th>
    <th>Location</th>
    <th>Weather</th>
    <th>Risk Score</th>
    <th>AI Risk Reason</th>
    <th>Recommended Action</th>
  </tr>
  {% for s in shipments %}
  <tr>
    <td><b>{{ s.get('shipment_id','—') }}</b></td>
    <td>{{ s.get('location','—') }}</td>
    <td>{{ s.get('weather','—') }}</td>
    <td>
      {% set r = s.get('risk_score', 0)|int %}
      {% if r > 70 %}
        <span class="badge badge-hi">{{ r }}/100 HIGH</span>
      {% elif r > 40 %}
        <span class="badge badge-md">{{ r }}/100 MEDIUM</span>
      {% else %}
        <span class="badge badge-lo">{{ r }}/100 LOW</span>
      {% endif %}
    </td>
    <td>{{ s.get('risk_reason','—') }}</td>
    <td>{{ s.get('recommended_action','—') }}</td>
  </tr>
  {% endfor %}
</table>
{% else %}
<div class="empty">No shipments yet. Run the analyzer to see Gemini analysis here.</div>
{% endif %}
</div>
</body>
</html>"""

@app.route("/")
def index():
    try:
        db = firestore.Client()
        docs = list(db.collection("shipments").stream())
        shipments = [d.to_dict() for d in docs]
    except Exception as e:
        print(f"Error: {e}")
        shipments = []
    return render_template_string(HTML, shipments=shipments)

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
