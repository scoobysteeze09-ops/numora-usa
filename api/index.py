
from flask import Flask
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return """<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Numora USA - All Jobs + Visa</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}body{background:#f8fafc}
.top{background:#fff;padding:12px;border-bottom:1px solid #e2e8f0;position:sticky;top:0;z-index:20;display:flex;gap:10px;align-items:center}
.logo{font-weight:900;font-size:20px}.logo span{color:#16a34a}
.q{flex:1;background:#f1f5f9;padding:8px 12px;border-radius:999px;display:flex;gap:8px}.q input{border:0;background:transparent;outline:none;width:100%;font-size:14px}
.hero{margin:12px;background:linear-gradient(135deg,#0f172a,#16a34a);color:#fff;padding:20px;border-radius:18px}
.stats{display:flex;gap:10px;margin-top:12px}.st{background:rgba(255,255,255,.15);padding:8px 12px;border-radius:10px;font-size:12px;flex:1;text-align:center}
.card{background:#fff;margin:10px 12px;padding:14px;border-radius:14px;border:1px solid #e2e8f0}
.row{display:flex;gap:12px}.icon{width:52px;height:52px;background:#f0fdf4;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px}
.badge{background:#dcfce7;color:#166534;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}
.badge2{background:#dbeafe;color:#1e40af;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}
.badge3{background:#fef9c3;color:#854d0e;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}
.btn{background:#16a34a;color:#fff;border:0;padding:12px;border-radius:10px;width:100%;margin-top:10px;font-weight:800}
.btn2{background:#fff;border:1px solid #e2e8f0;padding:10px;border-radius:10px;width:100%;margin-top:8px;font-weight:700}
.filt{display:flex;gap:8px;overflow:auto;padding:0 12px 8px;scrollbar-width:none}.f{background:#fff;border:1px solid #e2e8f0;padding:7px 14px;border-radius:999px;font-size:13px;white-space:nowrap;cursor:pointer}.f.active{background:#111;color:#fff}
.paybox{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:99;align-items:center;justify-content:center;padding:18px}.pay{background:#fff;border-radius:18px;padding:20px;width:100%;max-width:380px}
.payopt{border:1px solid #e2e8f0;border-radius:12px;padding:12px;margin-top:10px;display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<div class=top><div class=logo>num<span>ora</span> USA</div><div class=q>🔍<input id=search placeholder='Search any job + visa...' oninput='render()'></div></div>
<div class=hero><h2>🇺🇸 USA Jobs + Visa Sponsorship</h2><p style='margin-top:6px;font-size:14px;opacity:.9'>From Kenya to USA • All Jobs • Visa + Flight + Housing</p><div class=stats><div class=st><b>2,400+</b><br>Jobs</div><div class=st><b>$15-45</b><br>/hr</div><div class=st><b>100%</b><br>Visa Sponsor</div></div><div style='margin-top:12px;background:rgba(255,255,255,.15);padding:8px;border-radius:8px;font-size:12px'>💳 Apply: M-Pesa KSH 150 / Bank / Crypto $2 USDT • Money goes to you</div></div>
<div class=filt><div class='f active' onclick="f='all';setA(this);render()">All Jobs</div><div class=f onclick="f='labour';setA(this);render()">Labour</div><div class=f onclick="f='nanny';setA(this);render()">Nanny</div><div class=f onclick="f='cleaner';setA(this);render()">Cleaner</div><div class=f onclick="f='hotel';setA(this);render()">Hotel</div><div class=f onclick="f='nurse';setA(this);render()">Nurse</div><div class=f onclick="f='truck';setA(this);render()">Driver</div><div class=f onclick="f='construction';setA(this);render()">Construction</div><div class=f onclick="f='warehouse';setA(this);render()">Warehouse</div></div>
<div id=grid></div>
<div class=paybox id=paybox><div class=pay><h3>Pay to Apply - KSH 150 / $2</h3><p id=jobname style