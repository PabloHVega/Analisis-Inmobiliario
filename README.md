# Madrid Short-Term Rental Investment Analysis

> **Business Analytics case study** — identifying the most profitable property profiles for tourist rental investment in Madrid using Airbnb public data.

---

## Business Problem

A real estate investment firm wants to enter the Madrid tourist rental market. The goal is to determine **which property profiles** and **which districts/neighbourhoods** maximise commercial potential, so the acquisitions team knows exactly what to look for.

---

## Data Sources

| Dataset | Description |
|---|---|
| **Inside Airbnb** (Sept 2025) | ~20,000 active listings in Madrid — price, occupancy, location, property type |
| **Idealista** | Price per m² by district — used to estimate acquisition cost |
| **POIs Madrid** | Points of interest with weighted importance — used to build a custom tourism attractiveness index |

All raw data is loaded into a **SQLite database** (`datos/intermedios/`) for reproducibility.

---

## Methodology

The project follows a **Business Analytics Discovery** approach structured in three notebooks:

### `01_ImportacionDatos` — Data ingestion
Loads Airbnb listings, detailed listings and Idealista price data into SQLite.

### `02_CreacionVariables` — Feature engineering
Constructs the key business KPIs from raw data:

| Variable | Logic |
|---|---|
| `precio_noche_total` | Adjusted nightly revenue accounting for room type (entire home / private room / shared) and capacity |
| `estimated_occupancy_l365d` | Annual rental days (fixed at 365 as conservative upper bound) |
| `ingreso_anual` | `precio_noche_total × occupancy` |
| `m2_estimado` | Estimated surface area based on bedroom/bathroom count |
| `coste_adquisicion` | `m² × price_per_m² × 0.75` (25% discount reflecting purchase negotiation power) |
| `margen_bruto` | `ingreso_anual / coste_adquisicion` — the main profitability KPI |
| `atractivo_turistico` | Custom index (0–100) based on weighted Haversine distance to Madrid's main tourist POIs |

### `03_Analisis` — Analysis & insights
- Univariate price and occupancy analysis by district and neighbourhood
- **Mini-cube** methodology: pre-aggregated metrics across all dimensions (district, neighbourhood, room type, bedrooms, accommodates, beds) for fast multi-dimensional exploration
- Filtered opportunity identification with scatter plots and heatmaps
- Four interactive Folium maps exported to `entregables/graficos/`

---

## Key Findings

### Optimal property profile
> **2–3 bedrooms · 3+ guests · Entire home/apt**
> Achievable gross margins up to **40%**

### Priority districts
| District | Why |
|---|---|
| **Barajas** | Properties under €200K with >200 days occupancy and >10% margin. Also viable as private/shared rooms — unique in Madrid |
| **Centro** | Highest nightly prices; best margins for entire flats |
| **Arganzuela** | Good margin/price balance with lower acquisition cost than Centro |
| **Villa de Vallecas** | Emerging zone with above-average margins relative to acquisition cost |

### Secondary targets
- **5+ bedrooms** → Usera, Moratalaz, Puente de Vallecas
- **3 bedrooms** → Carabanchel
- **2 bedrooms** → San Blas

### Room type recommendation
Buy **entire apartments** in all priority districts. Barajas is the only exception where private and shared rooms also deliver solid returns.

---

## Deliverables

| File | Content |
|---|---|
| `entregables/graficos/mapa_rentabilidad.html` | Heatmap — properties with gross margin ≥ 20% |
| `entregables/graficos/mapa_ocupacion.html` | Heatmap — properties with occupancy ≥ 250 days/year |
| `entregables/graficos/mapa_oportunidades.html` | Opportunity map — margin ≥ 15% **AND** occupancy ≥ 250 days |
| `entregables/graficos/mapa_barajas.html` | Barajas deep-dive map |
| `entregables/informes/informeFinal.html` | Final report |

---

## Tech Stack

`Python` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `folium` · `haversine` · `SQLite`

---

## Project Structure

```
datos/
  brutos/          ← Raw CSVs (Airbnb, Idealista, POIs)
  intermedios/     ← SQLite database
  procesados/      ← Clean outputs
notebooks/
  01_ImportacionDatos.ipynb
  02_CreacionVariables.ipynb
  03_Analisis.ipynb
funciones/
  funciones.py     ← tourism_index(), tourism heatmap helper
entregables/
  graficos/        ← Interactive Folium maps
  informes/        ← Final HTML report
docs/              ← Project objectives, methodology notes, provisional insights
```
