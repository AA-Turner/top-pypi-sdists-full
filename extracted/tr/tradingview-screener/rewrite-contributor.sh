#!/usr/bin/env bash
set -euo pipefail

# Requires: git filter-repo (pip install git-filter-repo)

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: not inside a git repository." >&2
    exit 1
fi

if ! command -v git-filter-repo &> /dev/null; then
    echo "Error: git-filter-repo is not installed. Run: pip install git-filter-repo" >&2
    exit 1
fi

# Collect all unique "Name <email>" contributors from history
mapfile -t contributors < <(
    git log --format="%an <%ae>" | sort -u
)

if [ ${#contributors[@]} -eq 0 ]; then
    echo "No commits found in this repository."
    exit 0
fi

echo ""
echo "Contributors found in git history:"
echo ""
for i in "${!contributors[@]}"; do
    printf "  [%d] %s\n" "$((i + 1))" "${contributors[$i]}"
done
echo ""

# Prompt user to pick one
while true; do
    read -rp "Enter the number of the contributor to remove/replace: " choice
    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#contributors[@]}" ]; then
        break
    fi
    echo "Invalid choice. Enter a number between 1 and ${#contributors[@]}."
done

selected="${contributors[$((choice - 1))]}"
old_name="${selected% <*}"
old_email="${selected#*<}"; old_email="${old_email%>}"

echo ""
echo "Selected: $selected"
echo ""
echo "Enter the replacement identity (leave blank to use a placeholder):"
read -rp "  New name  [default: 'Removed Contributor']: " new_name
read -rp "  New email [default: 'removed@invalid']:      " new_email

new_name="${new_name:-Removed Contributor}"
new_email="${new_email:-removed@invalid}"

echo ""
echo "---"
echo "This will rewrite ALL commits by:"
echo "  $old_name <$old_email>"
echo "to:"
echo "  $new_name <$new_email>"
echo ""
echo "WARNING: This rewrites history. All commit SHAs will change."
echo "         Everyone with a clone must re-clone afterwards."
echo "         Make sure you have a backup before proceeding."
echo "---"
echo ""
read -rp "Type 'yes' to continue: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# Build a temp mailmap file covering both name+email and email-only variants
mailmap_file="$(mktemp /tmp/mailmap.XXXXXX)"
trap 'rm -f "$mailmap_file"' EXIT

echo "$new_name <$new_email> $old_name <$old_email>" >> "$mailmap_file"
echo "$new_name <$new_email> <$old_email>"           >> "$mailmap_file"

echo ""
echo "Running git filter-repo..."
git filter-repo --mailmap "$mailmap_file" --force

echo ""
echo "Done. Verify with:"
echo "  git log --format='%an <%ae>' | sort -u"
echo ""
echo "If everything looks correct, re-add your remote and force-push:"
echo "  git remote add origin <url>"
echo "  git push --force --all"
echo "  git push --force --tags"
