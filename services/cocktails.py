from typing import Dict, List, cast
from models import CocktailPairing


def get_cocktail_for_movie(title: str) -> CocktailPairing:
    mapping: Dict[str, Dict[str, List[str] | str]] = {
        "Casablanca": {
            "cocktail": "French 75",
            "recipe": [
                "1 oz gin",
                "1/2 oz lemon juice",
                "1/2 oz simple syrup",
                "3 oz Champagne",
                "Lemon twist",
            ],
            "why": "Classic, elegant, and timeless—like the film's romance and wartime poise.",
        },
        "Pulp Fiction": {
            "cocktail": "White Russian",
            "recipe": [
                "2 oz vodka",
                "1 oz coffee liqueur",
                "1 oz heavy cream",
            ],
            "why": "A cheeky nod to the film's pop-culture cool and offbeat humor.",
        },
        "Inception": {
            "cocktail": "Negroni",
            "recipe": [
                "1 oz gin",
                "1 oz Campari",
                "1 oz sweet vermouth",
                "Orange peel",
            ],
            "why": "Layered, bitter-sweet complexity mirrors the film's nested dreamscapes.",
        },
        "The Godfather": {
            "cocktail": "Godfather",
            "recipe": [
                "1.5 oz Scotch",
                "1.5 oz amaretto",
                "Orange twist (optional)",
            ],
            "why": "Namesake cocktail—smooth with a quiet authority, fitting the family saga.",
        },
        "Schindler's List": {
            "cocktail": "Mocktail - Pomegranate Spritz",
            "recipe": [
                "2 oz pomegranate juice",
                "1 oz soda water",
                "Squeeze of lemon",
                "Rosemary sprig",
            ],
            "why": "Respectful, sober pairing—somber tones with a subtle, reflective profile.",
        },
    }
    picked = mapping.get(
        title,
        {
            "cocktail": "Old Fashioned",
            "recipe": [
                "2 oz bourbon",
                "2 dashes Angostura bitters",
                "1 sugar cube",
                "Orange peel",
            ],
            "why": "A versatile classic that pairs with many narratives—simple, bold, and storied.",
        },
    )
    name = cast(str, picked["cocktail"])
    recipe = cast(List[str], picked["recipe"])
    why = cast(str, picked["why"])
    return CocktailPairing(name=name, recipe=recipe, why=why)
