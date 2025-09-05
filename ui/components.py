from pathlib import Path
import streamlit as st


def load_css(file_path: Path) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def appbar(title: str) -> None:
    st.markdown(
        f"""
        <div class='appbar'>
            <h1 class='appbar-title'>{title}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str, level: int = 3) -> None:
    level = max(1, min(level, 6))
    st.markdown(
        f"<h{level} class='section-title'>{text}</h{level}>", unsafe_allow_html=True)


def divider() -> None:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


def result_card_html(poster_url: str | None, title: str, year: str | None) -> str:
    poster_html = f"<img src='{poster_url}' alt='Poster' class='poster' />" if poster_url else ""
    return f"""
    <div class='result-card'>
        {poster_html}
        <div class='result-title'>{title}{f" ({year})" if year else ''}</div>
    </div>
    """
