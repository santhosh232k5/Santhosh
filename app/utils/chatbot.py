from typing import Optional, Tuple

from .constants import SERVICE_CATEGORIES

CITY_COORDS = {
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "hyderabad": (17.3850, 78.4867),
}

KEYWORDS = {
    "Electrical Works": ["electric", "wiring", "switch", "fan", "light"],
    "Plumbing": ["plumb", "pipe", "tap", "water leak", "drain"],
    "Carpentry": ["carpenter", "wood", "furniture", "door", "shelf"],
    "Painting": ["paint", "wall color", "repaint"],
    "Masonry": ["mason", "brick", "concrete", "tiles"],
    "Cleaning": ["clean", "deep clean", "sanitization"],
    "Appliance Repair": ["appliance", "fridge", "ac", "washing machine", "repair"],
}


def detect_service(message: str) -> Optional[str]:
    lower = message.lower()
    for category in SERVICE_CATEGORIES:
        if category.lower() in lower:
            return category
    for category, terms in KEYWORDS.items():
        if any(term in lower for term in terms):
            return category
    return None


def detect_location(message: str) -> Optional[Tuple[float, float]]:
    lower = message.lower()
    for city, coords in CITY_COORDS.items():
        if city in lower:
            return coords

    parts = message.replace(",", " ").split()
    numbers = []
    for token in parts:
        try:
            numbers.append(float(token))
        except ValueError:
            continue

    if len(numbers) >= 2:
        return numbers[0], numbers[1]
    return None
