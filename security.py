import pickle

VULN_KEYS = {}
try:
    with open('exception_commands.bin', 'rb') as f:
        VULN_KEYS = pickle.load(f)
except Exception:
    pass

def security_check_ifsafe(code, lang):
    for key in VULN_KEYS.get(lang, []):
        if key in code:
            return False
    return True
