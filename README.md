# Alpha Growth Solutions — website

Static site published with GitHub Pages. Serves as the public business site and
carries the policy pages required for payment gateway verification.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home — what the business does, product, how buying works |
| `about.html` | About Us |
| `pricing.html` | Pricing, what's included, taxes, payment methods |
| `contact.html` | Contact Us — email, phone, address, support hours |
| `delivery.html` | Delivery Policy (digital delivery, access window) |
| `refunds.html` | Refund & Cancellation Policy |
| `terms.html` | Terms & Conditions |
| `privacy.html` | Privacy Policy |

Every page links to all of the above from the footer.

## Editing

Do not edit the `.html` files directly — they are generated. Edit the `BUSINESS`
block at the top of `build.py`, then regenerate:

```
python3 build.py
```

Commit and push; GitHub Pages redeploys automatically.

## Before submitting for verification

- [ ] Set `checkout` in `build.py` to the live Razorpay Payment Page URL (currently `#`)
- [ ] Confirm `alphagrowthsolutions.biz@gmail.com` is monitored — reviewers may email it
- [ ] Consider a custom domain; a `github.io` subdomain is an easy reason to be rejected

Sanity check for unfilled placeholders before any submission:

```
grep -o '\[\[[A-Z_]*\]\]' *.html | sort -u
```

## Notes

Contact is email-only by choice — no phone number or postal address is published.
Reviewers sometimes expect one of those on the Contact page, so if the account is
rejected on contactability, adding a phone number is the first thing to try.
