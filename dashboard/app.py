import os
from flask import Flask, render_template_string, jsonify
from google.cloud import firestore

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html>
<head>
<title>LogiSense AI — Supply Chain Dashboard</title>
<meta http-equiv="refresh" content="20">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Google Sans, sans-serif; background: #f1f3f4; color: #202124; }

.nav {
  background: linear-gradient(135deg, #1557b0, #1a73e8);
  padding: 14px 28px; color: white;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.nav h1 { font-size: 18px; font-weight: 600; letter-spacing: 0.2px; }
.nav p { font-size: 11px; opacity: 0.8; margin-top: 3px; }
.nav-stats { display: flex; gap: 10px; }
.stat-pill {
  background: rgba(255,255,255,0.18);
  border-radius: 20px; padding: 6px 14px; text-align: center;
}
.stat-pill .n { font-size: 18px; font-weight: 700; }
.stat-pill .l { font-size: 10px; opacity: 0.85; }

.container { padding: 20px 28px; }

.cards { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 20px; }
.card {
  background: white; border-radius: 10px; padding: 14px 18px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  display: flex; align-items: center; gap: 14px;
  border-left: 5px solid #eee;
}
.card.c { border-left-color: #b71c1c; }
.card.h { border-left-color: #e53935; }
.card.m { border-left-color: #f9a825; }
.card.l { border-left-color: #2e7d32; }
.card-icon { font-size: 28px; }
.card-num { font-size: 28px; font-weight: 700; line-height: 1; }
.card-lbl { font-size: 11px; color: #666; margin-top: 3px; }

.tbl-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.tbl-title { font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #34a853; animation: pulse 2s infinite; }
@keyframes pulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(52,168,83,0.5); }
  50% { box-shadow: 0 0 0 6px rgba(52,168,83,0); }
}
.ai-badge {
  background: #e8f0fe; color: #1a73e8;
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600;
}

.table-wrap { overflow-x: auto; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
table { width: 100%; border-collapse: collapse; background: white; min-width: 900px; }
thead tr { background: #1a73e8; }
th {
  color: white; padding: 10px 12px;
  text-align: left; font-size: 11px;
  font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em; white-space: nowrap;
}
td {
  padding: 10px 12px; border-bottom: 1px solid #f0f0f0;
  font-size: 12px; vertical-align: middle;
}
tr:last-child td { border: none; }
tbody tr:hover td { background: #f8faff; }

.ship-id { font-weight: 700; font-size: 13px; color: #1a73e8; }
.route-from { font-weight: 600; font-size: 12px; }
.route-arrow { color: #999; font-size: 11px; }
.route-to { font-size: 12px; color: #444; }

.tag {
  display: inline-block; padding: 2px 8px;
  border-radius: 4px; font-size: 10px; font-weight: 600;
  white-space: nowrap;
}
.tag-blue { background: #e8f0fe; color: #1557b0; }
.tag-gray { background: #f1f3f4; color: #444; font-size: 10px; margin-top: 3px; }

.cond-main { font-size: 12px; font-weight: 500; }
.cond-sub { font-size: 10px; color: #888; margin-top: 2px; }

.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 4px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 700; white-space: nowrap;
}
.badge-critical { background: #3c0000; color: #ff8a80; }
.badge-high { background: #fce8e6; color: #b71c1c; }
.badge-medium { background: #fff8e1; color: #e65100; }
.badge-low { background: #e8f5e9; color: #2e7d32; }

.bar-wrap { margin-top: 5px; }
.bar-bg { background: #f0f0f0; border-radius: 3px; height: 4px; width: 70px; }
.bar-fill { height: 4px; border-radius: 3px; }

.risk-text { font-size: 11px; color: #444; line-height: 1.5; max-width: 200px; }
.action-tag {
  display: inline-block; background: #fce8e6; color: #b71c1c;
  padding: 1px 6px; border-radius: 3px;
  font-size: 10px; font-weight: 600; margin-bottom: 4px;
}
.action-text { font-size: 11px; color: #444; line-height: 1.5; max-width: 180px; }

.route-alt { font-size: 11px; color: #1557b0; font-weight: 500; max-width: 160px; line-height: 1.4; }

.impact-cost { font-size: 12px; font-weight: 600; color: #b71c1c; }
.impact-days { font-size: 10px; color: #888; margin-top: 2px; }

.footer {
  text-align: center; padding: 16px;
  font-size: 11px; color: #999; margin-top: 20px;
}

.empty { text-align: center; padding: 80px; color: #999; font-size: 14px; background: white; border-radius: 10px; }
</style>
</head>
<body>

<div class="nav">
  <div>
    <h1>🚢 LogiSense AI — Supply Chain Intelligence Platform</h1>
    <p>Powered by Gemini 2.0 Flash · Google Cloud · Real-time Disruption Detection & Dynamic Rerouting</p>
  </div>
  <div class="nav-stats">
    <div class="stat-pill">
      <div class="n">{{ shipments|length }}</div>
      <div class="l">Shipments</div>
    </div>
    <div class="stat-pill">
      <div class="n">{{ critical_count + high_count }}</div>
      <div class="l">Need Action</div>
    </div>
  </div>
</div>

<div class="container">

  <div class="cards">
    <div class="card c">
      <div class="card-icon">🚨</div>
      <div>
        <div class="card-num">{{ critical_count }}</div>
        <div class="card-lbl">Critical Risk</div>
      </div>
    </div>
    <div class="card h">
      <div class="card-icon">⚠️</div>
      <div>
        <div class="card-num">{{ high_count }}</div>
        <div class="card-lbl">High Risk</div>
      </div>
    </div>
    <div class="card m">
      <div class="card-icon">📊</div>
      <div>
        <div class="card-num">{{ medium_count }}</div>
        <div class="card-lbl">Medium Risk</div>
      </div>
    </div>
    <div class="card l">
      <div class="card-icon">✅</div>
      <div>
        <div class="card-num">{{ low_count }}</div>
        <div class="card-lbl">On Track</div>
      </div>
    </div>
  </div>

  <div class="tbl-header">
    <div class="tbl-title">
      <div class="dot"></div>
      Live Shipment Intelligence · Auto-refreshes every 20s
    </div>
    <span class="ai-badge">⚡ Gemini 2.0 Flash AI</span>
  </div>

  {% if shipments %}
  <div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Route</th>
        <th>Cargo & Carrier</th>
        <th>Conditions</th>
        <th>Risk Score</th>
        <th>AI Risk Analysis</th>
        <th>Recommended Action</th>
        <th>Alternate Route</th>
        <th>Impact</th>
      </tr>
    </thead>
    <tbody>
    {% for s in shipments %}
    <tr>
      <td><span class="ship-id">{{ s.get('shipment_id','—') }}</span></td>
      <td>
        <div class="route-from">{{ s.get('origin','—') }}</div>
        <div class="route-arrow">↓</div>
        <div class="route-to">{{ s.get('destination','—') }}</div>
      </td>
      <td>
        <span class="tag tag-blue">{{ s.get('cargo_type','—') }}</span><br>
        <span class="tag tag-gray">{{ s.get('carrier','—') }}</span>
      </td>
      <td>
        <div class="cond-main">{{ s.get('weather','—') }}</div>
        <div class="cond-sub">Congestion: {{ (s.get('port_congestion_score',0)*100)|int }}%</div>
        <div class="cond-sub">Delay: {{ s.get('carrier_delay_hrs',0) }}hrs</div>
      </td>
      <td>
        {% set r = s.get('risk_score', 0)|int %}
        {% set level = s.get('risk_level','LOW') %}
        {% if level == 'CRITICAL' %}
          <span class="badge badge-critical">🚨 {{ r }} CRITICAL</span>
        {% elif level == 'HIGH' or r > 70 %}
          <span class="badge badge-high">⚠️ {{ r }} HIGH</span>
        {% elif level == 'MEDIUM' or r > 40 %}
          <span class="badge badge-medium">📊 {{ r }} MEDIUM</span>
        {% else %}
          <span class="badge badge-low">✅ {{ r }} LOW</span>
        {% endif %}
        <div class="bar-wrap">
          <div class="bar-bg">
            <div class="bar-fill" style="width:{{ r }}%;background:{% if r > 80 %}#b71c1c{% elif r > 70 %}#e53935{% elif r > 40 %}#f9a825{% else %}#34a853{% endif %}"></div>
          </div>
        </div>
      </td>
      <td><div class="risk-text">{{ s.get('risk_reason','—') }}</div></td>
      <td>
        {% if s.get('risk_score',0)|int > 40 %}
          <div class="action-tag">Action Required</div>
        {% endif %}
        <div class="action-text">{{ s.get('recommended_action','—') }}</div>
      </td>
      <td><div class="route-alt">{{ s.get('alternate_route','—') }}</div></td>
      <td>
        <div class="impact-cost">{{ s.get('financial_impact','—') }}</div>
        <div class="impact-days">+{{ s.get('estimated_delay_days',0) }} days</div>
      </td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
  </div>
  {% else %}
  <div class="empty">No shipments yet. Run the analyzer to see Gemini AI analysis.</div>
  {% endif %}

</div>

<div class="footer">
  LogiSense AI · Google Solution Challenge 2026 · Smart Supply Chains Track ·
  Built on Google Cloud Free Tier · Gemini 2.0 Flash AI
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
