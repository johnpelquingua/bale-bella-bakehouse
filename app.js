const CONFIG = {
  whatsappNumber: "639171344775",
  whatsappDisplay: "0917 134 4775",
  currency: "₱"
};

const PRODUCTS = [
  { id: "mayumu", name: "Mayumu Chunk", category: "Cookies", desc: "Brown butter, dark chocolate chunks and flaky sea salt.", price: 95, emoji: "🍪", tag: "Signature" },
  { id: "tablea-cookie", name: "Tablea Trouble", category: "Cookies", desc: "Deep chocolate cookie with Philippine tablea and dark chocolate.", price: 110, emoji: "🍫", tag: "Pampanga pick" },
  { id: "ube", name: "Ube Keso Please", category: "Cookies", desc: "Ube cookie, white chocolate and a creamy cheese centre.", price: 115, emoji: "💜", tag: "Playful" },
  { id: "biscoff", name: "Biscoff Ka Pa", category: "Cookies", desc: "Brown butter cookie with a gooey Biscoff centre.", price: 120, emoji: "🥠", tag: "Stuffed" },
  { id: "brownie", name: "Manyaman Brownie", category: "Brownies", desc: "Dense, fudgy dark chocolate brownie with a glossy top.", price: 85, emoji: "🟫", tag: "Fudgy" },
  { id: "tablea-brownie", name: "Tablea After Dark", category: "Brownies", desc: "Fudgy brownie with tablea depth and sea salt.", price: 95, emoji: "🍫", tag: "Rich" },
  { id: "banana", name: "Bella's Banana Loaf", category: "Loaves", desc: "Brown butter banana loaf with choco chunks.", price: 365, emoji: "🍌", tag: "Family fave" },
  { id: "basque", name: "Kaluguran Basque", category: "Cheesecake", desc: "Caramelised top, creamy centre and minimalist finish.", price: 799, emoji: "🍰", tag: "Premium" }
];

const $ = (id) => document.getElementById(id);
const money = (n) => CONFIG.currency + Number(n).toLocaleString("en-PH");

let activeCategory = "All";
let fulfillment = "pickup";
let cart = loadCart();

function loadCart() {
  try {
    const parsed = JSON.parse(localStorage.getItem("bb_cart") || "{}");
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function saveCart() {
  try {
    localStorage.setItem("bb_cart", JSON.stringify(cart));
  } catch {
    // The app still works if storage is blocked.
  }
}

function categories() {
  return ["All", ...new Set(PRODUCTS.map((p) => p.category))];
}

function renderFilters() {
  $("filters").innerHTML = categories().map((category) => `
    <button type="button" class="filter ${category === activeCategory ? "active" : ""}" data-category="${category}" aria-pressed="${category === activeCategory}">${category}</button>
  `).join("");
}

function renderMenu() {
  const visible = activeCategory === "All" ? PRODUCTS : PRODUCTS.filter((p) => p.category === activeCategory);
  $("menuGrid").innerHTML = visible.map((p) => `
    <article class="card reveal visible">
      <div class="visual" aria-hidden="true">
        <span class="tag">${p.tag}</span>
        <span class="food-emoji">${p.emoji}</span>
      </div>
      <div class="card-body">
        <h3>${p.name}</h3>
        <p>${p.desc}</p>
        <div class="card-bottom">
          <span class="price">${money(p.price)}</span>
          <button type="button" class="add-btn" data-add="${p.id}" aria-label="Add ${p.name} to order">+ Add</button>
        </div>
      </div>
    </article>
  `).join("");
}

function getCartItems() {
  return PRODUCTS.filter((p) => Number(cart[p.id]) > 0).map((p) => ({ ...p, qty: Number(cart[p.id]) }));
}

function subtotal() {
  return getCartItems().reduce((sum, item) => sum + item.price * item.qty, 0);
}

function totalCount() {
  return getCartItems().reduce((sum, item) => sum + item.qty, 0);
}

function renderCart() {
  const items = getCartItems();
  const cartList = $("cartList");

  cartList.innerHTML = items.length ? items.map((item) => `
    <div class="cart-item">
      <div>
        <b>${item.name}</b>
        <div class="meta">${money(item.price)} each · ${money(item.price * item.qty)}</div>
      </div>
      <div class="qty" aria-label="Quantity controls for ${item.name}">
        <button type="button" data-qty="-1" data-id="${item.id}" aria-label="Decrease ${item.name}">−</button>
        <b aria-label="Quantity ${item.qty}">${item.qty}</b>
        <button type="button" data-qty="1" data-id="${item.id}" aria-label="Increase ${item.name}">+</button>
      </div>
    </div>
  `).join("") : `
    <div class="empty">
      <span class="empty-emoji" aria-hidden="true">🍪</span>
      Your box is empty.<br><small>Pick something sweet above.</small>
    </div>
  `;

  $("subtotal").textContent = money(subtotal());
  $("delivery").textContent = fulfillment === "pickup" ? "Pickup" : "Quoted separately";
  $("total").textContent = money(subtotal());
  $("mobileTotal").textContent = money(subtotal());
  $("mobileCount").textContent = totalCount();
  $("cartCount").textContent = totalCount();
  $("sendBtn").disabled = items.length === 0;
}

function addToCart(id, button) {
  cart[id] = (Number(cart[id]) || 0) + 1;
  saveCart();
  renderCart();
  animateAdd(button);
  pulseCartCount();
  toast("Added to your order 🍪");
}

function changeQuantity(id, delta) {
  cart[id] = (Number(cart[id]) || 0) + delta;
  if (cart[id] <= 0) delete cart[id];
  saveCart();
  renderCart();
}

function animateAdd(button) {
  if (!button) return;
  button.classList.remove("added");
  void button.offsetWidth;
  button.classList.add("added");
  button.textContent = "Added ✓";
  setTimeout(() => { button.textContent = "+ Add"; }, 800);
  createBurst(button);
}

function pulseCartCount() {
  const count = $("cartCount");
  count.classList.remove("bump");
  void count.offsetWidth;
  count.classList.add("bump");
}

function createBurst(button) {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const rect = button.getBoundingClientRect();
  const symbols = ["♥", "·", "✦", "♥", "·"];
  symbols.forEach((symbol, index) => {
    const particle = document.createElement("span");
    particle.className = "burst";
    particle.textContent = symbol;
    particle.style.left = `${rect.left + rect.width / 2}px`;
    particle.style.top = `${rect.top + rect.height / 2}px`;
    particle.style.color = index % 2 ? "#c68d54" : "#6f4027";
    particle.style.setProperty("--x", `${(index - 2) * 18 + (Math.random() * 12 - 6)}px`);
    particle.style.setProperty("--y", `${-34 - Math.random() * 34}px`);
    particle.style.setProperty("--r", `${(Math.random() * 80 - 40)}deg`);
    document.body.appendChild(particle);
    setTimeout(() => particle.remove(), 760);
  });
}

function setFulfillment(mode) {
  fulfillment = mode;
  document.querySelectorAll(".seg").forEach((button) => {
    const isActive = button.dataset.mode === mode;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
  $("addressField").hidden = mode !== "delivery";
  $("deliveryHint").classList.toggle("show", mode === "delivery");
  clearError("address");
  renderCart();
}

function normalizedPhone(value) {
  return value.replace(/[\s()\-]/g, "");
}

function setError(id, message) {
  const field = $(id);
  const error = $(`${id}Error`);
  if (field) {
    field.classList.add("invalid");
    field.setAttribute("aria-invalid", "true");
  }
  if (error) error.textContent = message;
}

function clearError(id) {
  const field = $(id);
  const error = $(`${id}Error`);
  if (field) {
    field.classList.remove("invalid");
    field.removeAttribute("aria-invalid");
  }
  if (error) error.textContent = "";
}

function clearAllErrors() {
  ["customerName", "customerPhone", "orderDate", "address"].forEach(clearError);
}

function validateOrder() {
  clearAllErrors();
  let firstInvalid = null;
  const customerName = $("customerName").value.trim();
  const customerPhone = normalizedPhone($("customerPhone").value.trim());
  const orderDate = $("orderDate").value;
  const address = $("address").value.trim();

  if (getCartItems().length === 0) {
    toast("Add at least one item first.");
    $("menu").scrollIntoView({ behavior: "smooth" });
    return false;
  }

  if (customerName.length < 2) {
    setError("customerName", "Please enter your name.");
    firstInvalid = firstInvalid || $("customerName");
  }

  if (!/^(?:\+?63|0)9\d{9}$/.test(customerPhone)) {
    setError("customerPhone", "Use a valid PH mobile number, e.g. 0917 123 4567.");
    firstInvalid = firstInvalid || $("customerPhone");
  }

  if (!orderDate) {
    setError("orderDate", "Please select your preferred date.");
    firstInvalid = firstInvalid || $("orderDate");
  }

  if (fulfillment === "delivery" && address.length < 5) {
    setError("address", "Please add your delivery address or landmark.");
    firstInvalid = firstInvalid || $("address");
  }

  if (firstInvalid) {
    firstInvalid.focus();
    toast("Please check the highlighted details.");
    return false;
  }

  return true;
}

function makeOrderReference() {
  let ref = sessionStorage.getItem("bb_order_ref");
  if (ref) return ref;
  const now = new Date();
  const date = `${String(now.getFullYear()).slice(-2)}${String(now.getMonth() + 1).padStart(2, "0")}${String(now.getDate()).padStart(2, "0")}`;
  const suffix = Math.floor(1000 + Math.random() * 9000);
  ref = `BB-${date}-${suffix}`;
  try { sessionStorage.setItem("bb_order_ref", ref); } catch {}
  return ref;
}

function buildOrderText() {
  const items = getCartItems();
  const lines = items.map((item) => `• ${item.qty} × ${item.name} — ${money(item.qty * item.price)}`).join("\n");
  const customerName = $("customerName").value.trim();
  const customerPhone = $("customerPhone").value.trim();
  const orderDate = $("orderDate").value || "To confirm";
  const orderTime = $("orderTime").value;
  const address = $("address").value.trim();
  const notes = $("notes").value.trim();
  const ref = makeOrderReference();

  return [
    "🍪 BALE BELLA BAKEHOUSE",
    "ORDER REQUEST",
    `Reference: ${ref}`,
    "",
    `Name: ${customerName}`,
    `Mobile: ${customerPhone}`,
    `Fulfillment: ${fulfillment === "pickup" ? "Pickup" : "Delivery"}`,
    `Preferred date: ${orderDate}`,
    `Preferred time: ${orderTime}`,
    fulfillment === "delivery" ? `Address: ${address}` : null,
    "",
    "ORDER",
    lines,
    "",
    `Subtotal: ${money(subtotal())}`,
    `Delivery: ${fulfillment === "pickup" ? "Pickup" : "Quoted separately"}`,
    `Current order total: ${money(subtotal())}`,
    "",
    `Notes: ${notes || "None"}`,
    "",
    "Please confirm availability, payment instructions, and final pickup/delivery details. Thank you! 🤎"
  ].filter((line) => line !== null).join("\n");
}

async function copyOrderText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      // Use the fallback below.
    }
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.top = "-1000px";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);

  let copied = false;
  try {
    copied = document.execCommand("copy");
  } catch {
    copied = false;
  }
  textarea.remove();
  return copied;
}

function sendOrder() {
  if (!validateOrder()) return;
  const text = buildOrderText();
  const url = `https://wa.me/${CONFIG.whatsappNumber}?text=${encodeURIComponent(text)}`;

  // Keep this synchronous so browsers do not treat WhatsApp as an unwanted popup.
  const popup = window.open(url, "_blank");
  if (popup) {
    try { popup.opener = null; } catch {}
    toast("Opening WhatsApp with your order…");
  } else {
    window.location.href = url;
  }
}

async function copyOrder() {
  if (!validateOrder()) return;
  const copied = await copyOrderText(buildOrderText());
  if (copied) {
    toast("Order copied ✓ Paste it into Messenger.");
    const button = $("copyBtn");
    const previous = button.innerHTML;
    button.innerHTML = "✓ Copied for Messenger";
    setTimeout(() => { button.innerHTML = previous; }, 1600);
  } else {
    window.prompt("Copy this order and paste it into Messenger:", buildOrderText());
  }
}

function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(window.__bbToastTimer);
  window.__bbToastTimer = setTimeout(() => el.classList.remove("show"), 2200);
}

function initDate() {
  const dateInput = $("orderDate");
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const iso = tomorrow.toISOString().split("T")[0];
  dateInput.min = iso;
  if (!dateInput.value) dateInput.value = iso;
}

function initRevealAnimations() {
  const nodes = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    nodes.forEach((node) => node.classList.add("visible"));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  nodes.forEach((node) => observer.observe(node));
}

function wireEvents() {
  $("filters").addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) return;
    activeCategory = button.dataset.category;
    renderFilters();
    renderMenu();
  });

  $("menuGrid").addEventListener("click", (event) => {
    const button = event.target.closest("[data-add]");
    if (!button) return;
    addToCart(button.dataset.add, button);
  });

  $("cartList").addEventListener("click", (event) => {
    const button = event.target.closest("[data-qty]");
    if (!button) return;
    changeQuantity(button.dataset.id, Number(button.dataset.qty));
  });

  document.querySelectorAll(".seg").forEach((button) => {
    button.addEventListener("click", () => setFulfillment(button.dataset.mode));
  });

  $("sendBtn").addEventListener("click", sendOrder);
  $("copyBtn").addEventListener("click", copyOrder);
  $("mobileCartBtn").addEventListener("click", () => $("order").scrollIntoView({ behavior: "smooth" }));

  ["customerName", "customerPhone", "orderDate", "address"].forEach((id) => {
    $(id).addEventListener("input", () => clearError(id));
    $(id).addEventListener("change", () => clearError(id));
  });
}

function init() {
  $("businessPhone").textContent = CONFIG.whatsappDisplay;
  $("businessPhone").href = `https://wa.me/${CONFIG.whatsappNumber}`;
  renderFilters();
  renderMenu();
  renderCart();
  initDate();
  wireEvents();
  initRevealAnimations();
}

document.addEventListener("DOMContentLoaded", init);