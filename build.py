from datetime import datetime, timezone
import csv
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
    fqdn_sources = {}  # Dictionary to track source files for each FQDN
    tmp_to_script = {} # Dictionary to map .tmp files to their generator scripts

    # 1. Run all dynamic scripts
    print("Run dynamic scripts...")
    for script in sorted(glob.glob(os.path.join(DYNAMIC_DIR, "*"))):
        script_name = os.path.basename(script)
        before_tmps = set(glob.glob("dynamic_*.tmp"))
        
        if script.endswith(".py"):
            subprocess.run(["python3", script], check=True)
        elif script.endswith(".sh"):
            subprocess.run(["bash", script], check=True)
            
        after_tmps = set(glob.glob("dynamic_*.tmp"))
        
        # Map any newly created .tmp files to the script that just ran
        for new_tmp in (after_tmps - before_tmps):
            tmp_to_script[new_tmp] = script_name

    # 2. Collect temporary dynamic files
    for tmp_file in glob.glob("dynamic_*.tmp"):
        # Get the actual script name, fallback to the tmp filename if not found
        source_name = tmp_to_script.get(tmp_file, os.path.basename(tmp_file))
        
        with open(tmp_file, "r") as f:
            for line in f:
                clean = sanitize_entry(line)
                if clean:
                    dynamic_fqdns.add(clean)
                    if clean not in fqdn_sources:
                        fqdn_sources[clean] = set()
                    fqdn_sources[clean].add(source_name)
        os.remove(tmp_file)

    # 3. Read static text files
    print("Read static files...")
    for static_file in sorted(glob.glob(os.path.join(STATIC_DIR, "*.txt"))):
        filename = os.path.basename(static_file)
        with open(static_file, "r") as f:
            for line in f:
                clean = sanitize_entry(line)
                if clean:
                    static_fqdns.add(clean)
                    if clean not in fqdn_sources:
                        fqdn_sources[clean] = set()
                    fqdn_sources[clean].add(filename)

    # Add the default domain name
    default_domain = "ssl-decrypt-bypass.pages.dev"
    static_fqdns.add(default_domain)
    if default_domain not in fqdn_sources:
        fqdn_sources[default_domain] = set()
    fqdn_sources[default_domain].add("default")

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
        
    # 5b. Write the commented list
    with open(os.path.join(DIST_DIR, "ssl-bypass-fqdn-comments.txt"), "w") as f:
        f.write(header)
        for fqdn in sorted(total_fqdns):
            sources = ", ".join(sorted(fqdn_sources[fqdn]))
            f.write(f"{fqdn} #{sources}\n")

    # 5c. Write the debug CSV
    with open(os.path.join(DIST_DIR, "ssl-bypass-debug.csv"), "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write CSV Header
        csv_writer.writerow(["FQDN", "Type", "Source"])
        for fqdn in sorted(total_fqdns):
            # Determine the type category
            if fqdn == default_domain:
                fqdn_type = "Default"
            elif fqdn in dynamic_fqdns and fqdn in static_fqdns:
                fqdn_type = "Dynamic / Static"
            elif fqdn in dynamic_fqdns:
                fqdn_type = "Dynamic"
            else:
                fqdn_type = "Static"
            
            sources = ", ".join(sorted(fqdn_sources[fqdn]))
            csv_writer.writerow([fqdn, fqdn_type, sources])

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