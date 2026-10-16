import re,os,shutil,html
def build(page,IFR,strip):
    os.makedirs('library/raw/img',exist_ok=True)
    shutil.copy('/workspace/bakery-mockups-html/base.css','library/raw/doc.css')
    shutil.copy('/workspace/plan/base.css','library/raw/guide.css')
    FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600;700&family=Fraunces:wght@400;600;800&display=swap">'
    fit='<script>function f(){var w=document.querySelector(".page")||document.body.firstElementChild;var z=Math.min(1,innerWidth/((w&&w.scrollWidth)||794));if(document.querySelector(".page"))document.body.style.zoom=z}addEventListener("load",f);addEventListener("resize",f)</script>'
    SCRUB=[("On my Level up plan, I work after 4:30pm and some weekend hours. Homework comes before client work. If grades slip, I take fewer clients.","I work from 4:30pm on school days and some weekend hours. If school needs more time, I take fewer clients."),
      ("a day with Dad's team at Innovo","a day at work with Dad"),("a day at Innovo","a day at work with Dad"),("A day with Dad's team at Innovo","A day at work with Dad"),
      ("no drinking or weed today","rested, sharp and healthy today"),("Illegal e-bikes can be confiscated.","Non-compliant e-bikes can be confiscated."),("Police can seize illegal e-bikes.","Non-compliant e-bikes can be confiscated."),
      ("Ground rules first: ","The basics first: "),("so it feels like yours and not homework.","so it feels like yours, not a chore."),("Live the ground rules (next page) · ","")]
    def scrub(s):
        for a,b in SCRUB: s=s.replace(a,b)
        return s
    def raw(fn,css,body,head=''):
        open('library/raw/'+fn,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><script src="../../gate.js"></script>{FONTS}<link rel="stylesheet" href="{css}">{head}<style>body{{margin:0 auto;background:#fff}} .page{{margin:0 auto!important;box-shadow:none!important}} img{{max-width:100%;height:auto}}</style></head><body>{body}{fit}</body></html>')
    def doc(src,fn,cssname):
        s=open(src).read()
        head=re.search(r'<head>(.*?)</head>',s,re.S|re.I); h=head.group(1) if head else ''
        h=re.sub(r'<link[^>]*>','',h); body=re.search(r'<body[^>]*>(.*)</body>',s,re.S|re.I); body=body.group(1) if body else s
        return scrub(h),scrub(body)
    # business plan
    h,b=doc('/workspace/plan2/plan.html','business-plan.html','doc.css')
    # remove branded mock-up block: from the 'branded mock-ups' heading up to 'Alternative concepts'
    i=b.find('Mrs Jones The Baker: branded mock-ups'); j=b.find('Alternative concepts')
    if i>0 and j>i:
        st=b.rfind('<h',0,i); en=b.rfind('<h',0,j)
        b=b[:st]+'<div class=note><p><b>Branded mock-ups kept private.</b> The main Mrs Jones mock-ups use the bakery&rsquo;s real logo and photos, so they stay private until the bakery says yes in writing. The unbranded Canva concepts are shown below.</p></div>'+b[en:]
    b=re.sub(r'<img[^>]*src="\.\./bakery-mockups-html/[^"]*"[^>]*>','',b)
    # before/after uses their real homepage: drop that image (already removed) and keep text
    for f in os.listdir('/workspace/bakery-mockups'):
        if f.endswith('.png'): shutil.copy('/workspace/bakery-mockups/'+f,'library/raw/img/'+f)
    b=b.replace('../bakery-mockups/','img/')
    raw('business-plan.html','doc.css',b,h)
    for src,fn in [('/workspace/tb/b.html','tools-budget.html'),('/workspace/bp/p.html','prospects.html')]:
        h,b=doc(src,fn,'doc.css'); raw(fn,'doc.css',b,h)
    # level up guide
    g=open('/workspace/plan/guide.html').read()
    gh=scrub(re.sub(r'<link[^>]*>','',re.search(r'<head>(.*?)</head>',g,re.S).group(1)))
    P=re.split(r'(?=<div class="page)',g)[1:]
    P[-1]=P[-1].split('</body>')[0]
    EXCL={3:"Phase 1 ground rules page (private family rules and legal references)",4:"Pillar 1 'Clear head' (alcohol and drug health content)",5:"Pillar 1 'Clear head' athlete stories (alcohol and drug content)",18:"'Rough starts, big comebacks' stories (prison, arrests, drug dealing)",20:"'Your dad' story (names the other business and the family surname)"}
    for f in os.listdir('/workspace/plan/img'): shutil.copy('/workspace/plan/img/'+f,'library/raw/img/'+f)
    kept=[]
    for i,p in enumerate(P):
        if i in EXCL: continue
        t=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',p))).strip()
        title=t[:70]
        m=re.search(r'<h[12][^>]*>(.*?)</h[12]>',p,re.S)
        if m: title=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.group(1)))).strip()[:70]
        p=scrub(p).replace('src="img/','src="img/')
        raw(f'levelup-{i:02d}.html','guide.css',p,gh); kept.append((i,title))
    for k,(i,t) in enumerate(kept):
        pv=f'<a class="btn o" href="levelup-{kept[k-1][0]:02d}.html">← Previous</a>' if k else '<a class="btn o" href="levelup.html">← Contents</a>'
        nx=f'<a class="btn o" href="levelup-{kept[k+1][0]:02d}.html">Next →</a>' if k<len(kept)-1 else '<a class="btn o" href="levelup.html">Contents</a>'
        page(f'library/levelup-{i:02d}.html',t,f'<section style="padding:40px 0"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Library</a> › <a href="levelup.html">Level up game plan</a> › Page {k+1} of {len(kept)}</div><h2>{t}</h2><div class="pn">{pv}{nx}</div>{IFR.format("raw/levelup-%02d.html"%i)}<div class="pn">{pv}{nx}</div></div></section>')
    page('library/levelup.html','Level up: 12-month game plan',f'<section style="padding:50px 0"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Library</a> › Level up</div><div class="label">The 12-month game plan</div><h2>Level up</h2><p class="sub">Five pillars, four phases, one year. Read it page by page.</p><div class="grid">'+''.join(f'<a class="card" style="text-decoration:none" href="levelup-{i:02d}.html"><div class="label">Page {k+1}</div><h3>{t}</h3></a>' for k,(i,t) in enumerate(kept))+'</div></div></section>')
    def docpage(fn,title,lead):
        page(f'library/{fn}',title,f'<section style="padding:40px 0"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Library</a> › {title}</div><h2>{title}</h2><p class="sub">{lead}</p>{IFR.format("raw/"+fn)}</div></section>')
    docpage('business-plan.html','The full business plan','Services, pricing, Instagram strategy, support costs, target audience, the 24-month 3-scenario forecast, &ldquo;Sales is the speed limit&rdquo;, assumptions and risks.')
    docpage('tools-budget.html','Tools budget','Every tool, what it costs, who pays, and what gets passed on to clients.')
    docpage('prospects.html','Brookvale prospects','Local businesses to approach with a free website and Instagram check (public business information).')
    cards=[("business-plan.html","📘","The full business plan","Services, prices, Instagram strategy, forecast and risks"),("tools-budget.html","🧾","Tools budget","Costs, who pays, and what's passed on"),("prospects.html","📍","Brookvale prospects","Local businesses to pitch"),("levelup.html","🏆","Level up: 12-month game plan",f"{len(kept)} pages"),("../learn/index.html","📚","The 21-day program","Every day, every lesson"),("../outcomes.html","🎯","By Day 21, I can…","The outcomes")]
    page('library/index.html','Library',f'<header style="padding:70px 0 30px"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › Library</div><div class="tag">Plans + library</div><h1>Everything, <span class="g">in one place</span>.</h1><p class="lead">The full plans, online. No PDFs needed.</p></div></header><section style="padding-top:0"><div class="w"><div class="grid">'+''.join(f'<a class="card" style="text-decoration:none" href="{h}"><div style="font-size:2rem">{e}</div><h3>{t}</h3><p>{d}</p></a>' for h,e,t,d in cards)+'</div></div></section>')
    return EXCL
