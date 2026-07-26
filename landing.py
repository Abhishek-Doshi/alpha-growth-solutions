#!/usr/bin/env python3
"""
Sales landing page for The Faceless Creator Kit.

Deliberately separate from the corporate site (index/about/pricing/contact):
  - the corporate site is the compliance surface Razorpay verified — keep it boring
  - this page is the ad destination — one job, one CTA, no navigation to leak clicks

Run via build.py, which imports and renders this.
"""

LANDING_FILE = "faceless-creator-kit.html"

LANDING_LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{product} &middot; {name}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0b1220">
<meta property="og:title" content="{product}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="product">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="alternate icon" type="image/png" href="assets/favicon-180.png">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@700;800&display=swap">
<link rel="stylesheet" href="assets/styles.css?v={cssver}">
{pixel}
</head>
<body class="lp">

<header class="lp-header">
  <div class="wrap lp-header-inner">
    <a class="brand" href="index.html">
      <span class="ags-badge">AGS</span>
      <span class="brand-name">{name}</span>
    </a>
    <a class="btn btn-sm" href="{checkout}" data-cta="header">Get the kit &mdash; {price}</a>
  </div>
</header>

{body}

<footer class="lp-footer">
  <div class="wrap">
    <div class="lp-foot-top">
      <span class="ags-badge inv">AGS</span>
      <span>{name}</span>
    </div>
    <div class="lp-foot-links">
      <a href="index.html">Home</a>
      <a href="pricing.html">Pricing</a>
      <a href="contact.html">Contact</a>
      <a href="delivery.html">Delivery Policy</a>
      <a href="refunds.html">Refund &amp; Cancellation</a>
      <a href="terms.html">Terms</a>
      <a href="privacy.html">Privacy</a>
    </div>
    <p class="lp-foot-note">
      Digital product. Delivered by email immediately after payment. No physical goods are shipped.
      Results depend on your own effort &mdash; we make no income or audience-growth guarantees.
    </p>
    <div class="lp-foot-bar">&copy; 2026 {name}. All rights reserved.</div>
  </div>
</footer>
</body>
</html>
"""


def render_body(B, P):
    cta = B["checkout"]
    return f"""
<section class="lp-hero">
  <div class="wrap">
    <p class="eyebrow">For creators who don't want to be on camera</p>
    <h1>Publish short-form video<br><span class="gradient-text">without showing your face</span></h1>
    <p class="lp-lede">A complete, ready-to-edit system &mdash; video templates, a hook library, a
       90-day content calendar and the guides that tie them together. Stop staring at a blank
       timeline and start posting this week.</p>

    <div class="lp-buy">
      <div class="lp-price"><span class="amt">{P}</span><span class="per">one-time &middot; no subscription</span></div>
      <a class="btn btn-lg" href="{cta}" data-cta="hero">Get instant access</a>
    </div>

    <div class="hero-badges">
      <span class="pill">{{check}} Instant email delivery</span>
      <span class="pill">{{check}} UPI, cards &amp; net banking</span>
      <span class="pill">{{check}} Yours to keep</span>
    </div>
  </div>
</section>

<main class="wrap">

  <section class="band">
    <div class="band-head">
      <p class="eyebrow">The problem</p>
      <h2>Nobody quits because it's hard.<br>They quit because it's blank.</h2>
    </div>
    <div class="grid grid-3">
      <div class="card"><h3>No idea what to post</h3>
        <p>You open the app, stare at it, and close it again. The hardest part was never the editing.</p></div>
      <div class="card"><h3>You don't want to be on camera</h3>
        <p>Plenty of people won't film themselves &mdash; and every guide assumes you will.</p></div>
      <div class="card"><h3>Starting from zero, every time</h3>
        <p>Building a template from scratch for each post is why week three never happens.</p></div>
    </div>
  </section>

  <section class="band">
    <div class="band-head">
      <p class="eyebrow">What you get</p>
      <h2>Nineteen assets, organised into one system</h2>
      <p>Delivered as a single access document. Everything opens in a free browser-based editor.</p>
    </div>
    <div class="grid grid-2">
      <div class="card"><h3>6 &times; reel template packs</h3>
        <p>Editable short-form video templates in several visual styles, plus matching cover
           designs so your profile grid reads as one brand.</p></div>
      <div class="card"><h3>Hook &amp; script library</h3>
        <p>A library of opening lines you can adapt to any topic, plus story templates and two
           full social planners.</p></div>
      <div class="card"><h3>5 &times; guides &amp; playbooks</h3>
        <p>Faceless production, YouTube automation, growth mechanics, email, and a crash course
           on the editor itself.</p></div>
      <div class="card"><h3>90-day content calendar</h3>
        <p>A dated plan with one post idea per day, so the question of what to make next is
           already answered.</p></div>
    </div>
  </section>

  <section class="band">
    <div class="band-head">
      <p class="eyebrow">How it works</p>
      <h2>From payment to posting</h2>
    </div>
    <ol class="steps">
      <li><h3>Pay securely</h3>
        <p>Checkout is handled by our payment gateway partner. UPI, cards, net banking and wallets.
           We never see or store your payment details.</p></li>
      <li><h3>Get your access email immediately</h3>
        <p>A document with links to all nineteen assets arrives at the address you use at checkout,
           within minutes.</p></li>
      <li><h3>Save everything, then start</h3>
        <p>Copy each template into your own account. Once saved, it's yours permanently. The
           7-day quick-start plan tells you exactly what to do first.</p></li>
    </ol>
  </section>

  <section class="band">
    <div class="band-head">
      <p class="eyebrow">Honest fit</p>
      <h2>Who this is and isn't for</h2>
    </div>
    <div class="grid grid-2">
      <div class="card">
        <h3>A good fit if&hellip;</h3>
        <ul class="check">
          <li>You want to post short-form video without appearing on camera</li>
          <li>You'd rather adapt a working system than build one</li>
          <li>You can commit to posting consistently for a month</li>
          <li>You're comfortable editing in a browser-based design tool</li>
        </ul>
      </div>
      <div class="card">
        <h3>Not for you if&hellip;</h3>
        <ul class="check cross">
          <li>You're looking for guaranteed income &mdash; we promise none</li>
          <li>You want done-for-you content rather than templates</li>
          <li>You expect ongoing coaching or account management</li>
          <li>You won't publish anything unless it's perfect</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="note-box">
      <h3 style="margin-top:0">Before you buy, two things to know</h3>
      <p><strong>Save your files within 24 hours.</strong> The access links are guaranteed to work
         for 24 hours from purchase. Copy everything into your own account in that window and it's
         yours permanently &mdash; full detail in the <a href="delivery.html">Delivery Policy</a>.</p>
      <p style="margin-bottom:0"><strong>This is a toolkit, not a guarantee.</strong> What you get
         out of it depends on what you put in. We make no claims about income, followers or
         results, and you should be sceptical of anyone who does.</p>
    </div>
  </section>

  <section class="band">
    <div class="band-head">
      <p class="eyebrow">Questions</p>
      <h2>Before you ask</h2>
    </div>
    <div class="faq">
      <div class="faq-item"><h3>Do I need paid software?</h3>
        <p>No. A free account on the browser-based design tool referenced in the kit is enough.
           A laptop or desktop is recommended for the initial setup.</p></div>
      <div class="faq-item"><h3>Is this a subscription?</h3>
        <p>No. It's a single one-time payment of {P}. There is nothing to cancel and no renewal.</p></div>
      <div class="faq-item"><h3>How fast is delivery?</h3>
        <p>Immediate. The access email is sent as soon as payment is confirmed, usually within a
           few minutes. Check spam if you don't see it.</p></div>
      <div class="faq-item"><h3>Can I get a refund?</h3>
        <p>Because the product is delivered in full at the moment of purchase, we don't refund
           change-of-mind. We do refund in full if you were charged twice, never received access,
           or the links failed and we couldn't replace them. See the
           <a href="refunds.html">Refund Policy</a>.</p></div>
      <div class="faq-item"><h3>Do I need an existing audience?</h3>
        <p>No. The kit is built for starting from zero &mdash; that's the point of the 90-day
           calendar and the quick-start plan.</p></div>
      <div class="faq-item"><h3>Where do I get background footage?</h3>
        <p>The production guide shows you how to source it from free, commercially usable
           libraries. No copyright-strike stock footage is bundled or needed.</p></div>
    </div>
  </section>

</main>

<section class="lp-final">
  <div class="wrap">
    <h2>Start posting this week</h2>
    <p>Templates, hooks, a calendar and the guides to use them &mdash; delivered to your inbox in
       the next few minutes.</p>
    <div class="lp-buy centered">
      <div class="lp-price"><span class="amt light">{P}</span><span class="per light">one-time</span></div>
      <a class="btn btn-light btn-lg" href="{cta}" data-cta="footer">Get instant access</a>
    </div>
    <p class="lp-fine">Secure checkout &middot; UPI, cards &amp; net banking &middot; Instant email delivery</p>
  </div>
</section>
"""
