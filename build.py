from datetime import datetime, timezone
import glob
import os
import subprocess
import shutil

DIST_DIR = "dist"
STATIC_DIR = "static"
DYNAMIC_DIR = "dynamic"

# Ensure clean distribution directory
os.makedirs(DIST_DIR, exist_ok=True)

def sanitize_entry(line):
    line = line.split('#')[0].strip().lower()
    return line

def process_build():
    dynamic_fqdns = set()
    static_fqdns = set()

    # 1. Execute all dynamic scripts
    print("Executing dynamic scripts...")
    for script in sorted(glob.glob(os.path.join(DYNAMIC_DIR, "*"))):
        if script.endswith(".py"):
            subprocess.run(["python3", script], check=True)
        elif script.endswith(".sh"):
            subprocess.run(["bash", script], check=True)

    # 2. Collect temp dynamic files
    for tmp_file in glob.glob("dynamic_*.tmp"):
        with open(tmp_file, "r") as f:
            for line in f:
                clean = sanitize_entry(line)
                if clean:
                    dynamic_fqdns.add(clean)
        os.remove(tmp_file)

    # 3. Read static text files
    print("Reading static files...")
    for static_file in sorted(glob.glob(os.path.join(STATIC_DIR, "*.txt"))):
        with open(static_file, "r") as f:
            for line in f:
                clean = sanitize_entry(line)
                if clean:
                    static_fqdns.add(clean)

    # Combine sets for total unique deduplication
    total_fqdns = dynamic_fqdns.union(static_fqdns)

    # 4. Generate Output Header
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    header = (
        "# =============================================================\n"
        "# SSL Decryption Bypass List\n"
        "# High-reliability FQDN list for enterprise firewall exceptions\n"
        "# https://github.com/null1131/ssl-decrypt-bypass\n"
        "# LICENSE: MIT\n"
        f"# Last Updated: {timestamp}\n"
        f"# Dynamic Entries: {len(dynamic_fqdns)}\n"
        f"# Static Entries: {len(static_fqdns)}\n"
        f"# Total Unique Entries: {len(total_fqdns)}\n"
        "# =============================================================\n\n"
    )

    # 5. Write list to Dist Directory (sorted alphabetically to minimize git diffs)
    with open(os.path.join(DIST_DIR, "ssl-bypass-fqdn.txt"), "w") as f:
        f.write(header)
        f.write("\n".join(sorted(total_fqdns)) + "\n")

    # 6. Copy index.html for Cloudflare Pages
    if os.path.exists("index.html"):
        shutil.copy("index.html", os.path.join(DIST_DIR, "index.html"))

    print(f"Build complete. Dynamic: {len(dynamic_fqdns)} | Static: {len(static_fqdns)} | Total: {len(total_fqdns)}")

if __name__ == "__main__":
    process_build()