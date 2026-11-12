# Dati mappa-ready — atlante One Health AMR dell'Emilia-Romagna

Drop-in per un agente di coding: schema, nomi file, campi popup e avvertenza sono allineati a `aguaraglia/lombardy-one-health-amr-atlas` (main, 2026-11-12). Nessuna scrittura su GitHub in questo passo.

Edizione: `erm_amr_atlas`. Fonte geografica: ISTAT confini generalizzati 1 gennaio 2026 (`Limiti01012026_g.zip`), `COD_REG=8`, WGS84 (EPSG:4326). 330 comuni, 8 province + Città metropolitana di Bologna, 1 regione. I poligoni sono già la versione generalizzata ISTAT, adatta al web.

Avvertenza popup (tutti gli strati letteratura): *Il segnaposto indica dove è stato condotto lo studio, non una prevalenza.*

## Cosa va dove

| Strato | File | Feature | Studi (unici) |
|---|---|---:|---:|
| AMR umana | `public/data/human_amr_evidence.geojson` | 11 | 16 |
| AMR veterinaria | `public/data/veterinary_amr_evidence.geojson` | 3 | 3 |
| AMR alimentare | `public/data/food_chain_amr_evidence.geojson` | 2 | 2 |
| AMR ambientale | `public/data/environmental_amr_evidence.geojson` | 0 | 0 |
| AMR nella fauna selvatica | `public/data/wildlife_amr_evidence.geojson` | 1 | 2 |
| Studi a scala regionale (contorno non riempito) | `public/data/regional_study_outline.geojson` | 1 | 21 |

Catalogo: 44 studi mappati (`public/data/literature-catalog.json`). Partenza di scoping: 45 inclusi.

Strato ambientale vuoto di proposito: i tre lavori su api mellifere (Cilia 2023, Resci 2024 colistina, Resci 2024 modelli) e gli altri ambientali sono dichiarati a scala regionale (33 apiari/colonie non nominati, in tutte le province). Restano sul contorno regionale. Nessun alveare è localizzato.

Campi feature (identici alla Lombardia): `place`, `geography_level` (struttura / comune / provincia / regione), `geography_basis`, `study_count`, `study_ids`, `authors`, `year`, `title`, `sector`, `organism`, `doi` (`https://doi.org/…`), `geography_note`. Più studi nello stesso luogo sono uniti con ` | `. Uno studio può comparire in due feature se gli autori dichiarano due luoghi (Bonomo: Bologna e Imola; Milanović: Bologna e Parma).

### Punti di struttura (OSM Nominatim, 2026-11-12, 1 req/s, User-Agent identificabile)

- IRCCS AOU di Bologna, Policlinico Sant'Orsola-Malpighi (11.36096, 44.49153) — cinque studi umani (Cetatean, Djusse, Calza, Foschi; Fiorini elevato dal comune dopo il full text: «S. Orsola Hospital»).
- Policlinico di Modena, Via del Pozzo 71 (10.94215, 44.63535) — Gentile 2020 (MUHP, 677 posti letto, nominato esplicitamente).
- Hesperia Hospital, Via Arquà 80, Modena (10.92393, 44.62608) — Pedretti 2024.
- Ospedale Maggiore / AOU di Parma, Viale Gramsci (10.30830, 44.80162) — Nouvenne 2014.
- Ospedale veterinario universitario Giuseppe Gentile, Via Tolara di Sopra 50, Ozzano dell'Emilia (11.48650, 44.43607) — Scarpellini 2025 (cani e gatti).
- Ospedale Veterinario Didattico, Università di Parma: Nominatim non ha un POI distinto; il punto è il Dipartimento di Scienze Medico-Veterinarie, Strada del Taglio (10.30821, 44.81986) — Fidanzio 2025 (uso antimicrobico nel gatto). Non è un allevamento.

### Poligoni ISTAT

- Comuni: Modena (Coloretti e Di Marcello, degradati); Bologna (Menozzi, Bonomo, Milanović); Imola (Bonomo); Parma (Milanović; Barilli sullo strato alimentare).
- Province: Piacenza (Confalonieri, consumo AUSL); Reggio nell'Emilia (Corsini, AMU pediatrica; Bacci, suini, nessuna azienda localizzata); Modena e Parma insieme (Formoso, campagna AMU); Parma (Zanardi micromammiferi e Bonardi 2018 cinghiali ESBL, nessuna casa di caccia); cinque province dell'Appennino/ovest (Andriani 2026, carni di cinghiale: ATC in Piacenza, Parma, Reggio nell'Emilia, Modena e Città metropolitana di Bologna; otto GHE anonimi non puntati).

## Uso e stewardship (come in Lombardia)

- AMU/stewardship **regionali** (Servadio, D'Annibali, Buccellato 2014 e 2015, Holstiege, Pan 2011 e 2013, Barbarossa uso nei piccoli animali) → **contorno regionale**, come gli AMU ospedalieri e territoriali lombardi a scala di regione.
- AMU **provinciale** (Confalonieri AUSL Piacenza; Corsini AUSL Reggio Emilia; Formoso campagne Modena e Parma) → **strato AMR umana**, poligoni ISTAT di provincia, senza inferire ospedali. Equivale al pattern lombardo dell'uso antimicrobico a scala provinciale (es. allevamenti di Lodi sullo strato veterinario, senza punti azienda).
- Stewardship di **struttura nominata**: il modello San Matteo andrebbe su un punto ospedaliero. Di Marcello 2025 descrive un unico centro, «University Hospital of Modena» da 1200 posti letto (l'AOU nel suo insieme), senza distinguere Policlinico e Baggiovara → **comune di Modena**, non un campus presunto.
- Uso in **ospedale veterinario nominato** (Fidanzio, VTH Parma) → **strato veterinario**, punto di struttura.

## Esclusioni e ritocchi rispetto allo scoping (45)

Nuova esclusione (regola Ferrara: in dubbio, si esclude):

- **PMID 35740183, Bonardi et al. 2022.** Lo scoping lo collocava in provincia di Parma (suini al macello e pazienti ospedalizzati). Il full text precisa che i 300 lotti suini provenivano da 95 aziende di Lombardia, Veneto, Emilia-Romagna, Piemonte e Toscana, **72 delle 95 in Lombardia**. Il macello in provincia di Parma non è l'origine territoriale degli animali. Mappare lo studio come AMR veterinaria parmense sarebbe fuorviante; la componente umana da sola, con settore «AMR veterinaria», lo sarebbe altrettanto.

Degradati al comune (scala dichiarata di struttura non confermata sul full text):

- **PMID 41750467, Coloretti et al. 2026** — due ICU del «Modena University Hospital», senza Policlinico vs Baggiovara.
- **PMID 41079141, Di Marcello et al. 2025** — AOU di Modena da 1200 posti letto, campus non distinto.

Elevati o raffinati dopo il full text (non sono esclusioni):

- **PMID 32370005, Fiorini et al. 2020** — da comune di Bologna a Sant'Orsola (il full text nomina «S. Orsola Hospital»).
- **PMID 32961926, Milanović et al. 2020** — oltre a Bologna, il full text aggiunge il sito di arruolamento di Parma (33 volontari). Torino e Bari restano fuori ambito.
- **PMID 42148182, Andriani et al. 2026** — dallo scoping regionale alle cinque province nominati nel full text (ATC); i GHE restano anonimi.

Le 26 esclusioni/dubbi dello scoping restano valide (tra cui Viale 25658534, Gaibani 22152705, Pavoni 38060805, Pavesi 39847160, Tenuzzo, Sampieri, STEC senza AMR, «MODENA extender»).

Nessuna azienda, latteria, casa di caccia, supermercato o alveare anonimo è stato geolocalizzato.

## File

```
build/
  README.md
  public/data/literature-catalog.json
  public/data/layer-catalog.json
  public/data/human_amr_evidence.geojson
  public/data/veterinary_amr_evidence.geojson
  public/data/food_chain_amr_evidence.geojson
  public/data/environmental_amr_evidence.geojson
  public/data/wildlife_amr_evidence.geojson
  public/data/regional_study_outline.geojson
  public/geography/atlas_municipalities.geojson
  public/geography/atlas_provinces.geojson
  public/geography/atlas_region.geojson
  scripts/build_istat_geography.py
  scripts/build_study_evidence_layers.py
```

I due script riproducono geografia e strati. Confini ISTAT sorgente: `/workspace/emilia-romagna/raw/istat/src/`. Nominatim grezzo: `/workspace/emilia-romagna/raw/nominatim_facilities.json` e `nominatim_retries.json`.

Popup da usare (come in Lombardia): `geography_level`, `geography_basis`, `authors`, `year`, `title`, `sector`, `organism`, `doi`, `geography_note`. Etichette IT: Scala, Base geografica, Autori, Anno, Titolo, Settore, Organismo o ARG, DOI, Avvertenza. Lo strato regionale ha `fillOpacity: 0` e peso 2.8.
