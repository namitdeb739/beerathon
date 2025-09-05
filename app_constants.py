from pathlib import Path

# Page setup
APP_TITLE = "Clanker That Recommends Alcohol"
PAGE_ICON = "🍺"
CSS_FILE = "styles/movie_theater.css"

# UI labels and text
SECTION_FIND_MOVIE = "Find a movie"
SECTION_SELECT_MOVIE = "Select your movie"
PLACEHOLDER_TITLE = "e.g., Casablanca"
PLACEHOLDER_YEAR = "e.g., 1942"
BTN_SEARCH = "Search"
BTN_CHOOSE = "Choose"
BTN_CLOSE = "Close"
PAIRING_SUBTITLE = "Your movie-inspired pairing"
LABEL_RECIPE = "Recipe"
LABEL_WHY = "Why this cocktail?"
BADGE_MOVIE = "movie"
DIALOG_TITLE = "Your cocktail pairing"

# Messages
MSG_CSS_NOT_FOUND = "Custom CSS not found."
ERROR_OMDB_KEY_NOT_CONFIGURED = (
    "OMDb API key not configured. Add it to .streamlit/secrets.toml as omdb_api_key or [omdb].api_key"
)
ERROR_SEARCH_FAILED = "Search failed. Please try again."
SPINNER_SEARCHING = "Searching OMDb..."

# Session state keys
KEY_LAST_MATCHES = "last_matches"
KEY_LAST_QUERY = "last_query"
KEY_LAST_YEAR = "last_year"
KEY_SELECTED_MOVIE = "selected_movie"
KEY_OPEN_COCKTAIL_DIALOG = "open_cocktail_dialog"
KEY_COCKTAIL_INFO = "cocktail_info"
KEY_SELECTED_MOVIE_JSON = "selected_movie_json"

# Config/secrets keys
SECRETS_OMDB_KEY = "omdb_api_key"
SECRETS_OMDB_KEY_ALT = "OMDB_API_KEY"
SECRETS_SECTION = "omdb"
SECRETS_SECTION_KEY = "api_key"
ENV_OMDB_KEY = "OMDB_API_KEY"

# Utility


def css_path() -> Path:
    return Path(CSS_FILE)
