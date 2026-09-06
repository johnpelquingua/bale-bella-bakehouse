from pathlib import Path

INDEX = Path('index.html')
MARKER = '<!-- BALE-BELLA-STORY-V1 -->'

s = INDEX.read_text(encoding='utf-8')
if MARKER in s:
    raise SystemExit(0)

story_css = r'''
/* Bale Bella origin story */
.story-section{position:relative;padding:64px 0 66px;overflow:hidden}.story-shell{position:relative;display:grid;grid-template-columns:.9fr 1.1fr;gap:26px;align-items:stretch;background:linear-gradient(145deg,#fffaf1,#fffdf9);border:1px solid var(--line);border-radius:34px;padding:28px;box-shadow:var(--shadow-sm);overflow:hidden}.story-shell::before{content:"";position:absolute;width:250px;height:250px;border-radius:50%;background:rgba(241,189,91,.15);right:-90px;top:-110px;pointer-events:none}.story-shell::after{content:"";position:absolute;width:190px;height:190px;border-radius:50%;background:rgba(198,141,84,.10);left:-85px;bottom:-95px;pointer-events:none}.story-mark{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:space-between;min-height:310px;padding:26px;border-radius:26px;background:linear-gradient(160deg,#70412a,#8d6043);color:#fff;box-shadow:0 16px 38px rgba(88,52,31,.16)}.story-route{font-family:Georgia,"Times New Roman",serif;font-size:clamp(2.2rem,5vw,4.3rem);line-height:.94;letter-spacing:-.04em}.story-route span{display:block;font-family:Inter,system-ui,sans-serif;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;opacity:.76;margin-bottom:11px}.story-arrow{display:inline-flex;align-items:center;gap:10px;font-weight:900;margin-top:20px}.story-arrow::after{content:"→";font-size:1.25rem}.story-small{max-width:260px;font-size:.8rem;line-height:1.6;color:rgba(255,255,255,.78)}.story-copy{position:relative;z-index:1;padding:14px 8px 10px}.story-kicker{display:inline-flex;align-items:center;gap:8px;border:1px solid #eed8b9;background:#fff7e7;color:var(--cocoa);padding:8px 11px;border-radius:999px;font-size:.75rem;font-weight:900}.story-copy h2{margin:16px 0 14px;font-size:clamp(2.15rem,4vw,3.5rem);line-height:1;letter-spacing:-.04em}.story-copy .story-lead{font-size:1.03rem;line-height:1.78;color:var(--ink);margin:0 0 12px}.story-copy p{color:var(--muted);line-height:1.78;margin:0 0 13px}.story-highlight{margin-top:18px;padding:16px 18px;border-left:4px solid var(--butter);border-radius:0 16px 16px 0;background:#fff8e9;color:var(--cocoa);font-family:Georgia,"Times New Roman",serif;font-size:1.13rem;line-height:1.6}.story-points{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:19px}.story-point{padding:12px 13px;border-radius:16px;border:1px solid var(--line);background:rgba(255,255,255,.78)}.story-point b{display:block;color:var(--cocoa);font-size:.82rem}.story-point small{display:block;color:var(--muted);margin-top:2px;line-height:1.45}@media(max-width:900px){.story-shell{grid-template-columns:1fr}.story-mark{min-height:250px}.story-points{grid-template-columns:1fr 1fr 1fr}}@media(max-width:650px){.story-section{padding:44px 0}.story-shell{padding:14px;border-radius:26px}.story-mark{padding:22px;min-height:220px;border-radius:21px}.story-copy{padding:10px 6px 7px}.story-points{grid-template-columns:1fr}.story-highlight{font-size:1rem}}
'''

story_html = r'''
<!-- BALE-BELLA-STORY-V1 -->
<section id="story" class="story-section" aria-labelledby="story-title">
  <div class="wrap">
    <div class="story-shell reveal">
      <div class="story-mark">
        <div>
          <div class="story-route"><span>Our beginning</span>Manila<br>to Pampanga</div>
          <div class="story-arrow">A new chapter, baked slowly</div>
        </div>
        <div class="story-small">We still love Manila. Pampanga simply gave our family a different rhythm — more room to slow down, make things by hand, and enjoy being home together.</div>
      </div>

      <div class="story-copy">
        <span class="story-kicker">🤎 Why Bale Bella began</span>
        <h2 id="story-title">A family move that turned into something sweet.</h2>
        <p class="story-lead">Bale Bella Bakehouse began after a mother and daughter moved with their family from Manila to San Fernando, Pampanga looking for a little more calm, space, and time together.</p>
        <p>Manila will always be part of our story, but there was something about settling in Pampanga that made home feel slower in the best way. In between ordinary days, cooking, experimenting, and baking became a shared ritual — something they genuinely looked forward to.</p>
        <p>What started as homemade treats for the family slowly became recipes worth sharing. A passion that lived quietly in the kitchen turned into a small home bakehouse built around one simple idea: make food with care, make it memorable, and make people feel welcome.</p>
        <div class="story-highlight">Bale Bella is not a factory bakery. It is a family story being baked one batch at a time — from our bale to yours.</div>
        <div class="story-points" aria-label="Bale Bella story highlights">
          <div class="story-point"><b>Manila roots</b><small>A city we still love and a chapter we carry with us.</small></div>
          <div class="story-point"><b>Pampanga chapter</b><small>A quieter pace that gave the passion room to grow.</small></div>
          <div class="story-point"><b>Family-made</b><small>Started at home, inspired by time together, built to be shared.</small></div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

if '</style>' in s:
    s = s.replace('</style>', story_css + '\n</style>', 1)

menu_anchor = '<section id="menu">'
if menu_anchor in s:
    s = s.replace(menu_anchor, story_html + '\n' + menu_anchor, 1)
else:
    raise RuntimeError('Could not find menu insertion point')

# Add an Our Story navigation link if the current nav has the Menu link.
menu_link = '<a class="pill menu-link" href="#menu">Menu</a>'
if menu_link in s and 'href="#story"' not in s:
    s = s.replace(menu_link, menu_link + '<a class="pill story-link" href="#story">Our Story</a>', 1)

# Add lightweight business-origin details to the existing LocalBusiness JSON-LD.
if '"foundingDate":"2026"' not in s:
    s = s.replace('"priceRange":"₱₱"', '"foundingDate":"2026","slogan":"From our bale to yours.","priceRange":"₱₱"', 1)

INDEX.write_text(s, encoding='utf-8')
