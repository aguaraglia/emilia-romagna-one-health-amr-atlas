#!/usr/bin/env python3
"""Check literature files against the Emilia-Romagna placeholder schema.

Empty collections are valid. A feature with a missing property is not.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPERTIES = [
    "place",
    "geography_level",
    "geography_basis",
    "study_count",
    "study_ids",
    "authors",
    "year",
    "title",
    "sector",
    "organism",
    "doi",
    "geography_note",
]
RECORD_KEYS = [
    "id",
    "year",
    "title",
    "authors",
    "journal",
    "scope",
    "geographic_link",
    "pmid",
    "doi",
    "source_url",
]
LAYERS = [
    "human_amr_evidence.geojson",
    "veterinary_amr_evidence.geojson",
    "food_chain_amr_evidence.geojson",
    "environmental_amr_evidence.geojson",
    "wildlife_amr_evidence.geojson",
    "regional_study_outline.geojson",
]


def main() -> int:
    errors: list[str] = []
    catalog = json.loads((ROOT / "public/data/literature-catalog.json").read_text(encoding="utf-8"))
    if catalog.get("edition") != "erm_amr_atlas":
        errors.append("literature-catalog edition")
    for index, record in enumerate(catalog.get("records") or []):
        missing = [key for key in RECORD_KEYS if key not in record]
        if missing:
            errors.append(f"record {index} missing {', '.join(missing)}")
    for name in LAYERS:
        payload = json.loads((ROOT / "public/data" / name).read_text(encoding="utf-8"))
        if payload.get("type") != "FeatureCollection":
            errors.append(f"{name} is not a FeatureCollection")
            continue
        for index, feature in enumerate(payload.get("features") or []):
            props = feature.get("properties") or {}
            missing = [key for key in PROPERTIES if key not in props]
            if missing:
                errors.append(f"{name} feature {index} missing {', '.join(missing)}")
            geometry = feature.get("geometry") or {}
            if geometry.get("type") not in {"Point", "Polygon", "MultiPolygon"}:
                errors.append(f"{name} feature {index} geometry {geometry.get('type')}")
    if errors:
        print("\n".join(errors))
        return 1
    print("literature schema ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
