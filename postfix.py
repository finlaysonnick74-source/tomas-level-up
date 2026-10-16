import re,glob
R=[("At school on time, homework done before you build.","At school on time, every school day."),("School first, home by 4:30pm, homework, then 2 hours, 5:30&ndash;7:30pm.","School on time, then 2 hours at Dad&rsquo;s, 4:30&ndash;6:30pm."),(", after he&rsquo;s home by 4:30pm and homework is done.",", straight after school at Dad&rsquo;s."),('<text x="50" y="31" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">5:30&ndash;7:30</text><text x="50" y="51" text-anchor="middle" font-size="10" fill="#fff">Build session</text>','<text x="50" y="31" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">6:30pm</text><text x="50" y="51" text-anchor="middle" font-size="10" fill="#fff">Commit + journal</text>'),
('<text x="50" y="31" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">4:30&ndash;5:30</text><text x="50" y="51" text-anchor="middle" font-size="10" fill="#fff">Homework first</text>','<text x="50" y="31" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">4:30&ndash;6:30</text><text x="50" y="51" text-anchor="middle" font-size="10" fill="#fff">Build session</text>'),
('<text x="50" y="31" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">7:30</text><text x="50" y="51" text-anchor="middle" font-size="10" fill="#fff">Journal line done</text>','<text x="50" y="31" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">Evening</text><text x="50" y="51" text-anchor="middle" font-size="10" fill="#fff">Your time</text>'),
(" once you&rsquo;re home and homework is done."," once you&rsquo;re home."),("; homework done before the session.","."),
("Weekdays: home by 4:30pm, homework first, session 5:30–7:30pm.","Weekdays: session 4:30–6:30pm at Dad's, straight after school."),
(" &middot; homework first &middot; build 5:30&ndash;7:30pm"," &middot; build 4:30&ndash;6:30pm"),
("School and homework OK? ","At school on time today? "),
("School attendance &amp; homework first","School attendance on time"),("School attendance and homework ticked every school day","School attendance ticked every school day"),
(", after any weekend homework",""),(", homework first",""),(" School and homework always come before the session.",""),
("homework first","at school on time"),("Homework first","At school on time"),
("5:30&ndash;7:30","4:30&ndash;6:30"),("5:30–7:30","4:30–6:30"),("5:30-7:30","4:30-6:30"),
("For Mum and the school counsellor","For Mum and the counsellors, Melanie and Sio (The Burdekin)"),
("Tomas&rsquo;s school counsellor","Tomas&rsquo;s counsellors, Melanie and Sio (The Burdekin)"),
("For the counsellor and Mum","For Melanie, Sio and Mum"),("For the school counsellor and for Mum","For Melanie and Sio (The Burdekin) and for Mum"),
("the school counsellor","the counsellors, Melanie and Sio (The Burdekin)"),("school counsellor","counsellors, Melanie and Sio (The Burdekin)"),
("the counsellor and Mum","Melanie, Sio and Mum"),("Mum, grandparents and the counsellor ","Mum, the grandparents and Melanie and Sio (The Burdekin) "),
("For Mum, the grandparents and the counsellor","For Mum, the grandparents, Melanie and Sio")]
for f in glob.glob('**/*.html',recursive=True):
    s=open(f).read();o=s
    for a,b in R: s=s.replace(a,b)
    s=re.sub(r'Sessions sit after school and after homework\.[^<]*','Sessions start at 4:30pm, straight after school, at Dad&rsquo;s. Being at school on time is ticked every day in his log, alongside the build.',s)
    if s!=o: open(f,'w').write(s)
