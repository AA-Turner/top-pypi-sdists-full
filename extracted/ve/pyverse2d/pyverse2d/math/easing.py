# ======================================== IMPORTS ========================================
from __future__ import annotations
import math
from typing import Callable

# ======================================== TAG ========================================
_EASING_TAG = object()
EasingFunc = Callable[[float], float]

def easing(func: EasingFunc) -> Callable[[float], float]:
    """Décore une fonction comme fonction d'easing"""
    func._tag = _EASING_TAG
    return func

def is_easing(func: object) -> bool:
    """Vérifie qu'une fonction est une fonction d'easing"""
    return callable(func) and getattr(func, "_tag", None) is _EASING_TAG

# ======================================== LINEAR ========================================
@easing
def linear(t: float) -> float:
    """Progression constante, sans accélération ni décélération."""
    return t

# ======================================== QUAD ========================================
@easing
def ease_in_quad(t: float) -> float:
    """Démarre doucement puis accélère. Accélération proportionnelle à t."""
    return t ** 2

@easing
def ease_out_quad(t: float) -> float:
    """Démarre rapidement puis décélère progressivement jusqu'à l'arrêt."""
    return 1 - (1 - t) ** 2

@easing
def ease_in_out_quad(t: float) -> float:
    """Accélère en première moitié, décélère en seconde. Transition symétrique et douce."""
    return 2 * t ** 2 if t < 0.5 else 1 - (-2 * t + 2) ** 2 / 2

# ======================================== CUBIC ========================================
@easing
def ease_in_cubic(t: float) -> float:
    """Démarrage très lent, accélération plus marquée qu'en quad."""
    return t ** 3

@easing
def ease_out_cubic(t: float) -> float:
    """Arrivée plus franche qu'en quad : décélération rapide puis quasi-arrêt immédiat."""
    return 1 - (1 - t) ** 3

@easing
def ease_in_out_cubic(t: float) -> float:
    """Version cubic de l'ease_in_out. Contraste plus prononcé entre le début et la fin."""
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

# ======================================== QUART ========================================
@easing
def ease_in_quart(t: float) -> float:
    """Démarrage quasi immobile, accélération très tardive et intense."""
    return t ** 4

@easing
def ease_out_quart(t: float) -> float:
    """Arrivée sèche : la quasi-totalité du chemin est parcourue rapidement puis s'arrête net."""
    return 1 - (1 - t) ** 4

@easing
def ease_in_out_quart(t: float) -> float:
    """Transition très marquée : long immobilisme apparent aux deux extrémités."""
    return 8 * t ** 4 if t < 0.5 else 1 - (-2 * t + 2) ** 4 / 2

# ======================================== QUINT ========================================
@easing
def ease_in_quint(t: float) -> float:
    """Démarrage extrêmement lent. Quasi imperceptible jusqu'à t ≈ 0.5."""
    return t ** 5

@easing
def ease_out_quint(t: float) -> float:
    """Arrivée extrêmement franche. Quasi immobilité à partir de t ≈ 0.5."""
    return 1 - (1 - t) ** 5

@easing
def ease_in_out_quint(t: float) -> float:
    """Contraste maximum parmi les polynomiales : seul le milieu de la trajectoire bouge vraiment."""
    return 16 * t ** 5 if t < 0.5 else 1 - (-2 * t + 2) ** 5 / 2

# ======================================== SINE ========================================
@easing
def ease_in_sine(t: float) -> float:
    """Accélération douce basée sur un quart de sinusoïde. Plus subtil que quad."""
    return 1 - math.cos(t * math.pi / 2)

@easing
def ease_out_sine(t: float) -> float:
    """Décélération douce basée sur un quart de sinusoïde. Arrivée très naturelle."""
    return math.sin(t * math.pi / 2)

@easing
def ease_in_out_sine(t: float) -> float:
    """Demi-sinusoïde. La transition la plus douce et la plus naturelle de toutes."""
    return -(math.cos(math.pi * t) - 1) / 2

# ======================================== EXPO ========================================
@easing
def ease_in_expo(t: float) -> float:
    """
    Démarrage quasi nul (2^-10 ≈ 0.001), puis explosion exponentielle en fin de course.
    Vaut exactement 0 en t=0.
    """
    return 0.0 if t == 0 else 2 ** (10 * t - 10)

@easing
def ease_out_expo(t: float) -> float:
    """
    Démarre très vite puis converge asymptotiquement vers 1.
    Vaut exactement 1 en t=1.
    """
    return 1.0 if t == 1 else 1 - 2 ** (-10 * t)

@easing
def ease_in_out_expo(t: float) -> float:
    """
    Combinaison des deux : quasi immobile au départ, vitesse maximale au milieu,
    quasi immobile à l'arrivée. Effet très dramatique.
    """
    if t == 0: return 0.0
    if t == 1: return 1.0
    return 2 ** (20 * t - 10) / 2 if t < 0.5 else (2 - 2 ** (-20 * t + 10)) / 2

# ======================================== CIRC ========================================
@easing
def ease_in_circ(t: float) -> float:
    """
    Accélération basée sur un arc de cercle.
    Démarre encore plus lentement qu'expo, puis accélère brusquement en fin.
    """
    return 1 - math.sqrt(1 - t ** 2)

@easing
def ease_out_circ(t: float) -> float:
    """
    Décélération basée sur un arc de cercle.
    Vitesse initiale maximale, puis arrêt abrupt formant un angle droit apparent.
    """
    return math.sqrt(1 - (t - 1) ** 2)

@easing
def ease_in_out_circ(t: float) -> float:
    """Deux arcs de cercle raccordés. Transitions extrêmes très anguleuses au milieu."""
    return (1 - math.sqrt(1 - (2 * t) ** 2)) / 2 if t < 0.5 else (math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2

# ======================================== BACK ========================================
_BACK_C1 = 1.70158
_BACK_C2 = _BACK_C1 * 1.525
_BACK_C3 = _BACK_C1 + 1

@easing
def ease_in_back(t: float) -> float:
    """
    Recule légèrement avant de partir en avant (dépasse brièvement en dessous de 0).
    Effet d'anticipation, comme un personnage qui prend son élan.
    """
    return _BACK_C3 * t ** 3 - _BACK_C1 * t ** 2

@easing
def ease_out_back(t: float) -> float:
    """
    Dépasse légèrement la cible avant de revenir (dépasse brièvement au-dessus de 1).
    Effet de rebond d'arrivée, comme un objet qui se pose avec inertie.
    """
    return 1 + _BACK_C3 * (t - 1) ** 3 + _BACK_C1 * (t - 1) ** 2

@easing
def ease_in_out_back(t: float) -> float:
    """Recule au départ ET dépasse à l'arrivée. Effet très expressif, à utiliser avec parcimonie."""
    if t < 0.5:
        return ((2 * t) ** 2 * ((_BACK_C2 + 1) * 2 * t - _BACK_C2)) / 2
    return ((2 * t - 2) ** 2 * ((_BACK_C2 + 1) * (2 * t - 2) + _BACK_C2) + 2) / 2

# ======================================== ELASTIC ========================================
_ELASTIC_C4 = (2 * math.pi) / 3
_ELASTIC_C5 = (2 * math.pi) / 4.5

@easing
def ease_in_elastic(t: float) -> float:
    """
    Oscille autour de 0 avec une amplitude croissante avant de partir brusquement.
    Comme un ressort qu'on comprime avant de lâcher.
    Dépasse en négatif plusieurs fois en début de course.
    """
    if t == 0: return 0.0
    if t == 1: return 1.0
    return -(2 ** (10 * t - 10)) * math.sin((t * 10 - 10.75) * _ELASTIC_C4)

@easing
def ease_out_elastic(t: float) -> float:
    """
    Dépasse la cible puis oscille autour de 1 avec une amplitude décroissante.
    Comme un ressort qui se stabilise. Effet très vivant à l'arrivée.
    """
    if t == 0: return 0.0
    if t == 1: return 1.0
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * _ELASTIC_C4) + 1

@easing
def ease_in_out_elastic(t: float) -> float:
    """
    Oscillations aux deux extrémités. Effet très prononcé, réservé aux animations
    courtes et expressives (feedback UI, alertes).
    """
    if t == 0: return 0.0
    if t == 1: return 1.0
    if t < 0.5:
        return -(2 ** (20 * t - 10) * math.sin((20 * t - 11.125) * _ELASTIC_C5)) / 2
    return (2 ** (-20 * t + 10) * math.sin((20 * t - 11.125) * _ELASTIC_C5)) / 2 + 1

# ======================================== BOUNCE ========================================
def _bounce_out(t: float) -> float:
    """
    Noyau interne : simule plusieurs rebonds successifs (4 au total) d'amplitude
    décroissante. Non exposé directement car utilisé par les trois variantes.
    """
    n, d = 7.5625, 2.75
    if t < 1 / d:
        return n * t ** 2
    elif t < 2 / d:
        t -= 1.5 / d
        return n * t ** 2 + 0.75
    elif t < 2.5 / d:
        t -= 2.25 / d
        return n * t ** 2 + 0.9375
    else:
        t -= 2.625 / d
        return n * t ** 2 + 0.984375

@easing
def ease_in_bounce(t: float) -> float:
    """
    Enchaîne plusieurs micro-rebonds croissants avant de s'élancer.
    Comme une balle qui rebondit avant d'être lancée — rare en pratique.
    """
    return 1 - _bounce_out(1 - t)

@easing
def ease_out_bounce(t: float) -> float:
    """
    Rebondit 4 fois à l'arrivée avec une amplitude décroissante avant de se stabiliser.
    Comme une balle qui tombe et s'immobilise. Le bounce le plus utilisé.
    """
    return _bounce_out(t)

@easing
def ease_in_out_bounce(t: float) -> float:
    """
    Rebonds au départ ET à l'arrivée. Très agité, à réserver aux animations
    humoristiques ou très dynamiques.
    """
    return (1 - _bounce_out(1 - 2 * t)) / 2 if t < 0.5 else (1 + _bounce_out(2 * t - 1)) / 2

# ======================================== EXPORT ========================================
__all__ = [
    "EasingFunc",
    "easing",
    "is_easing",

    "linear",

    "ease_in_quad",
    "ease_out_quad",
    "ease_in_out_quad",

    "ease_in_cubic",
    "ease_out_cubic",
    "ease_in_out_cubic",

    "ease_in_quart",
    "ease_out_quart",
    "ease_in_out_quart",

    "ease_in_quint",
    "ease_out_quint",
    "ease_in_out_quint",

    "ease_in_sine",
    "ease_out_sine",
    "ease_in_out_sine",

    "ease_in_expo",
    "ease_out_expo",
    "ease_in_out_expo",

    "ease_in_circ",
    "ease_out_circ",
    "ease_in_out_circ",

    "ease_in_back",
    "ease_out_back",
    "ease_in_out_back",

    "ease_in_elastic",
    "ease_out_elastic",
    "ease_in_out_elastic",

    "ease_in_bounce",
    "ease_out_bounce",
    "ease_in_out_bounce",
]