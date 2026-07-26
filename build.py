#!/usr/bin/env python3
"""
Static site generator for Alpha Growth Solutions.

Edit BUSINESS below, then run:  python3 build.py
Regenerates every .html page from one source of truth.
"""
import os

# ---------------------------------------------------------------------------
# THE ONLY BLOCK YOU NEED TO EDIT
# Anything still wrapped in [[ ]] must be replaced before submitting for review.
# ---------------------------------------------------------------------------
BUSINESS = {
    "name":        "Alpha Growth Solutions",
    "tagline":     "Digital toolkits for independent creators and small businesses.",
    "email":       "alphagrowthsolutions.biz@gmail.com",
    "product":     "The Faceless Creator Kit",
    "price":       "499",
    "checkout":    "#",          # Razorpay Payment Page link once you have it
    "hours":       "Monday to Saturday, 10:00 to 18:00 IST",
    "response":    "within 2 to 3 business days",
}

NAV = [
    ("index.html",    "Home"),
    ("about.html",    "About"),
    ("pricing.html",  "Pricing"),
    ("contact.html",  "Contact"),
]
FOOTER_POLICIES = [
    ("delivery.html", "Delivery Policy"),
    ("refunds.html",  "Refund &amp; Cancellation"),
    ("terms.html",    "Terms &amp; Conditions"),
    ("privacy.html",  "Privacy Policy"),
]

ICONS = {
  "layers":  '<path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
  "quote":   '<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.757-2-2-2H4c-1.25 0-2 .75-2 2v6c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1Z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2-2-2h-4c-1.25 0-2 .75-2 2v6c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1Z"/>',
  "calendar":'<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/>',
  "book":    '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
  "mail":    '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
  "shield":  '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z"/><path d="m9 12 2 2 4-4"/>',
  "bolt":    '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/>',
  "lock":    '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
}


def icon(name, cls="icon-tile"):
    return (f'<div class="{cls}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg></div>')


def check_svg():
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5L20 7"/></svg>')


CTA_HTML = """
<div class="wrap">
  <section class="cta">
    <h2>Ready to get started?</h2>
    <p>One-time payment, instant digital delivery, and everything you need to start
       publishing in your first week.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="pricing.html">View pricing</a>
    </div>
  </section>
</div>
"""

CTA_PAGES = {"index.html", "about.html", "pricing.html", "contact.html"}

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; {name}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#2563eb">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="alternate icon" type="image/png" href="assets/favicon-180.png">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@700;800&display=swap">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">
      <span class="ags-badge">AGS</span>
      <span class="brand-name">{name}</span>
    </a>
    <nav class="nav">{nav}</nav>
  </div>
</header>

{body}
{cta}

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <span class="ags-badge inv">AGS</span>
          {name}
        </div>
        <p class="footer-text">{tagline}</p>
      </div>
      <div>
        <h4>Company</h4>
        {footer_nav}
      </div>
      <div>
        <h4>Policies</h4>
        {footer_policies}
      </div>
      <div>
        <h4>Contact</h4>
        <p class="footer-text">
          <a href="mailto:{email}">{email}</a>
        </p>
      </div>
    </div>
    <div class="footer-bar">
      <span>&copy; {year} {name}. All rights reserved.</span>
      <span class="dot-row">
        <span>Digital products</span>
        <span>Made in India</span>
      </span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def page_hero(title, sub):
    return f"""<section class="hero">
  <div class="wrap">
    <h1>{title}</h1>
    <p class="hero-sub">{sub}</p>
  </div>
</section>"""


def slug(text):
    import re as _re
    t = _re.sub(r"&[a-z]+;", " ", text).lower()
    return _re.sub(r"-+", "-", _re.sub(r"[^a-z0-9]+", "-", t)).strip("-")


def policy_page(title, sub, sections):
    blocks, toc = [], []
    for h, body in sections:
        sid = slug(h)
        blocks.append(f'<h2 id="{sid}">{h}</h2>\n{body}')
        toc.append(f'<a href="#{sid}">{h}</a>')
    return page_hero(title, sub) + f"""
<main class="wrap">
  <div class="prose-layout">
    <aside class="toc">
      <h4>On this page</h4>
      {chr(10)          .join(toc)}
    </aside>
    <div class="prose">
{chr(10).join(blocks)}
    </div>
  </div>
</main>"""


B = BUSINESS
P = f"&#8377;{B['price']}"

# ---------------------------------------------------------------------------
PAGES = {}

# ------------------------------- HOME --------------------------------------
PAGES["index.html"] = ("Home",
  f"{B['name']} builds and sells digital toolkits for independent creators and small businesses in India.",
  f"""<section class="hero hero-lg">
  <div class="wrap">
    <p class="eyebrow">Digital Products</p>
    <h1>Ready-to-use toolkits for <span class="gradient-text">people who publish</span></h1>
    <p class="hero-sub">{B['tagline']}</p>
    <div class="btn-row">
      <a class="btn" href="pricing.html">View pricing</a>
      <a class="btn btn-ghost" href="about.html">About us</a>
    </div>
    <div class="hero-badges">
      <span class="pill">{check_svg()} Instant digital delivery</span>
      <span class="pill">{check_svg()} One-time payment</span>
      <span class="pill">{check_svg()} No subscription</span>
    </div>
  </div>
</section>

<main class="wrap">
  <section class="band">
    <div class="band-head">
      <p class="eyebrow">What we do</p>
      <h2>Practical tools, not theory</h2>
    </div>
    <p>{B['name']} is an Indian digital products business. We build and sell ready-to-use content
       toolkits &mdash; editable templates, written copy libraries, planners and step-by-step guides
       &mdash; for people who create content or market a small business online.</p>
    <p>Everything we sell is delivered digitally. There are no physical goods, and nothing is
       shipped.</p>

    <div class="grid grid-3" style="margin-top:34px">
      <div class="card">
        {icon('layers')}
        <h3>Editable templates</h3>
        <p>Design files you duplicate and adapt in minutes, in a free browser-based editor.</p>
      </div>
      <div class="card">
        {icon('quote')}
        <h3>Written copy libraries</h3>
        <p>Opening lines and script structures, ready to adapt to whatever you publish about.</p>
      </div>
      <div class="card">
        {icon('calendar')}
        <h3>Planners and guides</h3>
        <p>A content calendar and step-by-step walkthroughs so you always know what comes next.</p>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="band-head">
      <p class="eyebrow">Our products</p>
      <h2>What we sell today</h2>
    </div>
    <div class="product-card">
      <div class="pc-head">
        <span class="tagline-badge">Flagship product</span>
        <h3 style="font-size:23px">{B['product']}</h3>
        <p style="margin:10px 0 0">A complete system for producing short-form video content without
           appearing on camera. It includes editable video templates, a library of opening lines, a
           90-day content calendar, and written guides covering production, growth and
           monetisation.</p>
      </div>
      <div class="pc-body">
        <ul class="check">
          <li>Editable design templates delivered as hosted links</li>
          <li>A written hook and script library</li>
          <li>Planning documents and step-by-step guides</li>
          <li>Delivered instantly by email after payment</li>
        </ul>
        <div class="price"><span class="amt">{P}</span> <span class="per">one-time</span></div>
        <p class="price-note">No subscription. No recurring charge.</p>
        <a class="btn" href="pricing.html">See what's included</a>
      </div>
    </div>
  </section>
</main>

<section class="section-alt">
  <div class="wrap">
    <div class="band-head">
      <p class="eyebrow">How buying works</p>
      <h2>Three steps, start to finish</h2>
    </div>
    <ol class="steps">
      <li>
        <h3>Pay online</h3>
        <p>Payments are processed by our payment gateway partner. We never see or store your card
           or UPI details.</p>
      </li>
      <li>
        <h3>Receive access immediately</h3>
        <p>A confirmation email with your access document is sent to the address used at
           checkout.</p>
      </li>
      <li>
        <h3>Save your files</h3>
        <p>Access links are guaranteed for 24 hours &mdash; copy everything to your own account
           within that window and it is yours permanently.</p>
      </li>
    </ol>
    <p style="margin-top:26px">Full details are in our <a href="delivery.html">Delivery Policy</a>.</p>
  </div>
</section>

<main class="wrap" style="padding-top:0">
  <section class="band">
    <div class="grid grid-2">
      <div class="card">
        {icon('mail')}
        <h3>Questions before you buy?</h3>
        <p>Email us at <a href="mailto:{B['email']}">{B['email']}</a> and we will reply
           {B['response']}. Full contact details are on our
           <a href="contact.html">Contact page</a>.</p>
      </div>
      <div class="card">
        {icon('lock')}
        <h3>Your payment details stay private</h3>
        <p>Checkout is handled entirely by our payment gateway partner. We receive only
           confirmation that a payment succeeded, never your card or banking credentials.</p>
      </div>
    </div>
  </section>
</main>""")

# ------------------------------- ABOUT -------------------------------------
PAGES["about.html"] = ("About Us",
  f"About {B['name']} &mdash; who we are and what we sell.",
  page_hero("About Us", f"Who we are and what we sell.") + f"""
<main class="wrap">
<div class="prose">
<h2>About {B['name']}</h2>
<p>{B['name']} is a digital products business based in India. We create and sell practical toolkits
   for independent creators, freelancers and small business owners who market themselves online.</p>

<h2>What we sell</h2>
<p>Our products are digital only. They consist of editable design templates, written content
   libraries, planning documents and instructional guides. Each product is delivered as a document
   containing access links, sent by email immediately after purchase.</p>
<p>We do not sell physical goods, subscriptions, financial products or services. There is nothing to
   ship and nothing to install.</p>

<h2>Who our products are for</h2>
<p>Our customers are typically people starting or growing a presence on social media &mdash; content
   creators, small business owners, freelancers and marketers. Our products are designed to remove
   the blank-page problem: instead of building templates and planning content from scratch, the
   customer starts from a working system and adapts it.</p>

<h2>How we operate</h2>
<p>We are a small, independent operation. Orders are fulfilled automatically at the moment of
   payment, and support is handled directly by email. We aim to respond to every message
   {B['response']}.</p>

<h2>Contact</h2>
<p>For any question about our products, an order, or these policies, write to
   <a href="mailto:{B['email']}">{B['email']}</a>. Our contact details and support hours are listed
   on the <a href="contact.html">Contact page</a>.</p>
</div>
</main>""")

# ------------------------------ PRICING ------------------------------------
PAGES["pricing.html"] = ("Pricing",
  f"Pricing for {B['name']} digital products.",
  page_hero("Pricing", "Simple one-time pricing. No subscriptions, no recurring charges.") + f"""
<main class="wrap">
<div class="product-card" style="max-width:760px">
  <div class="pc-head">
    <span class="tagline-badge">Flagship product</span>
    <h3 style="font-size:23px">{B['product']}</h3>
    <div class="price"><span class="amt">{P}</span> <span class="per">one-time payment</span></div>
    <p class="price-note" style="margin-bottom:0">No subscription. No recurring charge.</p>
  </div>
  <div class="pc-body">
    <h4 style="margin-bottom:14px">What is included</h4>
    <ul class="check">
      <li>Editable short-form video templates</li>
      <li>A library of opening lines and script structures</li>
      <li>A 90-day content calendar and planning documents</li>
      <li>Written guides covering production, growth, email and monetisation</li>
      <li>A quick-start plan for the first week</li>
    </ul>
    <h4 style="margin:26px 0 14px">What is not included</h4>
    <ul class="check cross">
      <li>No physical goods. Nothing is shipped.</li>
      <li>No subscription or recurring billing. This is a single one-time payment.</li>
      <li>No ongoing coaching, consulting or account management.</li>
      <li>No guarantee of any particular audience growth, income or business result.</li>
    </ul>
    <a class="btn" href="{B['checkout']}" style="margin-top:10px">Buy now</a>
  </div>
</div>

<div class="prose" style="margin-top:56px">

<h3>Taxes</h3>
<p>The price shown above is the total amount payable. Any applicable taxes are included in the
   displayed price. A payment receipt is issued by our payment gateway partner at the time of
   purchase.</p>

<h3>Payment methods</h3>
<p>Payments are accepted online through our payment gateway partner and support UPI, debit cards,
   credit cards, net banking and wallets. {B['name']} does not collect, see or store your card,
   UPI or banking credentials at any point.</p>

<h3>Delivery</h3>
<p>Delivery is immediate and digital. See our <a href="delivery.html">Delivery Policy</a> for full
   details, and our <a href="refunds.html">Refund &amp; Cancellation Policy</a> before purchasing.</p>

</div>
</main>""")

# ------------------------------ CONTACT ------------------------------------
PAGES["contact.html"] = ("Contact Us",
  f"Contact {B['name']} &mdash; email, address and support hours.",
  page_hero("Contact Us", "We reply to every message. Email is the fastest way to reach us.") + f"""
<main class="wrap">
<div class="contact-card">
  {icon('mail')}
  <h3>Email us</h3>
  <p class="contact-email"><a href="mailto:{B['email']}">{B['email']}</a></p>
  <p class="small">We respond {B['response']}, {B['hours']}.</p>
</div>

<div class="prose">
<h2>Support hours</h2>
<p>{B['hours']}. Messages received outside these hours are answered on the next working day.</p>

<h2>What to include in your message</h2>
<p>If you are writing about an order, please include the email address used at checkout and the
   date of purchase. This lets us locate your order and help you faster.</p>

<h2>Order and access problems</h2>
<p>If you paid and did not receive your access email, first check your spam or promotions folder.
   If it is not there, email us at <a href="mailto:{B['email']}">{B['email']}</a> and we will resend
   it. If you were unable to access your purchase because of a fault on our side, see our
   <a href="refunds.html">Refund &amp; Cancellation Policy</a>.</p>
</div>
</main>""")

# ----------------------------- DELIVERY ------------------------------------
PAGES["delivery.html"] = ("Delivery Policy",
  f"How {B['name']} delivers digital products.",
  policy_page("Delivery Policy", "How and when you receive what you buy.", [
    ("Digital delivery only", f"""<p>All products sold by {B['name']} are digital. No physical goods
       are sold and nothing is shipped. There are no shipping charges, courier partners or delivery
       addresses involved in any order.</p>"""),
    ("When you receive your product", """<p>Delivery is immediate. As soon as your payment is
       confirmed, an email is sent to the address you provided at checkout. That email contains your
       access document, which holds the links to every item in the product.</p>
       <p>Delivery normally completes within a few minutes. In rare cases email delivery may take up
       to 24 hours.</p>"""),
    ("If you do not receive it", f"""<p>If your access email has not arrived, please check your spam
       and promotions folders first, as automated emails are sometimes filtered there.</p>
       <p>If you still cannot find it, email <a href="mailto:{B['email']}">{B['email']}</a> from the
       address used at checkout and we will resend your access {B['response']}.</p>
       <p>Where we have had to resend, your 24-hour access window runs from the moment working
       access reaches you &mdash; not from the time of your original purchase. You are never
       penalised for a delivery problem on our side.</p>"""),
    ("Access window", """<p>The access links inside the product are guaranteed to work for
       <strong>24 hours from the time of purchase</strong>, or from the moment working access
       reaches you if we have had to resend it. Within that window you should save every item to
       your own account or device.</p>
       <p>Anything you have saved or copied within that window is yours to keep and use permanently.
       Because the underlying files are hosted on third-party platforms, we cannot guarantee that the
       links will remain available beyond the first 24 hours. This is stated clearly inside the
       product itself, on this page, and before purchase.</p>"""),
    ("What you need", """<p>To use our products you need an internet connection, a web browser, and
       a free account on the design platform referenced in the product. A desktop or laptop computer
       is recommended. No paid software is required.</p>"""),
  ]))

# ------------------------------ REFUNDS ------------------------------------
PAGES["refunds.html"] = ("Refund &amp; Cancellation Policy",
  f"Refund and cancellation terms for {B['name']}.",
  policy_page("Refund &amp; Cancellation Policy",
              "Please read this before purchasing.", [
    ("Summary", """<p>Our products are digital and are delivered in full the moment payment is
       confirmed. For that reason we do not offer refunds once access has been delivered. The one
       exception is where you were unable to access what you paid for because of a fault on our
       side, in which case we will restore access or refund you in full.</p>"""),
    ("Cancellation", """<p>Orders cannot be cancelled after payment, because delivery is immediate
       and access is granted at the moment of purchase. There is no subscription, recurring charge
       or renewal to cancel &mdash; every purchase is a single one-time payment.</p>"""),
    ("When we will refund you", f"""<p>We will issue a full refund if:</p>
       <ul>
         <li>You were charged more than once for the same order; or</li>
         <li>You did not receive your access email and we were unable to deliver it to you; or</li>
         <li>The access links did not work during the guaranteed 24-hour access window and we were
             unable to provide working replacements.</li>
       </ul>
       <p>To request a refund on any of these grounds, email
       <a href="mailto:{B['email']}">{B['email']}</a> within <strong>24 hours</strong> of your
       purchase, from the email address used at checkout, describing the problem.</p>"""),
    ("When we cannot refund you", """<p>Because the product is delivered digitally and in full at
       the point of sale, we are unable to offer refunds where:</p>
       <ul>
         <li>You have received and accessed the product and simply changed your mind;</li>
         <li>You did not save the files within the stated 24-hour access window;</li>
         <li>You did not achieve a particular result, income or audience growth from using the
             product. We make no such guarantees, and none should be inferred;</li>
         <li>You purchased the wrong product by mistake but have already accessed it.</li>
       </ul>"""),
    ("How refunds are processed", """<p>Approved refunds are issued to the original payment method
       through our payment gateway partner. Once approved, refunds are initiated within 3 business
       days and typically reach your account within 5 to 7 business days, depending on your bank or
       card issuer.</p>
       <p>We will confirm by email when a refund has been initiated.</p>"""),
    ("Contact", f"""<p>All refund and cancellation queries should be sent to
       <a href="mailto:{B['email']}">{B['email']}</a>. We respond {B['response']}.</p>"""),
  ]))

# ------------------------------- TERMS -------------------------------------
PAGES["terms.html"] = ("Terms &amp; Conditions",
  f"Terms and conditions for using {B['name']} and buying our products.",
  policy_page("Terms &amp; Conditions",
              f"The terms on which {B['name']} sells to you.", [
    ("Agreement", f"""<p>These Terms and Conditions govern your use of this website and your
       purchase of any product from {B['name']} ("we", "us", "our"). By using this website or buying
       from us, you agree to these terms. If you do not agree, please do not use the site or buy
       from us.</p>"""),
    ("Eligibility", """<p>You must be at least 18 years old and legally capable of entering into a
       contract in order to purchase from us. By placing an order you confirm that you meet these
       conditions and that the information you provide at checkout is accurate.</p>"""),
    ("Our products", """<p>We sell digital products consisting of editable templates, written
       content libraries, planning documents and instructional guides. Product descriptions on this
       site set out what is included. Nothing physical is sold or shipped.</p>"""),
    ("Licence to use our products", f"""<p>When you buy a product, {B['name']} grants you a
       non-exclusive, non-transferable licence to use it for your own personal or business purposes,
       including commercially in your own content.</p>
       <p>You may not resell, redistribute, share, sub-license or publish the product or its access
       links, in whole or in part, and you may not upload it to any public drive, channel or
       file-sharing service.</p>"""),
    ("Pricing and payment", """<p>Prices are listed on our Pricing page and are payable in Indian
       Rupees. Payment is collected online through our payment gateway partner. We do not collect,
       see or store your card, UPI or banking credentials at any point.</p>
       <p>We may change our prices at any time. Any change applies only to purchases made after the
       change and never retroactively to an order already placed.</p>"""),
    ("Delivery and access", """<p>Delivery is digital and immediate. Access links are guaranteed for
       24 hours from purchase, as set out in our Delivery Policy. You are responsible for saving the
       files to your own account or device within that window.</p>"""),
    ("Refunds", """<p>Our refund and cancellation terms are set out in full in our Refund &amp;
       Cancellation Policy, which forms part of these terms.</p>"""),
    ("No guarantee of results", """<p>Our products are educational and practical tools. We do not
       guarantee any particular outcome, including audience growth, engagement, income or business
       success. Any examples given are illustrative and are not a promise of results. What you
       achieve depends on your own effort and circumstances.</p>"""),
    ("Intellectual property", f"""<p>All content on this website, including text, layout and design,
       is the property of {B['name']} unless otherwise stated, and may not be copied or reproduced
       without permission.</p>"""),
    ("Limitation of liability", f"""<p>To the fullest extent permitted by law, {B['name']} shall not
       be liable for any indirect, incidental or consequential loss arising from the use of, or
       inability to use, our products or this website. Our total liability in respect of any order
       shall not exceed the amount you paid for that order.</p>"""),
    ("Changes to these terms", """<p>We may update these terms from time to time. The version
       published on this page at the time of your purchase is the version that applies to that
       purchase. The date of the most recent update is shown at the top of this page.</p>"""),
    ("Governing law", f"""<p>These terms are governed by the laws of India, and any dispute arising
       out of or in connection with them shall be subject to the exclusive jurisdiction of the
       courts of India.</p>"""),
    ("Contact", f"""<p>Questions about these terms can be sent to
       <a href="mailto:{B['email']}">{B['email']}</a>.</p>"""),
  ]))

# ------------------------------ PRIVACY ------------------------------------
PAGES["privacy.html"] = ("Privacy Policy",
  f"How {B['name']} collects, uses and protects your personal information.",
  policy_page("Privacy Policy",
              "What we collect, why we collect it, and what we do with it.", [
    ("Overview", f"""<p>This policy explains what personal information {B['name']} collects when you
       visit this website or buy from us, how we use it, and the choices you have. We collect as
       little as possible and we do not sell your data to anyone.</p>"""),
    ("Information we collect", """<p>When you make a purchase we collect your name, your email
       address, and the details of what you bought. This is the information we need in order to
       deliver your product and provide support.</p>
       <p>When you contact us by email, we hold that correspondence so that we can answer you and
       keep a record of the issue.</p>"""),
    ("Payment information", """<p>We do not collect, process or store your card, UPI or banking
       details at any point. All payments are handled directly by our payment gateway partner, which
       is responsible for the security of that information under its own privacy policy and under
       applicable regulations. We receive only confirmation that a payment succeeded, along with the
       order details.</p>"""),
    ("How we use your information", """<p>We use your information only to:</p>
       <ul>
         <li>deliver the product you purchased;</li>
         <li>send you the receipt and access details for your order;</li>
         <li>respond to your support requests;</li>
         <li>keep records of transactions as required by law.</li>
       </ul>
       <p>We do not use your information for automated profiling or advertising, and we do not sell,
       rent or trade it.</p>"""),
    ("Sharing your information", """<p>We share information only where it is necessary to run the
       business: with our payment gateway partner in order to process your payment, and with the
       email service used to deliver your order. These providers may only use the information to
       perform that service for us.</p>
       <p>We may also disclose information where we are required to do so by law.</p>"""),
    ("Cookies", """<p>This website is a static informational site and does not set advertising or
       tracking cookies. If you proceed to our payment gateway partner's checkout, that service may
       set its own cookies, governed by its privacy policy.</p>"""),
    ("Data retention", """<p>We keep order records for as long as necessary to provide support and
       to meet our legal and tax obligations. Support correspondence is retained only as long as it
       is useful for resolving your query.</p>"""),
    ("Security", """<p>We take reasonable steps to protect the information we hold against loss,
       misuse and unauthorised access. No method of transmission or storage is completely secure, and
       we cannot guarantee absolute security.</p>"""),
    ("Your rights", f"""<p>You may ask us what personal information we hold about you, ask us to
       correct it if it is wrong, or ask us to delete it where we are not required to keep it. Write
       to <a href="mailto:{B['email']}">{B['email']}</a> and we will respond {B['response']}.</p>"""),
    ("Children", """<p>Our products are not directed at children. We do not knowingly collect
       personal information from anyone under 18.</p>"""),
    ("Changes to this policy", """<p>We may update this policy from time to time. The current
       version is always published on this page, with the date of the last update shown at the
       top.</p>"""),
    ("Contact", f"""<p>Questions about privacy or your data can be sent to
       <a href="mailto:{B['email']}">{B['email']}</a>.</p>"""),
  ]))


# ---------------------------------------------------------------------------
def link_list(items, current):
    out = []
    for href, label in items:
        cls = ' class="active"' if href == current else ""
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "\n        ".join(out)


def build():
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "assets"), exist_ok=True)
    for filename, (title, desc, body) in PAGES.items():
        html = LAYOUT.format(
            title=title, name=B["name"], desc=desc, body=body,
            nav=link_list(NAV, filename),
            footer_nav=link_list(NAV, filename),
            footer_policies=link_list(FOOTER_POLICIES, filename),
            tagline=B["tagline"], email=B["email"], year=2026,
            cta=(CTA_HTML if filename in CTA_PAGES else ""),
        )
        with open(os.path.join(here, filename), "w") as f:
            f.write(html)
        print("wrote", filename)


if __name__ == "__main__":
    build()
