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

Replace every remaining placeholder. Check with:

```
grep -o '\[\[[A-Z_]*\]\]' *.html | sort -u
```

Required:

- `[[SUPPORT_EMAIL]]` — a real, monitored address
- `[[PHONE_NUMBER]]` — a reachable number
- `[[BUSINESS_ADDRESS]]` — must match KYC records
- `[[CITY]]` — jurisdiction named in Terms

Also set `checkout` in `build.py` to the live payment page URL once it exists.
