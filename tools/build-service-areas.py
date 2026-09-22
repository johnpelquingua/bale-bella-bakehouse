from pathlib import Path
from urllib.parse import quote_plus
import json, re, sys

BASE="https://balebellabakehouse.com/"
TODAY="2026-09-23"
PICKUP="Block 14, Lot 4, Abigail Street, Madonna Residences, Barangay Dela Paz Sur, City of San Fernando, Pampanga 2000, Philippines"
FB="https://www.facebook.com/balebellabakehouse"
IG="https://www.instagram.com/balebellabakehouse/"
YT="https://www.youtube.com/@balebellabakehouse"
TH="https://www.threads.com/@balebellabakehouse"
PIN="https://www.pinterest.com/balebellabakehouse/"
MSG="https://m.me/balebellabakehouse"
SOCIALS=[FB,IG,YT,TH,PIN]
SOCIAL_REL="".join(f'<link rel="me" href="{u}">' for u in SOCIALS)

AREAS=[
    {
      "slug":"angeles-city-pampanga","name":"Angeles City","full":"Angeles City, Pampanga","schema":"City","class":"area-angeles",
      "title":"Bakery Delivery Angeles City, Pampanga | Bale Bella Bakehouse",
      "desc":"Request Bale Bella cookie, brownie, cheesecake and dessert-box delivery to Angeles City, Pampanga, subject to bake-slot and courier confirmation.",
      "keywords":"bakery delivery Angeles City Pampanga, cookie delivery Angeles City, dessert delivery Angeles Pampanga, cheesecake Angeles City, dessert boxes Angeles City, Bale Bella Angeles",
      "lede":"Customers in Angeles City can request Bale Bella’s small-batch cookies, brownies, banana loaf, Basque cheesecake and dessert boxes for courier delivery from our San Fernando home bakehouse.",
      "route":"For pickup, live navigation typically routes you south toward the City of San Fernando and the Dela Paz Sur / Sindalan area. Road choice can vary by your starting point and traffic, so use the live directions button before leaving.",
      "ideas":[("Celebration boxes","Cookie and brownie boxes are easy to share for birthdays, office merienda and small gatherings."),("Giftable bakes","The Taste Box, banana loaf and whole Basque cheesecake work well when you want a ready-to-share dessert."),("Planned office orders","For larger quantities, send the event date, estimated quantity and packaging request through Messenger so we can confirm capacity.")],
      "faq_extra":("Can Bale Bella deliver to offices or residences in Angeles City?","You may request delivery to an Angeles City office or residence. The exact destination, courier availability, delivery fee and timing are confirmed before the order becomes final.")
    },
    {
      "slug":"mabalacat-city-pampanga","name":"Mabalacat City","full":"Mabalacat City, Pampanga","schema":"City","class":"area-mabalacat",
      "title":"Bakery Delivery Mabalacat City, Pampanga | Bale Bella",
      "desc":"Request Bale Bella cookies, brownies, Basque cheesecake, banana loaf and dessert boxes for Mabalacat City, subject to courier and schedule confirmation.",
      "keywords":"bakery delivery Mabalacat City Pampanga, cookie delivery Mabalacat, dessert delivery Mabalacat Pampanga, cheesecake Mabalacat, dessert boxes Mabalacat, Bale Bella Mabalacat",
      "lede":"Bale Bella accepts delivery requests for Mabalacat City when our bake schedule and a suitable courier arrangement are available. All products are prepared from our home bakehouse in San Fernando.",
      "route":"For pickup from Mabalacat City, use live navigation toward Dela Paz Sur in the City of San Fernando. Depending on your exact starting point, navigation may suggest different approaches, so we do not publish a fixed route or travel-time promise.",
      "ideas":[("Weekend dessert runs","Pre-order cookies, brownies or a whole bake and choose pickup when you are already heading toward San Fernando."),("Family sharing","Boxes and whole bakes are practical for family gatherings where several people want to share."),("Gifts by courier","Send the recipient’s Mabalacat destination in the order request so delivery feasibility can be checked before payment.")],
      "faq_extra":("Do you have a Bale Bella branch in Mabalacat City?","No. Bale Bella is a home-based bakery in Dela Paz Sur, City of San Fernando. Mabalacat City is a delivery-request service area, not a separate branch.")
    },
    {
      "slug":"mexico-pampanga","name":"Mexico","full":"Mexico, Pampanga","schema":"AdministrativeArea","class":"area-mexico",
      "title":"Bakery Delivery Mexico, Pampanga | Bale Bella Bakehouse",
      "desc":"Request cookies, brownies, banana loaf, Basque cheesecake and dessert boxes from Bale Bella for Mexico, Pampanga, subject to courier availability and fee.",
      "keywords":"bakery delivery Mexico Pampanga, cookie delivery Mexico Pampanga, dessert delivery Mexico Pampanga, cheesecake Mexico Pampanga, dessert boxes Mexico Pampanga, Bale Bella Mexico",
      "lede":"Customers in Mexico, Pampanga can request Bale Bella delivery for small-batch cookies, brownies, banana loaf, Basque cheesecake and giftable dessert boxes from our San Fernando home bakehouse.",
      "route":"If you prefer pickup, route toward our Dela Paz Sur address in the City of San Fernando using live navigation. Starting points across Mexico can produce different recommended roads, so the Google Maps link is the best source for current turn-by-turn directions.",
      "ideas":[("Merienda boxes","Cookies and brownies are convenient for family merienda, meetings and casual sharing."),("Special-occasion bakes","A whole Basque cheesecake or banana loaf can be reserved ahead for planned occasions."),("Gift deliveries","For gifts, include the recipient name, delivery destination and message so we can review the request before confirming.")],
      "faq_extra":("Can I request a gift delivery to Mexico, Pampanga?","Yes. Choose Gift in the order form, add the recipient and destination details, and send the request through Messenger. Delivery remains subject to confirmation.")
    },
    {
      "slug":"bacolor-pampanga","name":"Bacolor","full":"Bacolor, Pampanga","schema":"AdministrativeArea","class":"area-bacolor",
      "title":"Bakery Delivery Bacolor, Pampanga | Bale Bella Bakehouse",
      "desc":"Request Bale Bella cookies, brownies, cheesecake, banana loaf and dessert boxes for Bacolor, Pampanga, with delivery confirmed case by case before payment.",
      "keywords":"bakery delivery Bacolor Pampanga, cookie delivery Bacolor, dessert delivery Bacolor Pampanga, cheesecake Bacolor Pampanga, dessert boxes Bacolor, Bale Bella Bacolor",
      "lede":"Bacolor customers can request Bale Bella dessert delivery from our Dela Paz Sur home bakehouse. We confirm the bake slot, exact destination, courier arrangement and fee before payment.",
      "route":"For pickup from Bacolor, navigate toward Dela Paz Sur in the City of San Fernando and use the live route on the day of travel. Traffic and road conditions can change, so we avoid publishing a fixed travel time.",
      "ideas":[("Family celebrations","Choose cookies, brownies or a whole cake-style bake depending on how many people will share."),("Thank-you gifts","Dessert boxes make a simple local gift when you want something prepared in small batches."),("Advance orders","Planning ahead gives us time to confirm both production capacity and the delivery arrangement to Bacolor.")],
      "faq_extra":("Is delivery to Bacolor automatically included in the product price?","No. Product prices do not include a fixed Bacolor delivery fee. Any courier fee is quoted separately after the exact destination is reviewed.")
    },
    {
      "slug":"guagua-pampanga","name":"Guagua","full":"Guagua, Pampanga","schema":"AdministrativeArea","class":"area-guagua",
      "title":"Bakery Delivery Guagua, Pampanga | Bale Bella Bakehouse",
      "desc":"Request Bale Bella cookies, brownies, banana loaf, Basque cheesecake and dessert boxes for Guagua, Pampanga, subject to delivery and bake-slot confirmation.",
      "keywords":"bakery delivery Guagua Pampanga, cookie delivery Guagua, dessert delivery Guagua Pampanga, cheesecake Guagua Pampanga, dessert boxes Guagua, Bale Bella Guagua",
      "lede":"Bale Bella can review courier-delivery requests to Guagua for cookies, brownies, banana loaf, Basque cheesecake and dessert boxes prepared from our San Fernando home bakehouse.",
      "route":"For customers choosing pickup, use live navigation from Guagua to our Dela Paz Sur address in the City of San Fernando. Because route recommendations and traffic can change, the map link is preferable to a fixed set of turn-by-turn instructions.",
      "ideas":[("Planned dessert gifts","Reserve gift boxes ahead and provide the Guagua delivery destination before paying."),("Sharing boxes","Cookie and brownie boxes suit group sharing without requiring a whole cake."),("Whole-bake occasions","Banana loaf and Basque cheesecake are available with longer minimum lead times than most cookies and brownies.")],
      "faq_extra":("How early should I place a Guagua delivery request?","Published minimum lead times still apply: cookies and brownies generally start at one day, while banana loaf, Basque cheesecake and selected boxes generally start at two days. Delivery availability is checked separately.")
    }
]

BAKERY_AREA_SERVED=[
 {"@type":"City","name":"City of San Fernando, Pampanga"},
 {"@type":"Place","name":"Dela Paz Sur / Sindalan, San Fernando, Pampanga"},
 {"@type":"City","name":"Angeles City, Pampanga"},
 {"@type":"City","name":"Mabalacat City, Pampanga"},
 {"@type":"AdministrativeArea","name":"Mexico, Pampanga"},
 {"@type":"AdministrativeArea","name":"Bacolor, Pampanga"},
 {"@type":"AdministrativeArea","name":"Guagua, Pampanga"}
]
OLD_AREA='"areaServed":[{"@type":"City","name":"City of San Fernando, Pampanga"},{"@type":"Place","name":"Dela Paz Sur / Sindalan, San Fernando, Pampanga"}]'
NEW_AREA='"areaServed":'+json.dumps(BAKERY_AREA_SERVED,ensure_ascii=False,separators=(",",":"))

def minjson(obj):
    return json.dumps(obj,ensure_ascii=False,separators=(",",":"))

def social_hub():
    return f'''<section class="social-hub" aria-labelledby="social-hub-title"><div class="wrap"><div class="social-hub-card"><div class="social-hub-copy"><span class="eyebrow">Follow the bakehouse</span><h2 id="social-hub-title">Find Bale Bella everywhere as <span>@balebellabakehouse</span>.</h2><p>Follow fresh bakes, behind-the-scenes moments, menu drops and soft-launch updates across our official social channels.</p></div><nav class="social-hub-links" aria-label="Official Bale Bella social media"><a class="social-hub-link" href="{FB}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">f</span><div><b>Facebook</b><small>Updates &amp; community</small></div></a><a class="social-hub-link" href="{IG}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">◎</span><div><b>Instagram</b><small>Photos, reels &amp; DMs</small></div></a><a class="social-hub-link" href="{YT}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">▶</span><div><b>YouTube</b><small>Bakes &amp; video stories</small></div></a><a class="social-hub-link" href="{TH}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">@</span><div><b>Threads</b><small>Quick updates &amp; conversations</small></div></a><a class="social-hub-link" href="{PIN}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">P</span><div><b>Pinterest</b><small>Inspiration &amp; sweet ideas</small></div></a></nav><p class="social-hub-note">Official handle across platforms: <strong>@balebellabakehouse</strong> · Orders are handled primarily through <a href="{MSG}" target="_blank" rel="noopener noreferrer">Facebook Messenger</a>, with Instagram DM as the secondary option.</p></div></div></section>'''

def bakery_node():
    return {"@type":"Bakery","@id":BASE+"#bakery","name":"Bale Bella Bakehouse","alternateName":"Bale Bella Bakehouse EST 2026","url":BASE,"logo":BASE+"logo.svg","image":BASE+"bale-bella-social-share.png","description":"Family-run, home-based bakery in Dela Paz Sur, City of San Fernando, Pampanga offering small-batch cookies, brownies, banana loaf, Basque cheesecake, dessert boxes, gifts and corporate dessert orders.","foundingDate":"2026","slogan":"From our bale to yours.","priceRange":"₱85–₱799","currenciesAccepted":"PHP","paymentAccepted":"GCash, Bank transfer, Cash on pickup","address":{"@type":"PostalAddress","streetAddress":"Block 14, Lot 4, Abigail Street, Madonna Residences","addressLocality":"City of San Fernando","addressRegion":"Pampanga","postalCode":"2000","addressCountry":"PH"},"areaServed":BAKERY_AREA_SERVED,"hasMap":"https://www.google.com/maps/search/?api=1&query="+quote_plus(PICKUP),"menu":BASE+"menu/","servesCuisine":["Bakery","Desserts","Cookies","Brownies","Cheesecake"],"sameAs":SOCIALS,"contactPoint":{"@type":"ContactPoint","url":MSG,"contactType":"customer service and orders","availableLanguage":["English","Filipino"]},"potentialAction":{"@type":"OrderAction","target":{"@type":"EntryPoint","urlTemplate":BASE+"#order"}}}

def website_node():
    return {"@type":"WebSite","@id":BASE+"#website","url":BASE,"name":"Bale Bella Bakehouse","inLanguage":"en-PH","publisher":{"@id":BASE+"#bakery"}}

def head(title,desc,keywords,canonical,placename):
    return f'''<!-- Author: Johnpel Quingua <johnpelquingua@gmail.com> -->
<!doctype html><html lang="en-PH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#e9f1ec"><meta http-equiv="Content-Security-Policy" content="default-src &#x27;self&#x27;; script-src &#x27;self&#x27;; style-src &#x27;self&#x27; &#x27;unsafe-inline&#x27;; img-src &#x27;self&#x27; data:; font-src &#x27;self&#x27; data:; connect-src &#x27;self&#x27;; frame-src https://www.google.com https://maps.google.com; object-src &#x27;none&#x27;; base-uri &#x27;self&#x27;; form-action &#x27;self&#x27;; media-src &#x27;self&#x27;; worker-src &#x27;none&#x27;; manifest-src &#x27;self&#x27;; upgrade-insecure-requests; block-all-mixed-content"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="format-detection" content="telephone=no"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta name="googlebot" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta name="bingbot" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="author" content="Bale Bella Bakehouse"><meta name="geo.region" content="PH-PAM"><meta name="geo.placename" content="{placename}"><meta name="keywords" content="{keywords}"><link rel="canonical" href="{canonical}"><link rel="describedby" href="{BASE}llms.txt" type="text/markdown">{SOCIAL_REL}<link rel="alternate" hreflang="en-PH" href="{canonical}"><link rel="alternate" hreflang="x-default" href="{canonical}"><link rel="icon" href="/logo.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="Bale Bella Bakehouse"><meta property="og:locale" content="en_PH"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}bale-bella-social-share.png?v=1"><meta property="og:image:secure_url" content="{BASE}bale-bella-social-share.png?v=1"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Bale Bella Bakehouse logo on a warm cream background with the tagline From our bale to yours."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{BASE}bale-bella-social-share.png?v=1"><meta name="twitter:image:alt" content="Bale Bella Bakehouse logo on a warm cream background with the tagline From our bale to yours.">'''

def top_nav(service_current=False):
    current=' aria-current="page"' if service_current else ''
    return f'''<body class="content-page theme-service"><a class="skip-link" href="#main">Skip to main content</a><header><div class="wrap nav"><a class="brand" href="/" aria-label="Bale Bella Bakehouse home"><img src="/logo.svg" alt="Bale Bella Bakehouse logo"><div><strong>Bale Bella Bakehouse</strong><span>San Fernando, Pampanga · EST 2026</span></div></a><nav class="navlinks" aria-label="Main navigation"><a class="pill" href="/menu/">Menu</a><a class="pill" href="/#story">Our Story</a><a class="pill" href="/#location">Location</a><a class="pill" href="/blog/">Blog</a><a class="pill cart-link" href="/#order">Order</a></nav></div><div class="soft-launch-banner" role="status">SOFT LAUNCH ✦ Delivery to listed Pampanga service areas is confirmed case by case before payment.</div></header><div class="section-nav-shell"><div class="wrap"><nav class="section-nav" aria-label="Browse Bale Bella"><a href="/menu/">Menu Guide</a><a href="/cookies/">Cookies</a><a href="/brownies/">Brownies</a><a href="/basque-cheesecake/">Basque Cheesecake</a><a href="/banana-loaf/">Banana Loaf</a><a href="/gift-boxes/">Gift Boxes</a><a href="/corporate-orders/">Corporate</a><a href="/delivery-san-fernando-pampanga/">Pickup & Delivery</a><a href="/service-areas/"{current}>Service Areas</a><a href="/blog/">Journal</a></nav></div></div>'''

def footer():
    return f'''{social_hub()}<footer class="content-footer"><div class="wrap content-footer-grid"><address><strong>Bale Bella Bakehouse</strong><br>{PICKUP}<br><a href="{MSG}" target="_blank" rel="noopener noreferrer">Facebook Messenger</a> · <a href="{FB}" target="_blank" rel="noopener noreferrer">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram @balebellabakehouse</a></address><nav class="footer-links" aria-label="Footer navigation"><a href="/">Home</a><a href="/menu/">Menu Guide</a><a href="/cookies/">Cookies</a><a href="/brownies/">Brownies</a><a href="/basque-cheesecake/">Cheesecake</a><a href="/gift-boxes/">Gift Boxes</a><a href="/corporate-orders/">Corporate</a><a href="/delivery-san-fernando-pampanga/">Pickup & Delivery</a><a href="/service-areas/">Service Areas</a><a href="/blog/">Journal</a></nav></div><div class="wrap footer-signoff">© 2026 Bale Bella Bakehouse · Mayumu. Manyaman. Made with Lugud. 🤎</div></footer></body></html>'''

def faq_markup(faqs):
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)

def faq_schema(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def maps_dir(origin):
    return "https://www.google.com/maps/dir/?api=1&origin="+quote_plus(origin+", Philippines")+"&destination="+quote_plus(PICKUP)

def build_city(area):
    slug=area["slug"]; canonical=BASE+"service-areas/"+slug+"/"
    faqs=[
      (f"Does Bale Bella deliver to {area['full']}?",f"You can request courier delivery to {area['full']}. Delivery is not automatic or guaranteed; Bale Bella confirms the exact destination, courier availability, schedule and delivery fee before payment."),
      area["faq_extra"],
      (f"Can I pick up my order instead of having it delivered to {area['name']}?","Yes. All pickup orders are collected from Bale Bella’s home bakehouse in Dela Paz Sur, City of San Fernando, after the pickup schedule is confirmed."),
      ("How is the delivery fee determined?","There is no fixed published delivery fee for this service area. The fee is quoted separately based on the exact destination and the available courier arrangement."),
      ("How far ahead should I order?","Cookies and brownies generally require at least one day of lead time. Banana loaf, Basque cheesecake and selected boxes generally require at least two days. The live order form calculates the earliest date from the items in your cart."),
      ("How do I place and pay for an order?","Build your order on the Bale Bella website, then send the prepared request through Facebook Messenger, our primary order channel. Instagram DM is secondary. Pay by GCash or bank transfer only after we confirm the order and send the official payment details.")
    ]
    schema={"@context":"https://schema.org","@graph":[bakery_node(),website_node(),
      {"@type":"BreadcrumbList","@id":canonical+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Service Areas","item":BASE+"service-areas/"},{"@type":"ListItem","position":3,"name":area["full"],"item":canonical}]},
      {"@type":"WebPage","@id":canonical+"#webpage","url":canonical,"name":area["title"],"description":area["desc"],"isPartOf":{"@id":BASE+"#website"},"about":{"@id":BASE+"#bakery"},"breadcrumb":{"@id":canonical+"#breadcrumb"},"inLanguage":"en-PH","dateModified":TODAY,"keywords":area["keywords"],"mainEntity":{"@id":canonical+"#service"}},
      {"@type":"Service","@id":canonical+"#service","name":"Bale Bella Bakery Delivery Requests for "+area["full"],"serviceType":"Pre-order bakery courier delivery request","provider":{"@id":BASE+"#bakery"},"areaServed":{"@type":area["schema"],"name":area["full"]},"url":canonical,"description":area["desc"]},
      dict(faq_schema(faqs),**{"@id":canonical+"#faq"})
    ]}
    product_cards=''.join(f'<article class="content-card"><span class="mini-label">{label}</span><h3>{label}</h3><p>{copy}</p></article>' for label,copy in area["ideas"])
    related=[x for x in AREAS if x["slug"]!=slug][:3]
    related_cards=''.join(f'<a class="related-card" href="/service-areas/{x["slug"]}/"><span>Service area</span><strong>{x["full"]}</strong><small>See ordering, delivery and pickup guidance for {x["name"]}.</small><b>View area →</b></a>' for x in related)
    html=head(area["title"],area["desc"],area["keywords"],canonical,area["full"])+f'<script type="application/ld+json">{minjson(schema)}</script><link rel="stylesheet" href="/site.css"><link rel="stylesheet" href="/content.css"><script src="/content.js" defer></script></head>'+top_nav(True)
    html+=f'''<main id="main" tabindex="-1"><section class="content-hero {area['class']}"><div class="wrap content-hero-grid"><div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><a href="/service-areas/">Service Areas</a><span aria-hidden="true">›</span><span aria-current="page">{area['full']}</span></nav><span class="content-kicker">Pampanga service area · Delivery by request</span><h1>Bakery Delivery to {area['full']}</h1><p class="content-lede">{area['lede']}</p></div><aside class="content-hero-card"><img src="/logo.svg" alt="Bale Bella Bakehouse"><p><strong>One home bakehouse, not a city branch.</strong><br>Bale Bella bakes in Dela Paz Sur, City of San Fernando. {area['name']} orders are fulfilled by confirmed courier delivery or San Fernando pickup.</p></aside></div></section>
<section class="content-section"><div class="wrap"><div class="intro-split"><div><h2>Can Bale Bella deliver to {area['name']}?</h2><p class="content-intro">Yes, you may send a delivery request for {area['full']}. We review the exact destination together with the bake schedule and available courier before confirming the order. This keeps delivery information accurate without publishing a fixed radius or promising same-day service.</p></div><a class="live-menu-button" href="/#order">Start an order →</a></div><div class="service-coverage-note"><strong>Important:</strong> {area['name']} is a service area, not a Bale Bella branch. Product preparation and pickup remain at our San Fernando home bakehouse.</div>
<section class="process-strip"><div><span>1</span><strong>Choose your bakes</strong><small>Build a cart from the live menu and select your preferred date.</small></div><div><span>2</span><strong>Send the destination</strong><small>Choose Delivery and include the full {area['name']} address or landmark.</small></div><div><span>3</span><strong>Wait for confirmation</strong><small>We confirm the bake slot, courier, delivery fee and final amount in Messenger.</small></div></section>
<h2>What to order for {area['name']}</h2><p class="content-intro">The same Bale Bella menu is available for delivery requests, subject to current availability and the published minimum lead time for each item.</p><div class="content-grid">{product_cards}</div>
<div class="service-product-links"><a href="/cookies/">Cookies</a><a href="/brownies/">Brownies</a><a href="/banana-loaf/">Banana Loaf</a><a href="/basque-cheesecake/">Basque Cheesecake</a><a href="/gift-boxes/">Gift Boxes</a><a href="/corporate-orders/">Corporate Orders</a></div>
<section class="service-route-card"><div><span class="mini-label">Driving directions</span><h2>Picking up from {area['name']}?</h2><p>{area['route']}</p><div class="cta-actions"><a href="{maps_dir(area['full'])}" target="_blank" rel="noopener noreferrer">Open live directions →</a><a class="secondary-action" href="/delivery-san-fernando-pampanga/">See pickup details</a></div></div><address><strong>Pickup destination</strong><br>{PICKUP}</address></section>
<div class="content-grid two"><article class="content-card spotlight-card"><span class="mini-label">Courier delivery</span><h3>Best when you want convenience</h3><p>Send the exact destination before payment. We confirm whether a suitable courier arrangement is available and quote the fee separately.</p></article><article class="content-card"><span class="mini-label">San Fernando pickup</span><h3>Best when you can collect</h3><p>Pickup avoids a courier fee and lets you collect directly from the home bakehouse at the confirmed date and time.</p></article></div>
<section class="content-cta"><div><h2>Ready to request delivery to {area['name']}?</h2><p>Build the order online first so your products, quantities, preferred date and delivery details are complete before you message us.</p></div><div class="cta-actions"><a href="/#order">Build an order</a><a class="secondary-action" href="{MSG}" target="_blank" rel="noopener noreferrer">Message on Messenger</a></div></section>
<section class="faq-block" aria-labelledby="faq-title"><h2 id="faq-title">{area['name']} delivery FAQs</h2><div class="faq-list">{faq_markup(faqs)}</div></section>
<section class="related-block"><h2>Explore other Pampanga service areas</h2><div class="related-grid">{related_cards}</div><p class="content-intro"><a href="/service-areas/">View the complete Bale Bella service-area guide →</a></p></section></div></section></main>'''+footer()
    return html

def build_index():
    canonical=BASE+"service-areas/"
    title="Pampanga Bakery Delivery Service Areas | Bale Bella Bakehouse"
    desc="Explore Bale Bella Bakehouse delivery-request areas across Pampanga, including San Fernando, Angeles, Mabalacat, Mexico, Bacolor and Guagua."
    keywords="bakery delivery Pampanga, dessert delivery Pampanga, cookie delivery Pampanga, cheesecake delivery Pampanga, Bale Bella service areas, dessert boxes Pampanga"
    faqs=[
      ("Which Pampanga areas can currently request Bale Bella delivery?","Bale Bella currently publishes service-area guidance for the City of San Fernando, Angeles City, Mabalacat City, Mexico, Bacolor and Guagua. Every delivery request is still confirmed case by case."),
      ("Does being listed as a service area guarantee delivery?","No. A service-area page means customers in that area may request delivery. Actual fulfillment depends on the exact destination, bake schedule, courier availability and delivery fee."),
      ("Where is the actual Bale Bella Bakehouse location?","Bale Bella is a home-based bakery in Madonna Residences, Barangay Dela Paz Sur, City of San Fernando, Pampanga. There are no separate branches in the other listed service areas."),
      ("Can customers from any service area choose pickup?","Yes. Confirmed pickup is available from the San Fernando home bakehouse. Customers should wait for the confirmed pickup schedule before arriving."),
      ("How do I request delivery?","Build the order on the website, choose Delivery, add the full destination, then send the prepared request through Facebook Messenger. Instagram DM is the secondary communication channel."),
      ("When should I pay?","Pay only after Bale Bella confirms product availability, the schedule, fulfillment method, delivery fee if applicable and the final amount. Official GCash or bank-transfer details are sent in the same official conversation.")
    ]
    itemlist=[{"@type":"ListItem","position":1,"name":"City of San Fernando, Pampanga","url":BASE+"delivery-san-fernando-pampanga/"}]+[{"@type":"ListItem","position":i+2,"name":a["full"],"url":BASE+"service-areas/"+a["slug"]+"/"} for i,a in enumerate(AREAS)]
    schema={"@context":"https://schema.org","@graph":[bakery_node(),website_node(),
      {"@type":"BreadcrumbList","@id":canonical+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Service Areas","item":canonical}]},
      {"@type":["CollectionPage","WebPage"],"@id":canonical+"#webpage","url":canonical,"name":title,"description":desc,"isPartOf":{"@id":BASE+"#website"},"about":{"@id":BASE+"#bakery"},"breadcrumb":{"@id":canonical+"#breadcrumb"},"inLanguage":"en-PH","dateModified":TODAY,"keywords":keywords,"mainEntity":{"@id":canonical+"#areas"}},
      {"@type":"ItemList","@id":canonical+"#areas","name":"Bale Bella Pampanga Service Areas","itemListElement":itemlist},
      {"@type":"Service","@id":canonical+"#service","name":"Bale Bella Pampanga Bakery Delivery Requests","serviceType":"Pre-order bakery courier delivery requests and pickup fulfillment","provider":{"@id":BASE+"#bakery"},"areaServed":BAKERY_AREA_SERVED,"url":canonical,"description":desc},
      dict(faq_schema(faqs),**{"@id":canonical+"#faq"})
    ]}
    cards=f'''<a class="service-area-card home-area" href="/delivery-san-fernando-pampanga/"><span>Home base</span><strong>City of San Fernando</strong><small>Dela Paz Sur pickup plus local delivery requests.</small><b>Pickup &amp; delivery details →</b></a>'''+''.join(f'<a class="service-area-card {a["class"]}" href="/service-areas/{a["slug"]}/"><span>Delivery-request area</span><strong>{a["full"]}</strong><small>City- or municipality-specific ordering, courier and pickup guidance.</small><b>View service area →</b></a>' for a in AREAS)
    html=head(title,desc,keywords,canonical,"Pampanga")+f'<script type="application/ld+json">{minjson(schema)}</script><link rel="stylesheet" href="/site.css"><link rel="stylesheet" href="/content.css"><script src="/content.js" defer></script></head>'+top_nav(True)
    html+=f'''<main id="main" tabindex="-1"><section class="content-hero"><div class="wrap content-hero-grid"><div><nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">›</span><span aria-current="page">Service Areas</span></nav><span class="content-kicker">Pampanga delivery-request guide</span><h1>Bakery Delivery Service Areas in Pampanga</h1><p class="content-lede">Bale Bella is based in San Fernando and accepts delivery requests for selected nearby Pampanga cities and municipalities. Every request is confirmed individually so courier availability, destination and fees stay accurate.</p></div><aside class="content-hero-card"><img src="/logo.svg" alt="Bale Bella Bakehouse"><p><strong>One San Fernando home bakehouse.</strong><br>Our service-area pages explain where customers may request delivery; they do not represent additional Bale Bella branches.</p></aside></div></section>
<section class="content-section"><div class="wrap"><div class="intro-split"><div><h2>Choose your area</h2><p class="content-intro">Use these pages to understand how Bale Bella handles ordering, delivery requests and pickup for your part of Pampanga. If your exact destination is not listed, message us before paying and we can tell you whether a courier arrangement is practical.</p></div><a class="live-menu-button" href="/#order">Build an order →</a></div><div class="service-area-directory">{cards}</div>
<section class="content-note"><strong>No doorway-page shortcuts:</strong> Each service page explains a real fulfillment option, confirms that the bakery itself remains in San Fernando, and avoids promising a fixed delivery radius or branch location.</section>
<h2>How service-area ordering works</h2><section class="process-strip"><div><span>1</span><strong>Choose products</strong><small>Use the live menu for current variants, prices and minimum lead times.</small></div><div><span>2</span><strong>Add the destination</strong><small>Select Delivery and give us the complete address or useful landmark.</small></div><div><span>3</span><strong>Confirm before paying</strong><small>We confirm availability, courier arrangement, delivery fee and final amount in Messenger.</small></div></section>
<div class="content-grid two"><article class="content-card spotlight-card"><span class="mini-label">Pickup option</span><h3>All roads lead back to the San Fernando bakehouse</h3><p>Customers from any listed service area can choose confirmed pickup from Dela Paz Sur instead of courier delivery.</p><a class="card-link" href="/delivery-san-fernando-pampanga/">See pickup address and directions →</a></article><article class="content-card"><span class="mini-label">Delivery option</span><h3>Request first, pay after confirmation</h3><p>Because courier supply and destinations vary, Bale Bella quotes delivery separately. GCash payment should only be sent after we confirm the order and official payment details.</p><a class="card-link" href="/#order">Start the order form →</a></article></div>
<section class="faq-block" aria-labelledby="faq-title"><h2 id="faq-title">Pampanga service-area FAQs</h2><div class="faq-list">{faq_markup(faqs)}</div></section>
<section class="related-block"><h2>Shop before you choose fulfillment</h2><div class="related-grid"><a class="related-card" href="/cookies/"><span>Menu</span><strong>Fresh Cookies</strong><small>See current cookie flavors and box sizes.</small><b>Browse cookies →</b></a><a class="related-card" href="/gift-boxes/"><span>Gifting</span><strong>Dessert &amp; Gift Boxes</strong><small>Explore shareable and gift-ready options.</small><b>Browse gift boxes →</b></a><a class="related-card" href="/corporate-orders/"><span>Business</span><strong>Corporate Orders</strong><small>Plan office treats, client gifts and event requests.</small><b>Corporate ordering →</b></a></div></section></div></section></main>'''+footer()
    return html

# Create the six approved service-area pages.
Path("service-areas").mkdir(exist_ok=True)
(Path("service-areas")/"index.html").write_text(build_index(),encoding="utf-8")
for area in AREAS:
    d=Path("service-areas")/area["slug"]; d.mkdir(parents=True,exist_ok=True)
    (d/"index.html").write_text(build_city(area),encoding="utf-8")

# Strengthen entity consistency on all pre-existing HTML pages.
existing=[p for p in Path(".").rglob("index.html") if ".git" not in p.parts and "service-areas" not in p.parts]
for p in existing:
    text=p.read_text(encoding="utf-8")
    text=text.replace(OLD_AREA,NEW_AREA)
    text=text.replace('"dateModified":"2026-09-22"','"dateModified":"2026-09-23"')
    text=text.replace('<meta property="article:modified_time" content="2026-09-22">','<meta property="article:modified_time" content="2026-09-23">')
    if p.as_posix()!="index.html":
        text=text.replace('<a href="/delivery-san-fernando-pampanga/">Pickup & Delivery</a><a href="/blog/">Journal</a>','<a href="/delivery-san-fernando-pampanga/">Pickup & Delivery</a><a href="/service-areas/">Service Areas</a><a href="/blog/">Journal</a>')
        text=text.replace('<a href="/delivery-san-fernando-pampanga/">Pickup & Delivery</a><a href="/blog/">Journal</a></nav>','<a href="/delivery-san-fernando-pampanga/">Pickup & Delivery</a><a href="/service-areas/">Service Areas</a><a href="/blog/">Journal</a></nav>')
    p.write_text(text,encoding="utf-8")

# Add a meaningful service-area block to the existing San Fernando fulfillment page.
dp=Path("delivery-san-fernando-pampanga/index.html")
dt=dp.read_text(encoding="utf-8")
if 'id="nearby-service-areas"' not in dt:
    marker='<section class="faq-block"'
    block=f'''<section class="related-block" id="nearby-service-areas"><h2>Delivery requests beyond San Fernando</h2><p class="content-intro">Bale Bella also publishes delivery-request guidance for selected nearby Pampanga areas. These are service areas, not additional bakery branches, and every courier arrangement is confirmed before payment.</p><div class="related-grid"><a class="related-card" href="/service-areas/angeles-city-pampanga/"><span>Service area</span><strong>Angeles City</strong><small>Delivery-request and pickup guidance.</small><b>View Angeles →</b></a><a class="related-card" href="/service-areas/mabalacat-city-pampanga/"><span>Service area</span><strong>Mabalacat City</strong><small>Delivery-request and pickup guidance.</small><b>View Mabalacat →</b></a><a class="related-card" href="/service-areas/"><span>Pampanga</span><strong>All Service Areas</strong><small>San Fernando, Angeles, Mabalacat, Mexico, Bacolor and Guagua.</small><b>View all areas →</b></a></div></section>'''
    if marker not in dt:
        raise RuntimeError("Delivery FAQ insertion marker missing")
    dt=dt.replace(marker,block+marker,1)
dp.write_text(dt,encoding="utf-8")

# Add a homepage discovery link without creating a new top-level navigation item.
hp=Path("index.html"); ht=hp.read_text(encoding="utf-8")
needle='Delivery may be arranged in and around San Fernando, subject to courier availability and fee.</span>'
if needle in ht and '/service-areas/' not in ht:
    ht=ht.replace(needle,'Delivery may be arranged in San Fernando and selected Pampanga service areas, subject to courier availability and fee. <a href="/service-areas/">See service areas →</a></span>',1)
elif '/service-areas/' not in ht:
    # Fallback: place a link in the local SEO intro.
    ht=ht.replace('with pre-order pickup and delivery arrangements handled through Facebook Messenger.','with pre-order pickup and delivery arrangements handled through Facebook Messenger. <a href="/service-areas/">See our Pampanga service areas.</a>',1)
hp.write_text(ht,encoding="utf-8")

# Add service-area styling and mobile handling.
cp=Path("content.css"); css=cp.read_text(encoding="utf-8")
if ".theme-service{" not in css:
    css += '''.theme-service{--page-accent:#56756f;--page-accent-strong:#34534d;--page-soft:#e9f1ec;--page-glow:rgba(86,117,111,.18)}.area-angeles{--page-accent:#617b61;--page-accent-strong:#3f5d42;--page-soft:#edf3e8}.area-mabalacat{--page-accent:#52727b;--page-accent-strong:#35545c;--page-soft:#e8f1f2}.area-mexico{--page-accent:#7a6e4f;--page-accent-strong:#5a4d31;--page-soft:#f4efdf}.area-bacolor{--page-accent:#82645c;--page-accent-strong:#60423b;--page-soft:#f3e8e4}.area-guagua{--page-accent:#6d627e;--page-accent-strong:#4f4561;--page-soft:#eeeaf4}.service-area-directory{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:20px 0 34px}.service-area-card{display:flex;flex-direction:column;min-height:210px;padding:22px;border:1px solid var(--line);border-radius:22px;background:linear-gradient(145deg,#fff,var(--page-soft));text-decoration:none;box-shadow:var(--shadow-sm);transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease}.service-area-card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:color-mix(in srgb,var(--page-accent) 35%,var(--line))}.service-area-card span{font-size:.72rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:var(--page-accent)}.service-area-card strong{font:700 1.45rem/1.1 Georgia,"Times New Roman",serif;color:var(--page-accent-strong);margin:10px 0}.service-area-card small{color:var(--muted);line-height:1.55}.service-area-card b{margin-top:auto;padding-top:18px;color:var(--page-accent-strong)}.service-coverage-note{margin:0 0 26px;padding:17px 19px;border-left:4px solid var(--page-accent);border-radius:14px;background:var(--page-soft);color:var(--muted);line-height:1.65}.service-coverage-note strong{color:var(--page-accent-strong)}.service-product-links{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 34px}.service-product-links a{display:inline-flex;padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--page-accent-strong);font-size:.8rem;font-weight:850;text-decoration:none}.service-product-links a:hover{background:var(--page-soft)}.service-route-card{display:grid;grid-template-columns:1.4fr .8fr;gap:24px;align-items:center;margin:36px 0;padding:26px;border:1px solid color-mix(in srgb,var(--page-accent) 25%,var(--line));border-radius:24px;background:linear-gradient(135deg,#fff,var(--page-soft));box-shadow:var(--shadow-sm)}.service-route-card h2{margin:10px 0 8px}.service-route-card p,.service-route-card address{color:var(--muted);line-height:1.7}.service-route-card address{font-style:normal;padding:18px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.78)}.service-route-card address strong{color:var(--page-accent-strong)}@media(max-width:920px){.service-area-directory{grid-template-columns:repeat(2,minmax(0,1fr))}.service-route-card{grid-template-columns:1fr}}@media(max-width:620px){.service-area-directory{grid-template-columns:1fr}.service-area-card{min-height:0}.service-route-card{padding:20px}.service-product-links{gap:6px}}'''
cp.write_text(css,encoding="utf-8")

# Sitemap: preserve the approved page set plus six new URLs.
urls=[
 BASE,
 BASE+"menu/",BASE+"cookies/",BASE+"brownies/",BASE+"basque-cheesecake/",BASE+"banana-loaf/",BASE+"gift-boxes/",BASE+"corporate-orders/",BASE+"delivery-san-fernando-pampanga/",
 BASE+"blog/",BASE+"blog/how-to-store-fresh-baked-cookies/",BASE+"blog/basque-cheesecake-vs-regular-cheesecake/",BASE+"blog/dessert-gift-ideas-san-fernando-pampanga/",
 BASE+"service-areas/"
]+[BASE+"service-areas/"+a["slug"]+"/" for a in AREAS]
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    priority="1.0" if u==BASE else ("0.9" if u in {BASE+"menu/",BASE+"service-areas/"} else "0.8")
    sitemap+=f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
sitemap+='</urlset>\n'
Path("sitemap.xml").write_text(sitemap,encoding="utf-8")

# llms.txt service-area discovery.
lp=Path("llms.txt"); ll=lp.read_text(encoding="utf-8")
if "## Pampanga service areas" not in ll:
    marker="## Established commercial pages"
    block=f'''## Pampanga service areas
Bale Bella is physically based in Dela Paz Sur, City of San Fernando. The following pages describe areas where customers may request courier delivery; they are not separate Bale Bella branches and do not guarantee delivery. Exact destinations, courier availability, schedule and fees are confirmed before payment.

- [Pampanga Service Areas]({BASE}service-areas/): Directory of the currently published delivery-request areas.
- [San Fernando Pickup & Delivery]({BASE}delivery-san-fernando-pampanga/): Home-base pickup details and local delivery guidance.
'''+''.join(f'- [{a["full"]}]({BASE}service-areas/{a["slug"]}/): Delivery-request, pickup and ordering guidance for {a["full"]}.\n' for a in AREAS)+'''
For service-area questions, do not describe these pages as storefronts, branches, guaranteed delivery zones or fixed delivery-radius commitments. The home bakehouse remains in San Fernando.

'''
    if marker not in ll:
        raise RuntimeError("llms commercial marker missing")
    ll=ll.replace(marker,block+marker,1)
ll=ll.replace("- Official Facebook, Messenger and Instagram ordering channels updated: 2026-09-22.","- Official Facebook, Messenger and Instagram ordering channels updated: 2026-09-22.\n- Pampanga service-area directory and five additional delivery-request pages published: 2026-09-23.")
lp.write_text(ll,encoding="utf-8")

# QA before publishing.
errors=[]
all_html=sorted([p for p in Path(".").rglob("index.html") if ".git" not in p.parts])
if len(all_html)!=19:
    errors.append(f"Expected 19 HTML pages after approved expansion, found {len(all_html)}")
for p in all_html:
    text=p.read_text(encoding="utf-8")
    if text.count("<h1")!=1:
        errors.append(f"{p}: expected one H1")
    if "http://" in text:
        errors.append(f"{p}: insecure http URL")
    for u in SOCIALS:
        if u not in text:
            errors.append(f"{p}: missing social URL {u}")
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)
    if not m:
        errors.append(f"{p}: missing JSON-LD")
    else:
        try: json.loads(m.group(1))
        except Exception as exc: errors.append(f"{p}: JSON-LD invalid {exc}")
for area in AREAS:
    p=Path("service-areas")/area["slug"]/"index.html"
    text=p.read_text(encoding="utf-8")
    if len(re.findall(r"<details>",text))<6:
        errors.append(f"{p}: fewer than six visible FAQs")
    for href in ["/#order","/menu/","/blog/","/service-areas/","/delivery-san-fernando-pampanga/"]:
        if f'href="{href}"' not in text:
            errors.append(f"{p}: missing key internal link {href}")
st=Path("sitemap.xml").read_text(encoding="utf-8")
if st.count("<loc>")!=19:
    errors.append("sitemap does not contain exactly 19 URLs")
for u in urls:
    if u not in st: errors.append(f"sitemap missing {u}")
for u in [BASE+"service-areas/"]+[BASE+"service-areas/"+a["slug"]+"/" for a in AREAS]:
    if u not in ll: errors.append(f"llms.txt missing {u}")
if errors:
    print("SERVICE AREA BUILD QA FAILED")
    print("\n".join("- "+e for e in errors))
    sys.exit(1)
print("Built 6 approved service-area pages, updated internal links, entity schema, sitemap, llms.txt and responsive styles.")
print("QA passed for 19 total public HTML pages.")
