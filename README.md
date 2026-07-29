# Enterprise SSL/TLS Decryption Bypass List

An automated, minimal, community-curated FQDN bypass list designed for enterprise firewalls (Palo Alto Networks, Fortinet, Cisco Secure Firewall, pfSense, etc.) to prevent service disruption caused by SSL/TLS decryption.

> [!IMPORTANT]
> **THIS IS NOT A FILTER OR CONTENT BLOCKLIST.**  
> This list exists solely to bypass SSL/TLS decryption (TLS inspection) for services that **actively break** when intercepted due to hardcoded certificate pinning, proprietary non-HTTP protocols wrapped in TLS, or mutual TLS authentication (e.g., Office 365, Google Play services, Apple push notifications, banking apps).  
> 
> **Do not submit domains here just because a site is "trusted."** Every entry added to an inspection bypass list expands your network's blind spot.

---

## 🚀 Public Endpoint & CDN Links

This project deploys directly to a global edge CDN for maximum availability and low-latency fetching.

| Asset | CDN URL |
| :--- | :--- |
| **FQDN Bypass List** | `https://ssl-decrypt-bypass.pages.dev/ssl-bypass-fqdn.txt` |

### Firewall Integration Guidelines
* **Update Frequency:** Set your firewall's External Dynamic List (EDL) or threat feed refresh interval to **60 minutes** (1 hour) or longer. 
* **Format:** Plaintext, line-separated FQDNs with wildcards (e.g., `*.domain.com` or `sub.domain.com`), stripped of comments and duplicate entries.

---

## 🛠️ How It Works

The repository uses a hybrid ingestion build pipeline that runs on deploy:

1. **Dynamic Ingestion (`/dynamic`):** Runs lightweight Python and Bash scripts to fetch officially published endpoint APIs (e.g., Microsoft 365, Google ChromeOS) directly from vendors.
2. **Static Ingestion (`/static`):** Imports curated text files containing domains known to use TLS pinning that do not offer an official endpoint API.
3. **Build & Deduplication (`build.py`):** Normalizes, strips inline comments, deduplicates all entries, sorts them alphabetically, and writes metadata counts to the output header.
4. **Edge Delivery:** Cloudflare Pages executes the build script and immediately serves the generated `dist/` directory globally.

---

## 📄 License

Distributed under the [MIT License](LICENSE).

