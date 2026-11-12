# Emilia-Romagna One Health AMR Atlas

Edizione regionale `erm_amr_atlas`, curata da CodexVitae ETS.

Sito pubblico: <https://aguaraglia.github.io/emilia-romagna-one-health-amr-atlas/>

## Stato

La superficie pubblica contiene i confini ISTAT generalizzati al 1° gennaio 2026 (330 comuni, 8 province e la Città metropolitana di Bologna) e la letteratura georeferenziata in `public/data/`. Il numero di studi è la lunghezza di `records` in `literature-catalog.json`. Le fonti istituzionali in `public/data/evidence-catalog.json` sono censite e non hanno indicatori estratti. La nota di costruzione dei layer è in `reports/MAP_READY_DATA.md`.

## Pagine

`index.html` è il cruscotto con la mappa Leaflet. Le altre pagine sono `evidence.html`, `publications.html`, `methodology.html`, `about.html` e `dissemination.html`. Il sito è la radice del ramo `main`. Non c'è un CNAME.

GitHub Pages va impostato su Deploy from a branch, ramo `main`, cartella `/` (root). La creazione del sito via API risponde 403 (`Resource not accessible by integration`) sia con il token di push sia con il token del workflow: l'abilitazione resta da fare nelle impostazioni del repository.

## Directory

- `public/`: geografie e cataloghi approvati per il sito;
- `assets/`: foglio di stile, cruscotto, pubblicazioni e dodici moduli divulgativi;
- `private/`: dati riservati, esclusi dal repository salvo questo README;
- `raw/`: fonti originali, escluse dal repository;
- `metadata/`: fonti e snapshot;
- `schema/`: schemi, compresi quelli della letteratura ancora vuota;
- `scripts/`: costruzione dei confini ISTAT e del profilo regionale;
- `reports/`: audit;
- `releases/`: pacchetti congelati, non ancora prodotti.

## File di letteratura da compilare

Gli schemi sono in `schema/literature_catalog.schema.json` e `schema/study_evidence_feature.schema.json`.

- `public/data/literature-catalog.json` — ogni record ha `id`, `year`, `title`, `authors`, `journal`, `scope`, `geographic_link`, `pmid`, `doi`, `source_url`.
- `public/data/human_amr_evidence.geojson`
- `public/data/veterinary_amr_evidence.geojson`
- `public/data/food_chain_amr_evidence.geojson`
- `public/data/environmental_amr_evidence.geojson`
- `public/data/wildlife_amr_evidence.geojson`

Ogni feature ha geometria `Point`, `Polygon` o `MultiPolygon` e le proprietà `place`, `geography_level`, `geography_basis`, `study_count`, `study_ids`, `authors`, `year`, `title`, `sector`, `organism`, `doi`, `geography_note`. Lo strato ambientale può restare senza feature quando gli studi sono dichiarati a scala regionale.

- `public/data/regional_study_outline.geojson` — il confine regionale ISTAT, con `fillOpacity` 0 nel catalogo dei layer. Gli studi a scala regionale stanno su questo contorno, non su un punto di misura.

`geography_note` resta: «Il segnaposto indica dove è stato condotto lo studio, non una prevalenza.»

Il popup mostra autore, anno, titolo, settore, organismo o ARG, DOI e quell'avvertenza. I campi vuoti non sono mostrati.
