from pathlib import Path
import json, re, urllib.parse

INDEX = Path('index.html')
BASE = 'https://johnpelquingua.github.io/bale-bella-bakehouse/'
ADDRESS = 'Block 14, Lot 4, Abigail Street, Madonna Residences, Barangay Dela Paz Sur, City of San Fernando, Pampanga 2000, Philippines'
PHONE_DISPLAY = '0917 134 4775'
PHONE_E164 = '+639171344775'
WA = '639171344775'
MAP_URL = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(ADDRESS)
EMBED_URL = 'https://www.google.com/maps?q=' + urllib.parse.quote_plus(ADDRESS) + '&output=embed'
MARKER = '<!-- SEO-LOCAL-V1 -->'

FAQS = [
    ('Where is Bale Bella Bakehouse located?', 'Bale Bella Bakehouse is a home-based bakery at Block 14, Lot 4, Abigail Street, Madonna Residences, Barangay Dela Paz Sur, City of San Fernando, Pampanga 2000, Philippines. Pre-order pickup details are confirmed through WhatsApp.'),
    ('What can I order from Bale Bella Bakehouse?', 'Our menu includes brown-butter cookies, fudgy brownies, banana loaf, Basque cheesecake and curated sampler boxes. Available flavors, sizes and prices are shown in the menu above.'),
    ('Do you offer pickup and delivery in San Fernando, Pampanga?', 'Yes. Pre-order pickup is available from our Dela Paz Sur location. Delivery may also be arranged in and around San Fernando, Pampanga, subject to courier availability and a separately quoted delivery fee.'),
    ('How do I place an order?', 'Choose your products and box sizes, complete the order form, then send the prepared order request to Bale Bella Bakehouse on WhatsApp. Your order becomes final only after we confirm availability, schedule and the final amount.'),
    ('How far in advance should I order?', 'Cookies and brownies generally require at least one day of lead time. Banana loaves, cheesecakes and selected boxes may require two days or more. The ordering app automatically updates the earliest selectable date based on your cart.'),
    ('When do I pay with GCash?', 'Pay only after Bale Bella Bakehouse confirms your order. We will send the official GCash details in the same WhatsApp conversation. Use your Bale Bella order reference and reply with your payment receipt.'),
    ('Can I order Bale Bella products as gifts or for corporate events?', 'Yes. Choose Gift or Corporate in the order form. You can add a recipient name, gift message, company details, estimated quantity and customization requests such as individual packaging or branded stickers.'),
    ('How do I get driving directions to Bale Bella Bakehouse?', 'Use the Google Maps directions link on this page. From the MacArthur Highway and Sindalan area, head toward Dela Paz Sur and Madonna Residences, which is commonly referenced as being behind Jumbo Jenra, then proceed inside the subdivision to Abigail Street, Block 14, Lot 4.'),
]

schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': ['Bakery', 'LocalBusiness'], '@id': BASE + '#bakery', 'name': 'Bale Bella Bakehouse',
            'alternateName': 'Bale Bella Bakehouse EST 2026', 'url': BASE, 'logo': BASE + 'logo.svg',
            'image': BASE + 'logo.svg', 'telephone': PHONE_E164,
            'description': 'Home-based bakery in Dela Paz Sur, San Fernando, Pampanga offering fresh-baked cookies, brownies, banana loaf, Basque cheesecake, sampler boxes, gift orders and corporate orders.',
            'priceRange': '₱₱', 'currenciesAccepted': 'PHP', 'paymentAccepted': 'GCash, Bank transfer, Cash on pickup',
            'address': {'@type': 'PostalAddress', 'streetAddress': 'Block 14, Lot 4, Abigail Street, Madonna Residences', 'addressLocality': 'City of San Fernando', 'addressRegion': 'Pampanga', 'postalCode': '2000', 'addressCountry': 'PH'},
            'areaServed': [{'@type': 'City', 'name': 'City of San Fernando, Pampanga'}, {'@type': 'Place', 'name': 'Dela Paz Sur / Sindalan, San Fernando, Pampanga'}],
            'hasMap': MAP_URL, 'hasMenu': BASE + '#menu', 'servesCuisine': ['Bakery', 'Desserts', 'Cookies', 'Brownies', 'Cheesecake'],
            'contactPoint': {'@type': 'ContactPoint', 'telephone': PHONE_E164, 'contactType': 'customer service', 'availableLanguage': ['English', 'Filipino']},
            'potentialAction': {'@type': 'OrderAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': BASE + '#order'}},
        },
        {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE, 'name': 'Bale Bella Bakehouse', 'inLanguage': 'en-PH', 'publisher': {'@id': BASE + '#bakery'}},
        {'@type': 'WebPage', '@id': BASE + '#webpage', 'url': BASE, 'name': 'Bale Bella Bakehouse | Bakery in San Fernando, Pampanga', 'description': 'Order fresh cookies, brownies, banana loaf and Basque cheesecake from Bale Bella Bakehouse in Dela Paz Sur, San Fernando, Pampanga. Pickup and delivery available by pre-order.', 'isPartOf': {'@id': BASE + '#website'}, 'about': {'@id': BASE + '#bakery'}, 'inLanguage': 'en-PH'},
        {'@type': 'FAQPage', '@id': BASE + '#faq-schema', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQS]},
        {
            '@type': 'Menu', '@id': BASE + '#menu-schema', 'name': 'Bale Bella Bakehouse Menu', 'url': BASE + '#menu', 'inLanguage': 'en-PH', 'provider': {'@id': BASE + '#bakery'},
            'hasMenuSection': [
                {'@type': 'MenuSection', 'name': 'Cookies', 'hasMenuItem': [
                    {'@type': 'MenuItem', 'name': 'Mayumu Chunk', 'description': 'Brown butter, dark chocolate chunks and flaky sea salt.', 'offers': {'@type': 'Offer', 'price': '95', 'priceCurrency': 'PHP'}},
                    {'@type': 'MenuItem', 'name': 'Tablea Trouble', 'offers': {'@type': 'Offer', 'price': '110', 'priceCurrency': 'PHP'}},
                    {'@type': 'MenuItem', 'name': 'Ube Keso Please', 'offers': {'@type': 'Offer', 'price': '115', 'priceCurrency': 'PHP'}},
                    {'@type': 'MenuItem', 'name': 'Biscoff Ka Pa', 'offers': {'@type': 'Offer', 'price': '120', 'priceCurrency': 'PHP'}},
                ]},
                {'@type': 'MenuSection', 'name': 'Brownies', 'hasMenuItem': [
                    {'@type': 'MenuItem', 'name': 'Manyaman Brownie', 'offers': {'@type': 'Offer', 'price': '85', 'priceCurrency': 'PHP'}},
                    {'@type': 'MenuItem', 'name': 'Tablea After Dark', 'offers': {'@type': 'Offer', 'price': '95', 'priceCurrency': 'PHP'}},
                ]},
                {'@type': 'MenuSection', 'name': 'Loaves and Cheesecake', 'hasMenuItem': [
                    {'@type': 'MenuItem', 'name': "Bella's Banana Loaf", 'offers': {'@type': 'Offer', 'price': '365', 'priceCurrency': 'PHP'}},
                    {'@type': 'MenuItem', 'name': 'Kaluguran Basque', 'offers': {'@type': 'Offer', 'price': '799', 'priceCurrency': 'PHP'}},
                    {'@type': 'MenuItem', 'name': 'Bale Bella Taste Box', 'offers': {'@type': 'Offer', 'price': '549', 'priceCurrency': 'PHP'}},
                ]},
            ],
        },
    ],
}

s = INDEX.read_text(encoding='utf-8')
if MARKER not in s:
    jsonld = json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
    head = f'''{MARKER}\n<!doctype html>\n<html lang="en-PH">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#fbf6ed">\n<title>Bale Bella Bakehouse | Bakery in San Fernando, Pampanga</title>\n<meta name="description" content="Order fresh cookies, brownies, banana loaf and Basque cheesecake from Bale Bella Bakehouse in Dela Paz Sur, San Fernando, Pampanga. Pickup and delivery by pre-order.">\n<meta name="keywords" content="bakery San Fernando Pampanga, cookies San Fernando Pampanga, brownies Pampanga, cheesecake San Fernando, banana bread Pampanga, home bakery San Fernando, Dela Paz Sur bakery, Sindalan bakery, Bale Bella Bakehouse, cookie delivery Pampanga, dessert boxes Pampanga, gift boxes San Fernando Pampanga">\n<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n<meta name="googlebot" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n<meta name="bingbot" content="index,follow">\n<meta name="author" content="Bale Bella Bakehouse">\n<meta name="geo.region" content="PH-PAM">\n<meta name="geo.placename" content="City of San Fernando, Pampanga">\n<link rel="canonical" href="{BASE}">\n<link rel="alternate" hreflang="en-PH" href="{BASE}">\n<link rel="alternate" hreflang="x-default" href="{BASE}">\n<link rel="icon" href="logo.svg" type="image/svg+xml">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="Bale Bella Bakehouse">\n<meta property="og:locale" content="en_PH">\n<meta property="og:title" content="Bale Bella Bakehouse | Fresh Bakes in San Fernando, Pampanga">\n<meta property="og:description" content="Fresh cookies, brownies, banana loaf, Basque cheesecake and gift boxes from Bale Bella Bakehouse in Dela Paz Sur, San Fernando, Pampanga.">\n<meta property="og:url" content="{BASE}">\n<meta property="og:image" content="{BASE}logo.svg">\n<meta property="og:image:alt" content="Bale Bella Bakehouse logo">\n<meta name="twitter:card" content="summary">\n<meta name="twitter:title" content="Bale Bella Bakehouse | San Fernando, Pampanga">\n<meta name="twitter:description" content="Fresh-baked cookies, brownies, banana loaf and Basque cheesecake in San Fernando, Pampanga.">\n<meta name="twitter:image" content="{BASE}logo.svg">\n<script type="application/ld+json">{jsonld}</script>\n'''
    s = head + s[s.index('<style>'):]
    s = s.replace('<h1>Sweet things.<br>Made at home.</h1>', '<h1>Bale Bella Bakehouse.<br><span>Fresh bakes in San Fernando.</span></h1>')
    s = s.replace('Small-batch cookies, fudgy brownies, banana loaves and Basque cheesecake — baked in San Fernando, Pampanga and made for sharing.', 'A home-based bakery in Dela Paz Sur, City of San Fernando, Pampanga serving small-batch cookies, fudgy brownies, banana loaves, Basque cheesecake and giftable dessert boxes.')
    s = s.replace('<div><span class="eyebrow">Our bake menu</span><h2>Pick your happy.</h2></div>', '<div><span class="eyebrow">Fresh bakery menu</span><h2>Fresh Bakes in San Fernando, Pampanga.</h2></div>')
    s = s.replace('<div><span class="eyebrow">Easy ordering</span><h2>Your Bale Bella order.</h2></div>', '<div><span class="eyebrow">Order online</span><h2>Order from Bale Bella Bakehouse.</h2></div>')
    s = s.replace('<div class="section-head reveal"><div><span class="eyebrow">Simple by design</span><h2>How ordering works.</h2></div>', '<div class="section-head reveal"><div><span class="eyebrow">Simple by design</span><h2>How to Order from Bale Bella Bakehouse.</h2></div>')

    css = '''\n/* Local SEO and location */\nh1 span{font-size:.58em;line-height:1.08;color:var(--brown);letter-spacing:-.035em}.local-section{position:relative}.local-grid{display:grid;grid-template-columns:.92fr 1.08fr;gap:22px;align-items:stretch}.nap-card,.directions-card{background:var(--paper);border:1px solid var(--line);border-radius:26px;padding:24px;box-shadow:var(--shadow-sm)}.nap-card address{font-style:normal;color:var(--muted);line-height:1.72;margin-top:14px}.nap-card address strong{color:var(--cocoa);font-size:1.12rem}.nap-card a{color:var(--cocoa);font-weight:850;text-decoration:none}.nap-actions{display:flex;gap:9px;flex-wrap:wrap;margin-top:17px}.nap-actions a{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:11px 14px;border:1px solid var(--line);background:#fff;text-decoration:none;font-weight:900;color:var(--cocoa)}.nap-actions a:first-child{background:var(--cocoa);color:#fff;border-color:var(--cocoa)}.local-points{display:grid;gap:10px;margin-top:18px}.local-point{display:flex;gap:10px;padding:11px 12px;border-radius:15px;background:#fffaf2;border:1px solid #f0e0c7}.local-point b{display:block;color:var(--cocoa);font-size:.82rem}.local-point span{color:var(--muted);font-size:.78rem}.directions-card h3{margin:0 0 11px;color:var(--cocoa)}.direction-list{display:grid;gap:12px;margin:0;padding:0;list-style:none}.direction-list li{padding:12px 13px;border-left:3px solid var(--butter);background:#fffbf4;border-radius:0 14px 14px 0;color:var(--muted);font-size:.86rem;line-height:1.6}.direction-list strong{color:var(--cocoa)}.map-wrap{margin-top:18px;border-radius:20px;overflow:hidden;border:1px solid var(--line);background:#f6efe6;min-height:280px}.map-wrap iframe{display:block;width:100%;height:310px;border:0}.service-note{margin-top:14px;padding:12px 13px;border-radius:14px;background:#f4f8f3;border:1px solid #dce9dc;color:#4d6654;font-size:.8rem;line-height:1.55}.seo-intro{margin-top:22px;padding:18px 20px;border-radius:20px;background:linear-gradient(145deg,#fffaf1,#fffdf9);border:1px solid var(--line);color:var(--muted);line-height:1.72}.seo-intro h3{margin:0 0 7px;color:var(--cocoa)}.footer{padding:35px 0 44px}.footer-inner{align-items:flex-start}.footer-nap{max-width:620px}.footer-nap address{font-style:normal;line-height:1.65}.footer-nap strong{color:var(--cocoa)}@media(max-width:960px){.local-grid{grid-template-columns:1fr}}@media(max-width:650px){h1 span{font-size:.64em}.nap-card,.directions-card{padding:18px}.nap-actions{display:grid}.nap-actions a{width:100%}.map-wrap iframe{height:270px}}\n'''
    s = s.replace('</style>', css + '</style>')

    location = f'''\n<section id="location" class="local-section"><div class="wrap"><div class="section-head reveal"><div><span class="eyebrow">Local pickup · Dela Paz Sur</span><h2>Pickup Location & Driving Directions.</h2></div><p>Bale Bella Bakehouse is a home-based, pre-order bakery in Madonna Residences, Barangay Dela Paz Sur, City of San Fernando, Pampanga.</p></div><div class="local-grid"><article class="nap-card reveal"><span class="eyebrow">NAP · Name, address & phone</span><address><strong>Bale Bella Bakehouse</strong><br>Block 14, Lot 4, Abigail Street<br>Madonna Residences, Barangay Dela Paz Sur<br>City of San Fernando, Pampanga 2000<br>Philippines<br><br>Phone / WhatsApp: <a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a></address><div class="nap-actions"><a href="{MAP_URL}" target="_blank" rel="noopener">📍 Open in Google Maps</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener">💬 Message Bale Bella</a></div><div class="local-points"><div class="local-point"><span>🏠</span><div><b>Home-based bakery</b><span>Pre-order pickup only; pickup time is confirmed in WhatsApp.</span></div></div><div class="local-point"><span>🛵</span><div><b>Local delivery</b><span>Delivery may be arranged in and around San Fernando, subject to courier availability and fee.</span></div></div><div class="local-point"><span>📌</span><div><b>Nearby landmark</b><span>Madonna Residences in Dela Paz Sur / Sindalan is commonly referenced as being behind Jumbo Jenra.</span></div></div></div></article><article class="directions-card reveal"><h3>Driving directions to Bale Bella Bakehouse</h3><ul class="direction-list"><li><strong>From MacArthur Highway / Sindalan:</strong> head toward Dela Paz Sur and the Jumbo Jenra area. Follow the access toward Madonna Residences behind Jumbo Jenra, enter the subdivision, then continue to Abigail Street and proceed to Block 14, Lot 4.</li><li><strong>From San Fernando city proper:</strong> take MacArthur Highway toward Sindalan, then follow signs or navigation toward Madonna Residences in Barangay Dela Paz Sur. Once inside the subdivision, proceed to Abigail Street.</li><li><strong>For the most accurate route:</strong> tap “Open in Google Maps” and follow live turn-by-turn directions, since traffic, road access and subdivision entry conditions can change.</li></ul><div class="map-wrap"><iframe src="{EMBED_URL}" title="Map to Bale Bella Bakehouse in Madonna Residences, San Fernando, Pampanga" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div><div class="service-note"><strong>Pickup reminder:</strong> This is a home-based bakery, so please wait for your confirmed pickup schedule before arriving.</div></article></div><div class="seo-intro reveal"><h3>Home-based bakery in San Fernando, Pampanga</h3>Bale Bella Bakehouse serves customers looking for fresh cookies, brownies, banana loaf, Basque cheesecake, dessert boxes, gift orders and corporate bakes in San Fernando, Pampanga. Our Dela Paz Sur location is convenient for customers around Sindalan and nearby San Fernando communities, with pre-order pickup and delivery arrangements handled through WhatsApp.</div></div></section>\n'''
    s = s.replace('<section id="how">', location + '<section id="how">')

    faq = '<section id="faq"><div class="wrap"><div class="section-head reveal"><div><span class="eyebrow">Bale Bella FAQs</span><h2>Frequently Asked Questions.</h2></div><p>Quick answers about our San Fernando bakery location, ordering, pickup, delivery, lead times and GCash payments.</p></div><div class="faq">' + ''.join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS) + '</div></div></section>'
    s = re.sub(r'<section id="faq">.*?</section>', faq, s, flags=re.S)

    footer = f'''<footer class="footer"><div class="wrap footer-inner"><div class="footer-nap"><address><strong>Bale Bella Bakehouse</strong><br>Block 14, Lot 4, Abigail Street, Madonna Residences, Barangay Dela Paz Sur, City of San Fernando, Pampanga 2000, Philippines<br><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a> · <a href="{MAP_URL}" target="_blank" rel="noopener">Driving directions</a></address></div><div>© 2026 Bale Bella Bakehouse<br>Mayumu. Manyaman. Made with Lugud. 🤎</div></div></footer>'''
    s = re.sub(r'<footer class="footer">.*?</footer>', footer, s, flags=re.S)
    s = s.replace('<a class="pill" href="#how">How it works</a>', '<a class="pill" href="#location">Location</a><a class="pill" href="#how">How it works</a>')
    s = s.replace('<script>\nconst CONFIG=', f'<noscript><div style="padding:16px;text-align:center;background:#fff3d9;color:#6f4027;font-weight:700">JavaScript is required for the interactive cart, but you can still contact Bale Bella Bakehouse at {PHONE_DISPLAY} for orders.</div></noscript>\n<script>\nconst CONFIG=')
    INDEX.write_text(s, encoding='utf-8')
    print('SEO/local landing enhancements applied.')
else:
    print('SEO patch already present; no index changes required.')

Path('robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + 'sitemap.xml\n', encoding='utf-8')
Path('sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>' + BASE + '</loc>\n    <lastmod>2026-09-06</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n</urlset>\n', encoding='utf-8')
