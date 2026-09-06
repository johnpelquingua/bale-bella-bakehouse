from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
import html, json, re, sys, urllib.parse, xml.etree.ElementTree as ET

BASE = "https://balebellabakehouse.com/"
EXPECTED = {
    "index.html": BASE,
    "menu/index.html": BASE + "menu/",
    "cookies/index.html": BASE + "cookies/",
    "brownies/index.html": BASE + "brownies/",
    "basque-cheesecake/index.html": BASE + "basque-cheesecake/",
    "banana-loaf/index.html": BASE + "banana-loaf/",
    "gift-boxes/index.html": BASE + "gift-boxes/",
    "corporate-orders/index.html": BASE + "corporate-orders/",
    "delivery-san-fernando-pampanga/index.html": BASE + "delivery-san-fernando-pampanga/",
    "blog/index.html": BASE + "blog/",
    "blog/how-to-store-fresh-baked-cookies/index.html": BASE + "blog/how-to-store-fresh-baked-cookies/",
    "blog/basque-cheesecake-vs-regular-cheesecake/index.html": BASE + "blog/basque-cheesecake-vs-regular-cheesecake/",
    "blog/dessert-gift-ideas-san-fernando-pampanga/index.html": BASE + "blog/dessert-gift-ideas-san-fernando-pampanga/",
}
CONTENT = {k: v for k, v in EXPECTED.items() if k != "index.html"}
REQUIRED_NAV = ["Menu", "Our Story", "Location", "Blog", "Order"]
REQUIRED_TYPES = {
    "menu/index.html": {"Bakery", "WebSite", "BreadcrumbList", "CollectionPage", "WebPage", "Menu", "FAQPage"},
    "cookies/index.html": {"Bakery", "WebSite", "BreadcrumbList", "CollectionPage", "WebPage", "MenuSection", "FAQPage"},
    "brownies/index.html": {"Bakery", "WebSite", "BreadcrumbList", "CollectionPage", "WebPage", "MenuSection", "FAQPage"},
    "basque-cheesecake/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Product", "FAQPage"},
    "banana-loaf/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Product", "FAQPage"},
    "gift-boxes/index.html": {"Bakery", "WebSite", "BreadcrumbList", "CollectionPage", "WebPage", "ItemList", "FAQPage"},
    "corporate-orders/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Service", "FAQPage"},
    "delivery-san-fernando-pampanga/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Service", "FAQPage"},
    "blog/index.html": {"Bakery", "WebSite", "BreadcrumbList", "CollectionPage", "WebPage", "Blog", "FAQPage"},
    "blog/how-to-store-fresh-baked-cookies/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Blog", "BlogPosting", "FAQPage"},
    "blog/basque-cheesecake-vs-regular-cheesecake/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Blog", "BlogPosting", "FAQPage"},
    "blog/dessert-gift-ideas-san-fernando-pampanga/index.html": {"Bakery", "WebSite", "BreadcrumbList", "WebPage", "Blog", "BlogPosting", "FAQPage"},
}

errors = []

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.h1 = 0
        self.meta = []
        self.links = []
        self.scripts = []
        self.in_script = False
        self.script_type = ""
        self.script_src = None
        self.script_buf = []
        self.nav_depth = 0
        self.nav_text = []
        self.current_nav = []
        self.details = []
        self.in_details = False
        self.in_summary = False
        self.in_p = False
        self.detail_q = []
        self.detail_a = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); tag = tag.lower()
        if tag == "title": self.in_title = True
        if tag == "h1": self.h1 += 1
        if tag == "meta": self.meta.append(attrs)
        if tag == "a" and attrs.get("href"): self.links.append((attrs.get("href"), attrs.get("target"), attrs.get("rel", "")))
        if tag == "nav" and attrs.get("aria-label") == "Main navigation":
            self.nav_depth = 1; self.current_nav = []
        elif self.nav_depth:
            self.nav_depth += 1
        if tag == "script":
            self.in_script = True; self.script_type = attrs.get("type", "").lower(); self.script_src = attrs.get("src"); self.script_buf = []
        if tag == "details":
            self.in_details = True; self.detail_q = []; self.detail_a = []
        elif self.in_details and tag == "summary": self.in_summary = True
        elif self.in_details and tag == "p": self.in_p = True
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_script and not self.script_src: self.script_buf.append(data)
        if self.nav_depth: self.current_nav.append(data)
        if self.in_details and self.in_summary: self.detail_q.append(data)
        if self.in_details and self.in_p: self.detail_a.append(data)
    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title": self.in_title = False
        if self.nav_depth:
            self.nav_depth -= 1
            if tag == "nav" and self.nav_depth == 0: self.nav_text = self.current_nav[:]
        if tag == "script" and self.in_script:
            self.scripts.append((self.script_type, self.script_src, "".join(self.script_buf).strip()))
            self.in_script = False; self.script_type = ""; self.script_src = None; self.script_buf = []
        if tag == "summary": self.in_summary = False
        if tag == "p" and self.in_details: self.in_p = False
        if tag == "details" and self.in_details:
            q = " ".join("".join(self.detail_q).split()); a = " ".join("".join(self.detail_a).split())
            if q and a: self.details.append((q, a))
            self.in_details = False; self.in_summary = False; self.in_p = False


def meta(a, *, name=None, prop=None):
    for attrs in a.meta:
        if name and attrs.get("name", "").lower() == name.lower(): return attrs.get("content", "")
        if prop and attrs.get("property", "").lower() == prop.lower(): return attrs.get("content", "")
    return ""


def canonical(text):
    m = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', text, re.I)
    if not m: m = re.search(r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', text, re.I)
    return m.group(1) if m else ""


def hreflang(text, lang):
    for tag in re.findall(r'<link\b[^>]+>', text, re.I):
        if re.search(r'rel=["\']alternate["\']', tag, re.I) and re.search(rf'hreflang=["\']{re.escape(lang)}["\']', tag, re.I):
            m = re.search(r'href=["\']([^"\']+)', tag, re.I)
            return m.group(1) if m else ""
    return ""


def type_set(schema):
    found = set()
    def walk(x):
        if isinstance(x, dict):
            t = x.get("@type")
            if isinstance(t, str): found.add(t)
            elif isinstance(t, list): found.update(v for v in t if isinstance(v, str))
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(schema)
    return found


def graph_has_nested_array(schema):
    graph = schema.get("@graph") if isinstance(schema, dict) else None
    return isinstance(graph, list) and any(isinstance(x, list) for x in graph)


def local_exists(href):
    if href.startswith(("#", "mailto:", "tel:", "javascript:", "https://", "http://", "//")): return True
    path = urllib.parse.urlsplit(href).path
    if not path or path == "/": return Path("index.html").exists()
    p = PurePosixPath(path.lstrip("/"))
    if path.endswith("/"): return Path(p / "index.html").exists()
    return Path(p).exists() or Path(str(p) + "/index.html").exists()

# Freeze established HTML page set: adding a page requires deliberate gate update.
actual_html = {p.as_posix() for p in Path(".").rglob("index.html") if ".git" not in p.parts}
if actual_html != set(EXPECTED):
    errors.append("HTML page freeze mismatch; expected exactly established page set. Added: %s Removed: %s" % (sorted(actual_html-set(EXPECTED)), sorted(set(EXPECTED)-actual_html)))

seen_titles, seen_desc, seen_canon = {}, {}, {}
incoming = {url: 0 for url in EXPECTED.values()}

for file, wanted in CONTENT.items():
    p = Path(file)
    if not p.exists():
        errors.append(f"{file}: missing"); continue
    text = p.read_text(encoding="utf-8")
    a = Audit(); a.feed(text)
    title = " ".join(a.title.split()); desc = meta(a, name="description").strip(); keys = meta(a, name="keywords").strip(); canon = canonical(text)
    if a.h1 != 1: errors.append(f"{file}: expected one H1, found {a.h1}")
    if not (25 <= len(title) <= 70): errors.append(f"{file}: title length {len(title)} outside 25-70")
    if not (120 <= len(desc) <= 190): errors.append(f"{file}: description length {len(desc)} outside 120-190")
    if len([x for x in keys.split(',') if x.strip()]) < 4: errors.append(f"{file}: missing focused keyword set")
    if canon != wanted: errors.append(f"{file}: canonical mismatch {canon!r}")
    if hreflang(text, "en-PH") != wanted or hreflang(text, "x-default") != wanted: errors.append(f"{file}: hreflang mismatch")
    if "index" not in meta(a, name="robots").lower() or "follow" not in meta(a, name="robots").lower(): errors.append(f"{file}: robots is not index,follow")
    if not meta(a, name="googlebot") or not meta(a, name="bingbot"): errors.append(f"{file}: missing googlebot/bingbot directives")
    if meta(a, prop="og:url") != wanted: errors.append(f"{file}: og:url mismatch")
    for req in [("og:title", "prop"), ("og:description", "prop"), ("og:image", "prop"), ("twitter:card", "name"), ("twitter:title", "name"), ("twitter:description", "name"), ("twitter:image", "name")]:
        value = meta(a, prop=req[0]) if req[1] == "prop" else meta(a, name=req[0])
        if not value: errors.append(f"{file}: missing {req[0]}")
    nav = " ".join(" ".join(a.nav_text).split())
    for label in REQUIRED_NAV:
        if label not in nav: errors.append(f"{file}: main nav missing {label}")
    if 'href="/#order"' not in text and "href='/#order'" not in text: errors.append(f"{file}: missing order link")
    if 'href="/menu/"' not in text: errors.append(f"{file}: missing menu link")
    if 'href="/blog/"' not in text: errors.append(f"{file}: missing blog link")
    if "http://" in text.lower(): errors.append(f"{file}: insecure http:// URL")
    for href, target, rel in a.links:
        if not local_exists(href): errors.append(f"{file}: broken local link {href}")
        if target == "_blank" and ("noopener" not in rel or "noreferrer" not in rel): errors.append(f"{file}: target=_blank missing noopener noreferrer on {href}")
        full = urllib.parse.urljoin(BASE, href)
        normalized = full.split('#',1)[0]
        if normalized in incoming and normalized != wanted: incoming[normalized] += 1
    schemas = []
    for stype, src, body in a.scripts:
        if src and src.startswith(("http://", "https://", "//")): errors.append(f"{file}: external JS not self-hosted: {src}")
        if body and stype not in {"application/ld+json", "application/json"}: errors.append(f"{file}: executable inline script")
        if body and stype == "application/ld+json":
            try: schemas.append(json.loads(body))
            except Exception as e: errors.append(f"{file}: invalid JSON-LD: {e}")
    if not schemas: errors.append(f"{file}: missing JSON-LD")
    else:
        schema = schemas[0]
        if graph_has_nested_array(schema): errors.append(f"{file}: nested array found directly in @graph")
        found = type_set(schema)
        missing = REQUIRED_TYPES[file] - found
        if missing: errors.append(f"{file}: schema missing types {sorted(missing)}")
        faq_nodes = []
        def walk(x):
            if isinstance(x, dict):
                if x.get("@type") == "FAQPage": faq_nodes.append(x)
                for v in x.values(): walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(schema)
        if not a.details: errors.append(f"{file}: no visible FAQ details")
        if not faq_nodes: errors.append(f"{file}: missing FAQPage schema")
        elif len(faq_nodes[0].get("mainEntity", [])) != len(a.details): errors.append(f"{file}: FAQ schema/visible FAQ count mismatch")
    for value, seen, label in [(title, seen_titles, "title"), (desc, seen_desc, "description"), (canon, seen_canon, "canonical")]:
        if value in seen: errors.append(f"{file}: duplicate {label} with {seen[value]}")
        else: seen[value] = file

for url, count in incoming.items():
    if url != BASE and count == 0: errors.append(f"orphan page: {url}")

# Sitemap must contain only the fixed established URLs.
try:
    root = ET.parse("sitemap.xml").getroot(); ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {x.text.strip() for x in root.findall("sm:url/sm:loc", ns) if x.text}
    if locs != set(EXPECTED.values()): errors.append(f"sitemap URL set mismatch: missing={sorted(set(EXPECTED.values())-locs)} extra={sorted(locs-set(EXPECTED.values()))}")
except Exception as e:
    errors.append(f"sitemap invalid: {e}")

robots = Path("robots.txt").read_text(encoding="utf-8") if Path("robots.txt").exists() else ""
if BASE + "sitemap.xml" not in robots: errors.append("robots.txt missing production sitemap URL")
llms = Path("llms.txt").read_text(encoding="utf-8") if Path("llms.txt").exists() else ""
for url in CONTENT.values():
    if url not in llms: errors.append(f"llms.txt missing {url}")

if errors:
    print("EXISTING-PAGE SEO QA FAILED")
    for e in errors: print("-", e)
    sys.exit(1)
print(f"Existing-page SEO QA passed for {len(CONTENT)} content pages; page freeze, metadata, schemas, FAQs, links and sitemap are consistent.")
