from pathlib import Path
import html, json, re

BASE = "https://balebellabakehouse.com/"
DATE = "2026-09-06"
SOCIAL = BASE + "bale-bella-social-share.png"
ORDER = BASE + "#order"
MENU = BASE + "menu/"

PAGES = {
    "menu/index.html": {
        "canonical": BASE + "menu/",
        "title": "Bakery Menu in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Browse Bale Bella Bakehouse cookies, brownies, banana loaf, Basque cheesecake and dessert boxes in San Fernando, Pampanga, with soft-launch prices and ordering details.",
        "keywords": "bakery menu San Fernando Pampanga, Bale Bella Bakehouse menu, cookies San Fernando Pampanga, brownies Pampanga, Basque cheesecake San Fernando, dessert boxes Pampanga",
        "h1": "Bale Bella Bakehouse Menu in San Fernando, Pampanga",
        "kind": "menu",
        "theme": "theme-menu",
        "breadcrumbs": [("Home", BASE), ("Menu Guide", BASE + "menu/")],
    },
    "cookies/index.html": {
        "canonical": BASE + "cookies/",
        "title": "Fresh Cookies in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Order fresh small-batch cookies in San Fernando, Pampanga from Bale Bella Bakehouse, with brown butter, tablea, ube-cheese and Biscoff flavors in singles and boxes.",
        "keywords": "cookies San Fernando Pampanga, fresh cookies Pampanga, cookie boxes San Fernando, brown butter cookies Pampanga, tablea cookies, ube cheese cookies, Biscoff cookies",
        "h1": "Fresh Cookies in San Fernando, Pampanga",
        "kind": "cookies",
        "theme": "theme-cookies",
        "breadcrumbs": [("Home", BASE), ("Menu Guide", BASE + "menu/"), ("Cookies", BASE + "cookies/")],
    },
    "brownies/index.html": {
        "canonical": BASE + "brownies/",
        "title": "Fudgy Brownies in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Order fudgy brownies in San Fernando, Pampanga from Bale Bella Bakehouse, including Manyaman Brownie and Tablea After Dark in singles and shareable boxes.",
        "keywords": "brownies San Fernando Pampanga, fudgy brownies Pampanga, chocolate brownies San Fernando, tablea brownies Pampanga, brownie boxes San Fernando",
        "h1": "Fudgy Brownies in San Fernando, Pampanga",
        "kind": "brownies",
        "theme": "theme-brownies",
        "breadcrumbs": [("Home", BASE), ("Menu Guide", BASE + "menu/"), ("Brownies", BASE + "brownies/")],
    },
    "basque-cheesecake/index.html": {
        "canonical": BASE + "basque-cheesecake/",
        "title": "Basque Cheesecake in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Pre-order Kaluguran Basque cheesecake in San Fernando, Pampanga from Bale Bella Bakehouse: a 15 cm whole cake with a caramelised top and creamy centre.",
        "keywords": "Basque cheesecake San Fernando Pampanga, cheesecake Pampanga, burnt Basque cheesecake San Fernando, Kaluguran Basque, whole cheesecake Pampanga",
        "h1": "Basque Cheesecake in San Fernando, Pampanga",
        "kind": "cheesecake",
        "theme": "theme-cheesecake",
        "breadcrumbs": [("Home", BASE), ("Menu Guide", BASE + "menu/"), ("Basque Cheesecake", BASE + "basque-cheesecake/")],
    },
    "banana-loaf/index.html": {
        "canonical": BASE + "banana-loaf/",
        "title": "Banana Loaf in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Pre-order Bella's Banana Loaf in San Fernando, Pampanga: a whole brown-butter banana loaf with chocolate chunks from Bale Bella Bakehouse.",
        "keywords": "banana loaf San Fernando Pampanga, banana bread Pampanga, brown butter banana loaf, chocolate banana loaf San Fernando, Bale Bella banana loaf",
        "h1": "Banana Loaf in San Fernando, Pampanga",
        "kind": "banana",
        "theme": "theme-banana",
        "breadcrumbs": [("Home", BASE), ("Menu Guide", BASE + "menu/"), ("Banana Loaf", BASE + "banana-loaf/")],
    },
    "gift-boxes/index.html": {
        "canonical": BASE + "gift-boxes/",
        "title": "Dessert & Gift Boxes in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Order dessert and gift boxes in San Fernando, Pampanga from Bale Bella Bakehouse, including cookie boxes, brownie boxes and the Bale Bella Taste Box.",
        "keywords": "dessert boxes San Fernando Pampanga, gift boxes Pampanga, cookie gift boxes San Fernando, brownie boxes Pampanga, dessert gifts San Fernando, Bale Bella Taste Box",
        "h1": "Dessert & Gift Boxes in San Fernando, Pampanga",
        "kind": "gifts",
        "theme": "theme-gifts",
        "breadcrumbs": [("Home", BASE), ("Menu Guide", BASE + "menu/"), ("Gift Boxes", BASE + "gift-boxes/")],
    },
    "corporate-orders/index.html": {
        "canonical": BASE + "corporate-orders/",
        "title": "Corporate Dessert Orders in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "Plan corporate dessert boxes, office treats, client gifts and event orders with Bale Bella Bakehouse in San Fernando, Pampanga, subject to small-batch capacity.",
        "keywords": "corporate dessert orders San Fernando Pampanga, corporate gift boxes Pampanga, office treats San Fernando, client gifts Pampanga, event dessert boxes Pampanga",
        "h1": "Corporate Dessert Orders in San Fernando, Pampanga",
        "kind": "corporate",
        "theme": "theme-corporate",
        "breadcrumbs": [("Home", BASE), ("Corporate Orders", BASE + "corporate-orders/")],
    },
    "delivery-san-fernando-pampanga/index.html": {
        "canonical": BASE + "delivery-san-fernando-pampanga/",
        "title": "Bakery Pickup & Delivery in San Fernando, Pampanga | Bale Bella Bakehouse",
        "description": "See Bale Bella Bakehouse pickup details in Dela Paz Sur and delivery arrangements in and around San Fernando, Pampanga, subject to courier availability and fee.",
        "keywords": "bakery delivery San Fernando Pampanga, cookie delivery San Fernando, dessert delivery Pampanga, bakery pickup Dela Paz Sur, Bale Bella delivery, home bakery San Fernando",
        "h1": "Bakery Pickup & Delivery in San Fernando, Pampanga",
        "kind": "delivery",
        "theme": "theme-delivery",
        "breadcrumbs": [("Home", BASE), ("Pickup & Delivery", BASE + "delivery-san-fernando-pampanga/")],
    },
    "blog/index.html": {
        "canonical": BASE + "blog/",
        "title": "Bale Bella Journal | Baking Guides & Dessert Ideas in Pampanga",
        "description": "Read Bale Bella Bakehouse guides about cookies, Basque cheesecake, dessert gifting and fresh-bake care, written for dessert lovers in San Fernando, Pampanga.",
        "keywords": "Bale Bella Journal, baking guides Pampanga, dessert ideas San Fernando, cookie storage guide, Basque cheesecake guide, dessert gift ideas Pampanga",
        "h1": "Baking Guides & Dessert Ideas from San Fernando, Pampanga",
        "kind": "blog",
        "theme": "theme-journal",
        "breadcrumbs": [("Home", BASE), ("Journal", BASE + "blog/")],
    },
    "blog/how-to-store-fresh-baked-cookies/index.html": {
        "canonical": BASE + "blog/how-to-store-fresh-baked-cookies/",
        "title": "How to Store Fresh-Baked Cookies | Bale Bella Journal",
        "description": "Learn how to store fresh-baked cookies so they stay enjoyable, including cooling, airtight storage, separating textures, freezing and gentle reheating tips.",
        "keywords": "how to store fresh baked cookies, keep cookies soft, cookie storage tips, freeze cookies, reheat cookies, Bale Bella cookie guide",
        "h1": "How to Store Fresh-Baked Cookies",
        "kind": "article",
        "theme": "theme-cookies",
        "section": "Cookie care",
        "tags": ["cookie storage", "fresh-baked cookies", "cookie care", "baking tips"],
        "about": ["Cookies", "Food storage", "Baking"],
        "breadcrumbs": [("Home", BASE), ("Journal", BASE + "blog/"), ("Cookie Storage Guide", BASE + "blog/how-to-store-fresh-baked-cookies/")],
    },
    "blog/basque-cheesecake-vs-regular-cheesecake/index.html": {
        "canonical": BASE + "blog/basque-cheesecake-vs-regular-cheesecake/",
        "title": "Basque Cheesecake vs Regular Cheesecake | Bale Bella Journal",
        "description": "Compare Basque cheesecake vs regular cheesecake by crust, caramelisation, texture, baking style and serving experience, with a guide to choosing between them.",
        "keywords": "Basque cheesecake vs regular cheesecake, Basque cheesecake difference, burnt cheesecake vs cheesecake, cheesecake texture guide, Bale Bella cheesecake guide",
        "h1": "Basque Cheesecake vs Regular Cheesecake",
        "kind": "article",
        "theme": "theme-cheesecake",
        "section": "Cheesecake guide",
        "tags": ["Basque cheesecake", "cheesecake comparison", "dessert guide", "Kaluguran Basque"],
        "about": ["Basque cheesecake", "Cheesecake", "Baking"],
        "breadcrumbs": [("Home", BASE), ("Journal", BASE + "blog/"), ("Basque vs Regular Cheesecake", BASE + "blog/basque-cheesecake-vs-regular-cheesecake/")],
    },
    "blog/dessert-gift-ideas-san-fernando-pampanga/index.html": {
        "canonical": BASE + "blog/dessert-gift-ideas-san-fernando-pampanga/",
        "title": "Dessert Gift Ideas in San Fernando, Pampanga | Bale Bella Journal",
        "description": "Compare dessert gift ideas in San Fernando, Pampanga, from cookie and brownie boxes to sampler boxes and Basque cheesecake for birthdays, thank-yous and offices.",
        "keywords": "dessert gift ideas San Fernando Pampanga, food gifts Pampanga, cookie gifts San Fernando, brownie gift box Pampanga, cheesecake gift San Fernando, corporate dessert gifts",
        "h1": "Dessert Gift Ideas in San Fernando, Pampanga",
        "kind": "article",
        "theme": "theme-gifts",
        "section": "Local gifting guide",
        "tags": ["dessert gifts", "San Fernando Pampanga", "gift boxes", "food gifts"],
        "about": ["Dessert gifts", "Gift boxes", "San Fernando Pampanga"],
        "breadcrumbs": [("Home", BASE), ("Journal", BASE + "blog/"), ("Dessert Gift Ideas", BASE + "blog/dessert-gift-ideas-san-fernando-pampanga/")],
    },
}

COOKIE_ITEMS = [
    ("Mayumu Chunk", "Brown butter, dark chocolate chunks and flaky sea salt.", [("Single", 95), ("Box of 4", 360), ("Box of 6", 520)]),
    ("Tablea Trouble", "Deep chocolate cookie with Philippine tablea and dark chocolate.", [("Single", 110), ("Box of 4", 420), ("Box of 6", 610)]),
    ("Ube Keso Please", "Ube cookie with white chocolate and a creamy cheese centre.", [("Single", 115), ("Box of 4", 440), ("Box of 6", 640)]),
    ("Biscoff Ka Pa", "Brown-butter cookie with a gooey Biscoff centre.", [("Single", 120), ("Box of 4", 460), ("Box of 6", 670)]),
]
BROWNIE_ITEMS = [
    ("Manyaman Brownie", "Dense, fudgy dark chocolate brownie with a glossy top.", [("Single", 85), ("Box of 6", 450)]),
    ("Tablea After Dark", "Fudgy brownie with tablea depth and sea salt.", [("Single", 95), ("Box of 6", 520)]),
]


def attr(value):
    return html.escape(str(value), quote=True)


def strip_tags(value):
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def set_title(text, value):
    return re.sub(r"<title>.*?</title>", f"<title>{html.escape(value)}</title>", text, count=1, flags=re.S)


def set_meta_name(text, name, value):
    tag = f'<meta name="{name}" content="{attr(value)}">'
    pat = rf'<meta\s+name=["\']{re.escape(name)}["\'][^>]*>'
    if re.search(pat, text, re.I):
        return re.sub(pat, tag, text, count=1, flags=re.I)
    return text.replace('<link rel="canonical"', tag + '<link rel="canonical"', 1)


def set_meta_prop(text, prop, value):
    tag = f'<meta property="{prop}" content="{attr(value)}">'
    pat = rf'<meta\s+property=["\']{re.escape(prop)}["\'][^>]*>'
    if re.search(pat, text, re.I):
        return re.sub(pat, tag, text, count=1, flags=re.I)
    marker = '<script type="application/ld+json">'
    return text.replace(marker, tag + marker, 1)


def set_theme_color(text, value):
    return set_meta_name(text, "theme-color", value)


def set_h1(text, value):
    return re.sub(r"<h1>.*?</h1>", f"<h1>{html.escape(value)}</h1>", text, count=1, flags=re.S)


def extract_faqs(text):
    pairs = []
    for block in re.findall(r"<details[^>]*>(.*?)</details>", text, re.I | re.S):
        sm = re.search(r"<summary[^>]*>(.*?)</summary>", block, re.I | re.S)
        pm = re.search(r"<p[^>]*>(.*?)</p>", block, re.I | re.S)
        if sm and pm:
            q, a = strip_tags(sm.group(1)), strip_tags(pm.group(1))
            if q and a:
                pairs.append((q, a))
    return pairs


def offer(name, price, url):
    return {
        "@type": "Offer",
        "name": name,
        "price": str(price),
        "priceCurrency": "PHP",
        "availability": "https://schema.org/LimitedAvailability",
        "url": url,
        "seller": {"@id": BASE + "#bakery"},
    }


def menu_item(name, description, variants, url):
    return {
        "@type": "MenuItem",
        "name": name,
        "description": description,
        "offers": [offer(vname, price, url) for vname, price in variants],
    }


def bakery_node():
    return {
        "@type": "Bakery",
        "@id": BASE + "#bakery",
        "name": "Bale Bella Bakehouse",
        "alternateName": "Bale Bella Bakehouse EST 2026",
        "url": BASE,
        "logo": BASE + "logo.svg",
        "image": SOCIAL,
        "telephone": "+639171344775",
        "description": "Family-run, home-based bakery in Dela Paz Sur, City of San Fernando, Pampanga offering small-batch cookies, brownies, banana loaf, Basque cheesecake, dessert boxes, gifts and corporate dessert orders.",
        "foundingDate": "2026",
        "slogan": "From our bale to yours.",
        "priceRange": "₱85–₱799",
        "currenciesAccepted": "PHP",
        "paymentAccepted": "GCash, Bank transfer, Cash on pickup",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Block 14, Lot 4, Abigail Street, Madonna Residences",
            "addressLocality": "City of San Fernando",
            "addressRegion": "Pampanga",
            "postalCode": "2000",
            "addressCountry": "PH",
        },
        "areaServed": [
            {"@type": "City", "name": "City of San Fernando, Pampanga"},
            {"@type": "Place", "name": "Dela Paz Sur / Sindalan, San Fernando, Pampanga"},
        ],
        "hasMap": "https://www.google.com/maps/search/?api=1&query=Block%2014%2C%20Lot%204%2C%20Abigail%20Street%2C%20Madonna%20Residences%2C%20Barangay%20Dela%20Paz%20Sur%2C%20City%20of%20San%20Fernando%2C%20Pampanga%202000%2C%20Philippines",
        "menu": MENU,
        "servesCuisine": ["Bakery", "Desserts", "Cookies", "Brownies", "Cheesecake"],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+639171344775",
            "contactType": "customer service",
            "availableLanguage": ["English", "Filipino"],
        },
        "potentialAction": {
            "@type": "OrderAction",
            "target": {"@type": "EntryPoint", "urlTemplate": ORDER},
        },
    }


def website_node():
    return {
        "@type": "WebSite",
        "@id": BASE + "#website",
        "url": BASE,
        "name": "Bale Bella Bakehouse",
        "inLanguage": "en-PH",
        "publisher": {"@id": BASE + "#bakery"},
    }


def breadcrumb_node(cfg):
    return {
        "@type": "BreadcrumbList",
        "@id": cfg["canonical"] + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(cfg["breadcrumbs"])
        ],
    }


def webpage_node(cfg, main_id):
    ptype = ["CollectionPage", "WebPage"] if cfg["kind"] in {"menu", "cookies", "brownies", "gifts", "blog"} else "WebPage"
    node = {
        "@type": ptype,
        "@id": cfg["canonical"] + "#webpage",
        "url": cfg["canonical"],
        "name": cfg["title"],
        "description": cfg["description"],
        "isPartOf": {"@id": BASE + "#website"},
        "about": {"@id": BASE + "#bakery"},
        "breadcrumb": {"@id": cfg["canonical"] + "#breadcrumb"},
        "inLanguage": "en-PH",
        "dateModified": DATE,
        "keywords": cfg["keywords"],
    }
    if main_id:
        node["mainEntity"] = {"@id": main_id}
    return node


def build_schema(cfg, text):
    graph = [bakery_node(), website_node(), breadcrumb_node(cfg)]
    kind = cfg["kind"]
    main_id = None

    if kind == "menu":
        main_id = cfg["canonical"] + "#menu"
        graph.append({
            "@type": "Menu",
            "@id": main_id,
            "name": "Bale Bella Bakehouse Menu",
            "url": cfg["canonical"],
            "inLanguage": "en-PH",
            "provider": {"@id": BASE + "#bakery"},
            "hasMenuSection": [
                {"@type": "MenuSection", "name": "Cookies", "hasMenuItem": [menu_item(n, d, v, BASE + "cookies/") for n, d, v in COOKIE_ITEMS]},
                {"@type": "MenuSection", "name": "Brownies", "hasMenuItem": [menu_item(n, d, v, BASE + "brownies/") for n, d, v in BROWNIE_ITEMS]},
                {"@type": "MenuSection", "name": "Loaves and Cheesecake", "hasMenuItem": [
                    menu_item("Bella's Banana Loaf", "Brown-butter banana loaf with chocolate chunks.", [("Whole loaf", 365)], BASE + "banana-loaf/"),
                    menu_item("Kaluguran Basque", "15 cm Basque-style cheesecake with a caramelised top and creamy centre.", [("15 cm whole cake", 799)], BASE + "basque-cheesecake/"),
                    menu_item("Bale Bella Taste Box", "Curated sampler for first-timers, gifts and sharing.", [("Taste Box", 549)], BASE + "gift-boxes/"),
                ]},
            ],
        })
    elif kind == "cookies":
        main_id = cfg["canonical"] + "#menu-section"
        graph.append({"@type": "MenuSection", "@id": main_id, "name": "Bale Bella Cookies", "url": cfg["canonical"], "hasMenuItem": [menu_item(n, d, v, cfg["canonical"]) for n, d, v in COOKIE_ITEMS]})
    elif kind == "brownies":
        main_id = cfg["canonical"] + "#menu-section"
        graph.append({"@type": "MenuSection", "@id": main_id, "name": "Bale Bella Brownies", "url": cfg["canonical"], "hasMenuItem": [menu_item(n, d, v, cfg["canonical"]) for n, d, v in BROWNIE_ITEMS]})
    elif kind == "cheesecake":
        main_id = cfg["canonical"] + "#product"
        graph.append({
            "@type": "Product", "@id": main_id, "name": "Kaluguran Basque", "description": "15 cm Basque-style cheesecake with a deeply caramelised top and creamy centre.",
            "brand": {"@type": "Brand", "name": "Bale Bella Bakehouse"}, "category": "Basque cheesecake",
            "offers": offer("15 cm whole cake", 799, ORDER),
        })
    elif kind == "banana":
        main_id = cfg["canonical"] + "#product"
        graph.append({
            "@type": "Product", "@id": main_id, "name": "Bella's Banana Loaf", "description": "Whole brown-butter banana loaf with chocolate chunks.",
            "brand": {"@type": "Brand", "name": "Bale Bella Bakehouse"}, "category": "Banana loaf",
            "offers": offer("Whole loaf", 365, ORDER),
        })
    elif kind == "gifts":
        main_id = cfg["canonical"] + "#gift-options"
        graph.append({
            "@type": "ItemList", "@id": main_id, "name": "Bale Bella Dessert and Gift Box Options",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Cookie Boxes", "url": BASE + "cookies/"},
                {"@type": "ListItem", "position": 2, "name": "Brownie Boxes", "url": BASE + "brownies/"},
                {"@type": "ListItem", "position": 3, "item": menu_item("Bale Bella Taste Box", "Curated sampler for first-timers, gifts and sharing.", [("Taste Box", 549)], cfg["canonical"])},
            ],
        })
    elif kind == "corporate":
        main_id = cfg["canonical"] + "#service"
        graph.append({
            "@type": "Service", "@id": main_id, "name": "Corporate Dessert Orders", "serviceType": "Corporate dessert boxes, office treats, client gifts and event dessert orders",
            "provider": {"@id": BASE + "#bakery"}, "areaServed": {"@type": "City", "name": "City of San Fernando, Pampanga"},
            "url": cfg["canonical"], "description": cfg["description"],
        })
    elif kind == "delivery":
        main_id = cfg["canonical"] + "#service"
        graph.append({
            "@type": "Service", "@id": main_id, "name": "Bale Bella Pickup and Delivery Arrangements", "serviceType": "Pre-order bakery pickup and courier delivery arrangements",
            "provider": {"@id": BASE + "#bakery"}, "areaServed": {"@type": "City", "name": "City of San Fernando, Pampanga"},
            "url": cfg["canonical"], "description": cfg["description"],
        })
    elif kind == "blog":
        main_id = cfg["canonical"] + "#blog"
        posts = [
            ("How to Store Fresh-Baked Cookies", BASE + "blog/how-to-store-fresh-baked-cookies/"),
            ("Basque Cheesecake vs Regular Cheesecake", BASE + "blog/basque-cheesecake-vs-regular-cheesecake/"),
            ("Dessert Gift Ideas in San Fernando, Pampanga", BASE + "blog/dessert-gift-ideas-san-fernando-pampanga/"),
        ]
        graph.append({
            "@type": "Blog", "@id": main_id, "url": cfg["canonical"], "name": "Bale Bella Journal", "description": cfg["description"],
            "publisher": {"@id": BASE + "#bakery"}, "inLanguage": "en-PH",
            "blogPost": [{"@type": "BlogPosting", "headline": title, "url": url, "datePublished": DATE, "dateModified": DATE} for title, url in posts],
        })
    elif kind == "article":
        blog_id = BASE + "blog/#blog"
        graph.append({"@type": "Blog", "@id": blog_id, "url": BASE + "blog/", "name": "Bale Bella Journal", "publisher": {"@id": BASE + "#bakery"}, "inLanguage": "en-PH"})
        main_id = cfg["canonical"] + "#article"
        article_body = re.search(r'<article class="article-body">(.*?)</article>', text, re.S)
        words = len(re.findall(r"\b[\w’'-]+\b", strip_tags(article_body.group(1) if article_body else text)))
        graph.append({
            "@type": "BlogPosting", "@id": main_id, "headline": cfg["h1"], "description": cfg["description"],
            "url": cfg["canonical"], "mainEntityOfPage": {"@id": cfg["canonical"] + "#webpage"},
            "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "Bale Bella Bakehouse", "url": BASE},
            "publisher": {"@id": BASE + "#bakery"}, "image": SOCIAL, "thumbnailUrl": SOCIAL, "isPartOf": {"@id": blog_id},
            "articleSection": cfg["section"], "keywords": cfg["tags"], "about": [{"@type": "Thing", "name": x} for x in cfg["about"]],
            "inLanguage": "en-PH", "wordCount": words,
        })

    graph.insert(3, webpage_node(cfg, main_id))
    faqs = extract_faqs(text)
    if faqs:
        graph.append({
            "@type": "FAQPage", "@id": cfg["canonical"] + "#faq",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
        })
    return {"@context": "https://schema.org", "@graph": graph}


def replace_schema(text, schema):
    payload = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    tag = f'<script type="application/ld+json">{payload}</script>'
    pat = r'<script\s+type=["\']application/ld\+json["\'][^>]*>.*?</script>'
    if re.search(pat, text, re.I | re.S):
        return re.sub(pat, lambda _: tag, text, count=1, flags=re.I | re.S)
    return text.replace('</head>', tag + '</head>', 1)


def article_meta(text, cfg):
    if cfg["kind"] != "article":
        return text
    text = set_meta_prop(text, "article:published_time", DATE)
    text = set_meta_prop(text, "article:modified_time", DATE)
    text = set_meta_prop(text, "article:section", cfg["section"])
    text = re.sub(r'<meta\s+property=["\']article:tag["\'][^>]*>', '', text, flags=re.I)
    tags = ''.join(f'<meta property="article:tag" content="{attr(tag)}">' for tag in cfg["tags"])
    return text.replace('<script type="application/ld+json">', tags + '<script type="application/ld+json">', 1)


def optimize(path, cfg):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    text = set_title(text, cfg["title"])
    text = set_meta_name(text, "description", cfg["description"])
    text = set_meta_name(text, "keywords", cfg["keywords"])
    text = set_meta_name(text, "robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
    text = set_meta_name(text, "googlebot", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
    text = set_meta_name(text, "bingbot", "index,follow,max-image-preview:large,max-snippet:-1")
    text = set_meta_name(text, "author", "Bale Bella Bakehouse")
    text = set_meta_name(text, "geo.region", "PH-PAM")
    text = set_meta_name(text, "geo.placename", "City of San Fernando, Pampanga")
    theme_colors = {"theme-menu":"#fbf6ed","theme-cookies":"#fff0cf","theme-brownies":"#f5e4da","theme-cheesecake":"#fff0c7","theme-banana":"#fff4c9","theme-gifts":"#fae5df","theme-corporate":"#eee7e0","theme-delivery":"#e8f0e6","theme-journal":"#f1e6ee"}
    text = set_theme_color(text, theme_colors[cfg["theme"]])
    text = set_meta_prop(text, "og:type", "article" if cfg["kind"] == "article" else "website")
    text = set_meta_prop(text, "og:site_name", "Bale Bella Bakehouse")
    text = set_meta_prop(text, "og:locale", "en_PH")
    text = set_meta_prop(text, "og:title", cfg["title"])
    text = set_meta_prop(text, "og:description", cfg["description"])
    text = set_meta_prop(text, "og:url", cfg["canonical"])
    text = set_meta_prop(text, "og:image", SOCIAL + "?v=1")
    text = set_meta_prop(text, "og:image:secure_url", SOCIAL + "?v=1")
    text = set_meta_prop(text, "og:image:type", "image/png")
    text = set_meta_prop(text, "og:image:width", "1200")
    text = set_meta_prop(text, "og:image:height", "630")
    text = set_meta_prop(text, "og:image:alt", "Bale Bella Bakehouse logo on a warm cream background with the tagline From our bale to yours.")
    text = set_meta_name(text, "twitter:card", "summary_large_image")
    text = set_meta_name(text, "twitter:title", cfg["title"])
    text = set_meta_name(text, "twitter:description", cfg["description"])
    text = set_meta_name(text, "twitter:image", SOCIAL + "?v=1")
    text = set_meta_name(text, "twitter:image:alt", "Bale Bella Bakehouse logo on a warm cream background with the tagline From our bale to yours.")
    text = set_h1(text, cfg["h1"])
    text = article_meta(text, cfg)
    schema = build_schema(cfg, text)
    text = replace_schema(text, schema)
    p.write_text(text, encoding="utf-8")


for path, cfg in PAGES.items():
    optimize(path, cfg)

# Keep sitemap fixed to the established page set; update lastmod only.
sitemap = Path("sitemap.xml")
if sitemap.exists():
    s = sitemap.read_text(encoding="utf-8")
    s = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{DATE}</lastmod>", s)
    sitemap.write_text(s, encoding="utf-8")

print(f"Optimized {len(PAGES)} existing content pages without creating new pages.")
