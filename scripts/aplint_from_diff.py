import aplinter
import json
import sys
import os

if len(sys.argv) != 4:
    print("Usage: aplint_from_diff <output_path> <index_path> <lint_output_dir>")
    sys.exit(1)

output_path = sys.argv[1]
index_path = sys.argv[2]
lint_output = sys.argv[3]

changes_file = os.path.join(output_path, "changes.json")
apworlds_dir = os.path.join(output_path, "apworlds")

with open(changes_file) as fd:
    changes = json.load(fd)

for apworld_name, world_changes in changes["worlds"].items():
    for version in world_changes["added_versions"]:
        # apwm's Checksum enum is externally tagged: the unit variant
        # `Supported` serializes as the bare string "supported", while
        # `Hash(String)` becomes {"hash": "..."}. Supported worlds ship in
        # the AP release rather than being downloaded, so there are no bytes
        # under apworlds/ to lint.
        checksum = world_changes["checksums"].get(version)
        if checksum == "supported":
            continue

        apworld_file = os.path.join(apworlds_dir, f"{apworld_name}-{version}.apworld")
        if not os.path.exists(apworld_file):
            print(f"Warning: {apworld_file} not found, skipping lint")
            continue

        aplinter.lint(apworld_file, lint_output)
