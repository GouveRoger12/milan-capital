import os
import sys
import json
from typing import List, Dict, Any


def load_config(path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Failed to load config: {exc}", file=sys.stderr)
        return {}


def process_items(items: List[str]) -> List[str]:
    """Filter and normalize a list of strings."""
    seen = set()
    result = []
    for item in items:
        norm = item.strip().lower()
        if norm and norm not in seen:
            seen.add(norm)
            result.append(norm)
    return result


if __name__ == '__main__':
    config = load_config('config.json')
    data = process_items(config.get('items', []))
    print(f"Processed {len(data)} items.")
