import re,json,html,os,sys,shutil,datetime
sys.path.insert(0,'/workspace/learn21'); import data as D
from curriculum import C
import skills as SK
os.makedirs('learn/raw',exist_ok=True)
BIZ="https://finlaysonnick74-source.github.io/tomas-web-studio/"
css=open('/workspace/tomas-site-v-rich-backup/style.css').read()+"""
:root{--bg:#0a0c16;--card:#121628;--line:#ffffff14;--txt:#f2f4ff;--mut:#aab2d6}
body{font-family:"Inter",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-font-smoothing:antialiased;font-size:17px}
h1,h2,h3{letter-spacing:-.02em}h3{font-size:1.15rem}
.card{background:linear-gradient(180deg,#151a30,#111526);border:1px solid var(--line);box-shadow:0 10px 30px -15px #000a;border-radius:22px}
.card:hover{transform:translateY(-3px);border-color:#ffb44355}
a{color:#ffd08a}a.btn,a.card,a.chip,.logo,nav a{color:inherit}
nav ul{gap:6px}nav ul a{padding:7px 12px;border-radius:99px;color:#cfd5f2;font-weight:600}nav ul a:hover,nav ul a:focus{background:#ffffff14;color:#fff}
@media(max-width:760px){nav .w{flex-direction:column;height:auto;padding:10px 16px;gap:6px;align-items:flex-start}nav ul{display:flex;overflow-x:auto;max-width:100%;padding-bottom:4px;scrollbar-width:none}nav ul a{white-space:nowrap;font-size:.85rem;padding:6px 10px}body{font-size:16px}header{padding:50px 0 40px}}
.skip{position:absolute;left:-999px}.skip:focus{left:10px;top:10px;z-index:100;background:#fff;color:#000;padding:8px}
:focus-visible{outline:3px solid var(--b);outline-offset:2px}
.crumbs{font-size:.85rem;color:var(--mut);margin-bottom:10px}.crumbs a{color:var(--mut)}
.dash{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.kpi{font-size:2.6rem;font-weight:900;line-height:1}.ring{width:120px;height:120px}
.chip{color:var(--txt)}
"""+"""
#gate{position:fixed;inset:0;z-index:99;background:var(--bg);display:flex;align-items:center;justify-content:center}
html.locked body>*:not(#gate){display:none!important}
.tt{width:100%;border-collapse:collapse}.tt td{padding:10px;border-bottom:1px solid #ffffff12;vertical-align:top}.tt td:first-child{white-space:nowrap;color:var(--b);font-weight:700}
.quiz summary{cursor:pointer;font-weight:700;padding:8px 0}.quiz p{color:var(--c)}
iframe.lesson{width:100%;border:0;border-radius:14px;background:#fff;min-height:600px}
.pn{display:flex;justify-content:space-between;gap:10px;margin:20px 0;flex-wrap:wrap}
h3{margin:4px 0 8px}.card+.card{margin-top:0}.stack>.card{margin-bottom:20px}
"""
open('style.css','w').write(css)
open('gate.js','w').write("""(function(){var P='levelup2026';if(localStorage.getItem('lu')==='1')return;document.documentElement.classList.add('locked');
addEventListener('DOMContentLoaded',function(){var g=document.createElement('div');g.id='gate';g.innerHTML='<form style="background:#141829;padding:34px;border-radius:20px;max-width:360px;width:90%;font-family:system-ui;color:#eef0ff"><h2 style="margin:0 0 8px">Family access</h2><p style="color:#9aa3c7">This page is for Tomas\\'s family and support team. Enter the family passcode.</p><input type="password" id="gp" placeholder="Passcode" style="width:100%;padding:12px;border-radius:10px;border:1px solid #444;background:#0f1222;color:#fff;margin:10px 0"><button style="padding:12px 20px;border-radius:99px;border:0;background:linear-gradient(90deg,#ff6b4a,#ffb443);font-weight:800">Enter</button><p id="ge" style="color:#ff6b4a"></p></form>';
document.body.prepend(g);g.querySelector('form').onsubmit=function(e){e.preventDefault();if(document.getElementById('gp').value.trim()===P){localStorage.setItem('lu','1');location.reload()}else document.getElementById('ge').textContent='Not quite. Try again.'}})})();""")
open('robots.txt','w').write("User-agent: *\nDisallow: /\n")
def NAV(p): return f'''<a class="skip" href="#main">Skip to content</a><nav aria-label="Main"><div class="w"><a class="logo" href="{p}index.html" style="text-decoration:none">Tomas <span>Levels Up</span></a>
<ul><li><a href="{p}index.html">Home</a></li><li><a href="{p}today.html">Today</a></li><li><a href="{p}tracker.html">Tracker</a></li><li><a href="{p}learn/index.html">Program</a></li><li><a href="{p}skills.html">Skills</a></li><li><a href="{p}careers.html">Careers</a></li><li><a href="{p}library/index.html">Library</a></li><li><a href="{p}support.html">Support</a></li></ul></div></nav><div id="main"></div>'''
FOOT='<footer><div class="w">Tomas Levels Up · a private family page · <a href="'+BIZ+'">Watch the business site grow →</a></div></footer><script>const o=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add("in");o.unobserve(x.target)}}),{threshold:.1});document.querySelectorAll(".r").forEach(el=>o.observe(el));</script>'
def page(fn,title,body,extra=""):
    p='../'*fn.count('/')
    open(fn,'w').write(f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{title} · Tomas Levels Up</title><script src="{p}gate.js"></script><link rel="stylesheet" href="{p}style.css"></head><body>{NAV(p)}\n{body}\n{FOOT}{extra}</body></html>')
def hero(tag,h,lead): return f'<header style="padding:70px 0 30px"><div class="w"><div class="tag">{tag}</div><h1>{h}</h1><p class="lead">{lead}</p></div></header>'
def card(h,items): return f'<div class="card"><h3>{h}</h3><ul class="l">'+''.join(f'<li>{i}</li>' for i in items)+'</ul></div>'
def strip(x): return html.unescape(re.sub('<[^>]+>','',x))
# ---------- raw guide pages ----------
WB=re.split(r'(?=<section class="page)',open('/workspace/webbasics/index.html').read())
wbhead=WB[0]; WBS=[s.split('</body>')[0] for s in WB[1:]]
L21=re.split(r'(?=<section class="page)',open('/workspace/learn21/index.html').read())
l21style=re.search(r'<style>(.*?)</style>',L21[0],re.S).group(1); L21S=[s.split('</body>')[0] for s in L21[1:]]
shutil.copy('/workspace/webbasics/style.css','learn/raw/wb.css'); shutil.copy('/workspace/learn21/style.css','learn/raw/l21.css')
fit='<script>function f(){var w=document.querySelector(".page");if(!w)return;var z=Math.min(1,innerWidth/(w.offsetWidth||794));document.body.style.zoom=z}addEventListener("load",f);addEventListener("resize",f)</script>'
def raw(fn,sec,cssf,extra=""):
    open('learn/raw/'+fn,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><script src="../../gate.js"></script><link rel="stylesheet" href="{cssf}"><style>{extra} body{{margin:0;background:#fff}} .page{{margin:0 auto!important;box-shadow:none!important}}</style></head><body>{sec}{fit}</body></html>')
IFR='<iframe class="lesson" src="{}" loading="lazy" onload="try{{this.style.height=(this.contentDocument.documentElement.scrollHeight+10)+\'px\'}}catch(e){{}}"></iframe>'
WBT=["Cover","Welcome","What code is: HTML, CSS, JavaScript","How a website works","Domains and hosting","Hosting options","Change control","Branches and pull requests","Deployment","Old versus modern","Your toolkit map","The project roadmap","Next steps","Jargon buster"]
WBS=WBS[:14]
for i,s in enumerate(WBS): raw(f'wb-{i:02d}.html',s,'wb.css')
for i,s in enumerate(L21S): raw(f'l21-{i:02d}.html',s,'l21.css',l21style)
for i in range(1,14):
    pv=f'<a class="btn o" href="wb-{i-1:02d}.html">← {WBT[i-1]}</a>' if i>1 else '<span></span>'
    nx=f'<a class="btn o" href="wb-{i+1:02d}.html">{WBT[i+1]} →</a>' if i<13 else '<a class="btn o" href="index.html">Back to Learn</a>'
    page(f'learn/wb-{i:02d}.html',WBT[i],f'<section style="padding:40px 0"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Program</a> › Web Basics › Lesson {i}</div><div class="label">Web Basics · lesson {i} of 13</div><h2>{WBT[i]}</h2><div class="pn">{pv}{nx}</div>{IFR.format("raw/wb-%02d.html"%i)}<div class="pn">{pv}{nx}</div></div></section>')
# map l21 sections: find day pages
daysec={}
for i,s in enumerate(L21S):
    m=re.search(r'Days? (\d+)(?:&ndash;(\d+))?',strip(s)[:200].replace('–','&ndash;')) or re.search(r'Days? (\d+)',strip(s)[:200])
    t=strip(s)[:60]
    if 'Week' in t and 'Day' in t:
        nums=re.findall(r'\d+',t.split('·')[1] if '·' in t else t)
        for n in nums[:2]: daysec.setdefault(int(n),i)
weekintro={1:None,2:None,3:None}; review={}
for i,s in enumerate(L21S):
    t=re.sub(r'\s+',' ',strip(s))[:40]
    for w in (1,2,3):
        if t.startswith(f'Week {w} of 3'): weekintro[w]=i
        if t.startswith(f'Week {w} · Look back'): review[w]=i
toolsec=[i for i,s in enumerate(L21S) if 'Tools you' in strip(s)[:200]][0]
# ---------- day pages ----------
TB=["0:00–0:10","0:10–0:40","0:40–1:25","1:25–1:30","1:30–1:50","1:50–2:00"]
days=[]
for n,d in enumerate(D.DAYS,1):
    date=D.date(n); ds=date.strftime('%A %-d %B %Y'); ex=D.EXTRA.get(n,{}); wk=(n-1)//7+1; W=D.WEEKS[wk-1]
    if n==21:
        d=dict(d,title='Launch Day: Tomas Web Studio goes public')
        C[21]=([12,13],["Launch the business site to the public with pride","Announce it on Instagram (scheduled in Postiz)","Have your first pitches booked","Run a retro and set the target: first paying client in the next few weeks"],
         "Book your first 3 free website checks with local businesses (with Dad) and put the dates in your calendar.",C[21][3],
         ["Business site live to the public on your own domain","Launch post out on Instagram","First pitches booked (dates set)","Retro written + next-21-days plan","Target set: first paying client in the following weeks","Show-and-tell #3: launch night!"])
    wbs,obj,chal,quiz,done=C[n]; b=d['blocks']
    if n in daysec: pass
    else: daysec[n]=daysec.get(n-1)
    school=date.weekday()<5
    when="Weekdays: session 4:30–6:30pm at Dad's, straight after school." if school else "Weekend: same 2 hours, Tomas picks the time (e.g. 10am–12pm)."
    tt=[("Check-in + goal",b[0]+" Set today's goal: "+d['goal']),("Learn",b[1]+" Read the lesson below together."),("Build on the business site",b[2]),("Break","5 minutes away from the screen."),("Practise / challenge",chal),("Reflect, commit + log",b[3]+" Write your journal line and update progress.json.")]
    steps=[x.strip() for x in re.split(r'(?<=[.!])\s+',strip(b[2])) if x.strip()]
    tools=''.join(f'<span class="chip">{D.TOOLS[t]["name"]}</span>' for t in d['tools'])
    life=''.join(f'<span class="chip">{D.LIFE[l][0]}</span>' for l in ex.get('life',[]))
    tooldesc=''.join(f'<li><b>{D.TOOLS[t]["name"]}:</b> {D.TOOLS[t]["what"]}</li>' for t in d['tools'])
    wbl=''.join(f'<h3 style="margin-top:18px">Web Basics: {WBT[i]}</h3>'+IFR.format(f'raw/wb-{i:02d}.html') for i in wbs)
    plan21=f'<details class="quiz" style="margin-top:14px"><summary>Open this day\'s page from the 21-day plan</summary>{IFR.format("raw/l21-%02d.html"%daysec[n])}</details>' if n in daysec else ''
    show=f'<div class="card" style="border-color:var(--b)"><h3>🎤 Show-and-tell #{d["show"]} tonight</h3><ul class="l">'+''.join(f'<li>{x}</li>' for x in W['show_items'])+'</ul><p class="note">Family questions: '+' · '.join(W['ask'])+'</p></div>' if d.get('show') else ''
    pv=f'<a class="btn o" href="day-{n-1:02d}.html">← Day {n-1}</a>' if n>1 else '<a class="btn o" href="index.html">← Learn</a>'
    nx=f'<a class="btn o" href="day-{n+1:02d}.html">Day {n+1} →</a>' if n<21 else '<a class="btn o" href="../tracker.html">Tracker →</a>'
    body=f'''<header style="padding:60px 0 20px"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Program</a> › Week {wk} › Day {n}</div><div class="tag">Week {wk} · {W["theme"]} · Day {n} of 21</div><div class="pn" style="margin:0 0 14px">{pv}{nx}</div><h1 style="font-size:clamp(2rem,5vw,3.6rem)">{d["title"]}</h1>
<p class="lead">{ds} · {when}</p>{'<p><a class="btn" href="../outcomes.html">🚀 Launch countdown: '+str(21-n)+' days to Launch Day</a></p>' if n>=15 and n<21 else ('<p><a class="btn" href="../outcomes.html">🚀 Launch Day! See what I can do now</a></p>' if n==21 else '')}<div class="bar2"><i style="width:{n/21*100:.0f}%"></i></div></div></header>
<section style="padding:10px 0 40px"><div class="w stack">{show}
<div class="card"><h3>🎯 By the end you can…</h3><ul class="l">{''.join(f"<li>{o}</li>" for o in obj)}</ul><p class="note"><b>Today you make:</b> {d["make"]}</p></div>
{SK.today(n)}<div class="card"><h3>⏱ Your 2 hours</h3><table class="tt">{''.join(f"<tr><td>{TB[i]}</td><td><b>{a}</b><br>{x}</td></tr>" for i,(a,x) in enumerate(tt))}</table></div>
<div class="card"><h3>📚 The lesson</h3><p><b>Word of the day: {d["word"][0]}</b>: {d["word"][1]}</p><p style="margin-top:10px">{b[1]}</p><ul class="l" style="margin-top:10px">{tooldesc}</ul>{wbl}{plan21}</div>
<div class="card"><h3>🔨 Build tasks on the business site</h3><ol class="l">{''.join(f"<li>{s}</li>" for s in steps)}<li>Commit and push, then check the live site: <a href="{BIZ}">business site</a>.</li></ol></div>
<div class="card"><h3>🚀 Challenge</h3><p>{chal}</p></div>
<div class="card quiz"><h3>❓ Quick quiz</h3>{''.join(f"<details><summary>{i+1}. {q}</summary><p>{a}</p></details>" for i,(q,a) in enumerate(quiz))}</div>
<div class="grid"><div class="card"><h3>🧰 Tools</h3><div class="chips">{tools}</div></div><div class="card"><h3>🌱 Life skills</h3><div class="chips">{life}</div></div>
<div class="card"><h3>👨 Dad's role</h3><p>{d["dad"]}</p></div></div>
<div class="grid" style="margin-top:20px"><div class="card"><h3>✅ Done when</h3><ul class="l">{''.join(f"<li>☐ {x}</li>" for x in done)}</ul></div>
<div class="card"><h3>📝 Reflect (goes into progress.json)</h3><p><b>Journal prompt:</b> {ex.get("journal","What did I learn today?")}</p><p class="note">Fill in today's entry: <code>built</code>, <code>learned</code>, <code>proud</code> (e.g. "{strip(d["proud"])}"), <code>commit</code>. Set <code>status</code> to <code>"done"</code>.</p></div></div>
<div class="pn">{pv}{nx}</div></div></section>'''
    page(f'learn/day-{n:02d}.html',f'Day {n}: {strip(d["title"])}',body)
    days.append({"day":n,"date":str(date),"week":wk,"plan":strip(d["title"]),"lesson":f"learn/day-{n:02d}.html","status":"upcoming","built":"","learned":"","proud":"","commit":"","dad_note":""})
json.dump({"start":"2026-10-17","days":days},open('progress.json','w'),indent=2,ensure_ascii=False)
# week overview + review pages
for w in (1,2,3):
    for kind,idx in (("week",weekintro[w]),("review",review.get(w))):
        if idx is None: continue
        page(f'learn/{kind}-{w}.html',f'Week {w} {kind}',f'<section style="padding:40px 0"><div class="w"><div class="label">Week {w} · {"Overview" if kind=="week" else "Self-review"}</div><h2>{D.WEEKS[w-1]["theme"]}</h2>{IFR.format("raw/l21-%02d.html"%idx)}</div></section>')
# tools page
tc=''.join(f'<div class="card"><h3>{t["name"]} <span class="st upcoming">{t["tag"]}</span></h3><p>{t["what"]}</p><p class="note"><b>You\'ll use it for:</b> {t["use"]}</p><p class="note">Learned on: '+', '.join(f'<a href="day-{n:02d}.html">Day {n}</a>' for n,d in enumerate(D.DAYS,1) if k in d['tools'])+'</p></div>' for k,t in D.TOOLS.items())
page('learn/tools.html',"Tools I'll master",hero("Tools I'll master","Fourteen <span class='g'>real tools</span>.","The same tools professionals use, each learned on the day I need it.")+f'<section style="padding-top:0"><div class="w"><div class="grid">{tc}</div><details class="quiz" style="margin-top:20px"><summary>The toolkit page from the 21-day plan</summary>{IFR.format("raw/l21-%02d.html"%toolsec)}</details></div></section>')
# plan21 extra pages
P21=[]
for i,sct in enumerate(L21S):
    t=re.sub(r'\s+',' ',strip(sct)).strip()
    if any(t.startswith(k) for k in ('Start here','For Mum','The framework','The overview','Your real project','Tracker 1','Tracker 2','Tracker 3','For the counsellor','Keep going')):
        title=re.sub(r'\s+',' ',strip(re.search(r'<h1[^>]*>(.*?)</h1>',sct,re.S).group(1))) if '<h1' in sct else t[:40]
        P21.append((i,title)); page(f'learn/plan21-{i:02d}.html',title,f'<section style="padding:40px 0"><div class="w"><div class="label">The 21-day plan</div><h2>{title}</h2>{IFR.format("raw/l21-%02d.html"%i)}</div></section>')
# learn index
wkhtml=''
for w in (1,2,3):
    W=D.WEEKS[w-1];a,bb=W['range']
    wkhtml+=f'<div class="card"><div class="label">Week {w}</div><h3>{W["theme"]}</h3><p>{W["intro"]}</p><ul class="l" style="margin-top:10px">'+''.join(f'<li><a href="day-{n:02d}.html">Day {n} · {D.date(n).strftime("%a %-d %b")}: {D.DAYS[n-1]["title"]}</a>{" 🎤" if D.DAYS[n-1].get("show") else ""}</li>' for n in range(a,bb+1))+f'</ul><p class="note"><b>Milestone:</b> {W["milestone"]}</p><p class="note"><a href="week-{w}.html">Week overview</a> · <a href="review-{w}.html">Self-review</a></p></div>'
page('learn/index.html','Learn',hero("Learn","A real <span class='g'>21-day</span> program.","2 hours a day, side by side with Dad, Sat 17 Oct to Fri 6 Nov 2026. Each day has a timetable, objectives, the lesson, build tasks on the business site, a challenge, a quiz and a reflection.")+f'''<section style="padding-top:0"><div class="w"><p style="margin-bottom:24px"><a class="btn" href="../outcomes.html">🎯 By Day 21, I can… (the outcomes)</a></p><div class="grid">{wkhtml}</div>
<h2 style="margin-top:50px">Web Basics guide</h2><p class="sub">The full guide, one lesson per page, with every diagram.</p><div class="grid">'''+''.join(f'<a class="card" style="text-decoration:none" href="wb-{i:02d}.html"><div class="label">Lesson {i}</div><h3>{WBT[i]}</h3></a>' for i in range(1,14))+'''<a class="card" style="text-decoration:none" href="../outcomes.html"><div class="label">The goal</div><h3>By Day 21, I can…</h3></a><a class="card" style="text-decoration:none" href="tools.html"><div class="label">Toolkit</div><h3>Tools I'll master</h3></a></div>
<h2 style="margin-top:50px">From the 21-day plan</h2><div class="grid">'''+''.join(f'<a class="card" style="text-decoration:none" href="plan21-{i:02d}.html"><div class="label">21-day plan</div><h3>{t}</h3></a>' for i,t in P21)+'''</div></div></section>''')
print("days mapped",daysec,weekintro,review,toolsec)
# ================= PART 2: main pages =================
OUT=["Build and deploy a professional website","Run my own live business site on my own domain","Pitch Tomas Web Studio to a local business","Quote and price a job from my business plan","Set up a client's Instagram and Postiz scheduling","Handle domains, DNS and hosting","Use GitHub change control: commits, branches, pull requests, rollbacks","Track money in and out"]
page('outcomes.html','By Day 21, I can',hero("The outcome · Launch Day, Fri 6 Nov 2026","By Day 21, I can <span class='g'>launch my business</span>.","Truly launch Tomas Web Studio to the public, with pride and excitement, and start making money.")+f'''<section style="padding-top:0"><div class="w"><div class="grid">
<div class="card"><h3>✅ By Day 21, I can…</h3>{''.join(f'<div class="tick"><span>{o}</span><span class="st upcoming">upcoming</span></div>' for o in OUT)}<p class="note">These tick off on the <a href="tracker.html">tracker</a> as I go.</p><p style="margin-top:12px"><a class="btn o" href="skills.html">The skills framework →</a> <a class="btn o" href="careers.html">And after that? Where this can take me →</a></p></div>
<div class="card feat"><h3>🚀 Launch Day · Fri 6 Nov</h3><ul class="l"><li>The business site goes public on its own domain</li><li>Announced on Instagram (scheduled in Postiz)</li><li>My first pitches booked with local businesses</li><li>Target: my first paying client in the following weeks</li><li>Launch-night show-and-tell with the family</li></ul><p style="margin-top:14px"><a class="btn" href="learn/day-21.html">See the Launch Day lesson</a></p></div></div>
<h2 style="margin-top:40px">How week 3 builds to launch</h2><div class="grid">'''+''.join(f'<a class="card" style="text-decoration:none" href="learn/day-{n:02d}.html"><div class="label">Day {n} · {D.date(n).strftime("%a %-d %b")}</div><h3>{"Launch Day: go public!" if n==21 else D.DAYS[n-1]["title"]}</h3></a>' for n in range(15,22))+'</div></div></section>')
# journey section (from rich backup) + home
rich=open('/workspace/tomas-site-v-rich-backup/index.html').read()
jour=re.search(r'<section id="journey">.*?</section>',rich,re.S).group(0).replace('href="tracker.html"','href="tracker.html"')
jour=re.sub(r'<div class="day upcoming"><b>Day (\d+)</b>',lambda m:f'<a class="day upcoming" style="text-decoration:none" href="learn/day-{int(m.group(1)):02d}.html"><b>Day {m.group(1)}</b>',jour).replace('<br></div>','<br></a>')
pill=["Structure","Commitment","Discipline","Planning","Timelines","Money skills","Communication","Ownership","Resilience","School on time"]
page('index.html','Home',f'''<header><div class="w"><div class="tag">🌊 Northern Beaches · Level up · 17 Oct to 6 Nov 2026</div>
<h1>Tomas is <span class="g">levelling up</span>.</h1><p class="lead">A 21-day turnaround built on real work: 2 hours a day, side by side with Dad, building and launching a real business, and the habits that come with it.</p>
<div class="cta"><a class="btn" href="outcomes.html">By Day 21, I can…</a><a class="btn o" href="tracker.html">Daily tracker</a><a class="btn o" href="skills.html">Skills framework</a><a class="btn o" href="careers.html">Where this can take me</a><a class="btn o" href="{BIZ}">Watch the business site grow →</a></div></div></header>
<section style="padding-top:20px"><div class="w r"><div class="label">The turnaround</div><h2>Building the business. Building myself.</h2><p class="sub">The website is the vehicle. The destination is the person: someone who shows up, plans, finishes what he starts and is proud of his work.</p>
<div class="chips">{''.join(f'<span class="chip">{p}</span>' for p in pill)}</div></div></section>
<section><div class="w r"><div class="grid">
<div class="card"><h3>🕓 The daily routine</h3><ul class="l"><li><b>School first:</b> at school on time, every day</li><li><b>4:30–6:30pm</b> the 2-hour build session at Dad's, straight after school</li><li><b>6:30pm</b> commit + journal line, then the evening is his</li><li><b>Weekends:</b> same 2 hours, Tomas picks when</li></ul></div>
<div class="card"><h3>🎤 Weekly show-and-tells</h3><ul class="l"><li><b>Fri 23 Oct:</b> homepage online</li><li><b>Fri 30 Oct:</b> full site working</li><li><b>Fri 6 Nov:</b> Launch Day, live on his own domain</li></ul><p class="note">Mum, the grandparents, and Melanie and Sio (The Burdekin) are warmly invited. <a href="support.html">What I need from all of you →</a></p></div>
<div class="card"><h3>📚 A real learning program</h3><p>21 days of lessons, each with a timetable, objectives, build tasks, a quiz and a reflection.</p><p style="margin-top:12px"><a class="btn o" href="learn/index.html">Open the Learn program</a></p></div></div></div></section>
{jour}''')
# ambition (reuse rich, swap nav/foot)
def body_of(fn):
    s=open('/workspace/tomas-site-v-rich-backup/'+fn).read(); return re.search(r'</nav>(.*?)<footer',s,re.S).group(1)
page('ambition.html','My ambition',body_of('ambition.html').replace('<div class="grid">','<p style="margin-bottom:20px"><a class="btn" href="outcomes.html">By Day 21, I can…</a></p><div class="grid">',1))
tools=[(t['name'],"progress" if k in('grok','gh') else "upcoming") for k,t in D.TOOLS.items()]
life=[(v[1],"progress" if k in('routine','school','plan') else "upcoming") for k,v in D.LIFE.items()]
lab={"done":"✓ done","progress":"in progress","upcoming":"upcoming"}
def lst(h,xs): return f'<div class="card"><h3>{h}</h3>'+''.join(f'<div class="tick"><span>{n}</span><span class="st {k}">{lab[k]}</span></div>' for n,k in xs)+'</div>'
page('learning.html',"What I'm learning",hero("What I'm learning","Tools <span class='g'>+</span> life skills","14 professional tools and 11 life skills. Each one ticks over to done when I can do it myself.")+f'<section style="padding-top:0"><div class="w"><div class="grid">{lst("🧰 Tools",tools)}{lst("🌱 Life skills",life)}</div><p class="note"><a href="learn/tools.html">Tools I\'ll master: full details →</a></p><!-- UPDATE: change "st upcoming" to "st progress" or "st done" --></div></section>')
# support
page('support.html','What I need from all of you',hero("From Tomas · to Mum, my grandparents, Melanie and Sio","What I need from <span class='g'>all of you</span>.","I&rsquo;ve worked out a program with my dad, who is going to teach me, and I want everyone&rsquo;s support to make this a success. Thanks for being in my corner. Here&rsquo;s how you can help me actually pull this off.")+'''<section style="padding-top:0"><div class="w stack">
<div class="card"><div class="label">1</div><h3>This is my choice</h3><p>This is what I want to do. Nobody's making me. It's my business and my future, and I really want to see it through.</p></div>
<div class="card"><div class="label">2</div><h3>Why I need 21 days at Dad's, without interruptions</h3><p>I need these 3 weeks at Dad's to get my routine right. Same place, same time, every day. That's how you actually build habits. I read that research on habits says the same thing: doing the same thing in the same place over and over is what makes it stick (<a href="https://onlinelibrary.wiley.com/doi/10.1002/ejsp.674">Lally and others, 2010</a>).</p><p style="margin-top:10px">If I get pulled somewhere else, even for a good reason, my streak breaks and it's way harder to get going again. So please help me keep it steady.</p></div>
<div class="card feat"><div class="label">3</div><h3>What I'm asking</h3><ul class="l"><li>Please back me, out loud. It really helps when everyone says the same thing.</li><li>Please don't pull me in other directions, even if you mean well.</li><li>4:30 to 6:30 on school days is my time with Dad. Please keep it free (and my 2 hours on weekends).</li><li>Please don't make plans that take me away from Dad's for these 3 weeks.</li><li>Check my <a href="tracker.html">tracker</a> and tell me when I'm doing well.</li></ul></div>
<div class="card"><div class="label">4</div><h3>How you can be part of it</h3><div class="grid" style="margin-top:10px">
<div><h3>🏡 Come and visit</h3><p>Come and visit whenever you want, as much as you want. I'll show you what I'm building.</p></div>
<div><h3>🎤 Fridays</h3><p>Come to my show-and-tells: 23 Oct, 30 Oct and 6 Nov (Launch Day!). In person or on video.</p></div>
<div><h3>🍦 Treats</h3><p>Take me out for a treat or a movie night, a special dinner, or let me have friends over. Just around my sessions.</p></div>
<div><h3>🏆 Rewards</h3><p>If I hit my milestones, a reward would be awesome (yes, money counts!).</p></div>
<div><h3>💬 Messages</h3><p>Send me a message when you check my tracker, or ask Dad to add a note on that day.</p></div></div></div>
<div class="card"><div class="label">5</div><h3>🧭 Melanie and Sio (The Burdekin)</h3><p>Melanie and Sio, you can see everything I'm doing: my tracker and streak, my commits on GitHub, my journal lines, my weekly reviews and my show-and-tells. Please come by or check in whenever suits, and use it in our sessions. I'd like help connecting what I'm learning here (routine, owning my stuff, not giving up, talking to people) to school and everything else.</p></div>
<div class="card"><h3>Mum, Nan and Pop, Dad</h3><p>I know you all want the best for me. This is what the best looks like for me right now. Thanks for backing me.</p></div>
<div class="card" style="text-align:center;padding:44px;background:linear-gradient(135deg,#ff6b4a26,#5ee7c922)"><h2>Three weeks. One focus. <span class="g">Everyone in my corner.</span></h2><p class="note">Tomas</p></div>
</div></section>''')
# plan with scenarios
pb=body_of('plan.html')
scen='''<h2 style="margin-top:50px">Forecast: 3 scenarios (headline)</h2><p class="sub">From the business plan's 2-year forecast. Every figure is a forecast, not a promise.</p><div class="grid">
<div class="card"><div class="label">Conservative</div><div class="price">~A$81k</div><p>2-year net profit · about 48 sites over 2 years · 14 monthly clients by the end · break-even Mar 2027</p></div>
<div class="card feat"><div class="label">Realistic</div><div class="price">~A$239k</div><p>2-year net profit · about 114 sites over 2 years · 52 monthly clients by the end · break-even Jan 2027</p></div>
<div class="card"><div class="label">Stretch</div><div class="price">~A$559k</div><p>2-year net profit · about 281 sites over 2 years (a helper in year 2) · 158 monthly clients by the end · break-even Jan 2027</p></div></div>
<p class="note">Assumes build capacity of about 3 sites a week (Dad + Tomas + Grok Bot) and 4–6% monthly churn. Prices: builds A$1,500–3,000 (example A$1,800), website care A$99/mo, Instagram care A$300–500/mo.</p>'''
pb=pb.rsplit('</div></section>',1); pb=pb[0]+scen+'</div></section>'+pb[1]
page('plan.html','The business plan',pb+f'<section style="padding-top:0"><div class="w"><a class="btn o" href="{BIZ}">Watch the business site grow →</a></div></section>')
# tracker
tr=open('/workspace/tomas-site-v-rich-backup/tracker.html').read()
tb=re.search(r'</nav>(.*?)<footer',tr,re.S).group(1); tj=re.search(r'<script>\nconst L.*?</script>',tr,re.S).group(0)
tj=tj.replace('+f("Dad\'s note",x.dad_note)}','+f("Dad\'s note",x.dad_note)+"<p><a class=\'btn o\' href=\'"+x.lesson+"\'>Open the Day "+x.day+" lesson →</a></p>"}')
outc=''.join(f'<div class="tick"><span>{o}</span><span class="st upcoming">upcoming</span></div>' for o in OUT)
tb=tb.replace('<div class="card" style="margin-top:20px"><h3>Calendar','<div class="card" style="margin-top:20px"><h3>🎯 By Day 21, I can… <a href="outcomes.html" style="font-size:.8rem">(details)</a></h3><!-- UPDATE: change "st upcoming" to "st done" + text "✓ done" -->'+outc+'</div><div class="card" style="margin-top:20px"><h3>Calendar')
page('tracker.html','Daily tracker',tb,tj)
open('README.md','w').write(f'''# Tomas Levels Up (private family site)

Live: https://finlaysonnick74-source.github.io/tomas-level-up/ · Business site: {BIZ}

Light privacy screen only: the passcode (levelup2026) is in gate.js, and the site is public on GitHub Pages. noindex + robots.txt keep it out of search engines.

## Daily update (2 minutes)
1. Open `progress.json`, find today's day.
2. Set `status` to `"progress"` when you start, `"done"` when you finish.
3. Fill `built`, `learned`, `proud` (answer the day's reflection prompt) and paste your `commit` link. Dad can add `dad_note`.
4. `git add progress.json && git commit -m "Day N done" && git push`
5. About a minute later the tracker (calendar, progress bar, streak) updates by itself.

To tick an outcome or a skill, change `st upcoming` to `st done` in tracker.html / outcomes.html / learning.html.
Lesson pages are generated by `build.py` + `curriculum.py` from the Web Basics guide and the 21-day plan.
''')

from careers import careers_body
page('careers.html','Where this can take me',careers_body().replace('<section style="padding-top:0">','<section style="padding-top:0"><div class="w"><p style="margin-bottom:16px"><a class="btn" href="skills.html">See the skills framework: what I\'m learning →</a></p></div>',1))
page('skills.html','Skills framework',SK.page_body())
import library;EXCL=library.build(page,IFR,strip)
import subprocess;subprocess.run(['python3','postfix.py'])
# ===== today.html + dashboard =====
PICK='''function pick(D){var t=new Date();t.setHours(0,0,0,0);var p=D.find(function(x){return x.status=="progress"});if(p)return p;
var byDate=D.find(function(x){return new Date(x.date+"T00:00")>=t});var firstUp=D.find(function(x){return x.status!="done"});
if(new Date(D[0].date+"T00:00")>t)return D[0];return byDate&&byDate.status!="done"?byDate:(firstUp||D[D.length-1])}'''
page('today.html','Today','<section style="padding:80px 0"><div class="w"><h2>Finding today\'s lesson…</h2><p><a href="learn/index.html">Open the program</a></p></div></section>',f'<script>{PICK}fetch("progress.json?"+Date.now()).then(r=>r.json()).then(d=>{{location.replace(pick(d.days).lesson)}})</script>')
SKM=json.dumps({k:[s[2] for s in L] for k,_,_,L in SK.G})
SHOWS=[("2026-10-23","Fri 23 Oct","Homepage online"),("2026-10-30","Fri 30 Oct","Full site working"),("2026-11-06","Fri 6 Nov","Launch Day")]
WKM=json.dumps([strip(W['milestone']) for W in D.WEEKS])
dash=f'''<section style="padding:10px 0 40px" aria-label="Progress at a glance"><div class="w"><div class="label">Progress at a glance</div>
<div class="dash">
<div class="card" style="display:flex;gap:18px;align-items:center"><svg class="ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="50" stroke="#ffffff18" stroke-width="12" fill="none"/><circle id="rg" cx="60" cy="60" r="50" stroke="url(#rgg)" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="314" stroke-dashoffset="314" transform="rotate(-90 60 60)" style="transition:stroke-dashoffset 1.2s"/><defs><linearGradient id="rgg"><stop offset="0" stop-color="#ff6b4a"/><stop offset="1" stop-color="#5ee7c9"/></linearGradient></defs><text id="rgt" x="60" y="68" text-anchor="middle" font-size="24" font-weight="900" fill="#fff">0%</text></svg>
<div><div class="note" style="margin:0">Today</div><div class="kpi">Day <span id="dn">0</span></div><div class="note" style="margin:0"><span id="dd">0</span> of 21 done</div></div></div>
<div class="card"><div class="note" style="margin:0">Streak</div><div class="kpi">🔥 <span id="sk">0</span></div><div class="note">days in a row</div></div>
<div class="card"><div class="note" style="margin:0">Next show-and-tell</div><div class="kpi" style="font-size:1.8rem" id="ns">Fri 23 Oct</div><div class="note" id="nst">Homepage online</div></div>
<div class="card"><div class="note" style="margin:0">Skills practised so far</div><div style="display:flex;gap:16px;margin-top:6px"><div><div class="kpi" style="font-size:2rem" id="sA">0</div><div class="note" style="margin:0">Hard</div></div><div><div class="kpi" style="font-size:2rem" id="sB">0</div><div class="note" style="margin:0">Soft</div></div><div><div class="kpi" style="font-size:2rem" id="sC">0</div><div class="note" style="margin:0">Life</div></div></div></div>
</div>
<div class="grid" style="margin-top:16px"><div class="card"><div class="label">This week's milestone · Week <span id="wn">1</span></div><p id="wm"></p></div>
<div class="card"><div class="label">Latest build log</div><p id="lg"><b>Day 0:</b> Dad and I set up this site. Watch it change.</p></div>
<div class="card" style="display:flex;flex-direction:column;justify-content:center;gap:10px"><a class="btn" id="tl" href="learn/day-01.html" style="text-align:center;font-size:1.1rem">See today's lesson →</a><a class="btn o" href="tracker.html" style="text-align:center">Open the tracker</a></div></div></div></section>
<section style="padding:0 0 40px"><div class="w r"><div class="card" style="background:linear-gradient(135deg,#ff6b4a1f,#5ee7c91a)"><div class="label">New here? Start here</div><h2 style="font-size:1.8rem">Welcome, family 👋</h2>
<div class="grid" style="margin-top:14px"><div><h3>1 · What this is</h3><p>A 21-day program where Tomas spends 2 hours a day (4:30–6:30pm on school days) with Dad, learning real skills by building and launching his own web studio.</p></div>
<div><h3>2 · How to read the tracker</h3><p>Each day turns <b>in progress</b>, then <b>✓ done</b>. Tap a day to see what he built, learned and is proud of, plus Dad's note. The streak counts days in a row.</p></div>
<div><h3>3 · From Tomas</h3><p>"I&rsquo;ve worked out a program with my dad, who is going to teach me, and I want everyone&rsquo;s support to make this a success. This is what I want to do. I need these 3 weeks at Dad's to get my routine right, so please back me and keep 4:30–6:30 free. Come and visit whenever you want!" <a href="support.html">What I need from all of you →</a></p></div></div></div></div></section>
<script>{PICK}
var SK={SKM},WK={WKM},SH={json.dumps(SHOWS)};
fetch("progress.json?"+Date.now()).then(r=>r.json()).then(function(d){{var D=d.days,done=D.filter(x=>x.status=="done"),dn=done.map(x=>x.day),t=pick(D);
var pct=Math.round(done.length/21*100);document.getElementById("rg").style.strokeDashoffset=314-314*pct/100;document.getElementById("rgt").textContent=pct+"%";
document.getElementById("dn").textContent=t.day;document.getElementById("dd").textContent=done.length;
var st=0,l=D.map(x=>x.status).lastIndexOf("done");for(var i=l;i>=0&&D[i].status=="done";i--)st++;document.getElementById("sk").textContent=st;
var w=t.week||Math.ceil(t.day/7);document.getElementById("wn").textContent=w;document.getElementById("wm").textContent=WK[w-1];
var today=new Date();today.setHours(0,0,0,0);var ns=SH.find(s=>new Date(s[0]+"T00:00")>=today)||SH[2];document.getElementById("ns").textContent=ns[1];document.getElementById("nst").textContent=ns[2];
["A","B","C"].forEach(function(k){{document.getElementById("s"+k).textContent=SK[k].filter(ds=>ds.some(x=>dn.indexOf(x)>=0)).length}});
if(done.length){{var x=done[done.length-1];document.getElementById("lg").innerHTML="<b>Day "+x.day+":</b> "+(x.built||x.plan)+(x.proud?" <i>Proud of: "+x.proud+"</i>":"")}}
document.getElementById("tl").href=t.lesson;document.getElementById("tl").textContent="See today's lesson: Day "+t.day+" →"}});
</script>'''
s=open('index.html').read()
s=s.replace('</header>','</header>'+dash,1)
s=s.replace('<a class="btn" href="outcomes.html">By Day 21, I can…</a>','<a class="btn" href="today.html">See today\'s lesson</a><a class="btn o" href="outcomes.html">By Day 21, I can…</a>',1)
s=s.replace('<a class="btn o" href="{BIZ}">','<a class="btn o" href="ambition.html">My ambition</a><a class="btn o" href="plan.html">The business plan</a><a class="btn o" href="'+BIZ+'">')
open('index.html','w').write(s)
# ===== transformation story + school page =====
story='''<section style="padding:0 0 40px" aria-label="My transformation story"><div class="w r"><div class="label">My transformation story</div><h2>A story in the making</h2><div class="grid" style="margin-top:16px">
<div class="card"><div class="label">Chapter 1</div><h3>Where I'm starting</h3><p>I haven't had much structure so far, and I'm ready to change that. I've got ideas, I'm good with tech, and I've chosen to put in the work.</p></div>
<div class="card" id="ch2"><div class="label">Chapter 2</div><h3>The 21 days</h3><p id="ch2t">Starting Sat 17 Oct: 2 hours a day with Dad, building my business and my routine.</p><div class="bar2"><i id="ch2b" style="width:0%"></i></div></div>
<div class="card" id="ch3"><div class="label">Chapter 3</div><h3>Launch and beyond</h3><p id="ch3t">Coming on Fri 6 Nov: Launch Day. My site goes public, my first pitches are booked, and my first paying client is the next goal.</p></div>
</div></div></section>
<script>fetch("progress.json?"+Date.now()).then(r=>r.json()).then(function(d){var D=d.days,done=D.filter(x=>x.status=="done");
if(done.length){var last=done[done.length-1];document.getElementById("ch2t").innerHTML="<b>"+done.length+" of 21 days done.</b> Latest: Day "+last.day+", "+(last.built||last.plan)+(last.proud?". Proud of: "+last.proud:"")+".";}
document.getElementById("ch2b").style.width=(done.length/21*100)+"%";
var l=D[20];if(l.status=="done"){document.getElementById("ch3t").innerHTML="<b>Launched! 🚀</b> "+(l.built||"Tomas Web Studio is live.")+(l.proud?" "+l.proud:"")}
else if(done.length>=14){document.getElementById("ch3t").innerHTML="<b>Launch countdown: "+(21-done.length)+" days to go.</b> Site going public, first pitches being booked."}});</script>'''
s=open('index.html').read()
s=s.replace('<section style="padding:0 0 40px"><div class="w r"><div class="card" style="background:linear-gradient(135deg,#ff6b4a1f','STORYMARK<section style="padding:0 0 40px"><div class="w r"><div class="card" style="background:linear-gradient(135deg,#ff6b4a1f',1).replace('STORYMARK',story,1)
s=s.replace('<a class="btn o" href="careers.html">Where this can take me</a>','<a class="btn o" href="careers.html">Where this can take me</a><a class="btn o" href="school.html">Why school is part of my plan</a>',1)
open('index.html','w').write(s)
J="https://www.jobsandskills.gov.au/data/occupation-and-industry-profiles/occupations/"
page('school.html','Why staying in school is part of my plan',hero("In my words","Why staying in school is <span class='g'>part of my plan</span>.","I want to build a real business and a great career. Finishing school while I do this program is how I open the most doors.")+f'''<section style="padding-top:0"><div class="w stack">
<div class="card"><h3>Every path deserves respect</h3><p>Trades, apprenticeships, starting work, uni: people I respect have taken all of them, and they're all great paths. I'm choosing this one because it fits what I love: tech, building things and running my own business.</p></div>
<div class="card"><h3>📘 School subjects that fit my plan</h3><p>The NSW HSC now has two courses made for what I'm doing: <b>Software Engineering</b> (programming, web, secure software, automation) and <b>Enterprise Computing</b> (UX, networking, cybersecurity, data). They started in 2024. (<a href="https://education.nsw.gov.au/teaching-and-learning/curriculum/tas/leading-tas-7-12/software-engineering-11-12-syllabus-information">NSW Education</a>)</p></div>
<div class="card"><h3>🎓 TAFE and uni pathways</h3><p>Finishing school keeps every option open: TAFE NSW courses in IT and digital, uni degrees in software, cyber or data, and programs like the APS Data and Digital Cadet Program and the ASD Cadetship, which are for uni students. (<a href="https://content.apsjobs.gov.au/career-pathways/data-and-digital-cadet-program">APSJobs</a>, <a href="https://www.asd.gov.au/careers/im-starting-my-career">ASD</a>)</p></div>
<div class="card"><h3>🏅 Certifications alongside school</h3><p>I can add things like AWS Certified Cloud Practitioner and Google Career Certificates while I study.</p></div>
<div class="card"><h3>💼 Where it leads</h3><p>IT careers pay well. Jobs and Skills Australia reports median full-time weekly earnings of <b>A$2,537</b> for software and applications programmers and <b>A$2,476</b> for web developers and multimedia specialists, compared with <b>A$1,852</b> across all occupations (ABS, May 2025). <a href="careers.html">See all the careers →</a></p><p class="note">Sources: <a href="{J}2613-software-and-applications-programmers">JSA 2613</a>, <a href="{J}2612-multimedia-specialists-and-web-developers">JSA 2612</a>, viewed Oct 2026.</p></div>
<div class="card feat"><h3>Why this one is mine</h3><p>School gives me the qualifications. This program gives me real skills, a real business and the routine to keep going. Together they open the most doors, and I want all of them open.</p></div>
</div></section>''')
for fn,anchor in [('careers.html','<a class="btn" href="outcomes.html">Start with: By Day 21, I can…</a>'),('support.html','<div class="card"><h3>Mum, Nan and Pop, Dad</h3>')]:
    s=open(fn).read(); s=s.replace(anchor,('<a class="btn o" href="school.html">Why school is part of my plan</a> ' if fn=='careers.html' else '<div class="card"><h3>📘 School is part of my plan</h3><p>I&rsquo;m staying in school too. <a href="school.html">Here&rsquo;s why →</a></p></div>')+anchor,1); open(fn,'w').write(s)
import subprocess;subprocess.run(['python3','postfix.py'])
# ===== core message pull-quote =====
Q='<blockquote class="pq"><p>&ldquo;Give me the space to do something I want to do, and get behind me.&rdquo;</p><cite>Tomas</cite></blockquote>'
css=open('style.css').read()
if '.pq{' not in css:
    css+='\n.pq{margin:0 0 22px;padding:34px 36px;border-radius:24px;background:linear-gradient(135deg,#ff6b4a,#ffb443);color:#141018;box-shadow:0 20px 50px -20px #ff6b4a88}.pq p{font-size:clamp(1.6rem,4vw,2.6rem);font-weight:900;line-height:1.15;letter-spacing:-.02em;margin:0}.pq cite{display:block;margin-top:12px;font-style:normal;font-weight:700;opacity:.8}\n'
    open('style.css','w').write(css)
s=open('index.html').read()
s=s.replace('<div class="label">New here? Start here</div>','<div class="label">New here? Start here</div>'+Q,1); open('index.html','w').write(s)
s=open('support.html').read()
s=s.replace('<section style="padding-top:0"><div class="w stack">','<section style="padding-top:0"><div class="w stack">'+Q,1); open('support.html','w').write(s)
