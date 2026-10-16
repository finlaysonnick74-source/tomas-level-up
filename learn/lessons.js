/* Web Basics lessons — interactions. Safe to include once per page; auto-inits everything under .ls */
(function(){
const $=(s,r=document)=>[...r.querySelectorAll(s)];
const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
function init(root=document){
// Stepper: [data-step=n] get .on (reached) / .now (current); .ls-cap[data-cap=n]; [data-goto=n]; [data-go=prev|next|play|reset]
$('.ls-stepper:not([data-ready])',root).forEach(st=>{
  st.dataset.ready=1;st.classList.add('js');
  const els=$('[data-step]',st),caps=$('[data-cap]',st);
  const max=+st.dataset.steps||Math.max(...els.map(e=>+e.dataset.step));
  let cur=+st.dataset.start||1,timer=null;
  const cnt=st.querySelector('.ls-count'),play=st.querySelector('[data-go=play]');
  function set(n){cur=Math.max(1,Math.min(max,n));
    els.forEach(e=>{const s=+e.dataset.step;e.classList.toggle('on',s<=cur);e.classList.toggle('now',s===cur)});
    caps.forEach(c=>c.classList.toggle('now',+c.dataset.cap===cur));
    $('[data-goto]',st).forEach(g=>g.setAttribute('aria-current',+g.dataset.goto===cur?'step':'false'));
    $('[data-progress]',st).forEach(p=>p.style.strokeDashoffset=100-100*(cur-1)/Math.max(1,max-1));
    $('[data-go=prev]',st).forEach(b=>b.disabled=cur<=1);$('[data-go=next]',st).forEach(b=>b.disabled=cur>=max);
    if(cnt)cnt.textContent='Step '+cur+' of '+max;}
  function stop(){clearInterval(timer);timer=null;if(play){play.textContent='▶ Play';play.setAttribute('aria-pressed','false')}}
  st.addEventListener('click',e=>{const g=e.target.closest('[data-goto],[data-go]');if(!g||!st.contains(g))return;
    if(g.dataset.goto){stop();return set(+g.dataset.goto)}
    const a=g.dataset.go;
    if(a==='next'){stop();set(cur+1)}else if(a==='prev'){stop();set(cur-1)}else if(a==='reset'){stop();set(1)}
    else if(a==='play'){if(timer)return stop();if(cur>=max)set(1);play.textContent='❚❚ Pause';play.setAttribute('aria-pressed','true');
      timer=setInterval(()=>{if(cur>=max)return stop();set(cur+1)},still?3500:2200)}});
  st.addEventListener('keydown',e=>{const g=e.target.closest('[data-goto]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();g.click()}});
  set(cur);
});
// Layer toggle (lesson 1)
$('[data-layers]:not([data-ready])',root).forEach(w=>{w.dataset.ready=1;const d=w.querySelector('.ls-demo'),t=w.querySelector('.toast');
  const go=l=>{d.dataset.layer=l;$('[data-layer-btn]',w).forEach(b=>b.setAttribute('aria-pressed',b.dataset.layerBtn===l));
    $('[data-hint]',w).forEach(h=>h.hidden=h.dataset.hint!==l);t.classList.remove('show')};
  w.addEventListener('click',e=>{const b=e.target.closest('[data-layer-btn]');if(b)go(b.dataset.layerBtn);
    if(e.target.closest('.ls-demo button')){if(d.dataset.layer==='js')t.classList.add('show')}});
  go(d.dataset.layer||'html')});
// Filter chips (lesson 4)
$('[data-filter]:not([data-ready])',root).forEach(w=>{w.dataset.ready=1;w.addEventListener('click',e=>{const b=e.target.closest('[data-f]');if(!b)return;
  $('[data-f]',w).forEach(x=>x.setAttribute('aria-pressed',x===b));const f=b.dataset.f;
  $('.ls-opt',w).forEach(o=>o.hidden=f!=='all'&&o.dataset.kind!==f)})});
// Era switch (lesson 8)
$('[data-eras]:not([data-ready])',root).forEach(w=>{w.dataset.ready=1;const go=v=>{$('[data-era]',w).forEach(b=>b.setAttribute('aria-pressed',b.dataset.era===v));
  $('.ls-era',w).forEach(x=>x.classList.toggle('show',x.classList.contains(v)))};
  w.addEventListener('click',e=>{const b=e.target.closest('[data-era]');if(b)go(b.dataset.era)});go('old')});
// Toolkit map (lesson 9)
$('.ls-map-wrap:not([data-ready])',root).forEach(w=>{w.dataset.ready=1;const info=w.querySelector('.ls-info');
  const show=b=>{$('.ls-tool',w).forEach(x=>x.classList.toggle('act',x===b));
    info.innerHTML='<div class="label">'+b.dataset.tag+'</div><h3>'+b.querySelector('b').textContent+'</h3><p>'+b.dataset.text+'</p>'};
  $('.ls-tool',w).forEach(b=>{b.addEventListener('mouseenter',()=>show(b));b.addEventListener('focus',()=>show(b));b.addEventListener('click',()=>show(b))})});
// Glossary search (lesson 11)
$('.ls-gloss-wrap:not([data-ready])',root).forEach(w=>{w.dataset.ready=1;const inp=w.querySelector('.ls-search'),items=$('.ls-gloss>div',w),none=w.querySelector('.ls-none'),cnt=w.querySelector('.ls-gcount');
  items.forEach(i=>{i._b=i.querySelector('b').textContent;i._h=i.innerHTML});
  let letter='';
  function run(){const q=inp.value.trim().toLowerCase();let n=0;
    items.forEach(i=>{const ok=(letter?i._b.toUpperCase().startsWith(letter):true)&&(!q||i.textContent.toLowerCase().includes(q));i.hidden=!ok;
      i.innerHTML=i._h;if(ok&&q){const b=i.querySelector('b');const re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');b.innerHTML=b.textContent.replace(re,'<mark>$1</mark>')}
      if(ok)n++});
    none.classList.toggle('show',!n);cnt.textContent=n+' of '+items.length+' words'}
  inp.addEventListener('input',()=>{letter='';$('.ls-az button',w).forEach(b=>b.setAttribute('aria-pressed',false));run()});
  const az=w.querySelector('.ls-az');const L=[...new Set(items.map(i=>i._b[0].toUpperCase()))];
  az.innerHTML='<button class="ls-b" data-l="" aria-pressed="true">All</button>'+L.map(l=>'<button class="ls-b" data-l="'+l+'" aria-pressed="false">'+l+'</button>').join('');
  az.addEventListener('click',e=>{const b=e.target.closest('[data-l]');if(!b)return;letter=b.dataset.l;inp.value='';$('button',az).forEach(x=>x.setAttribute('aria-pressed',x===b));run()});
  run()});
// Checklist with memory (lesson 10)
$('.ls-checks[data-key]:not([data-ready])',root).forEach(l=>{l.dataset.ready=1;const k='ls-'+l.dataset.key;let s={};try{s=JSON.parse(localStorage.getItem(k))||{}}catch(e){}
  $('input',l).forEach((c,i)=>{c.checked=!!s[i];c.addEventListener('change',()=>{s[i]=c.checked;try{localStorage.setItem(k,JSON.stringify(s))}catch(e){}})})});
// Quiz
$('.ls-quiz:not([data-ready])',root).forEach(z=>{z.dataset.ready=1;const qs=$('.ls-q',z),sc=z.querySelector('.ls-score');let right=0;
  const upd=()=>{const d=qs.filter(q=>q.classList.contains('done')).length;if(sc)sc.textContent=d?('You got '+right+' of '+d+' answered'+(d===qs.length?(right===qs.length?' — perfect! 🎉':' — nice work. Try again any time.'):'')):''};
  qs.forEach(q=>q.addEventListener('click',e=>{if(q.classList.contains('done'))return;const b=e.target.closest('.opts button');
    if(b){b.classList.add('picked');if(b.hasAttribute('data-ok'))right++;q.classList.add('done');upd()}
    else if(e.target.closest('.show')){q.classList.add('done');upd()}}));
  const r=z.querySelector('[data-quiz-reset]');if(r)r.addEventListener('click',()=>{right=0;qs.forEach(q=>{q.classList.remove('done');$('.picked',q).forEach(b=>b.classList.remove('picked'))});upd()})});
}
window.LessonsInit=init;
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>init());else init();
})();
