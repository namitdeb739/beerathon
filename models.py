from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MovieSummary:
    id: str
    title: str
    year: Optional[str] = None
    poster: Optional[str] = None


@dataclass
class MovieDetails:
    title: str
    year: Optional[str] = None
    genre: Optional[str] = None
    plot: Optional[str] = None
    director: Optional[str] = None
    runtime: Optional[str] = None
    poster: Optional[str] = None


@dataclass
class CocktailPairing:
    name: str
    recipe: List[str]
    why: str
