#!/usr/bin/env python3
"""Cyber City static site generator.
Usage: python3 tools/build.py [--url https://USER.github.io/cyber-city/]
Regenerates all HTML pages, sitemap.xml and robots.txt from data/services.json + the page text below.
Edit shop details in assets/js/config.js, prices in data/services.json, notices in data/updates.json."""
import json, os, sys, html
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://YOUR-USERNAME.github.io/cyber-city/"
if "--url" in sys.argv:
    URL = sys.argv[sys.argv.index("--url") + 1]
if not URL.endswith("/"): URL += "/"
BASE = urlparse(URL).path or "/"
NAME = "Cyber City, Samastipur"
TAG = "आपकी सभी डिजिटल सेवाएँ, एक ही स्थान पर"
E = html.escape
SERV = json.load(open(os.path.join(ROOT, "data/services.json"), encoding="utf-8"))["services"]
BY = {s["id"]: s for s in SERV}

ICONS = {
 "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
 "id": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.5-2 5.5-2 6 0M14 10h4M14 14h3"/>',
 "file": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
 "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V4h6v3M3 13h18"/>',
 "printer": '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>',
 "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 15-5 16 0"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c1-5 11-5 12 0M16 5a3.5 3.5 0 010 7M18 14c2 .5 3.5 2.5 4 5"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4c0 1-1 2-2 2A15 15 0 013 6c0-1 1-2 2-2z"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 "pin": '<path d="M12 21s7-6 7-12a7 7 0 10-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "rupee": '<path d="M7 5h10M7 9h10M7 5c6 0 6 8 0 8l8 6"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "bell": '<path d="M6 16V11a6 6 0 0112 0v5l2 2H4zM10 21h4"/>',
 "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h4"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
 "type": '<path d="M4 6V4h16v2M12 4v16M9 20h6"/>',
 "link": '<path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + "</svg>"
def ic(n): return f'<svg class="ic" aria-hidden="true"><use href="#i-{n}"/></svg>'
LOGO = ('<svg viewBox="0 0 48 48" role="img" aria-label="Cyber City logo"><rect width="48" height="48" rx="11" fill="#1456c8"/>'
        '<rect x="8" y="10" width="32" height="21" rx="3" fill="#fff"/><rect x="11" y="13" width="26" height="15" rx="1.5" fill="#0b2545"/>'
        '<path d="M16 20.5h5M16 24h8M27 17l4 4-4 4" stroke="#7fb0ff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M17 38h14M24 31v7" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>')

# ---------------------------------------------------------------- pages
PAGES = [  # file, nav label hi, en, group
 ("index.html", "होम", "Home"), ("about.html", "हमारे बारे में", "About Us"), ("services.html", "सभी सेवाएँ", "All Services"),
 ("pan-card.html", "PAN कार्ड सेवाएँ", "PAN Card"), ("voter-id.html", "वोटर ID सेवाएँ", "Voter ID"),
 ("online-forms.html", "सरकारी ऑनलाइन फॉर्म", "Government Online Forms"), ("latest-jobs.html", "नवीनतम नौकरियाँ", "Latest Jobs"),
 ("admit-card.html", "एडमिट कार्ड", "Admit Card"), ("results.html", "रिज़ल्ट व मेरिट लिस्ट", "Results"),
 ("scholarship.html", "छात्रवृत्ति सेवाएँ", "Scholarship"), ("university-services.html", "कॉलेज व विश्वविद्यालय", "University Updates"),
 ("e-shram.html", "ई-श्रम सेवाएँ", "E-Shram"), ("government-schemes.html", "सरकारी योजनाएँ", "Government Schemes"),
 ("printing-services.html", "प्रिंटिंग व फोटोकॉपी", "Printing & Photocopy"), ("photo-services.html", "पासपोर्ट फोटो व एडिटिंग", "Photo Services"),
 ("pvc-card.html", "PVC कार्ड प्रिंटिंग", "PVC Card"), ("typing-resume.html", "रिज्यूमे व टाइपिंग", "Resume & Typing"),
 ("contact.html", "संपर्क करें", "Contact Us"), ("privacy-policy.html", "गोपनीयता नीति", "Privacy Policy"),
 ("terms.html", "नियम, अस्वीकरण व रिफंड", "Terms & Refund"),
]
LBL = {f: (h, e) for f, h, e in PAGES}
LBL["404.html"] = ("पेज नहीं मिला", "Not found")
TOPNAV = ["index.html", "about.html", None, "latest-jobs.html", "admit-card.html", "results.html", "scholarship.html",
          "university-services.html", "government-schemes.html", "contact.html"]
SUBNAV = ["services.html", "pan-card.html", "voter-id.html", "online-forms.html", "e-shram.html", "printing-services.html",
          "photo-services.html", "pvc-card.html", "typing-resume.html"]
SHORT = {"index.html": ("होम", "Home"), "about.html": ("हमारे बारे में", "About"), "latest-jobs.html": ("नवीनतम जॉब", "Latest Jobs"),
         "admit-card.html": ("एडमिट कार्ड", "Admit Card"), "results.html": ("रिज़ल्ट", "Results"), "scholarship.html": ("स्कॉलरशिप", "Scholarship"),
         "university-services.html": ("यूनिवर्सिटी", "University Updates"), "government-schemes.html": ("सरकारी योजनाएँ", "Govt Schemes"), "contact.html": ("संपर्क", "Contact Us")}

def head(f, title, desc, root=""):
    base = BASE if f == "404.html" else root
    can = URL + ("" if f == "index.html" else f)
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": URL, "inLanguage": "hi"}, ensure_ascii=False)
    robots = '<meta name="robots" content="noindex">' if f == "404.html" else ""
    return f'''<!DOCTYPE html>
<html lang="hi" data-root="{base}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{robots}
<link rel="canonical" href="{can}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="hi_IN">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{can}">
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#1456c8">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='11' fill='%231456c8'/%3E%3Crect x='8' y='10' width='32' height='21' rx='3' fill='%23fff'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{base}assets/css/style.css">
<script type="application/ld+json">{ld}</script>
<script src="{base}assets/js/config.js" defer></script><script src="{base}assets/js/main.js" defer></script></head>
<body>{SPRITE}<a class="skip" href="#main">मुख्य सामग्री पर जाएँ</a>'''

def header(active, root=""):
    r = BASE if active == "404.html" else root
    items = ""
    for f in TOPNAV:
        if f is None:
            subs = "".join(f'<li><a href="{r}{x}" data-en="{LBL[x][1]}"{" aria-current=page" if x == active else ""}>{LBL[x][0]}</a></li>' for x in SUBNAV)
            items += f'<li><button class="dd" aria-expanded="false" aria-haspopup="true" data-en="Services ▾">सेवाएँ ▾</button><ul class="sub">{subs}</ul></li>'
        else:
            h, e = SHORT[f]
            items += f'<li><a href="{r}{f}" data-en="{e}"{" aria-current=page" if f == active else ""}>{h}</a></li>'
    return f'''<div class="topbar"><div class="wrap"><span>स्वतंत्र डिजिटल सेवा केंद्र — सरकारी वेबसाइट नहीं</span><span class="grp">
<a href="#" data-call>{ic("phone")} <span data-cfg="phone"></span></a><a href="#" data-wa>{ic("chat")} WhatsApp</a></span></div></div>
<header class="site"><div class="wrap"><a class="brand" href="{r}index.html">{LOGO}<span>Cyber City<small>समस्तीपुर, बिहार</small></span></a>
<button class="burger" aria-expanded="false" aria-controls="nav" aria-label="मेन्यू खोलें">{ic("menu")}</button>
<nav class="main" id="nav" aria-label="मुख्य मेन्यू"><ul>{items}<li><button class="lang" id="lang" type="button">English</button></li></ul></nav></div></header>'''

def footer(root=""):
    r = BASE if root == "404" else root
    col = lambda lst: "".join(f'<li><a href="{r}{f}">{LBL[f][0]}</a></li>' for f in lst)
    return f'''<footer class="site"><div class="wrap"><div class="cols">
<div><h2>Cyber City, Samastipur</h2><p>{TAG}</p><p>{ic("pin")} <span data-cfg="address"></span><br>{ic("clock")} <span data-cfg="hours"></span></p>
<p><span>{ic("link")} <a data-social="facebook" href="#">Facebook</a></span> &nbsp; <span><a data-social="instagram" href="#">Instagram</a></span> &nbsp; <span><a data-social="youtube" href="#">YouTube</a></span> &nbsp; <span><a data-social="telegram" href="#">Telegram</a></span></p></div>
<div><h2>मुख्य पेज</h2><ul>{col(["index.html","about.html","services.html","latest-jobs.html","admit-card.html","results.html","contact.html"])}</ul></div>
<div><h2>सेवाएँ</h2><ul>{col(["pan-card.html","voter-id.html","online-forms.html","e-shram.html","scholarship.html","university-services.html","government-schemes.html"])}</ul></div>
<div><h2>प्रिंट व अन्य</h2><ul>{col(["printing-services.html","photo-services.html","pvc-card.html","typing-resume.html","privacy-policy.html","terms.html"])}</ul></div></div>
<p class="legal"><strong>अस्वीकरण:</strong> Cyber City, Samastipur एक स्वतंत्र डिजिटल सेवा केंद्र है। यह किसी सरकारी विभाग की वेबसाइट नहीं है और जब तक आधिकारिक प्राधिकरण सत्यापित होकर यहाँ न लिखा हो, कोई सरकारी संबद्धता दावा नहीं किया जाता। अंतिम निर्णय संबंधित सरकारी विभाग का होता है। OTP या पासवर्ड किसी को न बताएँ। &copy; <span data-year></span> Cyber City, Samastipur.</p></div></footer>
<div class="float"><a class="c" href="#" data-call aria-label="कॉल करें">{ic("phone")}</a><a class="w" href="#" data-wa aria-label="WhatsApp करें">{ic("chat")}</a></div>
</body></html>'''

def crumb(f, root=""):
    if f == "index.html": return ""
    return f'<nav class="crumb" aria-label="Breadcrumb"><div class="wrap"><ol><li><a href="{root}index.html">होम</a></li><li aria-current="page">{LBL[f][0]}</li></ol></div></nav>'

def card(s, root=""):
    ch = E(s["charge"]) if s["charge"] else "शुल्क: दुकान से पूछें"
    sk = (s["title"] + " " + s["title_en"] + " " + s["description"] + " " + s["keywords"] + " " + s["category"]).lower()
    return (f'<article class="card" data-s="{E(sk)}" data-cat="{E(s["category"])}"><span class="ico">{ic(s["icon"])}</span><h3>{E(s["title"])}</h3>'
            f'<p>{E(s["description"])}</p><div class="meta"><span class="ch">{ch}</span><a class="more" href="{root}services.html?s={s["id"]}">विवरण देखें</a></div></article>')

def cta():
    return f'<div class="btns"><a class="btn w" href="#" data-wa>{ic("chat")} <span data-en="WhatsApp">WhatsApp करें</span></a><a class="btn p" href="#" data-call>{ic("phone")} <span data-en="Call">कॉल करें</span></a></div>'

def feed(key, mx=6):
    return f'<ul class="feed" data-feed="{key}" data-max="{mx}" aria-live="polite"><li class="empty">अपडेट लोड हो रहे हैं…</li></ul><p class="note">ये अपडेट दुकान द्वारा हाथ से जोड़े जाते हैं (<code>data/updates.json</code>) और लाइव सरकारी फ़ीड नहीं हैं। आवेदन से पहले हमेशा आधिकारिक अधिसूचना पढ़ें।</p>'

def page(f, title, desc, body, root=""):
    return head(f, title, desc, root) + header(f, root) + crumb(f, root) + f'<main id="main">{body}</main>' + footer("404" if f == "404.html" else root)

def write(f, txt):
    open(os.path.join(ROOT, f), "w", encoding="utf-8").write(txt)

SAFETY = "<strong>सावधानी:</strong> OTP, ATM पिन या पासवर्ड कभी साझा न करें। आधार/दस्तावेज़ केवल आवश्यक आवेदन के लिए और आपकी सहमति से उपयोग होते हैं।"
FEE = "<strong>शुल्क:</strong> सरकारी शुल्क अलग होता है और सेवा शुल्क दुकान तय करती है। आवेदन से पहले शुल्क स्पष्ट बताया जाएगा — ताज़ा दर के लिए कॉल/WhatsApp करें।"
DISC = "हम आवेदन भरने में सहायता करते हैं; मंज़ूरी, स्वीकृति या अस्वीकृति का निर्णय संबंधित सरकारी विभाग का होता है।"

# Topic pages: file -> dict
T = {
 "pan-card.html": dict(t="PAN कार्ड सेवाएँ", d="समस्तीपुर में PAN कार्ड नया आवेदन, सुधार व जानकारी में सहायता। आवश्यक दस्तावेज़ और आधिकारिक लिंक।", ic="card",
  intro="नया PAN आवेदन, नाम/जन्म तिथि/पता सुधार और स्थिति जाँच में सहायता।", svc=["pan-new", "pan-correction"],
  docs=["पहचान प्रमाण (जैसे मतदाता पहचान पत्र, पासपोर्ट)", "पता प्रमाण", "जन्म तिथि का प्रमाण", "पासपोर्ट साइज़ फोटो व हस्ताक्षर", "सक्रिय मोबाइल नंबर व ईमेल"],
  steps=["दस्तावेज़ लेकर आएँ या WhatsApp पर पूछें", "फॉर्म में विवरण आपके सामने जाँचकर भरा जाता है", "सरकारी शुल्क व सेवा शुल्क बताकर भुगतान", "पावती (acknowledgement) संभालकर रखें"],
  links=[("NSDL e-Gov PAN पोर्टल", "https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html"), ("UTIITSL PAN पोर्टल", "https://www.pan.utiitsl.com"), ("आयकर विभाग", "https://www.incometax.gov.in")],
  rel=["online-forms.html", "photo-services.html", "e-shram.html"], extra="PAN के लिए तय शुल्क व समय सरकारी पोर्टल पर बदल सकते हैं; वहाँ जाँच लें।"),
 "voter-id.html": dict(t="वोटर ID सेवाएँ", d="नया मतदाता पंजीकरण, वोटर ID सुधार और स्थिति जाँच में सहायता — समस्तीपुर। चुनाव आयोग के आधिकारिक लिंक।", ic="users",
  intro="नए मतदाता पंजीकरण, सुधार, स्थानांतरण और आवेदन की स्थिति जाँचने में सहायता।", svc=["voter-new", "voter-correction"],
  docs=["आयु प्रमाण (जैसे 10वीं का प्रमाण पत्र/जन्म प्रमाण पत्र)", "वर्तमान पते का प्रमाण", "पासपोर्ट साइज़ फोटो", "मोबाइल नंबर", "सुधार हेतु मौजूदा EPIC नंबर"],
  steps=["पात्रता देखें (18+ वर्ष, भारतीय नागरिक)", "सही फॉर्म चुनकर ऑनलाइन भरें", "संदर्भ संख्या सुरक्षित रखें", "आधिकारिक पोर्टल पर स्थिति जाँचें"],
  links=[("मतदाता सेवा पोर्टल (ECI)", "https://voters.eci.gov.in"), ("भारत निर्वाचन आयोग", "https://eci.gov.in")], rel=["online-forms.html", "photo-services.html", "government-schemes.html"], extra=""),
 "online-forms.html": dict(t="सरकारी ऑनलाइन फॉर्म", d="केंद्र व बिहार सरकार के ऑनलाइन फॉर्म, प्रमाण पत्र आवेदन और पात्रता की जानकारी। समस्तीपुर में सहायता।", ic="file",
  intro="केंद्र और बिहार सरकार के ऑनलाइन आवेदन, प्रमाण पत्र (आय/जाति/निवास) व अन्य फॉर्म भरने में सहायता।", svc=["govt-forms", "certificates", "aadhaar-help"],
  docs=["पहचान प्रमाण", "पता प्रमाण", "पासपोर्ट साइज़ फोटो व हस्ताक्षर (निर्धारित साइज़ में)", "योजना/आवेदन के अनुसार अतिरिक्त प्रमाण पत्र", "बैंक खाता विवरण (जहाँ ज़रूरी)"],
  steps=["जिस आवेदन के लिए आना है, उसका नाम बताएँ", "पात्रता व दस्तावेज़ सूची की जाँच", "फॉर्म भरना, फाइल अपलोड व आपके सामने जाँच", "पावती/रसीद की प्रति लें"],
  links=[("भारत सरकार पोर्टल", "https://www.india.gov.in"), ("बिहार सरकार", "https://www.bihar.gov.in"), ("बिहार RTPS (सेवा आवेदन)", "https://serviceonline.bihar.gov.in"), ("UIDAI (आधार)", "https://uidai.gov.in")],
  rel=["government-schemes.html", "photo-services.html", "printing-services.html"], extra="आधार नामांकन/अपडेट जैसी सेवाएँ केवल अधिकृत केंद्र करते हैं। हमारे प्राधिकरण का दावा तभी लिखा जाएगा जब सत्यापित हो।"),
 "latest-jobs.html": dict(t="नवीनतम नौकरियाँ व भर्ती अपडेट", d="सरकारी नौकरी व भर्ती सूचनाएँ, पात्रता और आवेदन में सहायता — Cyber City, समस्तीपुर। आधिकारिक लिंक सहित।", ic="brief",
  intro="भर्ती की सूचनाएँ दुकान द्वारा हाथ से जोड़ी जाती हैं। आवेदन से पहले आधिकारिक विज्ञापन ज़रूर पढ़ें।", svc=["jobs-form"], feed="jobs",
  docs=["शैक्षणिक प्रमाण पत्र व मार्कशीट", "जाति/निवास प्रमाण पत्र (यदि लागू)", "फोटो व हस्ताक्षर (निर्धारित साइज़)", "आधार/पहचान प्रमाण", "ईमेल व मोबाइल नंबर"],
  steps=["आधिकारिक विज्ञापन पढ़ें", "पात्रता (आयु, योग्यता) जाँचें", "आवेदन भरें व शुल्क जमा करें", "आवेदन की प्रति सुरक्षित रखें"],
  links=[("BPSC", "https://www.bpsc.bih.nic.in"), ("UPSC", "https://upsc.gov.in"), ("SSC", "https://ssc.gov.in"), ("भारतीय रेलवे", "https://indianrailways.gov.in"), ("बिहार सरकार", "https://www.bihar.gov.in")],
  rel=["admit-card.html", "results.html", "photo-services.html"], extra=""),
 "admit-card.html": dict(t="एडमिट कार्ड अपडेट", d="परीक्षा एडमिट कार्ड कैसे डाउनलोड करें, परीक्षा विवरण और आधिकारिक लिंक — समस्तीपुर में प्रिंट सुविधा।", ic="id",
  intro="एडमिट कार्ड डाउनलोड करने और साफ़ प्रिंट निकालने में सहायता। अपना पासवर्ड/जन्म तिथि स्वयं दर्ज करें।", svc=["admit-card"], feed="admit",
  docs=["पंजीकरण/रोल नंबर", "जन्म तिथि या पासवर्ड", "पहचान पत्र (परीक्षा के दिन)"],
  steps=["आधिकारिक वेबसाइट खोलें", "पंजीकरण विवरण स्वयं दर्ज करें", "एडमिट कार्ड में नाम, तिथि, केंद्र जाँचें", "प्रिंट लें व गलती हो तो तुरंत संस्था से संपर्क करें"],
  links=[("UPSC", "https://upsc.gov.in"), ("SSC", "https://ssc.gov.in"), ("BPSC", "https://www.bpsc.bih.nic.in"), ("DigiLocker", "https://www.digilocker.gov.in")],
  rel=["latest-jobs.html", "printing-services.html", "results.html"], extra=""),
 "results.html": dict(t="रिज़ल्ट व मेरिट लिस्ट", d="बोर्ड, विश्वविद्यालय व प्रवेश परीक्षा के रिज़ल्ट और मेरिट लिस्ट देखने की जानकारी, आधिकारिक लिंक सहित।", ic="bell",
  intro="बोर्ड, विश्वविद्यालय और प्रवेश परीक्षा के परिणाम देखने व प्रिंट निकालने में सहायता।", svc=["results"], feed="results",
  docs=["रोल नंबर/पंजीकरण संख्या", "जन्म तिथि (जहाँ माँगी जाए)"],
  steps=["संस्था की आधिकारिक वेबसाइट खोलें", "रोल नंबर आदि दर्ज करें", "परिणाम की प्रति/PDF सेव करें", "अंक-पत्र की मूल प्रति संस्था से ही मान्य"],
  links=[("CBSE", "https://www.cbse.gov.in"), ("बिहार बोर्ड (BSEB)", "https://biharboardonline.bihar.gov.in"), ("DigiLocker", "https://www.digilocker.gov.in")],
  rel=["admit-card.html", "university-services.html", "scholarship.html"], extra="ऑनलाइन प्रिंट केवल जानकारी हेतु होता है; आधिकारिक अंक-पत्र संस्था से ही मान्य है।"),
 "scholarship.html": dict(t="छात्रवृत्ति सेवाएँ", d="बिहार पोस्ट मैट्रिक, NSP व अन्य छात्रवृत्ति आवेदन: पात्रता, दस्तावेज़ सूची और आधिकारिक लिंक — समस्तीपुर।", ic="cap",
  intro="छात्रवृत्ति के आवेदन, दस्तावेज़ तैयारी और सत्यापन प्रक्रिया में मार्गदर्शन।", svc=["scholarship"], feed="scholarship",
  docs=["आधार/पहचान प्रमाण", "पिछली कक्षा की मार्कशीट", "आय प्रमाण पत्र", "जाति प्रमाण पत्र (यदि लागू)", "बैंक पासबुक (आधार से जुड़ा खाता)", "संस्था का नामांकन/फीस रसीद"],
  steps=["पात्रता व अंतिम तिथि आधिकारिक पोर्टल पर जाँचें", "दस्तावेज़ स्कैन/रीसाइज़ करवाएँ", "आवेदन भरें व प्रिंट लें", "संस्था में सत्यापन करवाएँ"],
  links=[("राष्ट्रीय छात्रवृत्ति पोर्टल (NSP)", "https://scholarships.gov.in"), ("बिहार सरकार", "https://www.bihar.gov.in")], rel=["university-services.html", "photo-services.html", "online-forms.html"],
  extra="बिहार पोस्ट मैट्रिक छात्रवृत्ति सहित राज्य योजनाओं का वर्तमान आधिकारिक लिंक व नियम बिहार सरकार की साइट पर जाँचें; यहाँ दी गई जानकारी बदल सकती है।"),
 "university-services.html": dict(t="कॉलेज व विश्वविद्यालय सेवाएँ", d="प्रवेश फॉर्म, रजिस्ट्रेशन, परीक्षा फॉर्म, माइग्रेशन व मार्कशीट आवेदन में सहायता — समस्तीपुर।", ic="cap",
  intro="प्रवेश, रजिस्ट्रेशन, परीक्षा फॉर्म, माइग्रेशन व प्रमाण पत्र आवेदन में सहायता। विश्वविद्यालय की सूचनाएँ यहाँ हाथ से जोड़ी जाती हैं।", svc=["univ-admission", "univ-exam", "migration"], feed="university",
  docs=["पिछली मार्कशीट व प्रमाण पत्र", "पंजीकरण संख्या", "फोटो व हस्ताक्षर", "आधार/पहचान प्रमाण", "शुल्क भुगतान के लिए बैंक/UPI"],
  steps=["अपने विश्वविद्यालय/कॉलेज की सूचना देखें", "दस्तावेज़ तैयार करें", "फॉर्म भरें और शुल्क जमा करें", "प्रिंट/रसीद संभालकर रखें"],
  links=[("UGC", "https://www.ugc.gov.in"), ("DigiLocker", "https://www.digilocker.gov.in")], rel=["scholarship.html", "results.html", "photo-services.html"],
  extra="अपने विश्वविद्यालय की आधिकारिक वेबसाइट का पता उसके नोटिस/प्रवेश पत्र से सत्यापित करें।"),
 "e-shram.html": dict(t="ई-श्रम सेवाएँ", d="ई-श्रम कार्ड पंजीकरण, सुधार व जानकारी में सहायता — समस्तीपुर। आवश्यक दस्तावेज़ व आधिकारिक पोर्टल लिंक।", ic="brief",
  intro="असंगठित क्षेत्र के श्रमिकों के लिए ई-श्रम पंजीकरण व विवरण अपडेट में सहायता।", svc=["eshram-reg", "eshram-update"],
  docs=["आधार से जुड़ा मोबाइल नंबर (OTP आप स्वयं दर्ज करेंगे)", "बैंक खाता विवरण (IFSC सहित)", "पेशे/कार्य की जानकारी", "नामित व्यक्ति (नॉमिनी) का विवरण"],
  steps=["पात्रता की जानकारी लें", "आपके मोबाइल पर आया OTP आप स्वयं दर्ज करें", "विवरण जाँचकर पंजीकरण पूरा करें", "UAN/कार्ड की प्रति सुरक्षित रखें"],
  links=[("ई-श्रम पोर्टल", "https://eshram.gov.in")], rel=["government-schemes.html", "online-forms.html", "photo-services.html"], extra="ई-श्रम पंजीकरण निःशुल्क है — पोर्टल की नीति की जाँच करें। हम केवल सहायता का सेवा शुल्क बताएँगे।"),
 "government-schemes.html": dict(t="सरकारी योजनाएँ", d="केंद्र व बिहार सरकार की योजनाओं की पात्रता, दस्तावेज़ व आवेदन प्रक्रिया की जानकारी और आधिकारिक स्रोत।", ic="shield",
  intro="योजनाओं की पात्रता, ज़रूरी दस्तावेज़ और आवेदन प्रक्रिया समझने में मदद। अंतिम पात्रता आधिकारिक विभाग तय करता है।", svc=["schemes", "ration-card"], feed="schemes",
  docs=["आधार/पहचान प्रमाण", "निवास व आय प्रमाण", "बैंक खाता विवरण", "योजना-विशेष दस्तावेज़"],
  steps=["योजना का नाम या ज़रूरत बताएँ", "आधिकारिक वेबसाइट पर पात्रता जाँचें", "दस्तावेज़ तैयार करें", "आवेदन करें व पावती रखें"],
  links=[("myScheme (योजना खोजें)", "https://www.myscheme.gov.in"), ("भारत सरकार पोर्टल", "https://www.india.gov.in"), ("बिहार खाद्य आपूर्ति (EPDS)", "https://epds.bihar.gov.in"), ("बिहार सरकार", "https://www.bihar.gov.in")],
  rel=["online-forms.html", "e-shram.html", "scholarship.html"], extra="योजनाओं के नियम बदलते रहते हैं; यहाँ कोई योजना सूचीबद्ध होने का मतलब उसकी स्वीकृति की गारंटी नहीं है।"),
 "printing-services.html": dict(t="प्रिंटिंग, फोटोकॉपी व स्कैनिंग", d="समस्तीपुर में ब्लैक-व्हाइट/कलर प्रिंट, फोटोकॉपी, स्कैनिंग, डॉक्यूमेंट फॉर्मेटिंग व लैमिनेशन।", ic="printer",
  intro="ब्लैक-व्हाइट व कलर प्रिंट, फोटोकॉपी, स्कैन-टू-PDF, डॉक्यूमेंट फॉर्मेटिंग और लैमिनेशन।", svc=["printing", "photocopy", "lamination"],
  docs=["फाइल Pen-drive या WhatsApp से लाएँ", "पेज साइज़ (A4/A3/Legal) व कॉपियाँ बताएँ", "स्कैन के लिए मूल दस्तावेज़"],
  steps=["फाइल या दस्तावेज़ दें", "साइज़, रंग, कॉपियाँ बताएँ", "प्रिंट देखकर संतुष्ट हों", "भुगतान (दरें दुकान पर तय)"], links=[],
  rel=["photo-services.html", "pvc-card.html", "typing-resume.html"], extra="प्रिंट दरें दुकान तय करती है; आप data/services.json में दरें भर सकते हैं।"),
 "photo-services.html": dict(t="पासपोर्ट फोटो व फोटो एडिटिंग", d="पासपोर्ट साइज़ फोटो, फोटो रीसाइज़, बैकग्राउंड सुधार और फॉर्म के अनुसार फोटो-हस्ताक्षर तैयारी — समस्तीपुर।", ic="camera",
  intro="पासपोर्ट साइज़ फोटो, ऑनलाइन फॉर्म की KB/पिक्सेल सीमा के अनुसार फोटो-हस्ताक्षर और प्रिंट।", svc=["passport-photo", "photo-edit"],
  docs=["साफ़ रोशनी में खींची गई फोटो (या दुकान पर खिंचवाएँ)", "हस्ताक्षर सफ़ेद कागज़ पर काली/नीली स्याही से", "आवेदन में बताई गई साइज़/KB सीमा"],
  steps=["बताएँ किस फॉर्म के लिए चाहिए", "साइज़ व फॉर्मेट तय", "तैयार फाइल/प्रिंट देखें", "फाइल WhatsApp/Pen-drive में लें"], links=[],
  rel=["online-forms.html", "scholarship.html", "latest-jobs.html"], extra="सरकारी दस्तावेज़ों की फोटो में छेड़छाड़ या जालसाज़ी वाला कोई काम नहीं किया जाता।"),
 "pvc-card.html": dict(t="PVC कार्ड व ID कार्ड प्रिंटिंग", d="PVC कार्ड प्रिंटिंग, फोटो ID कार्ड और ग्राहक द्वारा दिए डिज़ाइन का प्रिंट — पारदर्शी मूल्य जानकारी के साथ।", ic="card",
  intro="स्कूल/संस्था/दुकान ID, सदस्यता कार्ड और व्यक्तिगत फोटो कार्ड, आपके दिए डिज़ाइन से PVC पर प्रिंट।", svc=["pvc"],
  docs=["डिज़ाइन फाइल (PDF/JPG/PNG) या विवरण", "फोटो (साफ़ व स्पष्ट)", "कार्ड की संख्या व साइज़"],
  steps=["डिज़ाइन/विवरण दें", "प्रूफ देखकर मंज़ूरी दें", "प्रिंट व लैमिनेशन", "भुगतान व कार्ड लें"], links=[],
  rel=["printing-services.html", "photo-services.html", "typing-resume.html"], extra="आधार, PAN, वोटर ID जैसे सरकारी पहचान पत्रों की नकल या डुप्लिकेट कार्ड नहीं बनाए जाते। आधिकारिक कार्ड सरकारी पोर्टल से ही प्राप्त करें।"),
 "typing-resume.html": dict(t="रिज्यूमे व टाइपिंग सेवाएँ", d="रिज्यूमे/बायोडाटा, हिन्दी-अंग्रेज़ी टाइपिंग, आवेदन पत्र व दस्तावेज़ फॉर्मेटिंग — Cyber City समस्तीपुर।", ic="type",
  intro="रिज्यूमे बनवाना, हिन्दी/अंग्रेज़ी टाइपिंग, आवेदन व पत्र लेखन, Word-PDF कन्वर्ज़न और शपथ-पत्र का मसौदा टाइप करना।", svc=["resume", "typing"],
  docs=["अपनी शिक्षा, अनुभव और संपर्क जानकारी", "हस्तलिखित/मूल सामग्री", "फोटो (यदि रिज्यूमे में लगानी हो)"],
  steps=["सामग्री/विवरण दें", "ड्राफ़्ट देखकर बदलाव बताएँ", "अंतिम फाइल तैयार", "PDF/प्रिंट लें"], links=[],
  rel=["printing-services.html", "latest-jobs.html", "photo-services.html"], extra="शपथ-पत्र केवल टाइप/फॉर्मेट किए जाते हैं; कानूनी मान्यता हेतु नोटरी/अधिकृत अधिकारी की प्रक्रिया अलग है। हम कानूनी सलाह नहीं देते।"),
}

def topic(f):
    p = T[f]
    cards = "".join(card(BY[i]) for i in p["svc"])
    docs = "".join(f"<li>{E(x)}</li>" for x in p["docs"])
    steps = "".join(f"<li>{E(x)}</li>" for x in p["steps"])
    links = "".join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{ic("link")} {E(n)}</a></li>' for n, u in p["links"]) or "<li>इस सेवा के लिए सरकारी पोर्टल लागू नहीं है।</li>"
    rel = "".join(f'<li><a href="{x}">{LBL[x][0]}</a></li>' for x in p["rel"])
    fd = f'<h2 class="t" style="margin-top:34px">नवीनतम सूचनाएँ</h2>{feed(p["feed"])}' if p.get("feed") else ""
    extra = f'<p class="note">{E(p["extra"])}</p>' if p["extra"] else ""
    body = f'''<div class="pagehead"><div class="wrap"><h1>{p["t"]}</h1><p>{E(p["intro"])}</p>{cta()}</div></div>
<section class="blk"><div class="wrap two"><div class="prose"><h2>हमारी सहायता</h2><div class="grid">{cards}</div>
<h2>आवश्यक दस्तावेज़</h2><ul class="checks">{docs}</ul><h2>प्रक्रिया</h2><ol class="steps">{steps}</ol>{fd}{extra}
<p class="note">{FEE}<br>{DISC}</p><p class="note">{SAFETY}</p></div>
<aside><div class="side"><h3>आधिकारिक वेबसाइट</h3><ul class="linklist">{links}</ul><p style="font-size:14px;color:var(--muted)">बाहरी लिंक नए टैब में खुलते हैं। पता हमेशा ब्राउज़र में जाँच लें (.gov.in).</p></div>
<div class="side" style="margin-top:16px"><h3>संबंधित सेवाएँ</h3><ul class="linklist">{rel}</ul></div></aside></div></section>'''
    return page(f, f'{p["t"]} | {NAME}', p["d"], body)

# ---------------------------------------------------------------- special pages
def home():
    groups = {}
    for s in SERV: groups.setdefault(s["category"], []).append(s)
    gpage = {"सरकारी सेवाएँ": "online-forms.html", "पहचान पत्र": "pan-card.html", "छात्र सेवाएँ": "scholarship.html", "प्रिंट व फोटो": "printing-services.html", "टाइपिंग व रिज्यूमे": "typing-resume.html"}
    gh = "".join(f'<div class="group"><h3>{E(c)}</h3><ul>{"".join("<li>"+E(s["title"])+"</li>" for s in v)}</ul><a href="{gpage[c]}">पूरी जानकारी</a></div>' for c, v in groups.items())
    pop = "".join(card(BY[i]) for i in ["pan-new", "voter-new", "eshram-reg", "scholarship", "jobs-form", "printing", "passport-photo", "pvc"])
    chips = "".join(f'<a href="services.html?q={q}">{q}</a>' for q in ["PAN", "वोटर ID", "ई-श्रम", "छात्रवृत्ति", "प्रिंट", "फोटो", "रिज्यूमे"])
    body = f'''<section class="hero"><div class="wrap"><div><h1>Cyber City, Samastipur</h1><p class="tag">{TAG}</p>
<p class="lead">सरकारी फॉर्म, पहचान पत्र सहायता, छात्रवृत्ति, नौकरी आवेदन, प्रिंटिंग, फोटो और टाइपिंग — समस्तीपुर में एक भरोसेमंद डिजिटल सेवा केंद्र।</p>
<div class="btns"><a class="btn p" href="services.html" data-en="View our services">हमारी सेवाएँ देखें</a><a class="btn w" href="#" data-wa data-en="WhatsApp">WhatsApp करें</a><a class="btn o" href="#" data-call data-en="Call">कॉल करें</a></div>
<form class="search" role="search" action="services.html" method="get"><label for="hq" class="hidden">सेवा खोजें</label><input id="hq" name="q" type="search" placeholder="सेवा खोजें, जैसे: PAN, छात्रवृत्ति, फोटो…" autocomplete="off"><button type="submit">{ic("search")} खोजें</button></form>
<div class="chips" aria-label="लोकप्रिय खोज">{chips}</div></div>
<div class="desk"><h2>काउंटर पर क्या मिलता है</h2><ul><li><span>फॉर्म भरना व आवेदन</span><b>सहायता</b></li><li><span>प्रिंट, स्कैन, फोटोकॉपी</span><b>तुरंत</b></li><li><span>फोटो, PVC, रिज्यूमे</span><b>तैयार</b></li><li><span>सेवा शुल्क</span><b>पहले बताया जाता है</b></li></ul></div></div></section>
<section class="blk"><div class="wrap"><h2 class="t">लोकप्रिय सेवाएँ</h2><p class="sub-t">सबसे ज़्यादा पूछी जाने वाली सेवाएँ। सारी सेवाएँ <a href="services.html">यहाँ</a> देखें।</p><div class="grid">{pop}</div></div></section>
<section class="blk alt"><div class="wrap"><h2 class="t">हमारी सभी सेवाएँ</h2><p class="sub-t">सरकारी फॉर्म, आधार संबंधी मार्गदर्शन (जहाँ अधिकृत), PAN, वोटर ID, ई-श्रम, राशन कार्ड व योजनाएँ, कॉलेज-विश्वविद्यालय सेवाएँ, प्रिंटिंग, PVC कार्ड, रिज्यूमे और छात्र सेवाएँ।</p><div class="groups">{gh}</div></div></section>
<section class="blk"><div class="wrap"><h2 class="t">ताज़ा अपडेट</h2><p class="sub-t">नौकरी, एडमिट कार्ड और रिज़ल्ट की सूचनाएँ।</p><div class="tabs">
<div><h3><a href="latest-jobs.html">नौकरी व भर्ती</a></h3>{feed("jobs",4)}</div><div><h3><a href="admit-card.html">एडमिट कार्ड व परीक्षा</a></h3>{feed("admit",4)}</div><div><h3><a href="results.html">रिज़ल्ट व मेरिट लिस्ट</a></h3>{feed("results",4)}</div></div>
<div class="tabs" style="margin-top:22px"><div><h3><a href="scholarship.html">छात्रवृत्ति</a></h3>{feed("scholarship",3)}</div><div><h3><a href="government-schemes.html">सरकारी योजनाएँ</a></h3>{feed("schemes",3)}</div><div><h3>सामान्य सूचना</h3>{feed("general",3)}</div></div></div></section>
<section class="blk alt"><div class="wrap"><h2 class="t">सेवा लेने की प्रक्रिया</h2><p class="sub-t">आसान चार कदम।</p><ol class="steps"><li><b>संपर्क करें</b><br>दुकान आएँ, कॉल या WhatsApp करें।</li><li><b>जानकारी लें</b><br>ज़रूरी दस्तावेज़ और शुल्क पहले जानें।</li><li><b>आवेदन भरवाएँ</b><br>विवरण आपके सामने जाँचे जाते हैं।</li><li><b>रसीद लें</b><br>पावती/रसीद संभालकर रखें।</li></ol></div></section>
<section class="blk"><div class="wrap"><h2 class="t">Cyber City क्यों चुनें</h2><div class="grid">
<div class="card"><span class="ico">{ic("shield")}</span><h3>स्पष्ट जानकारी</h3><p>हर पेज पर दस्तावेज़ सूची, प्रक्रिया और आधिकारिक लिंक।</p></div>
<div class="card"><span class="ico">{ic("rupee")}</span><h3>शुल्क पहले बताया जाता है</h3><p>सरकारी शुल्क और सेवा शुल्क अलग-अलग।</p></div>
<div class="card"><span class="ico">{ic("user")}</span><h3>आपकी जानकारी सुरक्षित</h3><p>OTP/पासवर्ड कभी नहीं माँगे जाते; दस्तावेज़ केवल ज़रूरत पर।</p></div>
<div class="card"><span class="ico">{ic("phone")}</span><h3>फोन पर आसान संपर्क</h3><p>मोबाइल पर एक टैप में कॉल या WhatsApp।</p></div></div>
<!-- ग्राहक समीक्षाएँ: केवल असली, सहमति से प्राप्त समीक्षाएँ यहाँ जोड़ें। अभी कोई समीक्षा प्रकाशित नहीं है। -->
<p class="note">ग्राहक समीक्षाएँ यहाँ तभी दिखाई जाएँगी जब वे असली हों और ग्राहक की सहमति से मिली हों।</p></div></section>
<section class="blk alt"><div class="wrap two"><div><h2 class="t">संपर्क व स्थान</h2><p>{ic("phone")} <span data-cfg="phone"></span><br>{ic("pin")} <span data-cfg="address"></span><br>{ic("clock")} <span data-cfg="hours"></span></p>{cta()}</div>
<div id="map" class="mapbox"><p>दुकान का पता <code>assets/js/config.js</code> में जोड़ने पर नक्शा यहाँ दिखेगा।</p></div></div></section>'''
    return page("index.html", f"Cyber Cafe in Samastipur | Online Services, Form Filling, Printing — {NAME}",
                "समस्तीपुर का Cyber City: ऑनलाइन फॉर्म, PAN, वोटर ID, ई-श्रम, छात्रवृत्ति, प्रिंटिंग, फोटो, PVC कार्ड और रिज्यूमे सेवाएँ एक ही जगह।", body)

def services():
    cats = sorted({s["category"] for s in SERV}, key=lambda c: [s["category"] for s in SERV].index(c))
    cb = "".join(f'<button type="button" class="btn o catbtn" data-cat="{E(c)}">{E(c)}</button>' for c in cats)
    det = ""
    for s in SERV:
        docs = "".join(f"<li>{E(d)}</li>" for d in s["documents"])
        off = "".join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{ic("link")} {E(n)}</a></li>' for n, u in s["official"]) or "<li>कोई विशेष सरकारी पोर्टल लागू नहीं।</li>"
        rel = "".join(f'<li><a href="services.html?s={r["id"]}">{E(r["title"])}</a></li>' for r in SERV if r["category"] == s["category"] and r["id"] != s["id"])
        det += f'''<article class="detail prose" id="detail-{s["id"]}"><h2>{E(s["title"])}</h2><p>{E(s["description"])}</p>
<p><strong>{E(s["charge"]) if s["charge"] else "शुल्क: दुकान से पूछें (सरकारी शुल्क अलग)"}</strong></p><h3>आवश्यक दस्तावेज़</h3><ul class="checks">{docs}</ul>
<h3>आधिकारिक लिंक</h3><ul class="linklist">{off}</ul><p><a href="{s["page"]}">इस विषय का पूरा पेज</a></p>
<div class="btns"><a class="btn w" href="#" data-wa data-msg="नमस्ते, मुझे &quot;{E(s["title"])}&quot; के बारे में जानकारी चाहिए।">{ic("chat")} इस सेवा के बारे में पूछें</a><a class="btn p" href="#" data-call>{ic("phone")} कॉल करें</a></div>
<h3>संबंधित सेवाएँ</h3><ul class="linklist">{rel}</ul><p class="note">{DISC}</p><p><a href="services.html">← सभी सेवाएँ</a></p></article>'''
    body = f'''<div class="pagehead"><div class="wrap"><h1>सभी सेवाएँ</h1><p>सेवा खोजें, विवरण देखें और सीधे हमसे संपर्क करें।</p></div></div>
<section class="blk"><div class="wrap"><div id="dirhead"><form class="search" role="search" onsubmit="return false"><label for="q" class="hidden">सेवा खोजें</label><input id="q" type="search" placeholder="सेवा खोजें…" autocomplete="off"><button type="button" aria-hidden="true" tabindex="-1">{ic("search")}</button></form>
<div class="btns" role="group" aria-label="श्रेणी">{cb}<button type="button" class="btn o catbtn" data-cat="">सभी</button></div><p id="count" role="status" aria-live="polite" style="color:var(--muted)">{len(SERV)} सेवाएँ मिलीं</p></div>
<div class="grid" id="svc-list">{"".join(card(s) for s in SERV)}</div><p id="none" class="empty hidden">कोई सेवा नहीं मिली। दूसरा शब्द आज़माएँ या हमें कॉल/WhatsApp करें।</p>
<div id="details" style="margin-top:36px">{det}</div></div></section>'''
    return page("services.html", f"Online Services in Samastipur — सभी सेवाएँ | {NAME}", "समस्तीपुर में ऑनलाइन फॉर्म, PAN, वोटर ID, छात्रवृत्ति, प्रिंटिंग, फोटो और टाइपिंग सेवाओं की पूरी सूची खोजें।", body)

def about():
    body = f'''<div class="pagehead"><div class="wrap"><h1>हमारे बारे में</h1><p>Cyber City, Samastipur — आपकी सभी डिजिटल सेवाएँ, एक ही स्थान पर।</p></div></div>
<section class="blk"><div class="wrap prose"><h2>परिचय</h2><p>Cyber City, समस्तीपुर (बिहार) में स्थित एक स्वतंत्र साइबर कैफ़े व डिजिटल सेवा केंद्र है, जो विद्यार्थियों, नौकरी चाहने वालों, किसानों, पेंशनर्स और आम नागरिकों को ऑनलाइन फॉर्म, दस्तावेज़ और प्रिंटिंग से जुड़ी सहायता देता है।</p>
<h2>हमारा मिशन</h2><p>ऑनलाइन सेवाओं को सरल, साफ़ और भरोसेमंद बनाना, ताकि हर ग्राहक को सही जानकारी, सही दस्तावेज़ सूची और पहले से बताया गया शुल्क मिले।</p>
<h2>हमारा विज़न</h2><p>समस्तीपुर और आसपास के लोगों के लिए पहली पसंद का पारदर्शी डिजिटल सेवा केंद्र बनना।</p>
<h2>सेवा का तरीका</h2><ul class="checks"><li>जानकारी पहले, आवेदन बाद में</li><li>शुल्क पहले बताया जाना</li><li>आपके सामने फॉर्म भरना व जाँच</li><li>OTP/पासवर्ड कभी नहीं माँगना</li><li>आधिकारिक वेबसाइट के लिंक देना</li></ul>
<p class="note">Cyber City एक स्वतंत्र केंद्र है और यह सरकारी वेबसाइट नहीं है। कोई सरकारी अधिकृतता, पंजीकरण या प्रमाणन तभी यहाँ लिखा जाएगा जब वह सत्यापित हो। दुकान का नाम, पता, पंजीकरण आदि विवरण <code>assets/js/config.js</code> से जोड़े जाते हैं।</p>{cta()}</div></section>'''
    return page("about.html", f"About Cyber City, Samastipur — हमारे बारे में | {NAME}", "Cyber City, समस्तीपुर का परिचय, मिशन, विज़न और सेवा का तरीका।", body)

def contact():
    opts = "".join(f'<option>{E(s["title"])}</option>' for s in SERV) + "<option>अन्य</option>"
    body = f'''<div class="pagehead"><div class="wrap"><h1>संपर्क करें</h1><p>कॉल, WhatsApp या नीचे फॉर्म से अपनी ज़रूरत बताएँ।</p></div></div>
<section class="blk"><div class="wrap two"><div><h2 class="t">संदेश भेजें</h2>
<form class="f" id="cform" novalidate><label for="name">आपका नाम<input id="name" autocomplete="name" required aria-describedby="e-name"><span class="err" id="e-name"></span></label>
<label for="mobile">मोबाइल नंबर<input id="mobile" inputmode="tel" autocomplete="tel" required aria-describedby="e-mobile"><span class="err" id="e-mobile"></span></label>
<label for="service">सेवा<select id="service">{opts}</select></label>
<label for="message">आपकी ज़रूरत<textarea id="message" rows="4" required aria-describedby="e-message"></textarea><span class="err" id="e-message"></span></label>
<p class="note" style="margin:0">यहाँ आधार नंबर, OTP, पासवर्ड या बैंक पिन <strong>न लिखें</strong>।</p>
<label class="chk" for="consent"><input type="checkbox" id="consent"><span>मैं सहमत हूँ कि मेरा नाम और नंबर केवल मुझसे संपर्क करने के लिए उपयोग हो। <a href="privacy-policy.html">गोपनीयता नीति</a></span></label><span class="err" id="e-consent"></span>
<button class="btn p" type="submit">संदेश भेजें</button><div id="fstatus" role="status" aria-live="polite"></div></form></div>
<aside><div class="side"><h3>दुकान की जानकारी</h3><p>{ic("phone")} फ़ोन: <span data-cfg="phone"></span><br>{ic("chat")} WhatsApp: <span data-cfg="whatsapp"></span><br>{ic("mail")} ईमेल: <span data-cfg="email"></span><br>{ic("pin")} पता: <span data-cfg="address"></span><br>{ic("clock")} समय: <span data-cfg="hours"></span></p>{cta()}</div></aside></div></section>
<section class="blk alt"><div class="wrap"><h2 class="t">नक्शा</h2><div id="map" class="mapbox"><p>दुकान का Google Maps embed लिंक <code>assets/js/config.js</code> (mapEmbed) में जोड़ने पर नक्शा यहाँ दिखेगा।</p></div></div></section>'''
    return page("contact.html", f"Contact Cyber City, Samastipur — संपर्क व पता | {NAME}", "Cyber City, समस्तीपुर से फ़ोन, WhatsApp या फॉर्म के ज़रिए संपर्क करें। पता, समय और नक्शा।", body)

def legal(f, title, desc, h, secs):
    s = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in secs)
    body = f'<div class="pagehead"><div class="wrap"><h1>{h}</h1><p>अंतिम अपडेट: दुकान द्वारा प्रकाशन तिथि यहाँ जोड़ें।</p></div></div><section class="blk"><div class="wrap prose">{s}<p class="note">यह एक सामान्य मसौदा है। प्रकाशित करने से पहले अपने व्यवसाय के अनुसार जाँचें और आवश्यकता हो तो वकील से सलाह लें।</p></div></section>'
    return page(f, f"{title} | {NAME}", desc, body)

def p404():
    body = f'<div class="pagehead"><div class="wrap"><h1>पेज नहीं मिला (404)</h1><p>आप जो पेज खोज रहे हैं वह उपलब्ध नहीं है।</p><div class="btns"><a class="btn p" href="{BASE}index.html">होम पर जाएँ</a><a class="btn o" href="{BASE}services.html">सेवाएँ देखें</a></div></div></div>'
    return page("404.html", f"पेज नहीं मिला | {NAME}", "यह पेज उपलब्ध नहीं है।", body)

PRIV = [("हम कौन सी जानकारी लेते हैं", "संपर्क फॉर्म में आपका नाम, मोबाइल नंबर, चुनी हुई सेवा और संदेश। सेवा के दौरान आवेदन हेतु आप जो दस्तावेज़ देंगे, वे केवल उसी आवेदन के लिए उपयोग होंगे।"),
 ("हम क्या नहीं माँगते", "हम OTP, पासवर्ड, ATM/UPI पिन कभी नहीं माँगते। कृपया ये किसी के साथ साझा न करें। आधार नंबर जैसी संवेदनशील जानकारी फॉर्म में न लिखें।"),
 ("उपयोग व सहमति", "आपकी जानकारी केवल आपसे संपर्क करने, आपकी सेवा पूरी करने और रसीद देने के लिए उपयोग होती है। हम इसे बेचते नहीं हैं। फॉर्म भेजने से पहले आपसे सहमति ली जाती है।"),
 ("दस्तावेज़ व सुरक्षा", "ग्राहक के दस्तावेज़ सार्वजनिक URL पर प्रकाशित नहीं किए जाते। सेवा पूरी होने के बाद कंप्यूटर/ड्राइव से फाइलें हटाई जाती हैं।"),
 ("डेटा रखने की अवधि", "संपर्क संदेश और रसीद का रिकॉर्ड केवल आवश्यक अवधि तक रखा जाता है। आप जानकारी हटवाने के लिए हमसे अनुरोध कर सकते हैं। (दुकान अपनी अवधि यहाँ लिखे।)"),
 ("कुकीज़ व तृतीय-पक्ष सेवाएँ", "यह साइट केवल आपकी भाषा-पसंद आपके ब्राउज़र में सहेज सकती है। Google Maps, WhatsApp या सरकारी पोर्टल जैसी बाहरी सेवाओं की अपनी गोपनीयता नीतियाँ होती हैं।"),
 ("गोपनीयता संबंधी संपर्क", "अपने डेटा से जुड़े प्रश्न के लिए <a href=\"contact.html\">संपर्क पेज</a> पर दिए माध्यम से लिखें।")]
TERMS = [("स्वतंत्र सेवा केंद्र", "Cyber City, Samastipur एक स्वतंत्र डिजिटल सेवा केंद्र है, कोई सरकारी कार्यालय या वेबसाइट नहीं। सरकारी अधिकृतता का दावा केवल सत्यापित होने पर किया जाएगा।"),
 ("ग्राहक की ज़िम्मेदारी", "सही व असली दस्तावेज़ देना, विवरण की जाँच करना और अपना OTP/पासवर्ड स्वयं दर्ज करना ग्राहक की ज़िम्मेदारी है। जाली दस्तावेज़ वाला कोई कार्य नहीं किया जाएगा।"),
 ("सरकारी पोर्टल अस्वीकरण", "आवेदन की स्वीकृति, अस्वीकृति, समय-सीमा, पोर्टल की तकनीकी समस्या या नियम बदलाव पर संबंधित विभाग का नियंत्रण है; दुकान उसके लिए ज़िम्मेदार नहीं है। यहाँ दी जानकारी बदल सकती है — आधिकारिक वेबसाइट अंतिम स्रोत है।"),
 ("शुल्क", "सरकारी/पोर्टल शुल्क और दुकान का सेवा शुल्क अलग होते हैं। शुल्क सेवा शुरू करने से पहले बताया जाएगा। (दुकान अपनी दरें data/services.json में भरे।)"),
 ("रिफंड नीति", "दुकान द्वारा काम शुरू करने से पहले रद्द करने पर सेवा शुल्क वापस हो सकता है। सरकारी पोर्टल पर जमा हो चुका शुल्क पोर्टल की नीति के अनुसार ही वापस होता है और दुकान उसकी गारंटी नहीं दे सकती। (दुकान अपनी शर्तें यहाँ अंतिम रूप दे।)"),
 ("ज़िम्मेदारी की सीमा", "ग्राहक द्वारा दी गई गलत जानकारी, देर से आवेदन या विभाग के निर्णय से हुई हानि के लिए दुकान की ज़िम्मेदारी सीमित है।")]

def main():
    out = {"index.html": home(), "about.html": about(), "services.html": services(), "contact.html": contact(), "404.html": p404(),
           "privacy-policy.html": legal("privacy-policy.html", "गोपनीयता नीति", "Cyber City, Samastipur की गोपनीयता नीति: डेटा, दस्तावेज़, कुकीज़ और संपर्क।", "गोपनीयता नीति", PRIV),
           "terms.html": legal("terms.html", "नियम, अस्वीकरण व रिफंड नीति", "Cyber City, Samastipur की सेवा शर्तें, सरकारी पोर्टल अस्वीकरण, शुल्क व रिफंड नीति।", "नियम, अस्वीकरण व रिफंड नीति", TERMS)}
    for f in T: out[f] = topic(f)
    for f, t in out.items(): write(f, t)
    urls = [f for f, _, _ in PAGES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{URL}{'' if f == 'index.html' else f}</loc></url>\n" for f in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n")
    print("built", len(out), "pages (incl. 404) for", URL)

if __name__ == "__main__":
    main()
