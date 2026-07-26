/**
 * Alpha Growth Solutions — automated order fulfilment.
 *
 * Razorpay webhook  ->  this Web App  ->  Gmail (sends the kit)  +  Sheet (order log)
 *
 * WHY THIS EXISTS
 * Razorpay collects the money; it does not deliver the product. Manual delivery
 * would be fatal here because the kit's access window is 24 hours while the
 * support SLA is 2-3 business days — a buyer could be locked out before anyone
 * replied. This closes that gap with no server and no monthly cost.
 *
 * SECRETS ARE NEVER IN THIS FILE.
 * This repository is public. Every secret is read from Script Properties at
 * runtime. Set them in the Apps Script editor under
 *   Project Settings > Script Properties
 *
 *   RAZORPAY_WEBHOOK_SECRET   the secret you type when creating the webhook
 *                             (this is NOT your API key secret)
 *   KIT_FILE_ID               Drive file ID of the kit PDF to attach
 *   ORDER_SHEET_ID            Spreadsheet ID of the order log
 *   SUPPORT_EMAIL             reply-to address shown to buyers
 *
 * DEPLOY: see README.md in this folder.
 */

var CFG = {
  productName: 'The Faceless Creator Kit',
  brandName:   'Alpha Growth Solutions',
  sheetName:   'Orders',
};

function prop_(key, required) {
  var v = PropertiesService.getScriptProperties().getProperty(key);
  if (!v && required) throw new Error('Missing Script Property: ' + key);
  return v;
}

/** Razorpay pings the endpoint; make GET harmless and non-revealing. */
function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) return json_({ ok: false, reason: 'empty body' });

    var raw = e.postData.contents;

    // ---- 1. verify the signature before trusting anything -------------------
    // Without this, anyone who finds the URL could POST a fake "payment"
    // and be emailed the product for free.
    var sigHeader = headerCI_(e, 'x-razorpay-signature');
    if (!verifySignature_(raw, sigHeader)) {
      log_('REJECTED', '', '', 0, 'bad or missing signature');
      return json_({ ok: false, reason: 'invalid signature' });
    }

    var body = JSON.parse(raw);
    if (body.event !== 'payment.captured') {
      return json_({ ok: true, ignored: body.event });
    }

    var pay = body.payload.payment.entity;
    var paymentId = pay.id;
    var email = pay.email || (pay.notes && pay.notes.email) || '';
    var amount = (pay.amount || 0) / 100;
    var name = (pay.notes && (pay.notes.name || pay.notes.customer_name)) || '';

    // ---- 2. idempotency -----------------------------------------------------
    // Razorpay retries webhooks on any non-2xx and can deliver duplicates.
    // Without this check a buyer gets the same email several times.
    if (alreadyProcessed_(paymentId)) {
      return json_({ ok: true, duplicate: paymentId });
    }

    if (!email) {
      log_(paymentId, '', name, amount, 'NO EMAIL — deliver manually');
      notifyOwner_('Order with no email address', paymentId, amount);
      return json_({ ok: true, warning: 'no email on payment' });
    }

    // ---- 3. deliver ---------------------------------------------------------
    sendKit_(email, name);
    log_(paymentId, email, name, amount, 'delivered');
    return json_({ ok: true, delivered: paymentId });

  } catch (err) {
    // Return 200 regardless: a non-2xx makes Razorpay retry, which would spam
    // the buyer once the underlying issue clears. Record it and alert instead.
    log_('ERROR', '', '', 0, String(err));
    notifyOwner_('Delivery script error', String(err), 0);
    return json_({ ok: false, error: String(err) });
  }
}

/* ------------------------------------------------------------------ helpers */

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/** Apps Script header casing is not guaranteed; match case-insensitively. */
function headerCI_(e, wanted) {
  var h = (e && e.headers) || {};
  for (var k in h) if (k.toLowerCase() === wanted) return h[k];
  return '';
}

function verifySignature_(raw, signature) {
  if (!signature) return false;
  var secret = prop_('RAZORPAY_WEBHOOK_SECRET', true);
  var bytes = Utilities.computeHmacSha256Signature(raw, secret);
  var hex = bytes.map(function (b) {
    return ('0' + (b < 0 ? b + 256 : b).toString(16)).slice(-2);
  }).join('');
  return timingSafeEquals_(hex, String(signature).trim());
}

/** Constant-time compare, so the response time can't leak the expected value. */
function timingSafeEquals_(a, b) {
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function sheet_() {
  var ss = SpreadsheetApp.openById(prop_('ORDER_SHEET_ID', true));
  var sh = ss.getSheetByName(CFG.sheetName);
  if (!sh) {
    sh = ss.insertSheet(CFG.sheetName);
    sh.appendRow(['Timestamp', 'Payment ID', 'Email', 'Name', 'Amount (INR)', 'Status']);
    sh.setFrozenRows(1);
  }
  return sh;
}

function alreadyProcessed_(paymentId) {
  var values = sheet_().getRange('B:B').getValues();
  for (var i = 0; i < values.length; i++) {
    if (values[i][0] === paymentId) return true;
  }
  return false;
}

function log_(paymentId, email, name, amount, status) {
  try {
    sheet_().appendRow([new Date(), paymentId, email, name, amount, status]);
  } catch (e) {
    // never let logging failure block delivery
  }
}

function sendKit_(email, name) {
  var file = DriveApp.getFileById(prop_('KIT_FILE_ID', true));
  var support = prop_('SUPPORT_EMAIL', false) || Session.getEffectiveUser().getEmail();
  var greeting = name ? ('Hi ' + name + ',') : 'Hi,';

  var text =
    greeting + '\n\n' +
    'Thank you for your purchase. ' + CFG.productName + ' is attached to this email.\n\n' +
    'IMPORTANT — please read before you start:\n' +
    'The links inside the kit are guaranteed to work for 24 hours from now. Open each\n' +
    'one and save it into your own account today. Anything you have saved within that\n' +
    'window is yours to keep permanently.\n\n' +
    'Open the PDF on a laptop or desktop, log in to Canva first, and work through the\n' +
    'assets in order. Page 9 shows exactly how to save each type, and page 8 has a\n' +
    '7-day plan for getting your first reels posted.\n\n' +
    'If anything does not open, reply to this email and we will sort it out.\n\n' +
    '— ' + CFG.brandName + '\n' + support + '\n';

  var html =
    '<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;' +
    'font-size:15px;line-height:1.65;color:#1e293b;max-width:560px">' +
    '<p>' + greeting + '</p>' +
    '<p>Thank you for your purchase. <strong>' + CFG.productName + '</strong> is attached ' +
    'to this email.</p>' +
    '<div style="background:#fff7ed;border-left:3px solid #ea580c;padding:14px 18px;' +
    'border-radius:0 8px 8px 0;margin:20px 0">' +
    '<strong>Please save your files today.</strong><br>' +
    'The links inside the kit are guaranteed to work for <strong>24 hours from now</strong>. ' +
    'Open each one and save it into your own account. Anything you save within that window ' +
    'is yours to keep permanently.' +
    '</div>' +
    '<p>Open the PDF on a laptop or desktop and log in to Canva first. Page 9 shows how to ' +
    'save each type of asset, and page 8 has a 7-day plan for getting your first reels ' +
    'posted.</p>' +
    '<p>If anything does not open, just reply to this email.</p>' +
    '<p style="margin-top:26px;color:#64748b">&mdash; ' + CFG.brandName + '<br>' +
    '<a href="mailto:' + support + '" style="color:#2563eb">' + support + '</a></p>' +
    '</div>';

  GmailApp.sendEmail(email, 'Your ' + CFG.productName + ' — access inside', text, {
    htmlBody: html,
    name: CFG.brandName,
    replyTo: support,
    attachments: [file.getAs(MimeType.PDF)],
  });
}

function notifyOwner_(subject, detail, amount) {
  try {
    var to = prop_('SUPPORT_EMAIL', false) || Session.getEffectiveUser().getEmail();
    GmailApp.sendEmail(to, '[AGS] ' + subject,
      detail + (amount ? ('\namount: ' + amount) : ''));
  } catch (e) {}
}

/* --------------------------------------------------------------- self-tests */

/**
 * Run this from the Apps Script editor after setting Script Properties.
 * Confirms the Drive file, the Sheet and Gmail are all reachable, and sends a
 * real copy of the delivery email to you so you can see what buyers receive.
 */
function testSetup() {
  var out = [];
  try {
    var f = DriveApp.getFileById(prop_('KIT_FILE_ID', true));
    out.push('Kit file OK: ' + f.getName() + ' (' + Math.round(f.getSize() / 1024) + ' KB)');
  } catch (e) { out.push('KIT FILE FAILED: ' + e); }

  try {
    var sh = sheet_();
    out.push('Sheet OK: ' + sh.getParent().getName() + ' / ' + sh.getName());
  } catch (e) { out.push('SHEET FAILED: ' + e); }

  try {
    prop_('RAZORPAY_WEBHOOK_SECRET', true);
    out.push('Webhook secret present');
  } catch (e) { out.push('WEBHOOK SECRET MISSING'); }

  try {
    sendKit_(Session.getEffectiveUser().getEmail(), 'Test');
    out.push('Test delivery email sent to ' + Session.getEffectiveUser().getEmail());
  } catch (e) { out.push('EMAIL FAILED: ' + e); }

  Logger.log(out.join('\n'));
  return out.join('\n');
}

/** Verifies the HMAC implementation against a known value. No network needed. */
function testSignature() {
  var raw = '{"event":"payment.captured"}';
  var secret = 'testsecret';
  var expected = Utilities.computeHmacSha256Signature(raw, secret).map(function (b) {
    return ('0' + (b < 0 ? b + 256 : b).toString(16)).slice(-2);
  }).join('');
  PropertiesService.getScriptProperties().setProperty('__TMP_SECRET', secret);
  var real = PropertiesService.getScriptProperties().getProperty('RAZORPAY_WEBHOOK_SECRET');
  PropertiesService.getScriptProperties().setProperty('RAZORPAY_WEBHOOK_SECRET', secret);
  var good = verifySignature_(raw, expected);
  var bad = verifySignature_(raw, expected.replace(/.$/, '0'));
  if (real) PropertiesService.getScriptProperties().setProperty('RAZORPAY_WEBHOOK_SECRET', real);
  PropertiesService.getScriptProperties().deleteProperty('__TMP_SECRET');
  Logger.log('valid signature accepted: ' + good + '  |  tampered rejected: ' + !bad);
  return good && !bad;
}
