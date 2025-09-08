import app_constants as C
import streamlit as st
from models import MovieDetails, CocktailPairing
import json
from typing import Optional

from ui.components import appbar, divider, load_css, result_card_html, section_title
OMDB_API_KEY = "3b628e0a"


st.set_page_config(layout="wide", page_title=C.APP_TITLE,
                   page_icon=C.PAGE_ICON)


@st.cache_data(show_spinner=False, ttl=3600)
def omdb_search_cached(title: str, year: Optional[str], api_key: str):
    from services.omdb import search_movies
    return search_movies(title, year, api_key)


def load_theme() -> None:
    css = C.css_path()
    if css.exists():
        load_css(css)
    else:
        st.warning(C.MSG_CSS_NOT_FOUND)


def render_search_form():
    section_title(C.SECTION_FIND_MOVIE, level=3)
    with st.form(key="search_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            title = st.text_input("Title", placeholder=C.PLACEHOLDER_TITLE)
        with col2:
            year = st.text_input("Year", placeholder=C.PLACEHOLDER_YEAR)
        with col3:
            st.markdown("<div class='button-spacer'></div>",
                        unsafe_allow_html=True)
            submitted = st.form_submit_button(
                C.BTN_SEARCH, use_container_width=True)
    return submitted, title, year


def run_search(title: str, year: Optional[str]):
    api_key = OMDB_API_KEY
    with st.spinner(C.SPINNER_SEARCHING):
        try:
            matches = omdb_search_cached(title, year, api_key)
        except Exception:
            matches = []
            st.error(C.ERROR_SEARCH_FAILED)
    st.session_state[C.KEY_LAST_MATCHES] = matches
    st.session_state[C.KEY_LAST_QUERY] = title
    st.session_state[C.KEY_LAST_YEAR] = year


def on_choose_movie(m: dict):
    st.session_state[C.KEY_SELECTED_MOVIE] = m
    st.session_state[C.KEY_OPEN_COCKTAIL_DIALOG] = True
    st.session_state["show_loading"] = True
    try:
        api_key = OMDB_API_KEY
        from services.omdb import get_movie_by_id
        imdb_id = str(m.get("id") or "")
        details = get_movie_by_id(imdb_id, api_key)
        payload = {
            "title": details.get("Title"),
            "year": details.get("Year"),
            "genre": details.get("Genre"),
            "director": details.get("Director"),
            "runtime": details.get("Runtime"),
            "plot": details.get("Plot"),
            "poster": details.get("Poster"),
        }
        st.session_state[C.KEY_SELECTED_MOVIE_JSON] = json.dumps(payload)
    except Exception:
        st.session_state[C.KEY_SELECTED_MOVIE_JSON] = json.dumps({
            "title": m.get("title"),
            "year": m.get("year"),
            "genre": m.get("genre"),
            "director": m.get("director"),
            "runtime": m.get("runtime"),
            "plot": m.get("plot"),
            "poster": m.get("poster"),
        })


def render_results(matches: list[dict]):
    divider()
    section_title(C.SECTION_SELECT_MOVIE, level=4)
    cols = st.columns(4)
    for idx, m in enumerate(matches):
        with cols[idx % 4]:
            st.markdown(
                result_card_html(m.get("poster"), m.get(
                    "title", ""), m.get("year")),
                unsafe_allow_html=True,
            )
            if st.button(C.BTN_CHOOSE, key=f"choose_{m.get('id')}", use_container_width=True):
                on_choose_movie(m)


def build_movie_details(selected: dict, payload_json: Optional[str]) -> MovieDetails:
    try:
        payload = json.loads(payload_json) if payload_json else {}
    except Exception:
        payload = {}
    return MovieDetails(
        title=str(payload.get("title") or selected.get("title") or ""),
        year=payload.get("year"),
        genre=payload.get("genre"),
        plot=payload.get("plot"),
        director=payload.get("director"),
        runtime=payload.get("runtime"),
        poster=selected.get("poster"),
    )


def render_pairing_dialog(movie: MovieDetails, pairing: CocktailPairing):
    st.markdown("""
        <style>
        .fullwidth-dialog .stButton, .fullwidth-dialog .stMarkdown, .fullwidth-dialog .stImage {max-width: 100vw !important;}
        .fullwidth-dialog {width: 100vw !important; max-width: 100vw !important; margin-left: -10vw; margin-right: -10vw;}
        </style>
    """, unsafe_allow_html=True)
    with st.container():
        cols = st.columns([1, 1], gap="large")
        with cols[0]:
            if movie.poster:
                st.image(movie.poster, use_container_width=True)
            st.markdown(
                f"### {movie.title} {'(' + movie.year + ')' if movie.year else ''}")
            meta = " • ".join(
                [b for b in [movie.genre, movie.director, movie.runtime] if b])
            if meta:
                st.markdown(f"*{meta}*")
            if movie.plot:
                st.markdown("**Plot**")
                st.write(movie.plot)
        with cols[1]:
            st.markdown(f"### 🍸 {pairing.name}")
            st.markdown(f"*{C.PAIRING_SUBTITLE}*")
            st.markdown("**Recipe**")
            for ingredient in pairing.recipe:
                st.markdown(f"- {ingredient}")
            st.markdown("**Why this cocktail?**")
            st.write(pairing.why)
        st.button(
            C.BTN_CLOSE,
            key="close_cocktail_dialog_btn",
            use_container_width=True,
            on_click=lambda: st.session_state.update(
                {C.KEY_OPEN_COCKTAIL_DIALOG: False, C.KEY_COCKTAIL_INFO: None}
            ),
        )


def maybe_show_dialog():
    selected = st.session_state.get(C.KEY_SELECTED_MOVIE)
    if not selected:
        return
    import requests

    def fetch_cocktail_pairing(movie_title: str):
        try:
            resp = requests.post(
                "http://localhost:8000/pairing", json={"movie": movie_title}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("success") and data.get("cocktail"):
                    return CocktailPairing(
                        name=data["cocktail"]["name"],
                        recipe=data["cocktail"].get("ingredients", []),
                        why=data.get("explanation", "")
                    )
            return None
        except Exception:
            return None
    pairing = None
    loading = st.session_state.get("show_loading", True)
    if st.session_state.get(C.KEY_OPEN_COCKTAIL_DIALOG) and not st.session_state.get(C.KEY_COCKTAIL_INFO):
        if loading:
            st.markdown("""
                <div style='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:99999;background:rgba(20,20,30,0.85);display:flex;justify-content:center;align-items:center;'>
                    <div style='text-align:center;'>
                        <div style='font-size:3rem;'>⏳</div>
                        <div style='margin-top:1rem;font-size:1.3rem;color:#ffd700;'>Finding your perfect cocktail pairing...</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        pairing = fetch_cocktail_pairing(selected.get("title", ""))
        st.session_state[C.KEY_COCKTAIL_INFO] = pairing
        st.session_state["show_loading"] = False
        loading = False
    if pairing is None:
        pairing = st.session_state.get(C.KEY_COCKTAIL_INFO)
    if pairing is None:
        pairing = fetch_cocktail_pairing(selected.get("title", ""))
    movie_json = st.session_state.get(C.KEY_SELECTED_MOVIE_JSON)
    if not movie_json:
        return
    movie = build_movie_details(selected, movie_json)
    if pairing and not loading:
        if hasattr(st, "dialog"):
            try:
                def _content():
                    render_pairing_dialog(movie, pairing)
                st.dialog(C.DIALOG_TITLE)(_content)()
                return
            except Exception:
                pass
        render_pairing_dialog(movie, pairing)


def main() -> None:
    load_theme()
    appbar(C.APP_TITLE)
    submitted, title, year = render_search_form()
    if submitted and title:
        run_search(title, year)
    matches = st.session_state.get(C.KEY_LAST_MATCHES, [])
    if matches:
        render_results(matches)
    maybe_show_dialog()


if __name__ == "__main__":
    main()
