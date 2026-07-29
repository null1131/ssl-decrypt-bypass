# Contributing to the SSL Decryption Bypass List

Thank you for helping keep enterprise networks running smoothly without compromising security unnecessarily. 

Because bypassing SSL/TLS decryption creates a deliberate security blind spot, we maintain **extremely strict criteria** for what gets added to this repository.

---

## 🛑 Strict Inclusion Criteria

Before submitting a Pull Request, verify that your domain meets **ALL** of the following requirements:

1. **Hard Service Breakage:** The service or application must actively fail, crash, or refuse to connect when intercepted by a custom root CA.
2. **Technical Reason:** The failure must be caused by certificate pinning, proprietary/non-HTTP TLS wrappers, or mutual TLS (mTLS).
3. **Minimal Scope:** Submissions must be as granular as possible. Do not submit `*.google.com` if only `dl.google.com` or `*.gvt1.com` breaks.

### What Will Be Rejected ❌
* "Trusted" websites (e.g., news sites, enterprise SaaS) that function fine under TLS inspection.
* General ad-blocking or privacy lists.
* Broad top-level domains or wildcard domains that break more inspection than necessary.
* Full IP ranges (this project strictly tracks FQDNs).

---

## 📥 How to Submit Changes

### 1. Adding Static Domains (`static/`)
If a vendor does not provide an automated JSON/REST API for their endpoints:
1. Locate or create an appropriately named text file in `static/` (e.g., `static/02_apple.txt`).
2. Add the minimum required FQDNs (one per line).
3. Inline comments (`# reason`) are encouraged in static files for context.

```text
# Apple Push Notification Service (Cert Pinned)
*.push.apple.com
```

### 2. Adding Dynamic Ingestion Scripts (`dynamic/`)

If a vendor provides an official API endpoint (like Microsoft, Zoom, or AWS):

1. Create a script in `dynamic/` using Python (`.py`) or Bash (`.sh`).
2. Your script **must** write its extracted, raw FQDN lines into a temporary file named `dynamic_<vendor>_fqdn.tmp` in the root directory.
3. Do not handle header creation or file sorting in your dynamic script—`build.py` handles aggregation and cleaning automatically.

---

## 🧪 Local Testing

Before submitting your PR, test the build script locally to ensure there are no syntax errors or broken dynamic pulls:

```bash
python3 build.py
```

Verify that:

* The build completes without errors.
* Your temporary `.tmp` files were created and cleaned up.
* `dist/ssl-bypass-fqdn.txt` is generated cleanly. *(Do not commit the `dist/` directory; it is ignored by Git and compiled automatically by Cloudflare Pages).*