# How to Contribute to the SSL Decryption Bypass List

Thank you for your help to keep enterprise networks operational and secure. 

Bypassing SSL/TLS decryption creates a security risk. Therefore, you must follow strict rules to add items to this repository.

---

## 🛑 Rules for Inclusion

Before you submit a pull request, verify that your domain meets all of these requirements:

1. **Service Failure:** The service or application must fail or stop connection when a custom root CA intercepts it.
2. **Technical Cause:** Certificate pinning, non-HTTP TLS wrappers, or mutual TLS (mTLS) must cause the failure.
3. **Small Scope:** Add only the necessary domains. Do not add `*.google.com` if only `dl.google.com` or `*.gvt1.com` fails.

### Rejected Submissions ❌
* Websites that operate correctly with TLS inspection.
* Lists for ad-blocking or privacy.
* Top-level domains or wildcard domains that stop more inspection than necessary.
* IP address ranges. This project tracks only fully qualified domain names (FQDNs).

---

## 📥 How to Submit Changes

### 1. Add Static Domains (`static/`)
If a vendor does not provide an automated API for their endpoints, complete these steps:
1. Find or create a text file in the `static/` directory (for example, `static/02_apple.txt`).
2. Add the minimum required FQDNs. Write one FQDN on each line.
3. You can write comments (`# reason`) in static files to provide context.

```text
# Apple Push Notification Service (Certificate Pinned)
*.push.apple.com

```

### 2. Add Dynamic Scripts (`dynamic/`)

If a vendor provides an official API endpoint:

1. Create a Python script (`.py`) or a Bash script (`.sh`) in the `dynamic/` directory.
2. Make sure your script writes raw FQDN lines into a temporary file. Name the file `dynamic_<vendor>_fqdn.tmp` in the root directory.
3. Do not create headers or sort files in your script. The `build.py` file automatically combines and cleans all data.

---

## 🧪 Local Testing

Before you submit your pull request, test the build script on your local computer:

```bash
python3 build.py

```

Make sure that:

* The build finishes without errors.
* The process creates and deletes your temporary `.tmp` files.
* The system creates the `dist/ssl-bypass-fqdn.txt` file. Do not commit the `dist/` directory. Git ignores this directory, and Cloudflare Pages compiles it automatically.