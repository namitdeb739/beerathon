import json
from typing import Optional

from ui.components import appbar, divider, load_css, result_card_html, section_title
from services.utils import get_omdb_api_key
from models import MovieDetails, CocktailPairing

import streamlit as st
import app_constants as C


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
    api_key = get_omdb_api_key()
    if not api_key:
        st.error(C.ERROR_OMDB_KEY_NOT_CONFIGURED)
        matches = []
    else:
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
    try:
        api_key = get_omdb_api_key()
        if api_key:
            from services.omdb import get_movie_by_id
            details = get_movie_by_id(m["id"], api_key)
            payload = {
                "title": details.get("Title"),
                "year": details.get("Year"),
                "genre": details.get("Genre"),
                "plot": details.get("Plot"),
                "director": details.get("Director"),
                "runtime": details.get("Runtime"),
            }
            st.session_state[C.KEY_SELECTED_MOVIE_JSON] = json.dumps(payload)
        else:
            st.session_state[C.KEY_SELECTED_MOVIE_JSON] = json.dumps({
                "title": m.get("title"),
                "year": m.get("year"),
            })
    except Exception:
        st.session_state[C.KEY_SELECTED_MOVIE_JSON] = json.dumps({
            "title": m.get("title"),
            "year": m.get("year"),
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
    st.markdown("<div class='dialog-grid'>", unsafe_allow_html=True)
    st.markdown("<div class='dialog-section'>", unsafe_allow_html=True)
    if movie.poster:
        st.markdown(
            f"<img src='{movie.poster}' alt='Poster' class='poster' />",
            unsafe_allow_html=True,
        )
    title_line = movie.title + (f" ({movie.year})" if movie.year else "")
    st.markdown(
        f"<div class='cocktail-name'>{title_line}</div>", unsafe_allow_html=True)
    bits = [b for b in [movie.genre, movie.director, movie.runtime] if b]
    if bits:
        st.markdown(
            f"<div class='cocktail-meta'>{' • '.join(bits)}</div>", unsafe_allow_html=True)
    if movie.plot:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<b>Plot</b>")
        st.write(movie.plot)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='dialog-section'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='cocktail-name'>🍹 {pairing.name}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='cocktail-meta'>{C.PAIRING_SUBTITLE}</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(f"<b>{C.LABEL_RECIPE}</b>")
    st.markdown(
        "<ul class='recipe-list'>" +
        "".join([f"<li>{i}</li>" for i in pairing.recipe]) + "</ul>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<b>{C.LABEL_WHY}</b>")
    st.markdown(pairing.why)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
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
    from services.cocktails import get_cocktail_for_movie
    if st.session_state.get(C.KEY_OPEN_COCKTAIL_DIALOG) and not st.session_state.get(C.KEY_COCKTAIL_INFO):
        st.session_state[C.KEY_COCKTAIL_INFO] = get_cocktail_for_movie(
            selected.get("title", "")
        )
    pairing = st.session_state.get(C.KEY_COCKTAIL_INFO) or get_cocktail_for_movie(
        selected.get("title", "")
    )
    movie = build_movie_details(
        selected, st.session_state.get(C.KEY_SELECTED_MOVIE_JSON))
    if hasattr(st, "dialog"):
        try:
            def _content():
                render_pairing_dialog(movie, pairing)
            st.dialog(C.DIALOG_TITLE)(_content)()
            return
        except Exception:
            pass
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_pairing_dialog(movie, pairing)
        st.markdown("</div>", unsafe_allow_html=True)


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
