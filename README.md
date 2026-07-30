# Enterprise SSL/TLS Decryption Bypass List

This repository provides an automated list of FQDN items for enterprise firewalls. It prevents service problems caused by SSL/TLS decryption.

> [!IMPORTANT]
> **THIS IS NOT A FILTER OR A BLOCKLIST.**  
> Use this list only to bypass SSL/TLS decryption for services that fail during inspection. These failures occur because of certificate pinning, non-HTTP TLS protocols, or mutual TLS authentication.  
> 
> **Do not add domains only because a website is trusted.** Each domain in the bypass list reduces network security.

---

## 🚀 Public Endpoints and CDN Links

This project deploys to a global content delivery network (CDN) for fast access and high availability.

| Asset | CDN URL |
| :--- | :--- |
| **FQDN Bypass List** | `https://ssl-decrypt-bypass.pages.dev/ssl-bypass-fqdn.txt` |

### Guidelines for Firewall Integration
* **Update Frequency:** Set your firewall to update the list every 60 minutes or longer.
* **Format:** Plain text list of FQDNs. Put each item on a new line. The list contains no comments or duplicate items.

---

## 🛠️ How the System Works

The repository uses an automated build process during deployment:

1. **Dynamic Processing (`/dynamic`):** Runs Python and Bash scripts to get official endpoint data from vendors.
2. **Static Processing (`/static`):** Reads text files that contain domains with TLS pinning when no official API exists.
3. **Build and Clean Process (`build.py`):** Cleans the data, removes comments and duplicates, sorts the list in alphabetical order, and writes summary information to the header.
4. **Global Delivery:** Cloudflare Pages runs the build script and delivers the generated `dist/` directory to all locations.

---

## 📄 License

This project uses the [MIT License](LICENSE).