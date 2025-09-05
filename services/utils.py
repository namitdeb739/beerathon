import os
from typing import Optional
import streamlit as st
import app_constants as C


def get_omdb_api_key() -> Optional[str]:
    try:
        s = st.secrets
        if C.SECRETS_OMDB_KEY in s:
            return s[C.SECRETS_OMDB_KEY]
        if C.SECRETS_OMDB_KEY_ALT in s:
            return s[C.SECRETS_OMDB_KEY_ALT]
        if C.SECRETS_SECTION in s and C.SECRETS_SECTION_KEY in s[C.SECRETS_SECTION]:
            return s[C.SECRETS_SECTION][C.SECRETS_SECTION_KEY]
    except Exception:
        pass
    return os.environ.get(C.ENV_OMDB_KEY)
