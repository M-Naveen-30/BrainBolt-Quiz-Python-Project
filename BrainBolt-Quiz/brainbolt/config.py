"""
config.py
~~~~~~~~~
Centralised paths and constants. Reads config.ini for Gmail creds.
"""
import os
import configparser

# ---------- PATHS ----------
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR      = os.path.join(BASE_DIR, "assets")
DATA_DIR        = os.path.join(BASE_DIR, "data")
OUTPUT_DIR      = os.path.join(BASE_DIR, "output")
ANSWER_PDF_DIR  = os.path.join(BASE_DIR, "answers_pdf")
DB_FILE         = os.path.join(BASE_DIR, "brainbolt.db")
CONFIG_FILE     = os.path.join(BASE_DIR, "config.ini")
QUESTIONS_FILE  = os.path.join(DATA_DIR, "questions.json")

LOGO_FILE       = os.path.join(ASSETS_DIR, "logo.png")
MUSIC_FILE      = os.path.join(ASSETS_DIR, "opening.wav")
CERT_TEMPLATE   = os.path.join(ASSETS_DIR, "cert_template.png")
CORRECT_SND     = os.path.join(ASSETS_DIR, "correct.wav")
WRONG_SND       = os.path.join(ASSETS_DIR, "wrong.wav")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(ANSWER_PDF_DIR, exist_ok=True)

# ---------- QUIZ RULES ----------
QUESTIONS_PER_QUIZ = 15
QUESTION_TIMER     = 30   # seconds per question

CERT_TIERS = [
    (13, "GOLD",          "#FFD700"),   # > 13
    (11, "SILVER",        "#C0C0C0"),   # 11 - 13
    (9,  "BRONZE",        "#CD7F32"),   # 9 - 10
    (0,  "APPRECIATION",  "#7E57C2"),   # < 9
]

TOPICS = {
    "1": ("python",       "Python"),
    "2": ("data_science", "Data Science"),
    "3": ("java",         "Java"),
    "4": ("full_stack",   "Full Stack"),
}


# ---------- GMAIL CONFIG ----------
def load_email_config():
    """Read [email] section from config.ini. Returns a dict."""
    parser = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        return {"sender_email": "", "sender_app_pass": "", "sender_name": "BrainBolt"}
    parser.read(CONFIG_FILE)
    return {
        "sender_email":    parser.get("email", "sender_email",    fallback=""),
        "sender_app_pass": parser.get("email", "sender_app_pass", fallback=""),
        "sender_name":     parser.get("email", "sender_name",     fallback="BrainBolt"),
    }


def get_app_setting(key, default=""):
    """Read a value from [app] section."""
    parser = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        return default
    parser.read(CONFIG_FILE)
    return parser.get("app", key, fallback=default)
