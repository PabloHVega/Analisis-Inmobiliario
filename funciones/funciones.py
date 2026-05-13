from haversine import haversine
import pandas as pd

# Imports para el mapa de calor de atractivo turistico
import folium
from folium.plugins import HeatMap


def tourism_index(lat, lon, pois, weights=None, max_distance=5):
    """
    Calcula un índice turístico normalizado (0-100)
    Parámetros:
    - lat, lon: coordenadas del inmueble
    - pois: dict con nombre -> (lat, lon)
    - weights: dict opcional con nombre -> peso
    - max_distance: distancia máxima considerada (km)
    Retorna:
    - índice entre 0 y 100
    """
    total_score = 0
    total_weight = 0

    for name, coord in pois.items():
        d = haversine((lat, lon), coord)
        w = weights.get(name, 1) if weights is not None else 1
        score = max(0, (max_distance - d) / max_distance)
        total_score += score * w
        total_weight += w

    if total_weight == 0:
        return 0
    return (total_score / total_weight) * 100


def guardar_mapa_atractivo_turistico(
    df, ruta_guardado="../docs/mapa_atractivo_turistico.html"
):
    """
    Genera y guarda un mapa de calor de atractivo turístico en la ruta especificada.
    Parámetros:
    - df: DataFrame con columnas 'latitude', 'longitude', 'atractivo_turistico'
    - ruta_guardado: ruta donde se guardará el archivo HTML
    """
    import folium
    from folium.plugins import HeatMap

    madrid_center = [40.4168, -3.7038]
    m = folium.Map(location=madrid_center, zoom_start=12)
    heat_data = (
        df[["latitude", "longitude", "atractivo_turistico"]].dropna().values.tolist()
    )
    HeatMap(
        heat_data,
        min_opacity=0.2,
        max_opacity=0.8,
        radius=15,
        blur=20,
        gradient={0.2: "blue", 0.5: "lime", 0.8: "red"},
    ).add_to(m)
    m.save(ruta_guardado)
    print(f"Mapa guardado en {ruta_guardado}")
