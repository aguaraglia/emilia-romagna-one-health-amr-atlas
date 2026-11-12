# Geografia pubblica

Cartografia amministrativa dell'edizione Emilia-Romagna, da ISTAT, confini generalizzati al 1° gennaio 2026 (archivio `Limiti01012026_g.zip`, licenza CC BY 4.0):

- `atlas_region.geojson`: confine regionale, codice ISTAT 08;
- `atlas_provinces.geojson`: 8 province e la Città metropolitana di Bologna;
- `atlas_municipalities.geojson`: 330 comuni.

I nomi sono letti in UTF-8. Le coordinate sono trasformate da EPSG:32632 a EPSG:4326. Lo script è `scripts/build_istat_geography.py`.

Non sono pubblicati il reticolo idrografico né le geometrie degli impianti di depurazione: per le acque reflue urbane è censito soltanto il dataset aperto ARPAE ARU-HERA, senza estrazione di valori e senza layer cartografico.

Gli studi della letteratura stanno nei layer distinti sotto `public/data/`. Il file `regional_study_outline.geojson` è il contorno regionale non riempito, riservato agli studi a scala regionale.
