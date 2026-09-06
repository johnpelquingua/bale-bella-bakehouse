from pathlib import Path
import re

INDEX = Path('index.html')
html = INDEX.read_text(encoding='utf-8')

# --- 1) Externalize inline CSS so script policy can be stricter without breaking layout.
style_match = re.search(r'<style>(.*?)</style>', html, flags=re.S | re.I)
if style_match:
    css = style_match.group(1).strip() + '\n'
    Path('site.css').write_text(css, encoding='utf-8')
    html = html[:style_match.start()] + '<link rel="stylesheet" href="site.css">\n' + html[style_match.end():]

# --- 2) Externalize the executable inline JavaScript. Keep JSON-LD inline for SEO.
script_pattern = re.compile(r'<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>', flags=re.S | re.I)
extracted_js = None
parts = []
last = 0
for match in script_pattern.finditer(html):
    attrs = match.group('attrs') or ''
    body = match.group('body') or ''
    lower_attrs = attrs.lower()
    parts.append(html[last:match.start()])
    if 'application/ld+json' in lower_attrs or 'src=' in lower_attrs:
        parts.append(match.group(0))
    elif body.strip():
        # This app has one executable inline script. If there are several, concatenate safely.
        extracted_js = ((extracted_js + '\n\n') if extracted_js else '') + body.strip()
        parts.append('<script src="site.js" defer></script>')
    else:
        parts.append(match.group(0))
    last = match.end()
parts.append(html[last:])
html = ''.join(parts)

if extracted_js:
    # Anti-clickjacking fallback for static hosting where response headers are limited.
    hardening_prefix = '''"use strict";\n\n// Static-site clickjacking fallback. A future Cloudflare deployment should also send\n// Content-Security-Policy: frame-ancestors 'none' and X-Frame-Options: DENY as HTTP headers.\ntry {\n  if (window.top !== window.self) {\n    window.top.location = window.self.location.href;\n  }\n} catch (_) {\n  document.documentElement.style.display = "none";\n}\n\n'''
    # Constrain customer-controlled fields before any order is built.
    hardening_suffix = '''\n\n// Defensive limits for public form fields. These reduce accidental or abusive oversized submissions.\ndocument.addEventListener("DOMContentLoaded", () => {\n  const limits = {\n    customerName: 80, customerPhone: 24, address: 240, notes: 600,\n    recipientName: 80, giftMessage: 180, companyName: 120, corporateNotes: 400\n  };\n  Object.entries(limits).forEach(([id, max]) => {\n    const el = document.getElementById(id);\n    if (el && !el.hasAttribute("maxlength")) el.setAttribute("maxlength", String(max));\n  });\n});\n'''
    Path('site.js').write_text(hardening_prefix + extracted_js + hardening_suffix, encoding='utf-8')

# --- 3) Browser security policy suitable for GitHub Pages.
# Note: style-src retains unsafe-inline because the app uses dynamic inline style transforms for animation.
# Executable scripts are restricted to same-origin files only.
security_meta = '''\n<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; frame-src https://www.google.com https://maps.google.com; object-src 'none'; base-uri 'self'; form-action 'self'; media-src 'self'; worker-src 'none'; manifest-src 'self'; upgrade-insecure-requests; block-all-mixed-content">\n<meta name="referrer" content="strict-origin-when-cross-origin">\n<meta name="format-detection" content="telephone=no">\n'''
if 'http-equiv="Content-Security-Policy"' not in html:
    html = html.replace('<meta name="theme-color" content="#fbf6ed">', '<meta name="theme-color" content="#fbf6ed">' + security_meta, 1)

# --- 4) Add an authenticity / anti-fraud notice near the footer if missing.
auth_notice = '''\n<section class="authenticity" aria-label="Official Bale Bella ordering notice"><div class="wrap"><div class="authenticity-card"><div><strong>Official Bale Bella ordering website</strong><p>For your protection, orders and payment instructions are confirmed only through Bale Bella Bakehouse at <a href="https://wa.me/639171344775" target="_blank" rel="noopener noreferrer">0917 134 4775</a>. We will never ask you to send payment to an unrelated number or account.</p></div><span aria-hidden="true">🔒</span></div></div></section>\n'''
if 'Official Bale Bella ordering website' not in html:
    footer_pos = html.lower().find('<footer')
    if footer_pos != -1:
        html = html[:footer_pos] + auth_notice + html[footer_pos:]

# Add styles for authenticity notice to external stylesheet.
css_path = Path('site.css')
if css_path.exists():
    css = css_path.read_text(encoding='utf-8')
    if '.authenticity-card' not in css:
        css += '''\n.authenticity{padding:18px 0 36px}.authenticity-card{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;padding:16px 18px;border:1px solid #dce9dc;background:#f5faf5;border-radius:18px;color:#4d6654}.authenticity-card strong{display:block;color:var(--cocoa);margin-bottom:4px}.authenticity-card p{margin:0;line-height:1.55;font-size:.82rem}.authenticity-card a{color:var(--cocoa);font-weight:900;text-decoration:none}.authenticity-card>span{font-size:1.35rem}@media(max-width:650px){.authenticity-card{padding:14px}.authenticity-card>span{display:none}}\n'''
        css_path.write_text(css, encoding='utf-8')

INDEX.write_text(html, encoding='utf-8')

# --- 5) Repository security / ownership / secret hygiene files.
Path('.github').mkdir(exist_ok=True)
Path('.github/CODEOWNERS').write_text('* @johnpelquingua\n', encoding='utf-8')

Path('SECURITY.md').write_text('''# Security Policy\n\n## Supported site\n\nThe only official Bale Bella Bakehouse ordering site for this repository is:\n\nhttps://johnpelquingua.github.io/bale-bella-bakehouse/\n\n## Reporting a security issue\n\nPlease do **not** post exploitable security details in a public GitHub issue. Contact Bale Bella Bakehouse through the official WhatsApp number **0917 134 4775** and state that the message is a security report.\n\nUseful reports include unauthorized content changes, malicious redirects, impersonation, payment-number tampering, cross-site scripting, exposed credentials, or vulnerabilities that could affect customer order information.\n\n## Payment safety\n\nBale Bella confirms payment instructions only through the official WhatsApp number above. Never trust a different payment number merely because it appears in a screenshot, forwarded message, third-party post, or copied website.\n''', encoding='utf-8')

Path('.gitignore').write_text('''# Secrets and local configuration\n.env\n.env.*\n!.env.example\n*.pem\n*.key\n*.p12\n*.pfx\n*.crt\n*.cer\nsecrets.*\ncredentials.*\n\n# Local / tooling\n.DS_Store\nThumbs.db\nnode_modules/\n__pycache__/\n*.pyc\n.vscode/\n.idea/\n''', encoding='utf-8')

Path('.well-known').mkdir(exist_ok=True)
Path('.well-known/security.txt').write_text('''Contact: https://wa.me/639171344775\nExpires: 2027-09-06T23:59:59+08:00\nPreferred-Languages: en, fil\nCanonical: https://johnpelquingua.github.io/bale-bella-bakehouse/.well-known/security.txt\nPolicy: https://github.com/johnpelquingua/bale-bella-bakehouse/security/policy\n''', encoding='utf-8')

Path('.nojekyll').write_text('', encoding='utf-8')
