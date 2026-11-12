#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path


def distance(point, start, end):
    if start == end:
        return math.dist(point, start)
    x, y = point
    x1, y1 = start
    x2, y2 = end
    t = max(0.0, min(1.0, ((x-x1)*(x2-x1)+(y-y1)*(y2-y1))/((x2-x1)**2+(y2-y1)**2)))
    return math.dist((x, y), (x1+t*(x2-x1), y1+t*(y2-y1)))


def simplify(points, epsilon=0.008):
    if len(points) < 3:
        return points
    index, maximum = 0, 0.0
    for i in range(1, len(points)-1):
        value = distance(points[i], points[0], points[-1])
        if value > maximum:
            index, maximum = i, value
    if maximum > epsilon:
        return simplify(points[:index+1], epsilon)[:-1] + simplify(points[index:], epsilon)
    return [points[0], points[-1]]


def rings(geometry):
    if geometry["type"] == "Polygon":
        return geometry["coordinates"]
    if geometry["type"] == "MultiPolygon":
        return [ring for polygon in geometry["coordinates"] for ring in polygon]
    raise ValueError(f"Unsupported geometry: {geometry['type']}")


def main():
    parser = argparse.ArgumentParser(description="Build a compact SVG mark from the public region boundary.")
    parser.add_argument("--input", default="public/geography/atlas_region.geojson")
    parser.add_argument("--output", default="public/brand/emilia-romagna-region-mark.svg")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    all_rings = rings(data["features"][0]["geometry"])
    points = [tuple(point) for ring in all_rings for point in ring]
    minx, maxx = min(p[0] for p in points), max(p[0] for p in points)
    miny, maxy = min(p[1] for p in points), max(p[1] for p in points)
    scale = 86 / max(maxx-minx, maxy-miny)
    offsetx = (100-(maxx-minx)*scale)/2
    offsety = (100-(maxy-miny)*scale)/2
    commands = []
    for ring in all_rings:
        reduced = simplify([tuple(point) for point in ring])
        transformed = [(offsetx+(x-minx)*scale, 100-(offsety+(y-miny)*scale)) for x, y in reduced]
        if len(transformed) < 3:
            continue
        commands.append("M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in transformed) + " Z")
    svg = "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Profilo dell&#39;Emilia-Romagna">',
        f'  <path d="{" ".join(commands)}" fill="#1558b0" fill-rule="evenodd"/>',
        '</svg>',
        ''
    ])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print(f"WROTE={output}")


if __name__ == "__main__":
    main()
