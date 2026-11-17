"""Paste this into PythonAnywhere -> Web -> WSGI configuration file.

THIS FILE IS NOT PART OF THE APP.  Do not copy it into the repository's
`wsgi.py`, and do not import it from `wsgi.py` - it imports `wsgi`, so doing
either creates a circular import.  It is only a snippet for the *other* file:
the one PythonAnywhere itself loads, which lives at
/var/www/<youruser>_pythonanywhere_com_wsgi.py and is edited through the Web
tab, not through git.

Replace EVERYTHING that PythonAnywhere put in that file (the default template
contains its own `application` stub; leaving it in place shadows this one).

Only two things need to match your account:

  * PROJECT  - the folder the app was unzipped into (see DEPLOY_PA.md step 1)
  * the virtualenv path is set in the Web tab, NOT here:
        Web -> Virtualenv -> /home/<youruser>/ams/venv

Everything else (schema version, DB path at instance/ahmed_cement_v44_fresh.db,
PUBLIC_BASE_URL = the Cloudflare Worker origin, SQLITE_JOURNAL_MODE=DELETE on
PA's network filesystem, and keeping background workers off in the web process)
is already set inside wsgi.py, so importing `application` is enough.
"""

import os
import sys

# --- 1. Project folder -------------------------------------------------------
PROJECT = os.path.expanduser("~/ams")          # <-- change if unzipped elsewhere
if PROJECT not in sys.path:
    sys.path.insert(0, PROJECT)

# --- 2. PythonAnywhere markers ----------------------------------------------
# PA sets these on a real site.  The fallback keeps wsgi.py's network-filesystem
# journal fix (SQLITE_JOURNAL_MODE=DELETE) active even if the marker is missing;
# without it SQLite/WAL on PA's /home raises "unable to open database file".
os.environ.setdefault("PYTHONANYWHERE_DOMAIN", "FREE")

# Optional overrides - wsgi.py already defaults these, so leave commented unless
# you need a different value.
# os.environ["PUBLIC_BASE_URL"] = "https://still-base-ac7a.rizwanahmedsora9.workers.dev"
# os.environ["APP_DB_PATH"] = os.path.join(PROJECT, "instance", "ahmed_cement_v44_fresh.db")

# --- 3. The application ------------------------------------------------------
# Do not wrap in try/except: wsgi.py already serves the real startup traceback
# as a 500 page, which is how you diagnose a failed deploy from the browser.
from wsgi import application  # noqa: E402,F401
