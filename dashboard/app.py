import os
from flask import Flask, render_template_string, jsonify
from google.cloud import firestore
from datetime import datetime

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html>
<head>
<title>LogiSense AI — Supply Chain Dashboard</title>
<meta http-equiv="refresh" content="20">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Google Sans, sans-serif; background: #f1f3f4; }
.nav {
  background: linear-gradient(135deg, #1a73e8, #0d47a1);
  padding: 16px 24px; color: white;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.nav-left h1 { font-size: 20px; font-weight: 500; }
.nav-left p { font-size: 12px; opacity: 0.85; margin-top: 4px; }
.nav-right { display: flex; gap: 12px; }
.stat-box {
  background: rgba(255,255,255,0.15);
  border-radius: 8px; padding: 8px 16px; text-align: center;
}
.stat-box .num { font-size: 22px; font-weight: 600; }
.stat-box .lbl { font-size: 10px; opacity: 0.85; text-transform: uppercase; }
.container { padding: 24px; }
.summary-cards { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.card {
  background: white; border-radius: 10px; padding: 16px 20px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.08);
  border-left: 4px solid #eee;
}
.card.critical { border-left-color: #b71c1c; }
.card.high { border-left-color: #c5221f; }
.card.medium { border-left-color: #b06000; }
.card.low { border-left-color: #188038; }
.card .card-num { font-size: 32px; font-weight: 600; color: #202124; }
.card .card-lbl { font-size: 12px; color: #666; margin-top: 4px; }
.card .card-icon { font-size: 24px; float: right; }
.section-title {
  font-size: 15px; font-weight: 500; color: #202124;
  margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
}
.live-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #34a853; animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(52,168,83,0.6); }
  70% { box-shadow: 0 0 0 8px rgba(52,168,83,0); }
  100% { box-shadow: 0 0 0 0 rgba(52,168,83,0); }
}
table {
  width: 100%; border-collapse: collapse; background: white;
  border-radius: 10px; overflow: hidden;
  box-shadow: 0 1px 6px rgba(0,0,0,0.08);
}
th {
  background: #1a73e8; color: white; padding: 12px 14px;
  text-align: left; font-size: 12px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.04em;
}
td { padding: 12px 14px; border-bottom: 1px solid #f0f0f0; font-size: 13px; color: #202124; vertical-align: top; }
tr:last-child td { border: none; }
tr:hover td { background: #f8f9fa; }
.badge {
  display: inline-block; padding: 3px 10px;
  border-radius: 99px; font-size: 11px; font-weight: 600;
}
.badge-critical { background: #3c0000; color: #ff8a80; }
.badge-high { background: #fce8e6; color: #c5221f; }
.badge-medium { background: #fef7e0; color: #b06000; }
.badge-low { background: #e6f4ea; color: #188038; }
.risk-bar-bg { background: #f0f0f0; border-radius: 4px; height: 6px; margin-top: 4px; width: 80px; }
.risk-bar { height: 6px; border-radius: 4px; }
.tag { display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-top: 4px; }
.alert-tag { background: #fce8e6; color: #c5221f; }
.empty { text-align: center; padding: 80px; color: #999; }
.footer { text-align: center; padding: 16px; font-size: 12px; color: #999; margin-top: 24px; }
.gemini-badge { background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; }
</style>
</head>
<body>

<div class="nav">
  <div class="nav-left">
    <h1>LogiSense AI — Supply Chain Intelligence Platform</h1>
    <p>Powered by Gemini 2.0 Flash · Google Cloud · Real-time Disruption Detection & Rerouting</p>
  </div>
  <div class="nav-right">
    <div class="stat-box">
      <div class="num">{{ shipments|length }}</div>
      <div class="lbl">Active Shipments</div>
    </div>
    <div class="stat-box">
      <div class="num">{{ critical_count + high_count }}</div>
      <div class="lbl">Needs Action</div>
    </div>
  </div>
</div>

<div class="container">

  <div class="summary-cards">
    <div class="card critical">
      <span class="card-icon">🚨</span>
      <div class="card-num">{{ critical_count }}</div>
      <div class="card-lbl">Critical Risk</div>
    </div>
    <div class="card high">
      <span class="card-icon">⚠️</span>
      <div class="card-num">{{ high_count }}</div>
      <div class="card-lbl">High Risk</div>
    </div>
    <div class="card medium">
      <span class="card-icon">📊</span>
      <div class="card-num">{{ medium_count }}</div>
      <div class="card-lbl">Medium Risk</div>
    </div>
    <div class="card low">
      <span class="card-icon">✅</span>
      <div class="card-num">{{ low_count }}</div>
      <div class="card-lbl">On Track</div>
    </div>
  </div>

  <div class="section-title">
    <div class="live-dot"></div>
    Live Shipment Intelligence · Auto-refreshes every 20s
    <span class="gemini-badge">⚡ Gemini 2.0 Flash AI</span>
  </div>

  {% if shipments %}
  <table>
    <tr>
      <th>Shipment</th>
      <th>Route</th>
      <th>Cargo & Carrier</th>
      <th>Conditions</th>
      <th>Risk Score</th>
      <th>AI Risk Analysis</th>
      <th>Recommended Action</th>
      <th>Alternate Route</th>
      <th>Impact</th>
    </tr>
    {% for s in shipments %}
    <tr>
      <td><b>{{ s.get('shipment_id','—') }}</b></td>
      <td>
        {{ s.get('origin','—') }}<br>
        <small style="color:#666">→ {{ s.get('destination','—') }}</small>
      </td>
      <td>
        <span class="tag">{{ s.get('cargo_type','—') }}</span><br>
        <small style="color:#666;margin-top:4px;display:block">{{ s.get('carrier','—') }}</small>
      </td>
      <td>
        {{ s.get('weather','—') }}<br>
        <small style="color:#666">Congestion: {{ (s.get('port_congestion_score',0)*100)|int }}%</small><br>
        <small style="color:#666">Delay: {{ s.get('carrier_delay_hrs',0) }}hrs</small>
      </td>
      <td>
        {% set r = s.get('risk_score', 0)|int %}
        {% set level = s.get('risk_level','LOW') %}
        {% if level == 'CRITICAL' %}
          <span class="badge badge-critical">{{ r }}/100 CRITICAL</span>
        {% elif level == 'HIGH' or r > 70 %}
          <span class="badge badge-high">{{ r }}/100 HIGH</span>
        {% elif level == 'MEDIUM' or r > 40 %}
          <span class="badge badge-medium">{{ r }}/100 MEDIUM</span>
        {% else %}
          <span class="badge badge-low">{{ r }}/100 LOW</span>
        {% endif %}
        <div class="risk-bar-bg">
          <div class="risk-bar" style="width:{{ r }}%;background:{% if r > 70 %}#c5221f{% elif r > 40 %}#f9ab00{% else %}#34a853{% endif %}"></div>
        </div>
      </td>
      <td style="max-width:200px">{{ s.get('risk_reason','—') }}</td>
      <td style="max-width:200px">
        {% if s.get('risk_score',0)|int > 40 %}
          <span class="tag alert-tag">Action Required</span><br>
        {% endif %}
        {{ s.get('recommended_action','—') }}
      </td>
      <td>{{ s.get('alternate_route','—') }}</td>
      <td>
        <small>{{ s.get('financial_impact','—') }}</small><br>
        <small style="color:#666">+{{ s.get('estimated_delay_days',0) }} days</small>
      </td>
    </tr>
    {% endfor %}
  </table>
  {% else %}
  <div class="empty">No shipments yet. Run the analyzer to see Gemini AI analysis.</div>
  {% endif %}

</div>

<div class="footer">
  LogiSense AI · Google Solution Challenge 2026 · Smart Supply Chains Track ·
  Built on Google Cloud Free Tier · Powered by Gemini 2.0 Flash
</div>

</body>
</html>"""

@app.route("/")
def index():
    try:
        db = firestore.Client()
        docs = list(db.collection("shipments").stream())
        shipments = [d.to_dict() for d in docs]
        shipments.sort(key=lambda x: x.get('risk_score', 0), reverse=True)
        critical_count = sum(1 for s in shipments if s.get('risk_score',0) > 90)
        high_count = sum(1 for s in shipments if 70 < s.get('risk_score',0) <= 90)
        medium_count = sum(1 for s in shipments if 40 < s.get('risk_score',0) <= 70)
        low_count = sum(1 for s in shipments if s.get('risk_score',0) <= 40)
    except Exception as e:
        print(f"Error: {e}")
        shipments = []
        critical_count = high_count = medium_count = low_count = 0
    return render_template_string(HTML, shipments=shipments,
        critical_count=critical_count, high_count=high_count,
        medium_count=medium_count, low_count=low_count)

@app.route("/health")
def health():
    return "ok", 200

@app.route("/api/shipments")
def api_shipments():
    try:
        db = firestore.Client()
        docs = list(db.collection("shipments").stream())
        return jsonify([d.to_dict() for d in docs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
