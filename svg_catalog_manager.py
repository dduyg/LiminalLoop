"""
█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█
  
   ｓｖｇ－ｃａｔａｌｏｇ－ｍａｎａｇｅｒ ™        ベクター  アーカイブ  システム
   ［ Ｓ Ｙ Ｓ Ｔ Ｅ Ｍ   Ｓ Ｔ Ａ Ｔ Ｕ Ｓ   Ｓ Ｅ Ｃ Ｕ Ｒ Ｅ ］
     
   視覚記号管理装置  Ａｕｔｈｏｒ  ／  Duygu Dağdelen ［ ２０２６－０９－２３ ］
    
█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█

   ［ Ｕ Ｓ Ａ Ｇ Ｅ   —   Ｖ Ｉ Ａ   Ｇ Ｉ Ｔ Ｈ Ｕ Ｂ   Ａ Ｃ Ｔ Ｉ Ｏ Ｎ Ｓ ］

   1. Actions tab -> "Stage <svg> inputs" -> "Run workflow"
   2. Stage inputs as many as you need, each in this exact format:
      id ::: tags ::: <svg>...</svg>
      (Leave any unused entry fields empty)
   3. Check 'overwrite' only if intentionally replacing existing ids.

   Note: The batch is ATOMIC. If any filled-in entry is malformed,
   has a duplicate id within the batch, or collides with an existing
   id (without overwrite checked), the whole run fails and nothing is
   written. The error message indicates which entry failed and why.

█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█
"""
import argparse
import json
import re
import sys
from pathlib import Path

DELIMITER = " ::: "


def parse_vector_data(raw_svg: str):
    """Extracts the viewBox and inner path/content from a raw <svg> string."""
    viewbox_search = re.search(r'viewBox=["\']([^"\']+)["\']', raw_svg)
    viewbox = viewbox_search.group(1) if viewbox_search else "0 0 100 100"

    content_search = re.search(r'<svg[^>]*>(.*)</svg>', raw_svg, re.DOTALL)
    inner = content_search.group(1).strip() if content_search else raw_svg.strip()
    return viewbox, inner


def serialize_with_compact_arrays(dataset) -> str:
    pretty_json = json.dumps(dataset, indent=2)

    def inline_list(match):
        items = [item.strip() for item in match.group(1).split(",")]
        return f'"tags": [{", ".join(items)}]'

    return re.sub(r'"tags":\s*\[(.*?)\]', inline_list, pretty_json, flags=re.DOTALL)


def load_catalog(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def parse_entries(raw_text: str):
    entries = []
    errors = []

    for line_no, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        parts = line.split(DELIMITER)
        if len(parts) != 3:
            errors.append(
                f"line {line_no}: expected 3 parts separated by '{DELIMITER.strip()}' "
                f"(id, tags, svg) — found {len(parts)}."
            )
            continue

        raw_id, raw_tags, raw_svg = parts
        entry_id = raw_id.strip().lower().replace(" ", "-")
        raw_svg = raw_svg.strip()

        if not entry_id:
            errors.append(f"line {line_no}: id is empty.")
            continue
        if not raw_svg:
            errors.append(f"line {line_no}: svg markup is empty.")
            continue
        if "<svg" not in raw_svg.lower():
            errors.append(f"line {line_no}: doesn't look like it contains an <svg> tag.")
            continue

        tag_list = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
        entries.append((line_no, entry_id, tag_list, raw_svg))

    if errors:
        raise ValueError("\n".join(errors))

    return entries


def main():
    parser = argparse.ArgumentParser(description="Add or update one or more SVG entries in the catalog.")
    parser.add_argument("--entries-file", default=None,
                         help="Path to a file with one entry per line: 'id ::: tags ::: <svg>...</svg>'")
    parser.add_argument("--catalog", default="catalog.svgs.json", help="Path to the catalog JSON file")
    parser.add_argument("--overwrite", action="store_true",
                         help="Allow replacing entries whose id already exists in the catalog")
    args = parser.parse_args()

    if args.entries_file:
        raw_text = Path(args.entries_file).read_text(encoding="utf-8")
    else:
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        print("Error: no entries provided (via --entries-file or stdin).", file=sys.stderr)
        sys.exit(1)

    try:
        parsed = parse_entries(raw_text)
    except ValueError as e:
        print("Error: one or more lines could not be parsed — nothing was written.\n", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if not parsed:
        print("Error: no valid entries found (all lines were blank).", file=sys.stderr)
        sys.exit(1)

    # Reject duplicate ids within the batch itself before touching the catalog.
    seen_in_batch = {}
    dupe_errors = []
    for line_no, entry_id, _, _ in parsed:
        if entry_id in seen_in_batch:
            dupe_errors.append(
                f"line {line_no}: id '{entry_id}' is repeated (first seen on line {seen_in_batch[entry_id]})."
            )
        else:
            seen_in_batch[entry_id] = line_no

    if dupe_errors:
        print("Error: duplicate ids within this batch — nothing was written.\n", file=sys.stderr)
        print("\n".join(dupe_errors), file=sys.stderr)
        sys.exit(1)

    catalog_path = Path(args.catalog)
    dataset = load_catalog(catalog_path)
    existing_ids = {entry["id"] for entry in dataset}

    if not args.overwrite:
        collisions = [
            f"line {line_no}: id '{entry_id}' already exists in {catalog_path}."
            for line_no, entry_id, _, _ in parsed
            if entry_id in existing_ids
        ]
        if collisions:
            print(
                "Error: one or more ids already exist — "
                "Re-run with --overwrite to replace them.\n",
                file=sys.stderr,
            )
            print("\n".join(collisions), file=sys.stderr)
            sys.exit(1)

    added, updated = [], []
    for line_no, entry_id, tag_list, raw_svg in parsed:
        viewbox, svg_path = parse_vector_data(raw_svg)
        new_entry = {
            "id": entry_id,
            "viewBox": viewbox,
            "tags": tag_list,
            "svg": svg_path,
        }
        if entry_id in existing_ids:
            dataset = [item for item in dataset if item["id"] != entry_id]
            updated.append(entry_id)
        else:
            added.append(entry_id)
        dataset.append(new_entry)
        existing_ids.add(entry_id)

    processed_json = serialize_with_compact_arrays(dataset)
    catalog_path.write_text(processed_json + "\n", encoding="utf-8")

    summary = []
    if added:
        summary.append(f"added {len(added)}: {', '.join(added)}")
    if updated:
        summary.append(f"updated {len(updated)}: {', '.join(updated)}")
    print(f"Done — {'; '.join(summary)} ({len(dataset)} total entries in {catalog_path}).")


if __name__ == "__main__":
    main()
