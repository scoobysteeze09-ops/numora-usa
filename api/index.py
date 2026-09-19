from flask import Flask
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return """<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Numora - All USA Jobs + Visa</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}body{background:#f8fafc}
.top{background:#fff;padding:12px;border-bottom:1px solid #e2e8f0;position:sticky;top:0;z-index:20;display:flex;gap:10px;align-items:center}
.logo{font-weight:900;font-size:20px}.logo span{color:#16a34a}
.q{flex:1;background:#f1f5f9;padding:8px 12px;border-radius:999px;display:flex;gap:8px}.q input{border:0;background:transparent;outline:none;width:100%}
.hero{margin:12px;background:linear-gradient(135deg,#0f172a,#16a34a);color:#fff;padding:20px;border-radius:18px}
.card{background:#fff;margin:10px 12px;padding:14px;border-radius:14px;border:1px solid #e2e8f0}
.row{display:flex;gap:12px}.icon{width:52px;height:52px;background:#f0fdf4;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px}
.badge{background:#dcfce7;color:#166534;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}
.badge2{background:#dbeafe;color:#1e40af;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}
.badge3{background:#fef9c3;color:#854d0e;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}
.btn{background:#16a34a;color:#fff;border:0;padding:12px;border-radius:10px;width:100%;margin-top:10px;font-weight:800}
.btn2{background:#fff;border:1px solid #e2e8f0;padding:10px;border-radius:10px;width:100%;margin-top:8px;font-weight:700}
.filt{display:flex;gap:8px;overflow:auto;padding:0 12px 8px}.f{background:#fff;border:1px solid #e2e8f0;padding:7px 14px;border-radius:999px;font-size:13px;white-space:nowrap}.f.active{background:#111;color:#fff}
.paybox{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:99;align-items:center;justify-content:center;padding:18px}.pay{background:#fff;border-radius:18px;padding:20px;width:100%;max-width:380px}.payopt{border:1px solid #e2e8f0;border-radius:12px;padding:12px;margin-top:10px;display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<div class=top><div class=logo>num<span>ora</span> USA</div><div class=q>🔍<input id=search placeholder='Search any job...' oninput='render()'></div></div>
<div class=hero><h2>🇺🇸 USA Jobs + Visa Sponsorship</h2><p style='margin-top:6px;font-size:14px;opacity:.9'>All Jobs From Kenya to USA</p><div style='margin-top:10px;background:rgba(255,255,255,.15);padding:8px;border-radius:8px;font-size:12px'>Nanny • Cleaner • Hotel • Nurse • Driver • Construction • Warehouse • Farm • Security<br>💳 Apply: M-Pesa / Bank / USDT $2</div></div>
<div class=filt><div class='f active' onclick="f='all';setA(this);render()">All</div><div class=f onclick="f='nanny';setA(this);render()">Nanny</div><div class=f onclick="f='cleaner';setA(this);render()">Cleaner</div><div class=f onclick="f='hotel';setA(this);render()">Hotel</div><div class=f onclick="f='nurse';setA(this);render()">Nurse</div><div class=f onclick="f='truck';setA(this);render()">Driver</div><div class=f onclick="f='construction';setA(this);render()">Construction</div><div class=f onclick="f='warehouse';setA(this);render()">Warehouse</div><div class=f onclick="f='labour';setA(this);render()">Labour</div></div>
<div id=grid></div>
<div class=paybox id=paybox><div class=pay><h3>Pay to Apply - KSH 150 / $2</h3><p id=jobname style='font-size:13px;color:#64748b;margin-top:4px'>Job</p>
<div class=payopt><div><b>📱 M-Pesa</b><br><small>Till: 123456 - NUMORA</small></div><button onclick="paid('M-Pesa')" style='background:#16a34a;color:#fff;border:0;padding:8px 14px;border-radius:8px'>Copy</button></div>
<div class=payopt><div><b>🏦 Bank</b><br><small>KCB 1234567890<br>Numora KE</small></div><button onclick="paid('Bank')" style='background:#111;color:#fff;border:0;padding:8px 14px;border-radius:8px'>Copy</button></div>
<div class=payopt><div><b>₿ Crypto USDT</b><br><small>TRC20: TYOURUSDT</small></div><button onclick="paid('USDT')" style='background:#f59e0b;color:#fff;border:0;padding:8px 14px;border-radius:8px'>Copy</button></div>
<div style='margin-top:14px;display:flex;gap:8px'><button onclick="closePay()" style='flex:1;padding:11px;border:1px solid #e2e8f0;border-radius:10px;background:#fff'>Cancel</button><button onclick="whatsappApply()" style='flex:1;padding:11px;border-radius:10px;background:#25D366;color:#fff;border:0;font-weight:800'>I Paid ✅</button></div></div></div>
<script>
let f='all', selectedJob='';
jobs=[
{t:'Live-in Nanny - Texas Family',c:'Care.com Family',s:'$22/hr + Housing',d:'nanny',i:'👶',visa:'Visa Sponsor'},
{t:'House Girl / Housekeeper',c:'Elite Maids Florida',s:'$18/hr + House',d:'labour',i:'🧹',visa:'Housing'},
{t:'Hotel Room Attendant - Marriott',c:'Marriott Hotels',s:'$19/hr + Tips',d:'hotel',i:'🏨',visa:'Visa Sponsor'},
{t:'Office Cleaner - No Experience',c:'Molly Maid USA',s:'$17/hr',d:'cleaner',i:'✨',visa:'Training'},
{t:'Registered Nurse - Hospital USA',c:'HCA Healthcare',s:'$42/hr + Visa + Flight',d:'nurse',i:'👩‍⚕️',visa:'Visa + NCLEX'},
{t:'Truck Driver - CDL - USA',c:'Swift Transport USA',s:'$28/hr',d:'truck',i:'🚛',visa:'Visa Sponsor'},
{t:'Construction Worker',c:'Turner Construction',s:'$24/hr + Overtime',d:'construction',i:'👷',visa:'Visa Sponsor'},
{t:'House Boy - Beverly Hills',c:'Luxury Homes LA',s:'$20/hr + Housing',d:'labour',i:'👨‍🍳',visa:'Visa Sponsor'},
{t:'Warehouse - Amazon USA',c:'Amazon USA',s:'$20.5/hr',d:'warehouse',i:'📦',visa:'Visa Sponsor'},
{t:'Elderly Caregiver / CNA',c:'Home Instead',s:'$21/hr',d:'nurse',i:'👵',visa:'Visa Sponsor'},
{t:'Hotel Cleaner - Hilton',c:'Hilton Hotels',s:'$18.50/hr',d:'hotel',i:'🛏️',visa:'Urgent'},
{t:'Farm Worker - H2A Visa',c:'USA Farms',s:'$16/hr + Housing',d:'labour',i:'🌾',visa:'H2A Visa'},
{t:'Security Guard - Hotel',c:'Allied Universal',s:'$19/hr',d:'labour',i:'🛡️',visa:'Visa Sponsor'},
{t:'Restaurant Cleaner + Kitchen',c:'McDonalds USA',s:'$16/hr + Meals',d:'cleaner',i:'🍽️',visa:'No Experience'}
];
function setA(el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active')}
function render(){
let q=document.getElementById('search').value.toLowerCase();let h='';
jobs.filter(j=>(f=='all'||j.d==f)&&(!q||j.t.toLowerCase().includes(q))).forEach(j=>{
h+=`<div class=card><div class=row><div class=icon>${j.i}</div><div style='flex:1'><b>${j.t}</b><br><small>${j.c}</small><div style='margin-top:6px;display:flex;gap:6px;flex-wrap:wrap'><span class=badge>${j.visa}</span><span class=badge2>Visa Available</span><span class=badge3>${j.s}</span></div><button class=btn onclick="openPay('${j.t}')">Apply - KSH 150 / $2 / Bank</button><button class=btn2 onclick="share('${j.t}')">Share WhatsApp</button></div></div></div>`;
});
document.getElementById('grid').innerHTML=h;
}
function openPay(t){selectedJob=t;document.getElementById('jobname').innerText='Job: '+t;document.getElementById('paybox').style.display='flex'}
function closePay(){document.getElementById('paybox').style.display='none'}
function paid(m){alert(m+':\\nM-Pesa Till 123456\\nBank KCB 1234567890\\nUSDT TRC20 TYOURUSDT') }
function whatsappApply(){window.open("https://wa.me/254700000000?text="+encodeURIComponent("Hi Numora, I PAID for "+selectedJob),"_blank");closePay()}
function share(t){window.open("https://wa.me/?text="+encodeURIComponent("USA VISA JOB: "+t+" "+location.href),"_blank")}
render();
</script></body></html>"""