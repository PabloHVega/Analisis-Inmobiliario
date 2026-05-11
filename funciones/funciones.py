from haversine import haversine
import pandas as pd


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
