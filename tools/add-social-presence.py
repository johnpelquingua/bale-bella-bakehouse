from pathlib import Path
import json, re, sys

FB = "https://www.facebook.com/balebellabakehouse"
IG = "https://www.instagram.com/balebellabakehouse/"
YT = "https://www.youtube.com/@balebellabakehouse"
TH = "https://www.threads.com/@balebellabakehouse"
PIN = "https://www.pinterest.com/balebellabakehouse/"
MSG = "https://m.me/balebellabakehouse"
SOCIALS = [FB, IG, YT, TH, PIN]

ROOT = Path(".")
HTMLS = sorted([p for p in ROOT.rglob("index.html") if ".git" not in p.parts])

REL_ME = "".join(f'<link rel="me" href="{u}">' for u in SOCIALS)

SOCIAL_HUB = f'''<section class="social-hub" aria-labelledby="social-hub-title"><div class="wrap"><div class="social-hub-card"><div class="social-hub-copy"><span class="eyebrow">Follow the bakehouse</span><h2 id="social-hub-title">Find Bale Bella everywhere as <span>@balebellabakehouse</span>.</h2><p>Follow fresh bakes, behind-the-scenes moments, menu drops and soft-launch updates across our official social channels.</p></div><nav class="social-hub-links" aria-label="Official Bale Bella social media"><a class="social-hub-link social-facebook" href="{FB}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">f</span><div><b>Facebook</b><small>Updates &amp; community</small></div></a><a class="social-hub-link social-instagram" href="{IG}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">◎</span><div><b>Instagram</b><small>Photos, reels &amp; DMs</small></div></a><a class="social-hub-link social-youtube" href="{YT}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">▶</span><div><b>YouTube</b><small>Bakes &amp; video stories</small></div></a><a class="social-hub-link social-threads" href="{TH}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">@</span><div><b>Threads</b><small>Quick updates &amp; conversations</small></div></a><a class="social-hub-link social-pinterest" href="{PIN}" target="_blank" rel="me noopener noreferrer"><span aria-hidden="true">P</span><div><b>Pinterest</b><small>Inspiration &amp; sweet ideas</small></div></a></nav><p class="social-hub-note">Official handle across platforms: <strong>@balebellabakehouse</strong> · Orders are still handled primarily through <a href="{MSG}" target="_blank" rel="noopener noreferrer">Facebook Messenger</a>, with Instagram DM as the secondary option.</p></div></div></section>'''

CSS = r'''
.social-hub{padding:18px 0 34px}.social-hub-card{position:relative;overflow:hidden;border:1px solid rgba(111,64,39,.14);border-radius:28px;padding:clamp(22px,4vw,38px);background:radial-gradient(circle at top right,rgba(247,210,147,.33),transparent 34%),linear-gradient(145deg,#fffdf8,#f8ecdc);box-shadow:0 18px 50px rgba(91,55,34,.09)}.social-hub-card::after{content:"";position:absolute;width:210px;height:210px;border-radius:50%;right:-90px;bottom:-120px;background:rgba(111,64,39,.06);pointer-events:none}.social-hub-copy{max-width:820px;position:relative;z-index:1}.social-hub-copy h2{margin:9px 0 10px;font-size:clamp(1.65rem,3.1vw,2.7rem);line-height:1.05;color:#5f3724}.social-hub-copy h2 span{color:#8a5b3e}.social-hub-copy p{margin:0;color:#775746;line-height:1.7}.social-hub-links{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:22px;position:relative;z-index:1}.social-hub-link{display:flex;align-items:center;gap:10px;min-width:0;padding:14px;border:1px solid rgba(111,64,39,.13);border-radius:18px;background:rgba(255,255,255,.78);color:#6f4027;text-decoration:none;transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease}.social-hub-link:hover{transform:translateY(-3px);border-color:rgba(111,64,39,.28);box-shadow:0 10px 24px rgba(91,55,34,.09)}.social-hub-link>span{display:grid;place-items:center;width:38px;height:38px;flex:0 0 38px;border-radius:12px;background:#f5e5cf;font-weight:950;font-size:1rem}.social-hub-link>div{display:grid;min-width:0}.social-hub-link b{font-size:.91rem}.social-hub-link small{margin-top:2px;color:#856956;font-size:.71rem;line-height:1.3}.social-hub-note{margin:17px 0 0;padding-top:15px;border-top:1px solid rgba(111,64,39,.11);color:#775746;font-size:.83rem;line-height:1.55;position:relative;z-index:1}.social-hub-note a{color:#6f4027;font-weight:900}.content-page .social-hub{padding:24px 0 34px;background:var(--page-soft)}.content-page .social-hub-card{background:linear-gradient(145deg,#fffdf9,color-mix(in srgb,var(--page-soft) 82%,#fff));border-color:color-mix(in srgb,var(--page-accent) 17%,var(--line))}.content-page .social-hub-link>span{background:color-mix(in srgb,var(--page-soft) 80%,#fff)}@media(max-width:1050px){.social-hub-links{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:700px){.social-hub-links{grid-template-columns:1fr 1fr}.social-hub-card{border-radius:22px}.social-hub-link{padding:12px}}@media(max-width:430px){.social-hub-links{grid-template-columns:1fr}}
'''

def save(p, text):
    p.write_text(text, encoding="utf-8")

def update_schema(text):
    pattern = re.compile(r'"sameAs":["https://www\.facebook\.com/balebellabakehouse","https://www\.instagram\.com/balebellabakehouse/"(?:,"[^"]+")*]')
    replacement = '"sameAs":[' + ",".join(json.dumps(u) for u in SOCIALS) + ']'
    text, n = pattern.subn(replacement, text)
    if n == 0:
        raise RuntimeError("Could not find sameAs social array")
    return text

def update_head(text):
    if 'rel="me" href="https://www.youtube.com/@balebellabakehouse"' in text:
        return text
    marker = '<link rel="describedby" href="https://balebellabakehouse.com/llms.txt" type="text/markdown">'
    if marker not in text:
        raise RuntimeError("describedby marker missing")
    return text.replace(marker, marker + REL_ME, 1)

def insert_hub(text, path):
    if 'class="social-hub"' in text:
        return text
    footer = '<footer class="footer">' if path.as_posix() == "index.html" else '<footer class="content-footer">'
    if footer not in text:
        raise RuntimeError(f"footer marker missing in {path}")
    return text.replace(footer, SOCIAL_HUB + footer, 1)

for p in HTMLS:
    text = p.read_text(encoding="utf-8")
    text = update_schema(text)
    text = update_head(text)
    text = insert_hub(text, p)
    save(p, text)

css = Path("site.css").read_text(encoding="utf-8")
if ".social-hub{" not in css:
    css += CSS
save(Path("site.css"), css)

llms = Path("llms.txt").read_text(encoding="utf-8")
if "- Official YouTube:" not in llms:
    anchor = "- Instagram: https://www.instagram.com/balebellabakehouse/"
    addition = anchor + "\n- Official YouTube: " + YT + "\n- Official Threads: " + TH + "\n- Official Pinterest: " + PIN
    if anchor not in llms:
        raise RuntimeError("llms Instagram identity anchor missing")
    llms = llms.replace(anchor, addition, 1)
if "## Official social presence" not in llms:
    marker = "## Ordering and fulfillment"
    social_block = f'''## Official social presence
Bale Bella uses the same handle, @balebellabakehouse, across its established social profiles. The preferred presentation order is Facebook, Instagram, YouTube, Threads, then Pinterest.

- Facebook: {FB}
- Instagram: {IG}
- YouTube: {YT}
- Threads: {TH}
- Pinterest: {PIN}
- Messenger for orders: {MSG}

These profiles support brand discovery, updates, visual content and community presence. Facebook Messenger remains the primary order and customer-communication channel; Instagram DM remains secondary.

'''
    if marker not in llms:
        raise RuntimeError("llms ordering marker missing")
    llms = llms.replace(marker, social_block + marker, 1)
save(Path("llms.txt"), llms)

# QA
errors=[]
if len(HTMLS) != 13:
    errors.append(f"Expected 13 established pages, found {len(HTMLS)}")
for p in HTMLS:
    text=p.read_text(encoding="utf-8")
    if text.count('class="social-hub"') != 1:
        errors.append(f"{p}: social hub count is {text.count('class=\"social-hub\"')}")
    positions=[text.find(u) for u in SOCIALS]
    if any(x < 0 for x in positions):
        errors.append(f"{p}: one or more official social URLs missing")
    social_idx=text.find('class="social-hub-links"')
    if social_idx>=0:
        segment=text[social_idx:social_idx+5000]
        order=[segment.find(u) for u in SOCIALS]
        if any(x < 0 for x in order) or order != sorted(order):
            errors.append(f"{p}: social hub order is not Facebook, Instagram, YouTube, Threads, Pinterest")
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)
    if not m:
        errors.append(f"{p}: missing JSON-LD")
    else:
        try:
            data=json.loads(m.group(1))
            found=[]
            def walk(obj):
                if isinstance(obj, dict):
                    if isinstance(obj.get("sameAs"), list):
                        found.append(obj["sameAs"])
                    for value in obj.values():
                        walk(value)
                elif isinstance(obj, list):
                    for value in obj:
                        walk(value)
            walk(data)
            if SOCIALS not in found:
                errors.append(f"{p}: sameAs does not contain full official social set in required order")
        except Exception as exc:
            errors.append(f"{p}: invalid JSON-LD: {exc}")

ll=Path("llms.txt").read_text(encoding="utf-8")
for u in SOCIALS:
    if u not in ll:
        errors.append(f"llms.txt missing {u}")

if errors:
    print("SOCIAL PRESENCE QA FAILED")
    for e in errors: print("-",e)
    sys.exit(1)

print("Added official Facebook, Instagram, YouTube, Threads and Pinterest presence to all 13 established pages.")
print("No new public page was created.")
