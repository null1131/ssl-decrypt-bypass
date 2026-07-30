## Project Purpose

This repository creates a list of Fully Qualified Domain Names (FQDNs) to bypass enterprise SSL/TLS decryption. The output file (`dist/ssl-bypass-fqdn.txt`) combines static list files with dynamic scripts that fetch vendor data.

---

## Language and Style Requirements

All documentation, commit messages, code comments, and pull request text created by agents must adhere to the **ASD-STE100 Simplified Technical English** standard.

You must follow these core principles:

* **Short Sentences:** Keep sentences short (maximum 20 words).
* **Direct Active Voice:** Write imperative instructions (for example, write "Run the build script" instead of "The build script should be executed").
* **Approved Vocabulary:** Use standard technical terms consistently. Do not use complex words, jargon, or ambiguous phrasing.
* **One Meaning per Word:** Use verbs, nouns, and adjectives with single, clear definitions.
* **No Fluff:** State facts directly without unnecessary descriptive words.

---

## Technical Rules and Constraints

### Rules for Inclusion
Only add domains that meet all of these requirements:
1. **Service Failure:** The service fails when intercepted by a custom root CA.
2. **Technical Cause:** Failure occurs because of certificate pinning, non-HTTP TLS wrappers, or mutual TLS (mTLS).
3. **Small Scope:** Use the most specific FQDN possible (for example, `dl.google.com`). Do not add broad wildcards (for example, `*.google.com`).

### Prohibited Items
Do not add:
* Websites that operate correctly with TLS inspection.
* Lists for ad-blocking or privacy.
* IP address ranges (the repository tracks only FQDNs).
* Wildcard domains that bypass more inspection than necessary.

---

## Repository Structure


```

.
├── dynamic/          # Python (.py) and Bash (.sh) scripts for vendor APIs
├── static/           # Plain text files that contain FQDNs
├── dist/             # Output directory (ignored by Git)
├── build.py          # Main script to clean and combine data
├── CONTRIBUTING.md   # Rules for human contributors
├── index.html        # Redirect page for Cloudflare Pages
└── README.md         # Project documentation

```

---

## Development Instructions for Agents

### 1. Modify Static Files (`static/`)
* Save text files in the `static/` directory.
* Write one FQDN on each line.
* Add comments starting with `#` to give technical context.

### 2. Modify Dynamic Scripts (`dynamic/`)
* Add Python (`.py`) or Bash (`.sh`) scripts to the `dynamic/` directory.
* Configure scripts to output raw FQDN lines into a temporary file in the root directory:
  `dynamic_<vendor>_fqdn.tmp`
* Do not sort lists or add headers inside dynamic scripts. The `build.py` script cleans all data automatically.

### 3. Build and Test
Run the build script locally after you change any file:

```bash
python3 build.py

```

### 4. Verification Checklist

Before you submit changes, make sure that:

* `python3 build.py` completes without errors.
* The process deletes temporary `dynamic_*.tmp` files.
* The build updates `dist/ssl-bypass-fqdn.txt` correctly.
* Git does not track files in the `dist/` directory or temporary `.tmp` files.