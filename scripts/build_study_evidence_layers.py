#!/usr/bin/env python3
"""Build Emilia-Romagna study evidence layers, mirroring the Lombardy schema.

Geometries come from the ISTAT 2026 boundaries in this build, or from a named
facility geocoded on OpenStreetMap Nominatim (2026-11-12). The script does not
geocode farms, dairies, hunting estates, unnamed hospitals, or apiaries, and
does not invent a site the catalog does not name.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    "Il segnaposto indica dove è stato condotto lo studio, non una prevalenza."
)
SECTOR = {
    "healthcare_amr": "AMR clinica",
    "human_antimicrobial_use": "Consumo di antimicrobici",
    "antimicrobial_use": "Uso di antimicrobici",
    "companion_animal_amr": "AMR negli animali d'affezione",
    "wildlife_amr": "AMR nella fauna selvatica",
    "veterinary_amr": "AMR veterinaria",
    "food_amr": "AMR alimentare",
    "foodborne_amr": "AMR alimentare",
    "dairy_amr": "AMR nel comparto lattiero",
    "swine_amr": "AMR nella filiera suinicola",
    "environmental_amr": "AMR ambientale",
    "wastewater_amr": "AMR ambientale",
    "antimicrobial_stewardship": "Stewardship antimicrobica",
}

# Nominatim results checked on 2026-11-12. Coordinates are the facility or campus
# returned for the named institution, not a sample and not a farm.
POINTS = {
    "sant_orsola": (
        11.36096,
        44.49153,
        "IRCCS Azienda Ospedaliero-Universitaria di Bologna, Policlinico Sant'Orsola-Malpighi",
        "OpenStreetMap Nominatim: Policlinico Sant'Orsola-Malpighi, Bologna.",
    ),
    "policlinico_modena": (
        10.94215,
        44.63535,
        "Policlinico di Modena (Modena University Hospital Policlinico)",
        "OpenStreetMap Nominatim: Policlinico di Modena, Via del Pozzo 71, Modena.",
    ),
    "hesperia": (
        10.92393,
        44.62608,
        "Hesperia Hospital, Modena",
        "OpenStreetMap Nominatim: Hesperia Hospital, Via Arquà 80, Modena.",
    ),
    "vuh_ozzano": (
        11.48650,
        44.43607,
        "Ospedale veterinario universitario Giuseppe Gentile, Ozzano dell'Emilia",
        "OpenStreetMap Nominatim: Ospedale veterinario universitario Giuseppe Gentile, Via Tolara di Sopra 50, Ozzano dell'Emilia.",
    ),
    "vth_parma": (
        10.30821,
        44.81986,
        "Ospedale Veterinario Didattico, Università di Parma",
        "OpenStreetMap Nominatim non indicizza un POI distinto dell'ospedale veterinario; il punto è il Dipartimento di Scienze Medico-Veterinarie, Strada del Taglio, Parma, campus dichiarato dagli autori. Non è un allevamento.",
    ),
    "ospedale_maggiore_parma": (
        10.30830,
        44.80162,
        "Ospedale Maggiore, Azienda Ospedaliero-Universitaria di Parma",
        "OpenStreetMap Nominatim: Ospedale Maggiore Parma, Viale Antonio Gramsci, Parma.",
    ),
}

ORGANISM = {
    "pubmed_41750467": "organismi MDR in shock settico (ospedaliero vs comunitario)",
    "pubmed_41837856": "Neisseria gonorrhoeae XDR ST16406",
    "pubmed_42257329": "geni tet e beta-lattamasi (mucosa orofaringea e anorettale, MSM)",
    "pubmed_41805090": "Enterobacteriaceae resistenti (portaggio rettale, MSM in PrEP)",
    "pubmed_42148182": "Salmonella ed Escherichia coli su carni di cinghiale (igiene di processo, AMR limitata)",
    "pubmed_42095386": "consumo ospedaliero di antibiotici sistemici (indicatori PNCAR/AWaRe)",
    "pubmed_39947614": "Enterobacter cloacae ST837, blaIMP-19 e mcr-4.3",
    "pubmed_40431538": "batteriemie in cani e gatti",
    "pubmed_40005528": "Streptococcus pyogenes invasivo (iGAS), geni AMR",
    "pubmed_40001129": "prescrizione antimicrobica nel gatto",
    "pubmed_41079141": "stewardship su batteriemie (tempistica e appropriatezza terapeutica)",
    "pubmed_40269796": "uso di antibiotici in gravidanza",
    "pubmed_39317655": "prescrizione antibiotica pediatrica territoriale",
    "pubmed_38367164": "Staphylococcus aureus ed altri stafilococchi",
    "pubmed_38301758": "batteri ambientali resistenti (modelli predittivi, Apis mellifera)",
    "pubmed_37839149": "Salmonella enterica in equidi al macello",
    "pubmed_38944352": "resistenza alla colistina (fenotipo e geni mcr) in batteri ambientali da api mellifere",
    "pubmed_39357073": "batteri da uccelli selvatici (ossacillina, enrofloxacina, rifampicina)",
    "pubmed_40303743": "batteri ambientali resistenti isolati da corpo e intestino di api mellifere",
    "pubmed_35795463": "Salmonella da carne suina (beta-lattamici, fluorochinoloni, colistina)",
    "pubmed_34177854": "Streptococcus agalactiae (bovini e uomo, isolati simpatici)",
    "pubmed_33494307": "Escherichia coli ESBL/AmpC e resistente alla colistina in carni suine e di cinghiale",
    "pubmed_34351529": "mcr-1 (e un isolato mcr-4) in Enterobacterales, sorveglianza Micro-RER",
    "pubmed_34680787": "uropatogeni pediatrici",
    "pubmed_32408565": "Klebsiella pneumoniae resistente a carbapenemi e colistina",
    "pubmed_32370005": "Helicobacter pylori",
    "pubmed_32240057": "Escherichia coli da feci e carcasse di suini",
    "pubmed_32961926": "geni di resistenza nella saliva (erm, tet)",
    "pubmed_31934774": "Escherichia coli da carni al dettaglio (biofilm e AMR, anche ESBL)",
    "pubmed_31639545": "Enterobacterales produttori di carbapenemasi (screening rettale)",
    "pubmed_32668681": "batteri da micromammiferi selvatici",
    "pubmed_30993338": "prescrizione antibatterica in età prescolare (flusso di rimborso)",
    "pubmed_31119408": "Salmonella in cinghiali e suini domestici",
    "pubmed_30854342": "Escherichia coli ESBL da linfonodi mesenterici di cinghiale",
    "pubmed_28512231": "prescrizione antimicrobica nella pratica veterinaria per piccoli animali",
    "pubmed_26405817": "consumo di antibiotici nei reparti pediatrici ospedalieri",
    "pubmed_25335100": "Klebsiella pneumoniae resistente ai carbapenemi (colonizzazione/infezione)",
    "pubmed_25375901": "Klebsiella pneumoniae produttrice di carbapenemasi (CPKP)",
    "pubmed_24997585": "prescrizione sistemica pediatrica ambulatoriale",
    "pubmed_24484182": "consumo ospedaliero di antibatterici",
    "pubmed_27873629": "programmi di antimicrobial stewardship (indagine strutturale)",
    "pubmed_24030722": "campagna di prescrizione antibiotica territoriale",
    "pubmed_21888564": "Staphylococcus aureus",
    "pubmed_21595784": "consumo territoriale di antibiotici nella popolazione adulta",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def municipality(name: str, municipalities: dict) -> dict:
    return municipalities[name]["geometry"]


def provinces(names: list[str], provinces_by_name: dict) -> dict:
    parts = []
    for name in names:
        geometry = provinces_by_name[name]["geometry"]
        if geometry["type"] == "Polygon":
            parts.append(geometry["coordinates"])
        elif geometry["type"] == "MultiPolygon":
            parts.extend(geometry["coordinates"])
        else:
            raise ValueError(name)
    if len(parts) == 1:
        return {"type": "Polygon", "coordinates": parts[0]}
    return {"type": "MultiPolygon", "coordinates": parts}


def feature(geometry: dict, place: str, level: str, basis: str, studies: list[dict], extra_note: str = "") -> dict:
    note = NOTE if not extra_note else f"{NOTE} {extra_note}"
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "place": place,
            "geography_level": level,
            "geography_basis": basis,
            "study_count": len(studies),
            "study_ids": "; ".join(item["id"] for item in studies),
            "authors": " | ".join(item["authors"] for item in studies),
            "year": " | ".join(item["year"] for item in studies),
            "title": " | ".join(item["title"] for item in studies),
            "sector": " | ".join(item["sector"] for item in studies),
            "organism": " | ".join(item["organism"] for item in studies),
            "doi": " | ".join(item["doi"] for item in studies),
            "geography_note": note,
        },
    }


def point(key: str) -> dict:
    lon, lat, _label, _source = POINTS[key]
    return {"type": "Point", "coordinates": [round(lon, 5), round(lat, 5)]}


def place_label(key: str) -> str:
    return POINTS[key][2]


def place_basis(key: str, text: str) -> str:
    return f"{text} {POINTS[key][3]}"


def main() -> None:
    catalog = load_json(ROOT / "public/data/literature-catalog.json")
    by_id = {item["id"]: item for item in catalog["records"]}
    missing_organism = set(by_id) - set(ORGANISM)
    if missing_organism:
        raise SystemExit("Organismo mancante: " + ", ".join(sorted(missing_organism)))

    def card(study_id: str) -> dict:
        record = by_id[study_id]
        doi = record.get("doi") or ""
        return {
            "id": study_id,
            "authors": record["authors"],
            "year": str(record["year"]),
            "title": record["title"].rstrip("."),
            "sector": SECTOR[record["scope"]],
            "organism": ORGANISM[study_id],
            "doi": f"https://doi.org/{doi}" if doi else record["source_url"],
        }

    municipalities = {
        feature_["properties"]["name"]: feature_
        for feature_ in load_json(ROOT / "public/geography/atlas_municipalities.geojson")["features"]
    }
    province_features = {
        feature_["properties"]["name"]: feature_
        for feature_ in load_json(ROOT / "public/geography/atlas_provinces.geojson")["features"]
    }
    region = load_json(ROOT / "public/geography/atlas_region.geojson")["features"][0]["geometry"]

    layers: dict[str, list] = {
        "human": [],
        "veterinary": [],
        "food": [],
        "environment": [],
        "wildlife": [],
        "regional": [],
    }
    placed: dict[str, str] = {}

    def add(layer: str, study_ids: list[str], geometry: dict, place: str, level: str, basis: str, extra_note: str = "") -> None:
        for study_id in study_ids:
            if study_id in placed:
                placed[study_id] += f"; {level}: {place}"
            else:
                placed[study_id] = f"{level}: {place}"
        layers[layer].append(feature(geometry, place, level, basis, [card(study_id) for study_id in study_ids], extra_note))

    # --- AMR umana: strutture nominate ---
    add(
        "human",
        [
            "pubmed_41837856",
            "pubmed_42257329",
            "pubmed_41805090",
            "pubmed_31639545",
            "pubmed_32370005",
        ],
        point("sant_orsola"),
        place_label("sant_orsola"),
        "struttura",
        place_basis(
            "sant_orsola",
            "Struttura nominata nel full text o nell'abstract: IRCCS Azienda Ospedaliero-Universitaria di Bologna / Policlinico Sant'Orsola-Malpighi (Via Massarenti 9). Fiorini 2020, il cui abstract diceva solo «single center (Bologna)», è stato confermato nel full text come S. Orsola Hospital.",
        ),
    )
    add(
        "human",
        ["pubmed_32408565"],
        point("policlinico_modena"),
        place_label("policlinico_modena"),
        "struttura",
        place_basis(
            "policlinico_modena",
            "Full text: Modena University Hospital Policlinico (MUHP), ospedale terziario di 677 posti letto.",
        ),
    )
    add(
        "human",
        ["pubmed_38367164"],
        point("hesperia"),
        place_label("hesperia"),
        "struttura",
        place_basis(
            "hesperia",
            "Laboratorio di microbiologia dell'Hesperia Hospital, Modena, nominato nell'abstract e nella scheda IRIS.",
        ),
    )
    add(
        "human",
        ["pubmed_25335100"],
        point("ospedale_maggiore_parma"),
        place_label("ospedale_maggiore_parma"),
        "struttura",
        place_basis(
            "ospedale_maggiore_parma",
            "Full text: Internal Medicine and Critical Subacute Care Unit, Parma University Hospital (AOU / Ospedale Maggiore).",
        ),
    )

    # --- AMR umana: comuni (ospedale non nominato, oppure AOU su più sedi) ---
    add(
        "human",
        ["pubmed_41750467", "pubmed_41079141"],
        municipality("Modena", municipalities),
        "Modena",
        "comune",
        "Coloretti: due ICU multidisciplinari del «Modena University Hospital», senza distinguere Policlinico e Baggiovara. Di Marcello: stewardship in un unico centro descritto come University Hospital of Modena, struttura terziaria di 1200 posti letto (AOU nel suo insieme), senza nominare il campus. Nessun punto su una sede presunta.",
    )
    add(
        "human",
        ["pubmed_39947614", "pubmed_40005528", "pubmed_32961926"],
        municipality("Bologna", municipalities),
        "Bologna",
        "comune",
        "Menozzi: isolato da screening CPE «in Bologna», ospedale non nominato. Bonomo: isolati iGAS da ospedali non nominati di Bologna e Imola (l'altro poligono è Imola). Milanović: sito di arruolamento di volontari a Bologna (il full text aggiunge anche Parma; Torino e Bari sono fuori ambito).",
    )
    add(
        "human",
        ["pubmed_40005528"],
        municipality("Imola", municipalities),
        "Imola",
        "comune",
        "Full text: isolati iGAS da ospedali situati a Bologna e Imola, senza il nome delle strutture. Nessun punto di ospedale.",
    )
    add(
        "human",
        ["pubmed_32961926"],
        municipality("Parma", municipalities),
        "Parma",
        "comune",
        "Full text: reclutamento di volontari anche a Parma (33 persone), oltre a Bologna. Torino e Bari non sono mappati in questo atlante. Non è un punto ospedaliero.",
    )

    # --- AMR umana: uso/stewardship a scala provinciale ---
    add(
        "human",
        ["pubmed_42095386"],
        provinces(["Piacenza"], province_features),
        "Provincia di Piacenza",
        "provincia",
        "Abstract: analisi del consumo di antibiotici sistemici condotta presso l'AUSL di Piacenza (2021-2024). Full text chiuso; la scala dell'AUSL/provincia è dichiarata. Nessun ospedale inferito.",
    )
    add(
        "human",
        ["pubmed_39317655"],
        provinces(["Reggio nell'Emilia"], province_features),
        "Provincia di Reggio nell'Emilia",
        "provincia",
        "Full text: intervento sui pediatri dell'AUSL di Reggio Emilia (circa 530.000 residenti, la provincia). Il braccio di controllo (altre AUSL regionali) non è mappato come sito di studio.",
    )
    add(
        "human",
        ["pubmed_24030722"],
        provinces(["Modena", "Parma"], province_features),
        "Province di Modena e Parma",
        "provincia",
        "Full text: campagna di informazione attuata nelle province di Modena e Parma (novembre 2011–febbraio 2012). Le altre province della regione erano il controllo e non ricevono un poligono proprio.",
    )

    # --- AMR veterinaria ---
    add(
        "veterinary",
        ["pubmed_40431538"],
        point("vuh_ozzano"),
        place_label("vuh_ozzano"),
        "struttura",
        place_basis(
            "vuh_ozzano",
            "Full text: studio condotto presso il Veterinary University Hospital (VUH) dell'Università di Bologna; l'indirizzo del dipartimento è Via Tolara di Sopra 50, Ozzano dell'Emilia.",
        ),
    )
    add(
        "veterinary",
        ["pubmed_40001129"],
        point("vth_parma"),
        place_label("vth_parma"),
        "struttura",
        place_basis(
            "vth_parma",
            "Full text: prescrizioni antimicrobiche nei gatti visitati all'Ospedale Veterinario Didattico dell'Università di Parma (VTH-UP). Uso, non una prevalenza di resistenza.",
        ),
    )
    add(
        "veterinary",
        ["pubmed_32240057"],
        provinces(["Reggio nell'Emilia"], province_features),
        "Provincia di Reggio nell'Emilia",
        "provincia",
        "Abstract: E. coli da feci e carcasse di suini in aziende e macelli della provincia di Reggio Emilia. Full text chiuso; la provincia è dichiarata. Nessuna azienda o macello è localizzato.",
    )

    # --- AMR alimentare ---
    add(
        "food",
        ["pubmed_31934774"],
        municipality("Parma", municipalities),
        "Parma",
        "comune",
        "Abstract: 182 isolati di E. coli da carni acquistate in tre supermercati non nominati nell'area della «Italian Food Valley» (Parma). Nessun esercizio è localizzato.",
    )
    add(
        "food",
        ["pubmed_42148182"],
        provinces(["Piacenza", "Parma", "Reggio nell'Emilia", "Modena", "Bologna"], province_features),
        "Province di Piacenza, Parma, Reggio nell'Emilia, Modena e Città metropolitana di Bologna",
        "provincia",
        "Full text: cinghiali cacciati in ATC delle province di Parma, Reggio Emilia, Modena, Bologna e Piacenza, poi conferiti a otto centri di lavorazione della selvaggina (GHE) indicati solo come R1–P4. Nessun GHE e nessun sito di caccia è localizzato. L'AMR è un esito accessorio.",
    )

    # --- AMR ambientale: nessuno studio sub-regionale confermato ---
    # I tre lavori sulle api mellifere e gli altri ambientali restano sul contorno regionale.

    # --- Fauna selvatica ---
    add(
        "wildlife",
        ["pubmed_32668681", "pubmed_30854342"],
        provinces(["Parma"], province_features),
        "Provincia di Parma",
        "provincia",
        "Zanardi: quattordici aree di campionamento non nominate, distribuite nella provincia di Parma. Bonardi 2018: cinghiali cacciati in provincia di Parma. Nessun sito di cattura o casa di caccia è localizzato.",
    )

    # --- Contorno regionale ---
    regional_ids = [
        "pubmed_40269796",
        "pubmed_38301758",
        "pubmed_37839149",
        "pubmed_38944352",
        "pubmed_39357073",
        "pubmed_40303743",
        "pubmed_35795463",
        "pubmed_34177854",
        "pubmed_33494307",
        "pubmed_34351529",
        "pubmed_34680787",
        "pubmed_30993338",
        "pubmed_31119408",
        "pubmed_28512231",
        "pubmed_26405817",
        "pubmed_25375901",
        "pubmed_24997585",
        "pubmed_24484182",
        "pubmed_27873629",
        "pubmed_21888564",
        "pubmed_21595784",
    ]
    add(
        "regional",
        regional_ids,
        region,
        "Emilia-Romagna",
        "regione",
        "Gli autori dichiarano l'Emilia-Romagna, più ospedali o aziende non nominati, una rete regionale di alveari, o una filiera regionale. Il contorno regionale non è un punto di misura. Uso/stewardship a scala regionale e AMR clinica, veterinaria, alimentare, ambientale o faunistica dichiarata a scala regionale restano su questo strato, come nell'atlante lombardo.",
    )

    expected = set(by_id)
    got = set(placed)
    if got != expected:
        raise SystemExit(
            f"Copertura incompleta. Mancanti: {sorted(expected - got)}. Extra: {sorted(got - expected)}"
        )

    names = {
        "human": "human_amr_evidence.geojson",
        "veterinary": "veterinary_amr_evidence.geojson",
        "food": "food_chain_amr_evidence.geojson",
        "environment": "environmental_amr_evidence.geojson",
        "wildlife": "wildlife_amr_evidence.geojson",
        "regional": "regional_study_outline.geojson",
    }
    outdir = ROOT / "public/data"
    outdir.mkdir(parents=True, exist_ok=True)
    for key, filename in names.items():
        collection = {"type": "FeatureCollection", "features": layers[key]}
        path = outdir / filename
        path.write_text(json.dumps(collection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{filename}: {len(layers[key])} features")

    print("PLACED", len(placed))
    for study_id in sorted(placed, key=lambda s: placed[s] + s):
        print(f"{study_id}\t{placed[study_id]}")


if __name__ == "__main__":
    main()
