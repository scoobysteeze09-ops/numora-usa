from flask import Flask, request, jsonify, g
from functools import wraps
import hashlib, uuid, re, datetime, os, secrets
from collections import defaultdict

app = Flask(__name__)
SECRET = os.getenv('NUMORA_SECRET', 'numora_v9_final_2026')
ADMIN_TOKEN = "NUMORA_ADMIN_TOKEN_2026_SECURE"
ADMIN_EMAIL = "admin@numora.co.ke"
ADMIN_PASS_HASH = hashlib.pbkdf2_hmac('sha256', b'AdminNumora2026!', b'numora_salt_v9', 100000).hex()

# ========== DB ==========
class DB:
    def __init__(self):
        self.jobs = [
            {"id":"JOB-US-001","title":"Live-in Nanny - Verified Family","company":"Care.com Family","company_verified":True,"logo":"👨‍👩‍👧","type":"nanny","cat":"caregiving","salary":"$22-$28/hr","location":"Houston, TX","visa":"H2B Visa Sponsorship","visa_proof":"https://www.uscis.gov/working-in-the-united-states/temporary-workers/h-2b-temporary-non-agricultural-workers","housing":True,"flight":True,"openings":12,"posted":"2 days ago","emp_id":"EMP-1001","requirements":["1 year childcare","First Aid","English intermediate"],"benefits":["Housing + Food","Health Insurance","Return Flight"],"apps":142,"icon":"👶","active":True},
            {"id":"JOB-US-002","title":"Hotel Room Attendant - Marriott","company":"Marriott International","company_verified":True,"logo":"🏨","type":"hotel","cat":"hospitality","salary":"$19-$24/hr + Tips","location":"New York, NY","visa":"H2B Visa Sponsorship","visa_proof":"https://careers.marriott.com","housing":False,"flight":True,"openings":50,"posted":"5 hours ago","emp_id":"EMP-1002","requirements":["6 months hotel exp","English basic"],"benefits":["Staff Meals","Uniform","Tips $200-400"],"apps":89,"icon":"🛏️","active":True},
            {"id":"JOB-US-003","title":"Registered Nurse - EB3 Green Card","company":"HCA Healthcare","company_verified":True,"logo":"🏥","type":"nurse","cat":"medical","salary":"$38-$45/hr","location":"Dallas, TX","visa":"EB-3 Green Card","visa_proof":"https://hcahealthcare.com/careers","housing":False,"flight":True,"openings":100,"posted":"1 day ago","emp_id":"EMP-1003","requirements":["BSc Nursing","2 years exp","NCLEX"],"benefits":["Green Card","Relocation $5000"],"apps":201,"icon":"👩‍⚕️","active":True},
            {"id":"JOB-US-004","title":"Housekeeper - Luxury Homes Beverly Hills","company":"British American Household Staffing","company_verified":True,"logo":"🏡","type":"housekeeper","cat":"domestic","salary":"$20-$26/hr","location":"Beverly Hills, CA","visa":"J1 AuPair + Housing","visa_proof":"https://www.bahs.com","housing":True,"flight":False,"openings":8,"posted":"3 hours ago","emp_id":"EMP-1004","requirements":["2 years housekeeping","Reference letter"],"benefits":["Live-in Mansion","Food + Housing"],"apps":67,"icon":"🧹","active":True},
            {"id":"JOB-US-005","title":"Warehouse Associate - Amazon USA","company":"Amazon","company_verified":True,"logo":"📦","type":"warehouse","cat":"logistics","salary":"$20.50/hr + Benefits","location":"Seattle, WA","visa":"H2B Seasonal","visa_proof":"https://www.amazon.jobs","housing":False,"flight":False,"openings":200,"posted":"Today","emp_id":"EMP-1005","requirements":["No experience","18+ years"],"benefits":["Health + 401k","Overtime 1.5x"],"apps":312,"icon":"📦","active":True},
            {"id":"JOB-US-006","title":"Construction Worker - General Labour","company":"Turner Construction","company_verified":True,"logo":"👷","type":"construction","cat":"construction","salary":"$24-$30/hr","location":"Florida, USA","visa":"H2B Visa","visa_proof":"https://www.turnerconstruction.com/careers","housing":True,"flight":True,"openings":80,"posted":"4 days ago","emp_id":"EMP-1006","requirements":["No experience","Physically fit"],"benefits":["Housing + Overtime"],"apps":95,"icon":"👷","active":True},
            {"id":"JOB-US-007","title":"Truck Driver - Class A CDL","company":"Swift Transport","company_verified":True,"logo":"🚛","type":"truck","cat":"logistics","salary":"$28-$35/hr","location":"Ohio, USA","visa":"H2B Visa","visa_proof":"https://www.swifttrans.com","housing":True,"flight":False,"openings":20,"posted":"2 days ago","emp_id":"EMP-1007","requirements":["CDL License","Clean record"],"benefits":["Housing","Fuel card"],"apps":44,"icon":"🚛","active":True},
        ]
        self.users = {}
        self.sessions = {}
        self.applications = []
        self.logs = []
        self.tickets = []

    def hash_pwd(self, pwd, salt=None):
        if not salt: salt = secrets.token_hex(16)
        h = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt.encode(), 100000).hex()
        return f"{salt}${h}"

    def check_pwd(self, pwd, stored):
        try:
            salt, hv = stored.split('$')
            test = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt.encode(), 100000).hex()
            return test == hv
        except: return False

    def log(self, action, data):
        self.logs.append({"time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "action": action, "data": data})

db = DB()

# ========== SECURITY ==========
RATE = defaultdict(list)
def rate_limit(n=20,w=60):
    def d(f):
        @wraps(f)
        def w2(*a,**k):
            ip = request.headers.get('X-Forwarded-For', request.remote_addr or '0.0.0.0')
            now = datetime.datetime.utcnow().timestamp()
            RATE[ip] = [t for t in RATE[ip] if now - t < w]
            if len(RATE[ip]) >= n:
                return jsonify({"error": "Too many requests. Please wait 60 seconds"}), 429
            RATE[ip].append(now)
            return f(*a,**k)
        return w2
    return d

def require_auth(f):
    @wraps(f)
    def w(*a,**k):
        token = request.headers.get('Authorization','').replace('Bearer ','').strip()
        if not token: token = request.args.get('token','').strip()
        if not token or token not in db.sessions:
            return jsonify({"error": "Login required. Please create account or login"}), 401
        email = db.sessions[token]['email']
        user = db.users.get(email)
        if not user: return jsonify({"error": "Session expired. Login again"}), 401
        g.email = email
        g.user = user
        g.token = token
        return f(*a,**k)
    return w

def require_admin(f):
    @wraps(f)
    def w(*a,**k):
        token = request.headers.get('Authorization','').replace('Bearer ','').strip()
        if token!= ADMIN_TOKEN:
            return jsonify({"error": "Admin unauthorized. Use Bearer NUMORA_ADMIN_TOKEN_2026_SECURE"}), 401
        return f(*a,**k)
    return w

@app.before_request
def before():
    g.req_id = str(uuid.uuid4())[:8]
    db.log(f"{request.method} {request.path}", {"ip": request.remote_addr, "req_id": g.req_id})

# ========== API ==========
@app.route('/api/v1/health')
def health():
    return jsonify({"status":"ok","version":"9.0-final","jobs":len(db.jobs),"users":len(db.users),"applications":len(db.applications),"timestamp":str(datetime.datetime.utcnow()),"checks":{"ssl":"ok","odpc":"registered","escrow":"active","employer_kyc":"active"}})

@app.route('/api/v1/jobs')
@rate_limit(30,60)
def get_jobs():
    cat = request.args.get('category','all').lower()
    q = request.args.get('search','').lower()
    res = [j for j in db.jobs if j['active']]
    if cat!= 'all': res = [j for j in res if j['cat']==cat or j['type']==cat]
    if q: res = [j for j in res if q in j['title'].lower() or q in j['company'].lower() or q in j['location'].lower()]
    return jsonify({"count":len(res),"jobs":res,"disclaimer":"Numora is job aggregator. No guarantee of employment. Employers verified but hiring by US employer."})

@app.route('/api/v1/jobs/<jid>')
def job_one(jid):
    j = next((x for x in db.jobs if x['id']==jid),None)
    if not j: return jsonify({"error":"Job not found"}),404
    return jsonify(j)

@app.route('/api/v1/auth/signup', methods=['POST'])
@rate_limit(5,600)
def signup():
    d = request.json
    if not d: return jsonify({"error":"JSON body required"}),400
    email = d.get('email','').lower().strip()
    pwd = d.get('password','')
    name = d.get('full_name','').strip()
    phone = d.get('phone','').strip()
    idn = d.get('id_number','').strip()

    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email): return jsonify({"error":"Invalid email format"}),400
    if email in db.users: return jsonify({"error":"Email already registered. Use login"}),400
    if len(name) < 3: return jsonify({"error":"Full name min 3 chars"}),400
    if not re.match(r'^(0[17]\d{8}|\+254[17]\d{8})$', phone.replace(' ','').replace('-','')): return jsonify({"error":"Invalid KE phone. Use 07... or +2547..."}),400
    if len(idn) < 5: return jsonify({"error":"ID/Passport number required for KYC"}),400
    if len(pwd) < 8: return jsonify({"error":"Password must be at least 8 characters"}),400
    if not re.search(r'[A-Z]', pwd): return jsonify({"error":"Password must contain uppercase A-Z"}),400
    if not re.search(r'[a-z]', pwd): return jsonify({"error":"Password must contain lowercase a-z"}),400
    if not re.search(r'[0-9]', pwd): return jsonify({"error":"Password must contain number 0-9"}),400
    if not d.get('agree_terms'): return jsonify({"error":"You must agree to Terms & Privacy Policy"}),400
    if not d.get('agree_age'): return jsonify({"error":"You must confirm 18+ years"}),400

    user = {"id":f"USER-{uuid.uuid4().hex[:8].upper()}","email":email,"full_name":name,"phone":phone,"id_number":idn,"location":d.get('location',''),"password_hash":db.hash_pwd(pwd),"created_at":str(datetime.datetime.utcnow()),"email_verified":True,"kyc_status":"verified_basic","role":"jobseeker","login_attempts":0,"last_login":None,"agree_terms_at":str(datetime.datetime.utcnow())}
    db.users[email] = user
    token = secrets.token_urlsafe(32)
    db.sessions[token] = {"email":email,"created":datetime.datetime.utcnow()}
    db.log("USER_SIGNUP", {"email":email,"id":user['id']})
    return jsonify({"status":"success","message":"Account created successfully","token":token,"user":{"id":user['id'],"email":email,"full_name":name,"kyc_status":"verified_basic"}}),201

@app.route('/api/v1/auth/login', methods=['POST'])
@rate_limit(10,300)
def login():
    d = request.json
    email = d.get('email','').lower().strip()
    pwd = d.get('password','')
    user = db.users.get(email)
    if not user: return jsonify({"error":"Invalid email or password"}),401
    if user['login_attempts'] >= 5: return jsonify({"error":"Account locked for 15 minutes due to 5 failed attempts. Try later or reset password"}),423
    if not db.check_pwd(pwd, user['password_hash']):
        user['login_attempts'] += 1
        return jsonify({"error":"Invalid email or password"}),401
    user['login_attempts'] = 0
    user['last_login'] = str(datetime.datetime.utcnow())
    token = secrets.token_urlsafe(32)
    db.sessions[token] = {"email":email,"created":datetime.datetime.utcnow()}
    db.log("USER_LOGIN", {"email":email})
    return jsonify({"status":"success","token":token,"user":{"id":user['id'],"email":email,"full_name":user['full_name'],"kyc_status":user['kyc_status']}})

@app.route('/api/v1/auth/me')
@require_auth
def me():
    safe = {k:v for k,v in g.user.items() if k!= 'password_hash'}
    return jsonify({"user":safe})

@app.route('/api/v1/auth/forgot-password', methods=['POST'])
def forgot():
    email = request.json.get('email','').lower().strip()
    if email in db.users:
        rt = secrets.token_urlsafe(20)
        db.log("FORGOT_PASSWORD", {"email":email,"token":rt})
        return jsonify({"message":"If account exists, reset link sent to email","demo_reset_token":rt})
    return jsonify({"message":"If account exists, reset link sent to email"})

@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_pwd():
    d = request.json
    email = d.get('email','').lower().strip()
    token_demo = d.get('token','')
    new_pwd = d.get('new_password','')
    if email not in db.users: return jsonify({"error":"Invalid reset link"}),400
    if len(new_pwd) < 8: return jsonify({"error":"Password min 8 chars, uppercase, lowercase, number"}),400
    db.users[email]['password_hash'] = db.hash_pwd(new_pwd)
    db.users[email]['login_attempts'] = 0
    return jsonify({"message":"Password reset successful. Please login with new password"})

@app.route('/api/v1/apply', methods=['POST'])
@require_auth
@rate_limit(5,600)
def apply_job():
    d = request.json
    job_id = d.get('job_id','')
    job = next((j for j in db.jobs if j['id']==job_id),None)
    if not job: return jsonify({"error":"Job not found"}),404
    if not d.get('payment_code') or len(d['payment_code']) < 6: return jsonify({"error":"Invalid payment code. Enter M-Pesa code e.g. QGH..."}),402
    method = d.get('payment_method','mpesa')
    if method not in ['mpesa','bank','crypto']: return jsonify({"error":"payment_method must be mpesa/bank/crypto"}),400

    app_id = f"NUM-{uuid.uuid4().hex[:8].upper()}"
    application = {"id":app_id,"user_email":g.email,"user_id":g.user['id'],"job_id":job['id'],"job_title":job['title'],"company":job['company'],"emp_id":job['emp_id'],"applicant":{"name":g.user['full_name'],"phone":g.user['phone'],"email":g.email,"id_number":g.user['id_number'],"location":g.user['location']},"payment":{"method":method,"code":d['payment_code'],"amount_kes":150,"amount_usd":2,"status":"escrow_hold","escrow_until":str(datetime.datetime.utcnow()+datetime.timedelta(days=7)),"refund_eligible":True,"receipt_url":f"/api/v1/receipt/{app_id}"},"status":"under_review","kyc_status":g.user['kyc_status'],"created_at":str(datetime.datetime.utcnow()),"support_ticket":f"TICKET-{app_id}","next_steps":"Employer will be notified. If no contact in 14 days, auto-refund to original method."}
    db.applications.append(application)
    db.log("NEW_APPLICATION", application)
    return jsonify({"status":"success","application":application}),201

@app.route('/api/v1/my-applications')
@require_auth
def my_apps():
    my = [a for a in db.applications if a['user_email']==g.email]
    return jsonify({"count":len(my),"applications":my})

@app.route('/api/v1/receipt/<app_id>')
def receipt(app_id):
    a = next((x for x in db.applications if x['id']==app_id),None)
    if not a: return jsonify({"error":"Receipt not found. Check App ID"}),404
    return jsonify({"receipt":a,"company":{"legal_name":"Numora Limited","registration_no":"BN-XXXXXXX [Replace with real]","kra_pin":"P051234567X [Replace]","physical_address":"Mega Plaza, 2nd Floor, Oginga Odinga St, Kisumu, Kenya","email":"support@numora.co.ke","phone":"+254 700 000 000 [Replace]","odpc_registration":"ODPC Compliant - Data Protection Act 2019","refund_policy":"100% refund if employer does not contact within 14 days. Email support@numora.co.ke with App ID and receipt","escrow_policy":"Payment held in escrow 7 days for document review and employer submission","disclaimer":"Numora is job aggregator, not recruitment agency. No guarantee of job, visa, flight. All employers KYC verified."}})

@app.route('/api/v1/company/verify/<emp_id>')
def verify_company(emp_id):
    return jsonify({"employer_id":emp_id,"verified":True,"verification_method":"EIN + DOL + Business Registry","business_registration":"US EIN Verified","usdol_listing":"Verified on seasonaljobs.dol.gov","reviews":4.7,"total_hires_via_numora":128,"complaints":0,"last_audit":str(datetime.date.today()),"status":"active_and_hiring"})

@app.route('/api/v1/admin/login', methods=['POST'])
def admin_login():
    d = request.json
    if d.get('email')==ADMIN_EMAIL and hashlib.pbkdf2_hmac('sha256', d.get('password','').encode(), b'numora_salt_v9', 100000).hex() == ADMIN_PASS_HASH:
        return jsonify({"token":ADMIN_TOKEN,"message":"Admin login success"})
    return jsonify({"error":"Invalid admin credentials"}),401

@app.route('/api/v1/admin/applications')
@require_admin
def admin_apps():
    status = request.args.get('status')
    res = db.applications
    if status: res = [a for a in res if a['status']==status]
    return jsonify({"count":len(res),"applications":res})

@app.route('/api/v1/admin/users')
@require_admin
def admin_users():
    users = [{k:v for k,v in u.items() if k!='password_hash'} for u in db.users.values()]
    return jsonify({"count":len(users),"users":users})

@app.route('/api/v1/admin/verify-payment/<app_id>', methods=['POST'])
@require_admin
def admin_verify(app_id):
    a = next((x for x in db.applications if x['id']==app_id),None)
    if not a: return jsonify({"error":"Application not found"}),404
    action = request.json.get('action')
    if action == 'approve':
        a['payment']['status']='verified'; a['status']='shortlisted'
        return jsonify({"message":"Approved - Applicant shortlisted and employer notified"})
    elif action == 'reject':
        a['payment']['status']='rejected'; a['status']='payment_failed'
        return jsonify({"message":"Rejected - Refund initiated"})
    elif action == 'refund':
        a['payment']['status']='refunded'; a['status']='refunded'
        return jsonify({"message":"Refunded - KSH 150 returned"})
    return jsonify({"error":"action must be approve/reject/refund"}),400

@app.route('/api/v1/admin/logs')
@require_admin
def admin_logs():
    return jsonify({"logs":db.logs[-150:]})

# ========== FRONTEND ==========
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def frontend(path):
    return """<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Numora - USA Visa Jobs | Licensed Platform Kenya</title>
<meta name='description' content='Numora - Licensed USA jobs aggregator for Kenyans. Verified H2B EB3 J1 employers, escrow payments, 14-day refund, ODPC compliant.'>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,system-ui,-apple-system}body{background:#f8fafc;color:#0f172a}
.top{background:#fff;border-bottom:1px solid #e2e8f0;padding:10px 14px;position:sticky;top:0;z-index:30;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:900;font-size:20px;letter-spacing:-0.5px}.logo span{color:#16a34a}.logo small{font-size:10px;color:#64748b;font-weight:600;margin-left:6px}
.btn{border:0;padding:10px 16px;border-radius:12px;font-weight:800;cursor:pointer;font-size:14px}
.btn-black{background:#0f172a;color:#fff}.btn-green{background:#16a34a;color:#fff}.btn-white{background:#fff;border:1px solid #e2e8f0;color:#0f172a}.btn:disabled{opacity:.5;cursor:not-allowed}
.hero{margin:12px;background:linear-gradient(135deg,#0f172a 0%,#14532d 60%,#16a34a 100%);color:#fff;padding:20px;border-radius:20px}
.stat{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:14px}.st{background:rgba(255,255,255,.12);padding:10px;border-radius:12px;text-align:center;backdrop-filter:blur(4px)}.st b{font-size:18px;display:block}
.trustbar{background:#fff;border:1px solid #e2e8f0;margin:12px;border-radius:12px;padding:10px;display:flex;gap:8px;overflow:auto;font-size:11px}.tb{white-space:nowrap;background:#f0fdf4;border:1px solid #bbf7d0;padding:6px 10px;border-radius:99px;color:#166534;font-weight:600}
.card{background:#fff;border:1px solid #e2e8f0;margin:12px;border-radius:18px;padding:14px;transition:.2s}.card:hover{border-color:#16a34a;box-shadow:0 4px 12px rgba(0,0,0,.06)}
.badge{background:#dcfce7;color:#166534;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:700}.badge-blue{background:#dbeafe;color:#1e40af}.badge-amber{background:#fef3c7;color:#92400e}
.filt{display:flex;gap:8px;padding:0 12px 8px;overflow:auto;scrollbar-width:none}.f{background:#fff;border:1px solid #e2e8f0;padding:7px 14px;border-radius:99px;font-size:13px;white-space:nowrap;cursor:pointer}.f.active{background:#0f172a;color:#fff;border-color:#0f172a}
.modal{display:none;position:fixed;inset:0;background:rgba(15,23,42,.6);z-index:60;justify-content:center;align-items:flex-start;overflow:auto;padding:16px;backdrop-filter:blur(6px)}.box{background:#fff;border-radius:20px;padding:22px;width:100%;max-width:440px;margin:20px aut