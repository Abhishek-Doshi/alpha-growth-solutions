# Order fulfilment — setup

Razorpay collects payment but does not deliver the product. This Apps Script closes
that gap: it receives the Razorpay webhook, verifies it, emails the kit, and logs
the order. Free, no server, no monthly cost.

```
Razorpay payment.captured
        ↓  webhook (signed)
Apps Script Web App          ← verifies HMAC before trusting anything
        ↓
Gmail: kit PDF to buyer   +   Google Sheet: order row
```

## One-time setup

**1. Upload the kit to Drive**
Put `The-Faceless-Creator-Kit.pdf` in Drive. Open it and copy the file ID from the URL:
`drive.google.com/file/d/`**`THIS_PART`**`/view`

**2. Create the order log**
New Google Sheet, name it `AGS Orders`. Copy its ID from the URL the same way.
The script creates and formats the `Orders` tab on first run.

**3. Create the Apps Script**
[script.google.com](https://script.google.com) → New project → name it `AGS Delivery`.
Replace the default file contents with `Code.gs` from this folder.

**4. Add the secrets** — Project Settings → Script Properties:

| Property | Value |
|---|---|
| `RAZORPAY_WEBHOOK_SECRET` | a strong random string you invent (used again in step 6) |
| `KIT_FILE_ID` | Drive file ID from step 1 |
| `ORDER_SHEET_ID` | Sheet ID from step 2 |
| `SUPPORT_EMAIL` | `alphagrowthsolutions.biz@gmail.com` |

Secrets live here, never in the code — this repository is public.

**5. Deploy**
Deploy → New deployment → type **Web app**.
- Execute as: **Me**
- Who has access: **Anyone**

"Anyone" is required — Razorpay's servers call this unauthenticated. It is safe
because the script rejects any request without a valid signature. Authorise the
scopes when prompted, then copy the `/exec` URL.

**6. Point Razorpay at it**
Razorpay Dashboard → Settings → Webhooks → Add New Webhook.
- URL: the `/exec` URL from step 5
- Secret: the same string as `RAZORPAY_WEBHOOK_SECRET`
- Active event: **`payment.captured`** only

**7. Verify before taking real money**
In the Apps Script editor run `testSignature` (checks the HMAC logic, no network),
then `testSetup` (checks Drive, Sheet and Gmail, and sends you a real copy of the
buyer email). Then make one live ₹1 test purchase end to end.

## Design notes

**Signature verification is the security boundary.** The endpoint is public. Without
the HMAC check anyone who found the URL could POST a fake `payment.captured` and be
emailed the product for free. Verification happens before the payload is parsed.

**Idempotency.** Razorpay retries on any non-2xx and can send duplicates. Each
`payment_id` is checked against the sheet before sending, so a buyer never gets the
same email twice.

**Always returns 200.** Even on error. A non-2xx makes Razorpay retry, which would
re-send the email once the underlying problem cleared. Failures are written to the
sheet and emailed to you instead.

**Gmail sending quota.** A consumer Gmail account allows ~100 recipients/day from
Apps Script; Workspace allows ~1,500. At ₹499 that ceiling is roughly ₹50,000/day of
orders — fine to launch on, but move to a transactional email provider before you
approach it.

**Email is required.** Configure the Razorpay Payment Page to make the email field
mandatory. If a payment arrives without one, the order is logged as
`NO EMAIL — deliver manually` and you are alerted rather than the buyer being
silently dropped.
