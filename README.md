# Enterprise SSL/TLS Decryption Bypass List

An automated, minimal, community-curated FQDN bypass list designed for enterprise firewalls (Palo Alto Networks, Fortinet, Cisco Secure Firewall, pfSense, etc.) to prevent service disruption caused by SSL/TLS decryption.

> [!IMPORTANT]
> **THIS IS NOT A FILTER OR CONTENT BLOCKLIST.**  
> This list exists solely to bypass SSL/TLS decryption (TLS inspection) for services that **actively break** when intercepted due to hardcoded certificate pinning, proprietary non-HTTP protocols wrapped in TLS, or mutual TLS authentication (e.g., Office 365, Google Play services, Apple push notifications, banking apps).  
> 
> **Do not submit domains here just because a site is "trusted."** Every entry added to an inspection bypass list expands your network's blind spot.

---

## 🚀 Public Endpoint & CDN Links

This project builds nightly via GitHub Actions and deploys directly to Cloudflare Pages for maximum availability and global edge caching.

| Asset | CDN URL |
| :--- | :--- |
| **FQDN Bypass List** | `https://ssl-bypass.yourdomain.com/ssl-bypass-fqdn.txt` |
| **Cloudflare Pages Direct** | `https://<your-project>.pages.dev/ssl-bypass-fqdn.txt` |

### Firewall Integration Guidelines
* **Update Frequency:** Set your firewall's External Dynamic List (EDL) or threat feed refresh interval to **60 minutes** (1 hour) or longer. 
* **Format:** Plaintext, line-separated FQDNs with wildcards (e.g., `*.domain.com` or `sub.domain.com`), stripped of comments and duplicate entries.

---

## 🛠️ How It Works

The repository uses a hybrid ingestion process that executes every night at 03:00 UTC:

1. **Dynamic Ingestion (`/dynamic`):** Runs lightweight Python and Bash scripts to fetch officially published endpoint APIs (e.g., Microsoft 365 JSON endpoints) directly from vendors.
2. **Static Ingestion (`/static`):** Imports curated text files containing domains known to use TLS pinning that do not offer an official endpoint API.
3. **Build & Deduplication (`build.py`):** Normalizes, strips inline comments, deduplicates all entries, sorts them alphabetically (to prevent noisy Git diffs), and writes metadata counts to the header.
4. **Edge Deployment:** Commits the output to `dist/`, triggering an instant deployment to Cloudflare Pages.
