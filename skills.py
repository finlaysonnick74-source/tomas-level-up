# (name, meaning, days, evidence, career)
A=[("HTML / CSS / JavaScript","The three languages every web page is made of: structure, style and behaviour.",[5,6,8,9,10,14,19],"Commits in GitHub; pages he can explain line by line","Web and front-end development, software engineering"),
("Design","Making things clear, attractive and easy to use.",[2,3,4,6,9,13],"Mobbin collection, wireframes, brand kit","UX/UI design, product"),
("Git and GitHub","Saving every version of your work and working safely with others.",[1,5,6,8,12,15,21],"Daily commits, branches, pull requests, v1.0 release","Every software, cloud and DevOps job"),
("Deployment and hosting","Putting a site online and updating it safely.",[7,8,12,16],"Live site, preview links, a practised rollback","DevOps and cloud engineering"),
("DNS and domains","How a web address finds the right website.",[16,17],"Own domain with HTTPS","Cloud, networking, cybersecurity"),
("Testing","Finding and fixing problems before customers do.",[11,12,15],"GitHub issues closed, Lighthouse score","Quality and testing engineering"),
("AI-assisted building","Getting AI to build what you want with clear prompts, then checking its work.",[1,5,6,10,19],"Prompts and the code they produced","Automation and AI engineering"),
("Social media tools","Instagram business, Canva and Postiz scheduling.",[13,19,20,21],"Business profile, scheduled launch week","Digital marketing and social media"),
("Analytics","Reading the numbers: visits, reach, what works.",[17,19,21],"Search Console, Analytics, '21 days in numbers'","Data analysis, marketing"),
("Business maths (pricing, P&L)","Pricing a job, costs, profit and money in and out.",[1,8,16,21],"Price list matched to the plan, a simple money tracker","Running his own agency, consulting, product")]
B=[("Communication","Explaining clearly, in plain English.",[5,7,10,14,21],"Show-and-tells, explaining code to Dad","Every role, especially consulting and product"),
("Pitching and presenting","Showing your work with confidence.",[7,14,18,21],"Three show-and-tells, first pitches booked","Sales, consulting, own business"),
("Client service","Treating a client well: listening, replying, delivering.",[8,10,12,18],"Test enquiry reply, handling change requests","Consulting, agencies, product"),
("Writing","Clear briefs, captions and messages.",[1,9,13,20],"The brief, permission message, captions","Marketing, product, every role"),
("Teamwork with Dad","Working side by side, sharing the load.",[1,3,4,8,12],"Pull request reviews, daily sessions","Every team in IT"),
("Problem-solving","Sticking with a bug until it's fixed.",[5,11,12,15],"Bugs logged and fixed","Software, cyber, cloud"),
("Time management","Hitting the timetable and the Day 21 deadline.",[6,7,14,21],"On-time sessions, launch on schedule","Every role"),
("Planning","Thinking ahead: site maps, checklists, content calendars.",[1,3,15,20],"Site map, launch checklist, content plan","Product, project management"),
("Taking feedback","Hearing honest feedback and improving.",[3,4,8,12],"Changes made after Dad's reviews","Every role")]
C=[("Commitment","Doing all 21 days, even the hard ones.",list(range(1,22)),"Streak on the tracker","Employers hire people who finish"),
("Discipline and routine","4:30pm start, every school day, same steps.",[1,6,7,14,21],"Daily log","Reliable professionals get trusted with more"),
("Reliability","Doing what you said, when you said.",[7,14,21],"Show-and-tells delivered on time","Clients and bosses rely on it"),
("Ownership, no excuses","Owning mistakes and fixing them.",[4,9,11,15],"Bugs owned and fixed","Senior roles are about ownership"),
("Resilience","Bouncing back from setbacks.",[5,11,12,15],"Journal lines about hard days","Tech changes fast; resilience keeps you going"),
("Delayed gratification","Doing the work now for a bigger reward later.",[8,15,21],"Launch Day, milestones before rewards","Study and careers pay off over years"),
("Money responsibility","Respecting money: pricing fairly, tracking spending.",[1,8,16,21],"Money tracker, fair prices","Running a business, managing budgets"),
("Self-reflection","Looking back honestly to get better.",[7,14,21],"Journal lines, weekly self-reviews","Growth in any career"),
("Pride in work","Making things you're proud to show.",[6,7,14,21],"The live site","Great work builds a great reputation"),
("Trust","Earning trust by showing up.",[7,14,21],"Tracker and show-and-tells, open to family","Trust leads to responsibility and opportunity")]
G=[("A","Hard skills","Technical",A),("B","Soft skills","Professional",B),("C","Life skills","Character",C)]
def today(n):
    cols=''.join(f'<div><b>{t}</b><div class="chips">'+''.join(f'<span class="chip">{s[0]}</span>' for s in L if n in s[2])+'</div></div>' for _,t,_,L in G)
    return f'<div class="card" style="border-color:var(--c)"><h3>🧠 Today you\'re learning</h3><div class="grid" style="margin-top:10px">{cols}</div><p class="note"><a href="../skills.html">See the full skills framework →</a></p></div>'
SPEC=["Development","Cyber","Cloud","AI + automation","Data","UX","Digital marketing","Testing","Product / consulting","Own business"]
def svg():
    w=1000; x0=40; step=92
    boxes=''.join(f'<g><path d="M500 175 C 500 215, {x0+i*step+40} 205, {x0+i*step+40} 245" stroke="#ffffff30" stroke-width="2" fill="none"/><rect x="{x0+i*step}" y="245" width="84" height="56" rx="10" fill="#141829" stroke="#5ee7c9"/><text x="{x0+i*step+42}" y="278" font-size="11" text-anchor="middle" fill="#eef0ff">{s}</text></g>' for i,s in enumerate(SPEC))
    return f'''<svg viewBox="0 0 {w} 320" style="width:100%;height:auto" font-family="system-ui" role="img" aria-label="The 21-day program is the foundation for many specialisations">
<text x="500" y="22" text-anchor="middle" font-size="15" fill="#9aa3c7">SPECIALISE IN WHAT I LOVE ↓</text>
<rect x="250" y="40" width="500" height="135" rx="18" fill="url(#fg)"/><defs><linearGradient id="fg" x1="0" x2="1"><stop offset="0" stop-color="#ff6b4a"/><stop offset="1" stop-color="#ffb443"/></linearGradient></defs>
<text x="500" y="85" text-anchor="middle" font-size="24" font-weight="900" fill="#111">THE FOUNDATION</text><text x="500" y="112" text-anchor="middle" font-size="14" fill="#111">My 21-day program</text>
<text x="500" y="140" text-anchor="middle" font-size="13" fill="#111">Hard skills · Soft skills · Life skills</text>{boxes}</svg>'''
def page_body():
    days=range(1,22)
    def sec(code,title,sub,L):
        cards=''.join(f'<div class="card"><h3>{s[0]}</h3><p>{s[1]}</p><p class="note"><b>Days:</b> '+', '.join(f'<a href="learn/day-{d:02d}.html">{d}</a>' for d in s[2])+f'</p><p class="note"><b>Evidence:</b> {s[3]}</p><p class="note"><b>In an IT career:</b> <a href="careers.html">{s[4]}</a></p></div>' for s in L)
        return f'<section style="padding:40px 0"><div class="w r"><div class="label">Group {code} · {sub}</div><h2>{title}</h2><div class="grid">{cards}</div></div></section>'
    rows=''
    for code,t,_,L in G:
        rows+=f'<tr><td colspan="22" style="background:#ffffff10;font-weight:800">{code} · {t}</td></tr>'
        rows+=''.join(f'<tr><td style="white-space:nowrap">{s[0]}</td>'+''.join(f'<td style="text-align:center">{"●" if d in s[2] else ""}</td>' for d in days)+'</tr>' for s in L)
    head='<tr><th style="text-align:left">Skill</th>'+''.join(f'<th><a href="learn/day-{d:02d}.html">{d}</a></th>' for d in days)+'</tr>'
    return f'''<header style="padding:70px 0 30px"><div class="w"><div class="tag">Skills framework</div><h1>Exactly what I'm <span class="g">learning</span>.</h1><p class="lead">Three groups of skills, practised on real work every day: the hard skills to build things, the soft skills to work with people, and the life skills that make me someone people trust.</p>
<div class="chips"><a class="chip" href="#A">A · Hard skills</a><a class="chip" href="#B">B · Soft skills</a><a class="chip" href="#C">C · Life skills</a><a class="chip" href="#matrix">Skills by day</a><a class="chip" href="careers.html">Careers →</a></div></div></header>
<section style="padding-top:0"><div class="w r"><div class="card"><h3>Foundation for a career of your choice</h3>{svg()}</div></div></section>
<div id="A"></div>{sec("A","Hard skills","Technical",A)}<div id="B"></div>{sec("B","Soft skills","Professional",B)}<div id="C"></div>{sec("C","Life skills","Character",C)}
<section id="matrix" style="padding:40px 0"><div class="w"><div class="label">Skills by day</div><h2>The skills matrix</h2><p class="sub">● = taught or practised that day. Click a day to open its lesson.</p><div class="card" style="overflow-x:auto"><table class="tt" style="font-size:.82rem;min-width:900px">{head}{rows}</table></div></div></section>'''
