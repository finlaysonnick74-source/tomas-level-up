import re,html,json,os,shutil
NUM=r'(−?[\d,]+)'
def nums(seg,label,n):
    m=re.search(re.escape(label)+r'\s+'+r'\s+'.join([NUM]*n),seg)
    return [int(x.replace(',','').replace('−','-')) for x in m.groups()]
def clean(frag,T):
    frag=re.sub(r'<svg.*?</svg>|<img[^>]*>|<script.*?</script>|<style.*?</style>','',frag,flags=re.S)
    frag=re.sub(r'\s(style|class|width|height|align|bgcolor|cellpadding|cellspacing)=("[^"]*"|\'[^\']*\'|[^\s>]+)','',frag)
    frag=re.sub(r'<(/?)(div|section|span)[^>]*>',lambda m:'' if m.group(2)=='span' else f'<{m.group(1)}div>',frag)
    frag=re.sub(r'<table>','<div class="tbl"><table class="tt">',frag).replace('</table>','</table></div>')
    frag=re.sub(r'<h2>.*?</h2>','',frag,flags=re.S)
    for a,b in T: frag=frag.replace(a,b)
    frag=re.sub(r'(<div>\s*</div>)+','',frag)
    return frag
def build(page,T,SCRUB):
    s=open('/workspace/plan2/plan.html').read()
    body=re.search(r'<body[^>]*>(.*)</body>',s,re.S|re.I); s=body.group(1) if body else s
    parts=re.split(r'(?=<h2)',s)
    def P(k):
        for p in parts:
            if k in re.sub('<[^>]+>','',p[:300]): return p
        return ''
    TT=list(T)+list(SCRUB)+[("The honest bit","How I work"),("12. Key risks, honestly","Key risks")]
    txt=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s)))
    data={}
    for sc in ['Conservative','Realistic','Stretch']:
        i=txt.find(sc+' · year 1'); seg=txt[i:i+4000]
        data[sc]={'net':nums(seg,'Net profit',12),'cum':nums(seg,'Cumulative cash',12)}
    j=txt.find('Year 2 by quarter'); y2=txt[j:j+3000]
    for sc,nx in [('Conservative','Realistic'),('Realistic','Stretch'),('Stretch','Care · IG clients (end) 56')]:
        seg=y2[y2.find(sc):]
        data[sc]['q_net']=nums(seg,'Net profit',5)[:4]; data[sc]['q_cum']=nums(seg,'Cumulative cash (end)',4)
    os.makedirs('plan',exist_ok=True); os.makedirs('plan/img',exist_ok=True)
    for f in os.listdir('/workspace/bakery-mockups'):
        if f.endswith('.png'): shutil.copy('/workspace/bakery-mockups/'+f,'plan/img/'+f)
    SUB=[('index','Overview','🧭'),('opportunity','The opportunity','💡'),('services','Services and pricing','💳'),('living','Living websites','✨'),('instagram','Instagram strategy','📸'),('customers','Customers and the Northern Beaches','🌊'),('sales','How I win clients','🤝'),('costs','Support and costs','🧾'),('forecast','Forecast','📈'),('risks','Key risks','🛡'),('giving','Giving back','💛'),('roadmap','Roadmap','🗺')]
    def side(cur): return '<aside class="side"><div class="label">The business plan</div>'+''.join(f'<a class="{ "on" if k==cur else ""}" href="{k}.html">{e} {t}</a>' for k,t,e in SUB)+'<a href="../library/index.html">← Library</a></aside>'
    def mk(k,lead,inner):
        i=[x[0] for x in SUB].index(k); t=SUB[i][1]
        pv=f'<a class="btn o" href="{SUB[i-1][0]}.html">← {SUB[i-1][1]}</a>' if i else '<a class="btn o" href="../library/index.html">← Library</a>'
        nx=f'<a class="btn o" href="{SUB[i+1][0]}.html">{SUB[i+1][1]} →</a>' if i<len(SUB)-1 else '<a class="btn o" href="../library/index.html">Library →</a>'
        page(f'plan/{k}.html',t+' · Business plan',f'<section style="padding:40px 0 60px"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="../library/index.html">Library</a> › <a href="index.html">Business plan</a> › {t}</div><div class="planwrap">{side(k)}<div class="plancontent"><div class="label">Tomas Web Studio · Business plan</div><h1 style="font-size:clamp(2rem,4.5vw,3.2rem)">{SUB[i][2]} {t}</h1><p class="lead" style="margin:10px 0 24px">{lead}</p><div class="doc">{inner}</div><div class="pn">{pv}{nx}</div></div></div></div></section>')
    C=lambda k: clean(P(k),TT)
    tiles=lambda L:'<div class="tiles">'+''.join(f'<div class="tile"><div class="tv">{v}</div><div class="tl">{l}</div></div>' for v,l in L)+'</div>'
    mk('index','Websites + Instagram for local businesses, built by a 15-year-old who gets the internet.',tiles([("~2 wks","to build a modern site"),("A$1,800","example website build"),("A$99/mo","website care"),("~3/week","sites we can build")])+'<div class="card"><p>This plan has 12 short sections. Every price and number is a rough estimate or example to test with real clients, not a promise.</p></div><div class="grid" style="margin-top:20px">'+''.join(f'<a class="card" style="text-decoration:none" href="{k}.html"><div style="font-size:1.6rem">{e}</div><h3>{t}</h3></a>' for k,t,e in SUB[1:])+'</div><h2 style="margin-top:40px">How I work</h2>'+C('9. The honest bit'))
    mk('opportunity','Local businesses with a great story and an online shop window ready for a refresh.',C('1. The idea'))
    mk('services','Simple packages, clearly priced. Rough estimates to test with my first clients.','<div class="grid prices"><div class="card"><div class="label">One-off</div><h3>Website build</h3><div class="price">A$1,500–3,000</div><p class="note">Example: A$1,800</p><ul class="l"><li>Design and build, mobile-friendly</li><li>Google Maps, contact or order form</li><li>2 rounds of changes</li><li>About 2 weeks</li></ul></div><div class="card feat"><div class="label">Monthly</div><h3>Website care</h3><div class="price">A$99<small>/mo</small></div><ul class="l"><li>Hosting and updates</li><li>Menu and price changes</li><li>Small fixes</li><li>A quick monthly check</li></ul></div><div class="card"><div class="label">Monthly</div><h3>Instagram care</h3><div class="price">A$300–500<small>/mo</small></div><ul class="l"><li>12 posts + stories</li><li>Captions, hashtags, scheduling</li><li>A one-page monthly report</li></ul></div></div><div class="card" style="margin-top:20px"><p>Rough guesses only. Test them with the first 3 clients, then adjust. A &ldquo;both&rdquo; bundle (website care + Instagram) could get a small discount.</p></div><div class="card" style="margin-top:20px;border-color:#ffb44366"><h3>💛 Charities: free build</h3><p>I build websites for charities for free, to give back. <a href="giving.html">How giving back works →</a></p></div>')
    sc=P('The showcase'); sc=sc.split('SECTION 1')[0] if 'SECTION 1' in sc else sc
    imgs='<div class="grid">'+''.join(f'<figure class="card"><img src="img/{f}" alt="{a}" loading="lazy" style="width:100%;border-radius:12px"><figcaption class="note">{a} · <a href="https://{u}">Canva concept</a></figcaption></figure>' for f,a,u in [('1-cake-builder-desktop.png','A. Cake builder (example prices)','canva.link/iw4s22pjox1ih5f'),('2-fresh-oven-live-board-desktop.png','B. Fresh out of the oven live board (example data)','canva.link/yz72y5hpf4rscwf'),('3-jones-story-club-desktop.png','C. Jones story + club + bread subscription','canva.link/qydq6fx652fb1dd')])+'</div>'
    ba=clean(P('Before and after'),TT)
    mk('living','A site that stays fresh by itself, and the reason clients keep their monthly care plan.',clean(sc,TT)+'<h2>The concepts (unbranded)</h2><p class="note">Made in Canva with no real logo or photos. The branded versions stay private until the bakery says yes in writing.</p>'+imgs+'<h2 style="margin-top:30px">How a living website updates itself</h2>'+ba)
    mk('instagram','Real, local and simple beats fancy. Film once, post all month.',C('3. Instagram post creation')+'<h2 style="margin-top:30px">What I track every month</h2>'+C('5. Monitoring'))
    mk('customers','Who I help first, and who their customers are.',C('7. Target campaign audience'))
    mk('sales','Sales is the speed limit: we can build about 3 sites a week, so winning clients sets the pace.',tiles([("~3/wk","build capacity"),("11–25","businesses reached per site"),("Day 1/3/7","follow-up rhythm")])+'<h2>Following up</h2>'+C('4. Follow-up')+'<h2 style="margin-top:30px">Sales is the speed limit</h2>'+C('11. Sales is the speed limit'))
    mk('costs','What it takes to run, and how many hours each client needs.',C('6. Support and running costs')+'<h2 style="margin-top:30px">Example first 90 days</h2>'+C('Example numbers'))
    # forecast
    D=json.dumps(data)
    charts=f'''<div class="toggle" role="group" aria-label="Scenario"><button data-s="all" class="on">All</button><button data-s="Conservative">Conservative</button><button data-s="Realistic">Realistic</button><button data-s="Stretch">Stretch</button></div>
<div class="card"><h3>Cumulative cash over 24 months</h3><svg id="c1" viewBox="0 0 800 320" style="width:100%;height:auto" role="img" aria-label="Cumulative cash chart"></svg><p class="note">Year 1 monthly, year 2 at quarter ends. Forecast only.</p></div>
<div class="card" style="margin-top:20px"><h3>Net profit by month, year 1</h3><svg id="c2" viewBox="0 0 800 300" style="width:100%;height:auto" role="img" aria-label="Net profit by month chart"></svg></div>
<script>var DATA={D};var COL={{Conservative:"#5ee7c9",Realistic:"#ffb443",Stretch:"#ff6b4a"}};
var LAB=["Nov 26","Dec","Jan 27","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct 27","Jan 28","Apr 28","Jul 28","Oct 28"];
function fmt(v){{return (v<0?"−":"")+"A$"+(Math.abs(v)>=1000?Math.round(Math.abs(v)/1000)+"k":Math.abs(v))}}
function draw(sel){{var S=sel=="all"?["Conservative","Realistic","Stretch"]:[sel];
var c1=document.getElementById("c1"),W=800,H=320,L=70,B=40,T=20,R=20;var all=[];S.forEach(s=>all=all.concat(DATA[s].cum,DATA[s].q_cum));var mx=Math.max.apply(0,all),mn=Math.min(0,Math.min.apply(0,all));
var y=v=>T+(H-T-B)*(1-(v-mn)/(mx-mn)),x=i=>L+(W-L-R)*i/15;var g="";for(var k=0;k<=4;k++){{var v=mn+(mx-mn)*k/4;g+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y(v)+'" y2="'+y(v)+'" stroke="#ffffff14"/><text x="'+(L-8)+'" y="'+(y(v)+4)+'" text-anchor="end" font-size="12" fill="#aab2d6">'+fmt(v)+'</text>'}}
LAB.forEach((l,i)=>{{if(i%3==0||i>11)g+='<text x="'+x(i)+'" y="'+(H-14)+'" text-anchor="middle" font-size="11" fill="#aab2d6">'+l+'</text>'}});
g+='<line x1="'+x(11.5)+'" x2="'+x(11.5)+'" y1="'+T+'" y2="'+(H-B)+'" stroke="#ffffff40" stroke-dasharray="4 4"/><text x="'+x(11.6)+'" y="'+(T+12)+'" font-size="11" fill="#aab2d6">Year 2</text>';
S.forEach(s=>{{var v=DATA[s].cum.concat(DATA[s].q_cum);g+='<polyline fill="none" stroke="'+COL[s]+'" stroke-width="3.5" stroke-linejoin="round" points="'+v.map((a,i)=>x(i)+","+y(a)).join(" ")+'"/>';g+='<text x="'+(x(15)-4)+'" y="'+(y(v[15])-8)+'" text-anchor="end" font-size="13" font-weight="800" fill="'+COL[s]+'">'+s+' '+fmt(v[15])+'</text>'}});c1.innerHTML=g;
var c2=document.getElementById("c2");H=300;var a2=[];S.forEach(s=>a2=a2.concat(DATA[s].net));mx=Math.max.apply(0,a2);mn=Math.min(0,Math.min.apply(0,a2));var y2=v=>T+(H-T-B)*(1-(v-mn)/(mx-mn));
var bw=(W-L-R)/12/(S.length+1);g="";for(k=0;k<=4;k++){{v=mn+(mx-mn)*k/4;g+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y2(v)+'" y2="'+y2(v)+'" stroke="#ffffff14"/><text x="'+(L-8)+'" y="'+(y2(v)+4)+'" text-anchor="end" font-size="12" fill="#aab2d6">'+fmt(v)+'</text>'}}
for(var m=0;m<12;m++){{var x0=L+(W-L-R)*m/12+bw/2;S.forEach((s,j)=>{{var val=DATA[s].net[m],top=y2(Math.max(val,0)),h=Math.abs(y2(val)-y2(0));g+='<rect x="'+(x0+j*bw)+'" y="'+top+'" width="'+(bw-2)+'" height="'+Math.max(h,1)+'" rx="3" fill="'+COL[s]+'"><title>'+s+' '+LAB[m]+': '+fmt(val)+'</title></rect>'}});if(m%2==0)g+='<text x="'+(x0+bw)+'" y="'+(H-14)+'" text-anchor="middle" font-size="11" fill="#aab2d6">'+LAB[m]+'</text>'}}
c2.innerHTML=g;document.querySelectorAll(".sc").forEach(e=>e.style.opacity=(sel=="all"||e.dataset.s==sel)?1:.35)}}
document.querySelectorAll(".toggle button").forEach(b=>b.onclick=function(){{document.querySelectorAll(".toggle button").forEach(x=>x.classList.remove("on"));b.classList.add("on");draw(b.dataset.s)}});draw("all");</script>'''
    scen='<div class="grid">'+''.join(f'<div class="card sc" data-s="{n}" style="border-color:{c}55"><div class="label" style="color:{c}">{n}</div><div class="price">{t}</div><p class="note">2-year net profit (forecast)</p><div class="tbl"><table class="tt"><tr><td></td><td>Year 1</td><td>Year 2</td></tr>{r}</table></div><p class="note">Break-even: {be} · Lowest cash: {lc}</p></div>' for n,c,t,r,be,lc in [
     ('Conservative','#5ee7c9','A$80,924','<tr><td>Revenue</td><td>A$29k</td><td>A$65k</td></tr><tr><td>Costs</td><td>A$5.7k</td><td>A$7.6k</td></tr><tr><td>Net profit</td><td>A$24k</td><td>A$57k</td></tr><tr><td>Sites built</td><td>17</td><td>31</td></tr><tr><td>Sites a week</td><td>0.3</td><td>0.6</td></tr><tr><td>Clients at end</td><td>6</td><td>14</td></tr>','Mar 27','−A$1,296'),
     ('Realistic','#ffb443','A$239,470','<tr><td>Revenue</td><td>A$77k</td><td>A$205k</td></tr><tr><td>Costs</td><td>A$7.6k</td><td>A$36k</td></tr><tr><td>Net profit</td><td>A$70k</td><td>A$170k</td></tr><tr><td>Sites built</td><td>36</td><td>78</td></tr><tr><td>Sites a week</td><td>0.7</td><td>1.5</td></tr><tr><td>Clients at end</td><td>19</td><td>52</td></tr>','Jan 27','−A$903'),
     ('Stretch','#ff6b4a','A$558,955','<tr><td>Revenue</td><td>A$165k</td><td>A$584k</td></tr><tr><td>Costs</td><td>A$19k</td><td>A$171k</td></tr><tr><td>Net profit</td><td>A$146k</td><td>A$413k</td></tr><tr><td>Sites built</td><td>73</td><td>208</td></tr><tr><td>Sites a week</td><td>1.4</td><td>4.0</td></tr><tr><td>Clients at end</td><td>46</td><td>158</td></tr>','Jan 27','−A$903')])+'</div>'
    f10=P('10. Money forecast: the next 2 years'); intro=f10.split('CONSERVATIVE')[0]
    mk('forecast','A 24-month forecast (Nov 2026 to Oct 2028) in three scenarios, driven by sales. Every figure is a forecast, not a promise.','<div class="card" style="margin-bottom:16px"><p>Charity website builds are done for free, so they are unpaid and not included in the revenue figures below. <a href="giving.html">Giving back →</a></p></div>'+clean(intro,TT)+scen+'<div style="margin-top:24px">'+charts+'</div><h2 style="margin-top:40px">Year 1 by month</h2>'+C('10. Money forecast: year 1 by month')+'<h2 style="margin-top:30px">Year 1 (continued) and year 2</h2>'+C('10. Money forecast: year 1 (continued)')+'<h2 style="margin-top:30px">Assumptions</h2>'+C('Assumptions behind the forecast'))
    mk('risks','Every plan has risks. Here is each one, and what we do about it.',C('12. Key risks'))
    mk('giving','I want to give back to my community and to the people who have supported me.','''<div class="card feat"><h3>Why I&rsquo;m doing it</h3><p>Lots of people on the Northern Beaches have backed me. Building free websites for charities is my way of giving something back to the community and to the people who&rsquo;ve supported me. It&rsquo;s also something I&rsquo;m genuinely proud to do.</p></div>
<div class="grid" style="margin-top:20px"><div class="card"><h3>🎁 What charities get</h3><ul class="l"><li>A <b>free website build</b>: modern, mobile-friendly, with a contact or donation link</li><li>Optional <b>website care</b>, discounted or free, so the site stays up to date</li><li>Help connecting their Instagram so it stays fresh</li></ul></div>
<div class="card"><h3>📅 How many</h3><p><b>The plan:</b> about 1 charity site per quarter, alongside my paid work. That way every build gets my full attention.</p></div>
<div class="card"><h3>✉️ How a charity can ask</h3><p>Get in touch through Tomas Web Studio, tell me about your charity and what you need, and we&rsquo;ll have a chat with Dad about timing.</p></div>
<div class="card"><h3>🌱 It helps me grow too</h3><p>Every charity site adds to my portfolio and builds my skills, so giving back makes me better at what I do.</p></div></div>
<div class="card" style="margin-top:20px"><h3>💛 A charity I&rsquo;d love to build for: Burdekin</h3><p>Burdekin is an independent not-for-profit with its head office in Brookvale. It works with young people and their families, helping prevent youth homelessness, providing safe housing and supporting wellbeing, and it leads the Beaches Youth Hub in Avalon. I&rsquo;d love to offer Burdekin a free website build, if it would help them.</p><p class="note">This is an offer and a hope, not an agreed project. Sources: <a href="https://burdekin.org.au/">burdekin.org.au</a>, <a href="https://burdekin.org.au/contact-us/">contact page</a>, <a href="https://burdekin.org.au/beaches-youth-hub/">Beaches Youth Hub</a> (viewed Oct 2026).</p></div>''')
    mk('roadmap','From the first showcase to five monthly clients, then growing from there.',C('8. 90-day plan')+'<div class="grid" style="margin-top:24px"><div class="card"><div class="n g">1</div><h3>Days 1–30</h3><p>First showcase approved, my own Instagram and site live, 10 free checks.</p></div><div class="card"><div class="n g">2</div><h3>Days 31–60</h3><p>3 paying clients, each site shipped in about 2 weeks.</p></div><div class="card"><div class="n g">3</div><h3>Days 61–90</h3><p>5 monthly clients and the first monthly reports.</p></div><div class="card"><div class="n g">4</div><h3>Year 1 → 2</h3><p>Grow leads every week and follow the forecast. <a href="forecast.html">See the forecast →</a></p></div></div>')
    return data
def doc_native(page,src,out,title,lead,T):
    s=open(src).read(); s=re.search(r'<body[^>]*>(.*)</body>',s,re.S|re.I).group(1) if '<body' in s.lower() else s
    parts=re.split(r'(?=<h2)',s); html_=''
    for i,p in enumerate(parts):
        h=re.search(r'<h2[^>]*>(.*?)</h2>',p,re.S)
        c=clean(p,T)
        if i==0: html_+=f'<div class="card">{c}</div>'
        else: html_+=f'<h2 style="margin-top:34px">{re.sub("<[^>]+>","",h.group(1))}</h2><div class="doc">{c}</div>'
    page(out,title,f'<section style="padding:40px 0 60px"><div class="w"><div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Library</a> › {title}</div><h1 style="font-size:clamp(2rem,4.5vw,3.2rem)">{title}</h1><p class="lead" style="margin:10px 0 24px">{lead}</p><div class="doc">{html_}</div><div class="pn"><a class="btn o" href="index.html">← Library</a><a class="btn o" href="../plan/index.html">Business plan →</a></div></div></section>')
