const CONFIG = {
  whatsappNumber: "639171344775",
  whatsappDisplay: "0917 134 4775",
  currency: "₱",
  gcashDisplay: "Sent after order confirmation"
};

const PRODUCTS = [
  { id:"mayumu", name:"Mayumu Chunk", category:"Cookies", desc:"Brown butter, dark chocolate chunks and flaky sea salt.", emoji:"🍪", tag:"Signature", available:true, leadDays:1, variants:[{label:"Single",price:95},{label:"Box of 4",price:360},{label:"Box of 6",price:520}] },
  { id:"tablea-cookie", name:"Tablea Trouble", category:"Cookies", desc:"Deep chocolate cookie with Philippine tablea and dark chocolate.", emoji:"🍫", tag:"Pampanga pick", available:true, leadDays:1, variants:[{label:"Single",price:110},{label:"Box of 4",price:420},{label:"Box of 6",price:610}] },
  { id:"ube", name:"Ube Keso Please", category:"Cookies", desc:"Ube cookie, white chocolate and a creamy cheese centre.", emoji:"💜", tag:"Playful", available:true, leadDays:1, variants:[{label:"Single",price:115},{label:"Box of 4",price:440},{label:"Box of 6",price:640}] },
  { id:"biscoff", name:"Biscoff Ka Pa", category:"Cookies", desc:"Brown butter cookie with a gooey Biscoff centre.", emoji:"🥠", tag:"Stuffed", available:true, leadDays:1, variants:[{label:"Single",price:120},{label:"Box of 4",price:460},{label:"Box of 6",price:670}] },
  { id:"brownie", name:"Manyaman Brownie", category:"Brownies", desc:"Dense, fudgy dark chocolate brownie with a glossy top.", emoji:"🟫", tag:"Fudgy", available:true, leadDays:1, variants:[{label:"Single",price:85},{label:"Box of 6",price:450}] },
  { id:"tablea-brownie", name:"Tablea After Dark", category:"Brownies", desc:"Fudgy brownie with tablea depth and sea salt.", emoji:"🍫", tag:"Rich", available:true, leadDays:1, variants:[{label:"Single",price:95},{label:"Box of 6",price:520}] },
  { id:"banana", name:"Bella's Banana Loaf", category:"Loaves", desc:"Brown butter banana loaf with choco chunks.", emoji:"🍌", tag:"Family fave", available:true, leadDays:2, variants:[{label:"Whole loaf",price:365}] },
  { id:"basque", name:"Kaluguran Basque", category:"Cheesecake", desc:"Caramelised top, creamy centre and minimalist finish.", emoji:"🍰", tag:"Premium", available:true, leadDays:2, variants:[{label:"15 cm whole cake",price:799}] },
  { id:"sampler", name:"Bale Bella Taste Box", category:"Boxes", desc:"A curated mix for first-timers, gifts and sharing.", emoji:"🎁", tag:"Best intro", available:true, leadDays:2, variants:[{label:"Sampler box",price:549}] }
];

const $ = (id) => document.getElementById(id);
const money = (n) => CONFIG.currency + Number(n).toLocaleString("en-PH");
let activeCategory = "All";
let fulfillment = "pickup";
let orderType = "personal";
let paymentMethod = "GCash";
let cart = loadCart();

function loadCart(){try{const p=JSON.parse(localStorage.getItem("bb_cart")||"{}");return p&&typeof p==="object"?p:{}}catch{return{}}}
function saveCart(){try{localStorage.setItem("bb_cart",JSON.stringify(cart))}catch{}}
function keyFor(id,variantIndex){return `${id}::${variantIndex}`}
function categories(){return ["All",...new Set(PRODUCTS.map(p=>p.category))]}
function productById(id){return PRODUCTS.find(p=>p.id===id)}

function renderFilters(){
  $("filters").innerHTML=categories().map(c=>`<button type="button" class="filter ${c===activeCategory?"active":""}" data-category="${c}" aria-pressed="${c===activeCategory}">${c}</button>`).join("");
}

function renderMenu(){
  const visible=activeCategory==="All"?PRODUCTS:PRODUCTS.filter(p=>p.category===activeCategory);
  $("menuGrid").innerHTML=visible.map(p=>{
    const first=p.variants[0];
    return `<article class="card reveal visible ${p.available?"":"sold-out"}">
      <div class="visual" aria-hidden="true"><span class="tag">${p.tag}</span><span class="stock-badge ${p.available?"":"sold"}">${p.available?"Available":"Sold out"}</span><span class="food-emoji">${p.emoji}</span></div>
      <div class="card-body"><h3>${p.name}</h3><p>${p.desc}</p><div class="lead-time">⏱ ${p.leadDays} day${p.leadDays>1?"s":""} minimum lead time</div>
      ${p.variants.length>1?`<select class="variant-select" data-variant-select="${p.id}" aria-label="Choose size for ${p.name}">${p.variants.map((v,i)=>`<option value="${i}">${v.label} · ${money(v.price)}</option>`).join("")}</select>`:""}
      <div class="card-bottom"><span class="price" id="price-${p.id}">${money(first.price)}</span><button type="button" class="add-btn" data-add="${p.id}" ${p.available?"":"disabled"}>${p.available?"+ Add":"Unavailable"}</button></div></div></article>`;
  }).join("");
}

function getCartItems(){
  return Object.entries(cart).map(([key,qty])=>{
    const [id,variantIndexRaw]=key.split("::");
    const p=productById(id); const vi=Number(variantIndexRaw); if(!p||!p.variants[vi]||qty<=0)return null;
    return {...p,variantIndex:vi,variant:p.variants[vi],qty:Number(qty),cartKey:key};
  }).filter(Boolean);
}
function subtotal(){return getCartItems().reduce((s,i)=>s+i.variant.price*i.qty,0)}
function totalCount(){return getCartItems().reduce((s,i)=>s+i.qty,0)}
function maxLeadDays(){return Math.max(1,...getCartItems().map(i=>i.leadDays||1))}

function renderCart(){
  const items=getCartItems(); const list=$("cartList");
  list.innerHTML=items.length?items.map(i=>`<div class="cart-item"><div><b>${i.name}</b><div class="meta">${i.variant.label} · ${money(i.variant.price)} each · ${money(i.variant.price*i.qty)}</div></div><div class="qty"><button type="button" data-cart-key="${i.cartKey}" data-delta="-1" aria-label="Decrease ${i.name}">−</button><b>${i.qty}</b><button type="button" data-cart-key="${i.cartKey}" data-delta="1" aria-label="Increase ${i.name}">+</button></div></div>`).join(""):`<div class="empty"><span class="empty-emoji">🍪</span>Your box is empty.<br><small>Pick something sweet above.</small></div>`;
  $("subtotal").textContent=money(subtotal()); $("total").textContent=money(subtotal());
  $("delivery").textContent=fulfillment==="pickup"?"Pickup":"Quoted separately";
  $("paymentSummary").textContent=paymentMethod==="GCash"?"GCash after confirmation":paymentMethod;
  $("mobileTotal").textContent=money(subtotal()); $("mobileCount").textContent=totalCount(); $("cartCount").textContent=totalCount();
  $("sendBtn").disabled=!items.length; $("clearCartBtn").disabled=!items.length;
  updateMinimumDate();
}

function addToCart(id,button){
  const p=productById(id); if(!p||!p.available)return;
  const select=document.querySelector(`[data-variant-select="${id}"]`); const vi=select?Number(select.value):0; const key=keyFor(id,vi);
  cart[key]=(Number(cart[key])||0)+1; saveCart(); renderCart(); animateAdd(button); pulseCartCount(); toast(`${p.name} added 🤎`);
}
function changeQuantity(key,delta){cart[key]=(Number(cart[key])||0)+delta;if(cart[key]<=0)delete cart[key];saveCart();renderCart()}
function clearCart(){if(!getCartItems().length)return; if(confirm("Clear your Bale Bella order?")){cart={};saveCart();renderCart();toast("Cart cleared.")}}

function animateAdd(button){if(!button)return;button.classList.remove("added");void button.offsetWidth;button.classList.add("added");const old=button.textContent;button.textContent="Added ✓";setTimeout(()=>button.textContent=old,850);createBurst(button)}
function pulseCartCount(){const c=$("cartCount");c.classList.remove("bump");void c.offsetWidth;c.classList.add("bump")}
function createBurst(button){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;const r=button.getBoundingClientRect();["♥","✦","·","♥","✦"].forEach((s,i)=>{const e=document.createElement("span");e.className="burst";e.textContent=s;e.style.left=`${r.left+r.width/2}px`;e.style.top=`${r.top+r.height/2}px`;e.style.color=i%2?"#c68d54":"#6f4027";e.style.setProperty("--x",`${(i-2)*19+(Math.random()*12-6)}px`);e.style.setProperty("--y",`${-34-Math.random()*34}px`);e.style.setProperty("--r",`${Math.random()*80-40}deg`);document.body.appendChild(e);setTimeout(()=>e.remove(),760)})}

function setFulfillment(mode){fulfillment=mode;document.querySelectorAll("[data-mode]").forEach(b=>{const a=b.dataset.mode===mode;b.classList.toggle("active",a);b.setAttribute("aria-pressed",String(a))});$("addressField").hidden=mode!=="delivery";$("deliveryHint").classList.toggle("show",mode==="delivery");clearError("address");renderCart()}
function setOrderType(type){orderType=type;document.querySelectorAll("[data-order-type]").forEach(b=>{const a=b.dataset.orderType===type;b.classList.toggle("active",a);b.setAttribute("aria-pressed",String(a))});$("giftFields").hidden=type!=="gift";$("corporateFields").hidden=type!=="corporate";["recipientName","companyName","guestCount"].forEach(clearError)}
function setPayment(method){paymentMethod=method;document.querySelectorAll("[data-payment]").forEach(b=>{const a=b.dataset.payment===method;b.classList.toggle("active",a);b.setAttribute("aria-pressed",String(a))});$("gcashCard").hidden=method!=="GCash";renderCart()}

function normalizedPhone(v){return v.replace(/[\s()\-]/g,"")}
function setError(id,msg){const f=$(id),e=$(`${id}Error`);if(f){f.classList.add("invalid");f.setAttribute("aria-invalid","true")}if(e)e.textContent=msg}
function clearError(id){const f=$(id),e=$(`${id}Error`);if(f){f.classList.remove("invalid");f.removeAttribute("aria-invalid")}if(e)e.textContent=""}
function clearAllErrors(){["customerName","customerPhone","orderDate","address","recipientName","companyName","guestCount"].forEach(clearError)}

function updateMinimumDate(){
  const input=$("orderDate"); if(!input)return; const days=maxLeadDays(); const d=new Date(); d.setHours(12,0,0,0); d.setDate(d.getDate()+days); const iso=d.toISOString().split("T")[0]; input.min=iso; if(!input.value||input.value<iso)input.value=iso; $("leadHint").textContent=`Earliest date for this cart: ${days} day${days>1?"s":""} from today.`;
}

function validateOrder(){
  clearAllErrors(); let first=null; const name=$("customerName").value.trim(); const phone=normalizedPhone($("customerPhone").value.trim()); const date=$("orderDate").value; const addr=$("address").value.trim();
  if(!getCartItems().length){toast("Add at least one item first.");$("menu").scrollIntoView({behavior:"smooth"});return false}
  if(name.length<2){setError("customerName","Please enter your name.");first=first||$("customerName")}
  if(!/^(?:\+?63|0)9\d{9}$/.test(phone)){setError("customerPhone","Use a valid PH mobile number.");first=first||$("customerPhone")}
  if(!date){setError("orderDate","Please select a date.");first=first||$("orderDate")}
  if(fulfillment==="delivery"&&addr.length<5){setError("address","Add a delivery address or landmark.");first=first||$("address")}
  if(orderType==="gift"&&$("recipientName").value.trim().length<2){setError("recipientName","Add the recipient name.");first=first||$("recipientName")}
  if(orderType==="corporate"){
    if($("companyName").value.trim().length<2){setError("companyName","Add the company / organization.");first=first||$("companyName")}
    if(Number($("guestCount").value)<10){setError("guestCount","Enter at least 10 for a corporate request.");first=first||$("guestCount")}
  }
  if(first){first.focus();toast("Please check the highlighted details.");return false} return true;
}

function makeOrderReference(){let ref=sessionStorage.getItem("bb_order_ref");if(ref)return ref;const n=new Date();const d=`${String(n.getFullYear()).slice(-2)}${String(n.getMonth()+1).padStart(2,"0")}${String(n.getDate()).padStart(2,"0")}`;ref=`BB-${d}-${Math.floor(1000+Math.random()*9000)}`;try{sessionStorage.setItem("bb_order_ref",ref)}catch{}return ref}

function buildOrderText(){
  const lines=getCartItems().map(i=>`• ${i.qty} × ${i.name} (${i.variant.label}) — ${money(i.variant.price*i.qty)}`).join("\n");
  const extras=[];
  if(orderType==="gift"){extras.push(`Recipient: ${$("recipientName").value.trim()}`);if($("giftMessage").value.trim())extras.push(`Gift message: ${$("giftMessage").value.trim()}`)}
  if(orderType==="corporate"){extras.push(`Company: ${$("companyName").value.trim()}`);extras.push(`Estimated quantity / guests: ${$("guestCount").value}`);if($("corporateNotes").value.trim())extras.push(`Customization: ${$("corporateNotes").value.trim()}`)}
  const paymentNote=paymentMethod==="GCash"?"Please send official GCash details only after confirming this order. I will reply with the receipt using this reference.":`Preferred payment: ${paymentMethod}`;
  return ["🍪 BALE BELLA BAKEHOUSE","ORDER REQUEST",`Reference: ${makeOrderReference()}`,"",`Order type: ${orderType[0].toUpperCase()+orderType.slice(1)}`,`Name: ${$("customerName").value.trim()}`,`Mobile: ${$("customerPhone").value.trim()}`,...extras,`Fulfillment: ${fulfillment==="pickup"?"Pickup":"Delivery"}`,`Preferred date: ${$("orderDate").value}`,`Preferred time: ${$("orderTime").value}`,fulfillment==="delivery"?`Address: ${$("address").value.trim()}`:null,"","ORDER",lines,"",`Subtotal: ${money(subtotal())}`,`Delivery: ${fulfillment==="pickup"?"Pickup":"Quoted separately"}`,`Current total: ${money(subtotal())}`,`Payment preference: ${paymentMethod}`,"",paymentNote,"",`Notes: ${$("notes").value.trim()||"None"}`,"","Please confirm availability, final amount, payment details and pickup/delivery arrangements. Thank you! 🤎"].filter(v=>v!==null).join("\n");
}

async function copyOrderText(text){
  if(navigator.clipboard&&window.isSecureContext){try{await navigator.clipboard.writeText(text);return true}catch{}}
  const ta=document.createElement("textarea");ta.value=text;ta.setAttribute("readonly","");ta.style.position="fixed";ta.style.top="-2000px";document.body.appendChild(ta);ta.focus();ta.select();ta.setSelectionRange(0,ta.value.length);let ok=false;try{ok=document.execCommand("copy")}catch{}ta.remove();return ok;
}

function sendOrder(){if(!validateOrder())return;const text=buildOrderText();const url=`https://wa.me/${CONFIG.whatsappNumber}?text=${encodeURIComponent(text)}`;const w=window.open(url,"_blank");if(w){try{w.opener=null}catch{}toast("Opening WhatsApp with your order…")}else{window.location.href=url}}
async function copyOrder(){if(!validateOrder())return;const text=buildOrderText();const ok=await copyOrderText(text);if(ok){toast("Order copied ✓ Paste it into Messenger.");const b=$("copyBtn"),old=b.innerHTML;b.innerHTML="✓ Copied for Messenger";setTimeout(()=>b.innerHTML=old,1600)}else{$("manualCopyText").value=text;$("copyDialog").showModal();$("manualCopyText").focus();$("manualCopyText").select()}}

async function shareMenu(){const data={title:"Bale Bella Bakehouse",text:"Fresh-baked sweets from Bale Bella Bakehouse in San Fernando, Pampanga 🍪",url:location.href.split("#")[0]};if(navigator.share){try{await navigator.share(data);return}catch(e){if(e.name==="AbortError")return}}const ok=await copyOrderText(data.url);toast(ok?"Menu link copied ✓":"Copy this link: "+data.url)}

function toast(msg){const e=$("toast");e.textContent=msg;e.classList.add("show");clearTimeout(window.__toast);window.__toast=setTimeout(()=>e.classList.remove("show"),2200)}

function initRevealAnimations(){
  const nodes=document.querySelectorAll(".reveal"); if(!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches){nodes.forEach(n=>n.classList.add("visible"));return}
  const io=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("visible");io.unobserve(entry.target)}}),{threshold:.12});nodes.forEach(n=>io.observe(n));
}
function initParallax(){
  if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  const layers=[...document.querySelectorAll(".parallax")];const card=$("heroCard");let ticking=false;
  const draw=()=>{const y=window.scrollY;layers.forEach(el=>{const s=Number(el.dataset.speed||0);el.style.transform=`translate3d(0,${y*s}px,0)`});if(card&&innerWidth>700){const r=card.getBoundingClientRect();const p=Math.max(-1,Math.min(1,(innerHeight/2-(r.top+r.height/2))/innerHeight));card.style.transform=`translate3d(0,${p*8}px,0) rotate(${p*.5}deg)`}ticking=false};
  addEventListener("scroll",()=>{if(!ticking){requestAnimationFrame(draw);ticking=true}},{passive:true});draw();
}
function initScrollProgress(){const bar=$("scrollProgress");const update=()=>{const max=document.documentElement.scrollHeight-innerHeight;bar.style.width=`${max>0?Math.min(100,scrollY/max*100):0}%`};addEventListener("scroll",update,{passive:true});update()}

function bindEvents(){
  $("filters").addEventListener("click",e=>{const b=e.target.closest("[data-category]");if(!b)return;activeCategory=b.dataset.category;renderFilters();renderMenu()});
  $("menuGrid").addEventListener("change",e=>{const s=e.target.closest("[data-variant-select]");if(!s)return;const p=productById(s.dataset.variantSelect);const v=p.variants[Number(s.value)];$(`price-${p.id}`).textContent=money(v.price)});
  $("menuGrid").addEventListener("click",e=>{const b=e.target.closest("[data-add]");if(b)addToCart(b.dataset.add,b)});
  $("cartList").addEventListener("click",e=>{const b=e.target.closest("[data-cart-key]");if(b)changeQuantity(b.dataset.cartKey,Number(b.dataset.delta))});
  document.querySelectorAll("[data-mode]").forEach(b=>b.addEventListener("click",()=>setFulfillment(b.dataset.mode)));
  document.querySelectorAll("[data-order-type]").forEach(b=>b.addEventListener("click",()=>setOrderType(b.dataset.orderType)));
  document.querySelectorAll("[data-payment]").forEach(b=>b.addEventListener("click",()=>setPayment(b.dataset.payment)));
  $("sendBtn").addEventListener("click",sendOrder);$("copyBtn").addEventListener("click",copyOrder);$("shareBtn").addEventListener("click",shareMenu);$("clearCartBtn").addEventListener("click",clearCart);
  $("mobileCartBtn").addEventListener("click",()=>$("order").scrollIntoView({behavior:"smooth"}));
  ["customerName","customerPhone","orderDate","address","recipientName","companyName","guestCount"].forEach(id=>{const el=$(id);if(el)el.addEventListener("input",()=>clearError(id))});
}

function init(){renderFilters();renderMenu();setOrderType("personal");setPayment("GCash");setFulfillment("pickup");renderCart();bindEvents();initRevealAnimations();initParallax();initScrollProgress()}
document.addEventListener("DOMContentLoaded",init);