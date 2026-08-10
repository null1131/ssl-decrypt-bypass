from datetime import datetime, timezone
import glob
import json
import os
import shutil
import subprocess

DIST_DIR = "dist"
STATIC_DIR = "static"
DYNAMIC_DIR = "dynamic"

# Make a new distribution directory if it does not exist
os.makedirs(DIST_DIR, exist_ok=True)


def sanitize_entry(line):
    line = line.split("#")[0].strip().lower()
    return line


def process_build():
    dynamic_fqdns = set()
    static_fqdns = set()

    # 1. Run all dynamic scripts
    print("Run dynamic scripts...")
    for script in sorted(glob.glob(os.path.join(DYNAMIC_DIR, "*"))):
        if script.endswith(".py"):
            subprocess.run(["python3", script], check=True)
        elif script.endswith(".sh"):
            subprocess.run(["bash", script], check=True)

    # 2. Collect temporary dynamic files
    for tmp_file in glob.glob("dynamic_*.tmp"):
        with open(tmp_file, "r") as f:
            for line in f:
                clean = sanitize_entry(line)
                if clean:
                    dynamic_fqdns.add(clean)
        os.remove(tmp_file)

    # 3. Read static text files
    print("Read static files...")
    for static_file in sorted(glob.glob(os.path.join(STATIC_DIR, "*.txt"))):
        with open(static_file, "r") as f:
            for line in f:
                clean = sanitize_entry(line)
                if clean:
                    static_fqdns.add(clean)

    # Add the default domain name
    static_fqdns.add("ssl-decrypt-bypass.pages.dev")

    # Combine sets to remove duplicate items
    total_fqdns = dynamic_fqdns.union(static_fqdns)

    # 4. Create the output header
    timestamp_utc = datetime.now(timezone.utc)
    timestamp_str = timestamp_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

    header = (
        "# =============================================================\n"
        "# SSL Decryption Bypass List\n"
        "# List of FQDN items for firewall exceptions\n"
        "# https://github.com/null1131/ssl-decrypt-bypass\n"
        "# LICENSE: MIT\n"
        f"# Date of last update: {timestamp_str}\n"
        f"# Dynamic items: {len(dynamic_fqdns)}\n"
        f"# Static items: {len(static_fqdns)}\n"
        f"# Total unique items: {len(total_fqdns)}\n"
        "# =============================================================\n\n"
    )

    # 5. Write the list to the distribution directory in alphabetical order
    with open(os.path.join(DIST_DIR, "ssl-bypass-fqdn.txt"), "w") as f:
        f.write(header)
        f.write("\n".join(sorted(total_fqdns)) + "\n")

    # 6. Generate a single JSON file for Dynamic Shields.io Badges
    print("Generating stats.json for Shields.io...")
    stats_data = {
        "last_build": timestamp_utc.strftime("%Y-%m-%d %H:%M UTC"),
        "total": len(total_fqdns),
        "dynamic": len(dynamic_fqdns),
        "static": len(static_fqdns)
    }

    with open(os.path.join(DIST_DIR, "stats.json"), "w") as f:
        json.dump(stats_data, f, indent=2)

    # 7. Copy index.html for Cloudflare Pages
    if os.path.exists("index.html"):
        shutil.copy("index.html", os.path.join(DIST_DIR, "index.html"))

    print(
        f"Build complete. Dynamic: {len(dynamic_fqdns)} | Static:"
        f" {len(static_fqdns)} | Total: {len(total_fqdns)}"
    )


if __name__ == "__main__":
    process_build()