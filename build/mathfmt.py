"""Turn the ASCII math in the question bank into real mathematical typography.

DELIBERATELY CONSERVATIVE. Every rule here is unambiguous; anything that could corrupt a
variable name is left alone. Specifically:

  * Exponents are superscripted ONLY when the exponent is digits, `n`, or a signed integer.
    `^(1/3)` and `^1.5` have no Unicode superscript for `/` or `.`, so they stay as written.
  * Greek names are converted on WORD BOUNDARIES only. Without that, "precision" becomes
    "preciσon" and "must" becomes "μst" - both of which happened on the first attempt.
  * Multi-letter subscripts (`A_circle`, `sigma_avg`) keep the underscore, because
    "Acircle" reads worse than "A_circle".
  * A bare `x` is only turned into a times sign when it sits between two numeric or
    bracketed operands, never when it is the variable x.
"""
import re

SUP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
       '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
       'n': 'ⁿ', '-': '⁻', '+': '⁺'}
SUB = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
       '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
       'i': 'ᵢ', 'n': 'ₙ'}

# Longest first: `delta sigma` must win over `delta`, and `Phi` over `phi`.
GREEK = [
    ('delta sigma', 'Δσ'),
    ('Delta', 'Δ'), ('Phi', 'Φ'), ('Sigma', 'Σ'), ('Omega', 'Ω'),
    ('alpha', 'α'), ('beta', 'β'), ('gamma', 'γ'), ('delta', 'δ'),
    ('epsilon', 'ε'), ('theta', 'θ'), ('lambda', 'λ'), ('mu', 'μ'),
    ('nu', 'ν'), ('rho', 'ρ'), ('sigma', 'σ'), ('tau', 'τ'),
    ('phi', 'φ'), ('omega', 'ω'), ('pi', 'π'),
]

SIMPLE = [
    ('+/-', '±'), ('>=', '≥'), ('<=', '≤'), ('!=', '≠'),
    ('sqrt', '√'), ('integral', '∫'), (' ~ ', ' ≈ '),
    ("f'c", 'f′c'), ('degrees', '°'), ('infinity', '∞'),
]


def _superscript(m):
    body = m.group(1)
    if not all(c in SUP for c in body):
        return m.group(0)                      # leave ^(1/3), ^1.5 alone
    return ''.join(SUP[c] for c in body)


def _subscript(m):
    body = m.group(1)
    return ''.join(SUB[c] for c in body) if all(c in SUB for c in body) else m.group(0)


def pretty(s):
    if not isinstance(s, str) or not s:
        return s

    # bars first: xbar -> x with a combining macron
    s = re.sub(r'\b([a-zA-Z])bar\b', lambda m: m.group(1) + '̄', s)

    # sum( -> uppercase sigma; do this BEFORE the greek pass so `sum` is not touched by it
    s = re.sub(r'\bsum(?=[ (_])', 'Σ', s)

    for a, b in SIMPLE:
        s = s.replace(a, b)

    # Letter-only guards, NOT \b: `_` is a word character, so \b fails after "gamma" in
    # "gamma_w" and you get a converted γ sitting next to an unconverted gamma_w in the
    # same formula. This form converts gamma_w -> γ_w and N_gamma -> N_γ.
    for name, ch in GREEK:
        s = re.sub(r'(?<![A-Za-z])' + name + r'(?![A-Za-z])', ch, s)

    # Exponents. The trailing guard matters: without it `H^1.5` superscripts only the 1
    # and renders as H¹.5, which is wrong and worse than leaving it alone.
    s = re.sub(r'\^\(([^()]{1,4})\)(?![.\w])', _superscript, s)
    s = re.sub(r'\^(-?[0-9]+|n)(?![.\w])', _superscript, s)

    # Single-character subscripts. Excluding a following comma keeps `sigma_1,2` whole
    # rather than producing the mismatched σ₁,2.
    s = re.sub(r'_([0-9in])(?![\w,])', _subscript, s)

    s = re.sub(r'(?<=[0-9)]) \* (?=[0-9(])', ' · ', s)
    return s


def pretty_formula(s):
    """As `pretty`, plus a broader times-sign rule.

    Safe only in a formula: ` x ` between two operands is multiplication there, whereas in
    prose "the x axis" would become "the × axis".
    """
    s = pretty(s)
    if isinstance(s, str):
        s = re.sub(r'(?<=[\w)²³⁴⁵]) x (?=[\w(])', ' × ', s)
    return s


FIELDS = ('prompt', 'formula', 'note', 'pitfall', 'units')


def prettify_question(q):
    for f in FIELDS:
        if q.get(f):
            q[f] = pretty_formula(q[f]) if f == 'formula' else pretty(q[f])
    q['steps'] = [pretty(x) for x in q.get('steps', [])]
    for c in q.get('choices', []) or []:
        c['text'] = pretty(c['text'])
        if c.get('why'):
            c['why'] = pretty(c['why'])
    return q
