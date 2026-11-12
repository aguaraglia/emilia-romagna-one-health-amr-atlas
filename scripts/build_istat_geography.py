#!/usr/bin/env python3
"""Build Emilia-Romagna public geography from the annual ISTAT generalized boundary archive (2026)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import shapefile
from pyproj import Transformer

TRANSFORMER = Transformer.from_crs("EPSG:32632", "EPSG:4326", always_xy=True)
COD_REG = 8
REGION_CODE = "08"
SOURCE_DATE = "2026-01-01"
EXPECTED = {"municipalities": 330, "provinces": 9, "region": 1}


def transform_coordinates(value):
    if value and isinstance(value[0], (int, float)):
        x, y = TRANSFORMER.transform(float(value[0]), float(value[1]))
        return [x, y]
    return [transform_coordinates(item) for item in value]


def build(shp_path: Path, output: Path, kind: str) -> None:
    # The 2026 WGS84 shapefiles are UTF-8 (Forlì-Cesena, Città metropolitana).
    reader = shapefile.Reader(str(shp_path), encoding="utf-8", encodingErrors="strict")
    features = []
    for sr in reader.iterShapeRecords():
        record = sr.record.as_dict()
        if int(record["COD_REG"]) != COD_REG:
            continue
        if kind == "municipalities":
            props = {
                "name": record["COMUNE"],
                "istat_code": record["PRO_COM_T"],
                "province_code": str(record["COD_UTS"]).zfill(3),
                "region_code": REGION_CODE,
                "source_date": SOURCE_DATE,
            }
        elif kind == "provinces":
            props = {
                "name": record["DEN_UTS"],
                "istat_code": str(record["COD_UTS"]).zfill(3),
                "abbreviation": record["SIGLA"],
                "unit_type": record["TIPO_UTS"],
                "region_code": REGION_CODE,
                "source_date": SOURCE_DATE,
            }
        else:
            props = {
                "name": record["DEN_REG"],
                "istat_code": str(record["COD_REG"]).zfill(2),
                "source_date": SOURCE_DATE,
            }
        geometry = dict(sr.shape.__geo_interface__)
        geometry["coordinates"] = transform_coordinates(geometry["coordinates"])
        features.append({"type": "Feature", "properties": props, "geometry": geometry})
    if len(features) != EXPECTED[kind]:
        raise SystemExit(f"{kind}: expected {EXPECTED[kind]}, found {len(features)}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output-root", type=Path, required=True)
    a = p.parse_args()
    jobs = [
        ("Com01012026_g/Com01012026_g_WGS84.shp", "atlas_municipalities.geojson", "municipalities"),
        ("ProvCM01012026_g/ProvCM01012026_g_WGS84.shp", "atlas_provinces.geojson", "provinces"),
        ("Reg01012026_g/Reg01012026_g_WGS84.shp", "atlas_region.geojson", "region"),
    ]
    for source, name, kind in jobs:
        build(a.source_root / source, a.output_root / name, kind)


if __name__ == "__main__":
    main()
