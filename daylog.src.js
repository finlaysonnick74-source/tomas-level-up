/* Tomas Levels Up: self-serve daily log. Live store first (keyvalue.immanuel.co, app __AK__, keys day-NN and day-NN-dad), progress.json as fallback. Never touches wall keys. */
(function(){
var KV="https://keyvalue.immanuel.co/api/KeyVal/",AK="__AK__",_f=window.fetch.bind(window);
var STEPS=[["checkin","✅ Check-in + today's goal"],["lessons","📘 Today's lessons"],["build","🔨 Build time"],["talk","💬 Talk it through with Dad"]];
function pad(n){return String(n).padStart(2,"0")}
function g(k){return _f(KV+"GetValue/"+AK+"/"+k+"?"+Date.now()).then(function(r){return r.json()}).then(function(v){return v||""}).catch(function(){return ""})}
function p(k,v){return _f(KV+"UpdateValue/"+AK+"/"+k+"/"+v,{method:"POST"}).then(function(r){if(!r.ok)throw 0})}
function enc(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/,"")}
function dec(s){s=s.replace(/-/g,"+").replace(/_/g,"/");while(s.length%4)s+="=";return JSON.parse(decodeURIComponent(escape(atob(s))))}
function rd(k){return g(k).then(function(c){c=parseInt(c)||0;if(!c||c>40)return null;var a=[];for(var j=0;j<c;j++)a.push(g(k+"_"+j));return Promise.all(a).then(function(x){try{return dec(x.join(""))}catch(e){return null}})})}
function wr(k,o){var e=enc(o),ch=[];for(var i=0;i<e.length;i+=180)ch.push(e.slice(i,i+180));return Promise.all(ch.map(function(c,j){return p(k+"_"+j,c)})).then(function(){return p(k,ch.length)})}
function esc(s){return String(s||"").replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function okUrl(u){u=String(u||"").trim();return /^https:\/\/[^\s"'<>]+$/.test(u)?u:""}
var LIVE=null;
function load(){if(LIVE)return LIVE;var a=[];for(var n=1;n<=21;n++){(function(n){a.push(Promise.all([rd("day-"+pad(n)),rd("day-"+pad(n)+"-dad")]).then(function(r){return{day:n,e:r[0],dad:r[1]}}))})(n)}
 LIVE=Promise.all(a).then(function(r){var m={};r.forEach(function(x){var loc=null;try{loc=JSON.parse(localStorage.getItem("dl-"+x.day)||"null")}catch(e){}m[x.day]={e:x.e||loc,dad:x.dad}});return m});return LIVE}
function streak(D){/* D lists only session days (curriculum dates), so non-session days never break it. Count back from the latest done day. */
 var st=0,l=-1;D.forEach(function(x,i){if(x.status=="done")l=i});for(var i=l;i>=0&&D[i].status=="done";i--)st++;return st}
function merge(d){return load().then(function(m){d.days.forEach(function(x){var L=m[x.day]||{},e=L.e;
  if(e){["built","learned","proud"].forEach(function(k){if(e[k])x[k]=esc(e[k])});var u=okUrl(e.link);if(u){if(/\.(png|jpe?g|gif|webp)(\?|$)/i.test(u))x.photo=u;else x.commit=u}
   if(e.done)x.status="done";else if(x.status!="done"&&(e.ticks||[]).some(Boolean))x.status="progress";x.ticks=e.ticks||[]}
  if(L.dad&&L.dad.note)x.dad_note=esc(L.dad.note)});
 var nx=d.days.find(function(x){return x.status!="done"})||d.days[d.days.length-1];nx.next=true;d.streak=streak(d.days);return d}).catch(function(){return d})}
window.fetch=function(u,o){if(typeof u=="string"&&/progress\.json/.test(u)&&!(o&&o.method&&o.method!="GET"))return _f(u,o).then(function(r){return r.json()}).then(merge).then(function(d){return new Response(JSON.stringify(d),{headers:{"Content-Type":"application/json"}})});return _f.apply(window,arguments)};
function save(n,o){o.at=new Date().toISOString();try{localStorage.setItem("dl-"+n,JSON.stringify(o))}catch(e){}LIVE=null;return wr("day-"+pad(n),o)}
function saveDad(n,note){LIVE=null;return wr("day-"+pad(n)+"-dad",{note:note,at:new Date().toISOString()})}
/* ---- widget ---- */
function base(){return /\/(learn|results|plan|library)\//.test(location.pathname)?"../":""}
function widget(el){var fixed=parseInt(el.getAttribute("data-dlog"))||0,B=base();
 fetch(B+"progress.json?"+Date.now()).then(function(r){return r.json()}).then(function(d){return load().then(function(m){
 var D=d.days,cur=fixed||((D.find(function(x){return x.next})||D[0]).day);
 function render(n){var x=D[n-1],e=(m[n]||{}).e||{},t=e.ticks||[],done=x.status=="done";
  el.innerHTML='<div class="label">📝 Log my day</div>'+(fixed?'':'<label class="dl-pick">Which day? <select id="dl-day">'+D.map(function(y){return '<option value="'+y.day+'"'+(y.day==n?' selected':'')+'>Day '+y.day+(y.status=="done"?' ✓':'')+' · '+esc(y.plan.replace(/<[^>]+>/g,"")).slice(0,40)+'</option>'}).join("")+'</select></label>')+
  '<h3 style="margin:6px 0">'+(done?'🎉 Day '+n+' is done. Nice work!':'Day '+n+': tick each step as you finish it')+'</h3>'+
  '<div class="dl-steps">'+STEPS.map(function(s,i){return '<label class="dl-step'+(t[i]?' on':'')+'"><input type="checkbox" data-i="'+i+'"'+(t[i]?' checked':'')+'><span>'+s[1]+'</span></label>'}).join("")+'</div>'+
  '<div class="fm dl-form"><label for="dl-b">🛠️ What I built</label><textarea id="dl-b" maxlength="500" rows="2" placeholder="e.g. My hero section with a big orange button">'+esc(e.built)+'</textarea>'+
  '<label for="dl-l">💡 What I learned</label><textarea id="dl-l" maxlength="500" rows="2" placeholder="One thing that clicked today">'+esc(e.learned)+'</textarea>'+
  '<label for="dl-p">⭐ What I&rsquo;m proud of</label><textarea id="dl-p" maxlength="500" rows="2" placeholder="Big or small, it counts">'+esc(e.proud)+'</textarea>'+
  '<label for="dl-u">🔗 Link or photo URL <span class="note" style="font-weight:400">(optional)</span></label><input id="dl-u" type="url" maxlength="300" placeholder="https://…" value="'+esc(e.link)+'"></div>'+
  '<button class="btn dl-go" id="dl-go" type="button">'+(done?'💾 Update Day '+n:'✅ Mark Day '+n+' complete')+'</button><p class="dl-msg" id="dl-msg" role="status" aria-live="polite"></p>'+
  (x.dad_note?'<div class="dl-dad"><b>💬 Dad&rsquo;s note</b><p>'+x.dad_note+'</p></div>':'');
  var q=function(i){return el.querySelector(i)},val=function(){return{built:q("#dl-b").value.trim(),learned:q("#dl-l").value.trim(),proud:q("#dl-p").value.trim(),link:q("#dl-u").value.trim(),ticks:STEPS.map(function(s,i){return q('[data-i="'+i+'"]').checked}),done:!!e.done}};
  if(q("#dl-day"))q("#dl-day").onchange=function(){render(+this.value)};
  el.querySelectorAll("[data-i]").forEach(function(c){c.onchange=function(){c.parentNode.classList.toggle("on",c.checked);var v=val();e=Object.assign(e,v);m[n]={e:e,dad:(m[n]||{}).dad};
   if(!done&&v.ticks.some(Boolean))x.status="progress";save(n,v).then(function(){q("#dl-msg").textContent=v.ticks.every(Boolean)?"All 4 steps ticked. Now log your day and hit the big button 👇":"Saved ✓"}).catch(function(){q("#dl-msg").textContent="Saved on this device. It'll sync next time."})}});
  q("#dl-go").onclick=function(){var v=val(),b=this;if(v.link&&!okUrl(v.link)){q("#dl-msg").textContent="Links need to start with https://";return}v.done=true;b.disabled=true;b.textContent="Saving…";
   save(n,v).then(function(){e=v;m[n]={e:v,dad:(m[n]||{}).dad};x.status="done";var st=streak(D),nx=D.find(function(y){return y.status!="done"});
    render(n);q("#dl-msg").innerHTML="🔥 Streak: "+st+" day"+(st==1?"":"s")+". "+(nx?'Next up: <a href="'+B+nx.lesson+'">Day '+nx.day+' →</a>':"All 21 days done. Legend! 🚀");
    document.dispatchEvent(new CustomEvent("dl-saved"))}).catch(function(){b.disabled=false;b.textContent="Try again";q("#dl-msg").textContent="Couldn't reach the internet just now. Your words are still here, so try again in a moment."})}}
 render(cur)})})}
function dadBox(el){var B=base();fetch(B+"progress.json?"+Date.now()).then(function(r){return r.json()}).then(function(d){return load().then(function(m){var D=d.days,cur=(D.find(function(x){return x.next})||D[0]).day;
 function render(n){var dn=(m[n]||{}).dad||{};el.innerHTML='<div class="label">💬 Dad&rsquo;s note (optional)</div><h3 style="margin:6px 0">A few kind words for Tomas</h3><p class="note">For Dad: a line of encouragement about any day. It shows on that day&rsquo;s page and in the tracker. No marks, no sign-off needed.</p><div class="fm"><label for="dd-day">Day</label><select id="dd-day">'+D.map(function(y){return '<option value="'+y.day+'"'+(y.day==n?' selected':'')+'>Day '+y.day+(y.status=="done"?' ✓':'')+'</option>'}).join("")+'</select><label for="dd-n">Your note</label><textarea id="dd-n" rows="3" maxlength="500" placeholder="e.g. Loved how you stuck with that bug, mate. Proud of you.">'+esc(dn.note)+'</textarea></div><button class="btn o" id="dd-go" type="button" style="margin-top:12px">Save Dad&rsquo;s note</button><p class="dl-msg" id="dd-msg" role="status" aria-live="polite"></p>';
  el.querySelector("#dd-day").onchange=function(){render(+this.value)};
  el.querySelector("#dd-go").onclick=function(){var t=el.querySelector("#dd-n").value.trim();saveDad(n,t).then(function(){m[n]=Object.assign(m[n]||{},{dad:{note:t}});el.querySelector("#dd-msg").textContent="Saved ✓ Tomas will see it on Day "+n+"."}).catch(function(){el.querySelector("#dd-msg").textContent="Couldn't save just now. Try again in a moment."})}}
 render(cur)})})}
window.DL={load:load,save:save,saveDad:saveDad,streak:streak,esc:esc};
document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll("[data-dlog]").forEach(widget);document.querySelectorAll("[data-dlad]").forEach(dadBox)});
})();
