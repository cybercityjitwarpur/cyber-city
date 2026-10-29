/* Cyber City — vanilla JS. No secrets here. */
(function(){
"use strict";
var C=window.CYBERCITY||{};var $=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var ROOT=document.documentElement.getAttribute("data-root")||"";
var SOON="जल्द उपलब्ध";

/* --- config injection --- */
function digits(v){return String(v||"").replace(/\D/g,"")}
function setupContacts(){
  var ph=digits(C.phone),wa=digits(C.whatsapp);
  $$("[data-call]").forEach(function(a){
    if(ph){a.href="tel:+"+ph}else{a.href=ROOT+"contact.html";a.title="फ़ोन नंबर अभी जोड़ा नहीं गया है"}
  });
  $$("[data-wa]").forEach(function(a){
    var msg=a.getAttribute("data-msg")||"नमस्ते, मुझे Cyber City की सेवा के बारे में जानकारी चाहिए।";
    if(wa){a.href="https://wa.me/"+wa+"?text="+encodeURIComponent(msg);a.target="_blank";a.rel="noopener"}
    else{a.href=ROOT+"contact.html";a.title="WhatsApp नंबर अभी जोड़ा नहीं गया है"}
  });
  $$("[data-cfg]").forEach(function(el){
    var k=el.getAttribute("data-cfg"),v=C[k];
    if(k==="phone"&&v)v="+"+digits(v);
    el.textContent=v?v:SOON;
  });
  var s=C.social||{};
  $$("[data-social]").forEach(function(a){var u=s[a.getAttribute("data-social")];if(u){a.href=u;a.target="_blank";a.rel="noopener"}else{a.parentNode.classList.add("hidden")}});
  var mb=$("#map");
  if(mb&&C.mapEmbed&&/^https:\/\//.test(C.mapEmbed)){mb.className="";mb.innerHTML="";var f=document.createElement("iframe");f.src=C.mapEmbed;f.title="Cyber City का नक्शा";f.loading="lazy";f.referrerPolicy="no-referrer-when-downgrade";mb.appendChild(f)}
}

/* --- menu --- */
function setupNav(){
  var b=$(".burger"),n=$("nav.main");
  if(b){b.addEventListener("click",function(){var o=n.classList.toggle("open");b.setAttribute("aria-expanded",o)})}
  $$("button.dd").forEach(function(btn){
    var sub=btn.nextElementSibling;
    btn.addEventListener("click",function(e){e.stopPropagation();var o=!sub.classList.contains("open");closeAll();if(o){sub.classList.add("open");btn.setAttribute("aria-expanded","true")}});
  });
  function closeAll(){$$(".sub.open").forEach(function(s){s.classList.remove("open");s.previousElementSibling.setAttribute("aria-expanded","false")})}
  document.addEventListener("click",closeAll);
  document.addEventListener("keydown",function(e){if(e.key==="Escape"){closeAll();if(n)n.classList.remove("open")}});
}

/* --- English toggle (navigation, buttons and headings marked data-en) --- */
function setupLang(){
  var btn=$("#lang"),cur=null;try{cur=localStorage.getItem("cc-lang")}catch(e){}
  function apply(l){
    $$("[data-en]").forEach(function(el){if(!el.hasAttribute("data-hi"))el.setAttribute("data-hi",el.textContent);el.textContent=l==="en"?el.getAttribute("data-en"):el.getAttribute("data-hi")});
    if(btn){btn.textContent=l==="en"?"हिन्दी":"English"}document.documentElement.lang=l==="en"?"en":"hi";
  }
  if(cur==="en")apply("en");
  if(btn)btn.addEventListener("click",function(){var n=document.documentElement.lang==="en"?"hi":"en";apply(n);try{localStorage.setItem("cc-lang",n)}catch(e){}});
}

/* --- service search (works on static cards; no fetch needed) --- */
function norm(s){return String(s||"").toLowerCase().trim()}
function setupSearch(){
  $$("form.search").forEach(function(f){f.addEventListener("submit",function(e){
    var inp=$("input",f);if($("#svc-list")){e.preventDefault();filter(inp.value)}else{f.action=ROOT+"services.html"}
  })});
  var list=$("#svc-list");if(!list)return;
  var q=new URLSearchParams(location.search),inp=$("#q");
  if(q.get("q")){inp.value=q.get("q");filter(q.get("q"))}
  inp.addEventListener("input",function(){filter(inp.value)});
  $$(".catbtn").forEach(function(b){b.addEventListener("click",function(){inp.value="";filter("",b.getAttribute("data-cat"))})});
  var sid=q.get("s");if(sid){var d=$("#detail-"+CSS.escape(sid));if(d){list.classList.add("hidden");$("#dirhead").classList.add("hidden");$$(".detail").forEach(function(x){x.classList.add("hidden")});d.classList.remove("hidden");document.title=$("h2",d).textContent+" | Cyber City, Samastipur"}}
}
function filter(v,cat){
  var q=norm(v),n=0;
  $$("#svc-list .card").forEach(function(c){
    var ok=(!q||c.getAttribute("data-s").indexOf(q)>-1)&&(!cat||c.getAttribute("data-cat")===cat);
    c.classList.toggle("hidden",!ok);if(ok)n++;
  });
  var e=$("#none");if(e)e.classList.toggle("hidden",n>0);
  var c=$("#count");if(c)c.textContent=n+" सेवाएँ मिलीं";
}

/* --- manually maintained updates (data/updates.json) --- */
function setupFeeds(){
  var boxes=$$("[data-feed]");if(!boxes.length)return;
  fetch(ROOT+"data/updates.json").then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
    boxes.forEach(function(b){
      var items=(d[b.getAttribute("data-feed")]||[]).slice(0,+b.getAttribute("data-max")||8);
      b.innerHTML="";
      if(!items.length){b.innerHTML='<li class="empty">अभी कोई अपडेट नहीं जोड़ा गया। आधिकारिक वेबसाइट देखें।</li>';return}
      items.forEach(function(it){
        var li=document.createElement("li"),h="";
        var t=document.createElement("strong");t.textContent=it.title;
        if(it.link&&/^https:\/\//.test(it.link)){var a=document.createElement("a");a.href=it.link;a.target="_blank";a.rel="noopener noreferrer";a.appendChild(t);li.appendChild(a)}else li.appendChild(t);
        if(it.sample){var bd=document.createElement("span");bd.className="badge";bd.textContent="नमूना प्रविष्टि";li.lastChild.after(bd)}
        var m=document.createElement("span");m.className="d";m.textContent=[it.date,it.org,it.note].filter(Boolean).join(" • ")||"तिथि जोड़ी नहीं गई";li.appendChild(m);b.appendChild(li);
      });
    });
  }).catch(function(){boxes.forEach(function(b){b.innerHTML='<li class="empty">अपडेट लोड नहीं हो सके। साइट को वेब सर्वर/GitHub Pages से खोलें, या आधिकारिक वेबसाइट देखें।</li>'})});
}

/* --- contact form: client-side validation. No backend => opens WhatsApp or posts to configured endpoint --- */
function setupForm(){
  var f=$("#cform");if(!f)return;
  function err(id,m){var el=$("#"+id),e=$("#e-"+id);el.setAttribute("aria-invalid",m?"true":"false");e.textContent=m||"";return!m}
  f.addEventListener("submit",function(ev){
    ev.preventDefault();
    var name=$("#name").value.trim(),mob=$("#mobile").value.replace(/\s|-/g,""),msg=$("#message").value.trim(),svc=$("#service").value;
    var ok=true;
    ok=err("name",name.length<2?"कृपया अपना नाम लिखें":"")&&ok;
    ok=err("mobile",!/^(\+?91)?[6-9]\d{9}$/.test(mob)?"सही 10 अंकों का मोबाइल नंबर लिखें":"")&&ok;
    ok=err("message",msg.length<5?"कृपया अपनी ज़रूरत लिखें":(/(otp|password|पासवर्ड|\b\d{12}\b)/i.test(msg)?"OTP, पासवर्ड या आधार नंबर यहाँ न लिखें":""))&&ok;
    var cons=$("#consent");$("#e-consent").textContent=cons.checked?"":"आगे बढ़ने के लिए सहमति ज़रूरी है";ok=cons.checked&&ok;
    var st=$("#fstatus");st.className="";st.textContent="";if(!ok){var bad=$("[aria-invalid=true]",f);if(bad)bad.focus();return}
    var text="नमस्ते, मेरा नाम "+name+" है। मोबाइल: "+mob+"। सेवा: "+svc+"। "+msg;
    if(C.formEndpoint&&/^https:\/\//.test(C.formEndpoint)){
      fetch(C.formEndpoint,{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify({name:name,mobile:mob,service:svc,message:msg})})
        .then(function(r){if(!r.ok)throw 0;st.className="status";st.textContent="धन्यवाद! आपका संदेश भेज दिया गया है।";f.reset()}).catch(function(){st.textContent="संदेश नहीं जा सका। कृपया WhatsApp या कॉल करें।"});
    }else if(digits(C.whatsapp)){window.open("https://wa.me/"+digits(C.whatsapp)+"?text="+encodeURIComponent(text),"_blank","noopener");st.className="status";st.textContent="WhatsApp खुल रहा है — वहाँ 'Send' दबाएँ।"}
    else{st.className="status";st.textContent="फ़ॉर्म सही है, पर दुकान का WhatsApp नंबर/फ़ॉर्म endpoint अभी config.js में जोड़ा नहीं गया है।"}
  });
}

document.addEventListener("DOMContentLoaded",function(){
  setupContacts();setupNav();setupLang();setupSearch();setupFeeds();setupForm();
  $$("[data-year]").forEach(function(e){e.textContent=new Date().getFullYear()});
});
})();
