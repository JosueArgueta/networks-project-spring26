"""
RTT vs. Speed-of-Light
Networks Assignment — Measurement & Geography

Run with: python rtt_speedoflight.py   (no sudo needed)
Requires: pip install requests matplotlib numpy
"""

import math, time, os, requests, numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import urllib.request

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

TARGETS = {
    "Tokyo":        {"url": "http://www.google.co.jp",   "coords": (35.6762,  139.6503), "continent": "Asia"},
    "São Paulo":    {"url": "http://www.google.com.br",  "coords": (-23.5505, -46.6333), "continent": "S. America"},
    "Lagos":        {"url": "http://www.google.com.ng",  "coords": (6.5244,     3.3792), "continent": "Africa"},
    "Frankfurt":    {"url": "http://www.google.de",      "coords": (50.1109,    8.6821), "continent": "Europe"},
    "Sydney":       {"url": "http://www.google.com.au",  "coords": (-33.8688, 151.2093), "continent": "Oceania"},
    "Mumbai":       {"url": "http://www.google.co.in",   "coords": (19.0760,   72.8777), "continent": "Asia"},
    "London":       {"url": "http://www.google.co.uk",   "coords": (51.5074,   -0.1278), "continent": "Europe"},
    "Singapore":    {"url": "http://www.google.com.sg",  "coords": (1.3521,   103.8198), "continent": "Asia"},
}

PROBES           = 15
FIBER_SPEED_KM_S = 200_000
FIGURES_DIR      = "figures"

CONTINENT_COLORS = {
    "Asia":      "#e63946",
    "S. America":"#2a9d8f",
    "Africa":    "#e9c46a",
    "Europe":    "#457b9d",
    "Oceania":   "#a8dadc",
}

# ─────────────────────────────────────────────
# TASK 1 — MEASURE RTTs
# ─────────────────────────────────────────────

def measure_rtt(url: str, probes: int = PROBES) -> dict:
    """
    Measure RTT to `url` using HTTP requests.

    Return:
        {
            "min_ms":   float | None,
            "mean_ms":  float | None,
            "median_ms":float | None,
            "loss_pct": float,
            "samples":  list[float],
        }

    TODO:
        1. Loop `probes` times.
        2. Record time before and after urllib.request.urlopen(url, timeout=3).
           elapsed_ms = (time.perf_counter() - start) * 1000
        3. On any exception, count as lost.
        4. Compute min, mean, median using numpy.
        5. loss_pct = (lost / probes) * 100
        6. Sleep 0.2s between probes.
        7. If ALL probes lost, return None for all stats.
    """
    samples = []
    lost    = 0

    for _ in range(probes):
        start = time.perf_counter()
        try:
            urllib.request.urlopen(url, timeout=3)
            elapsed_ms = (time.perf_counter() - start) * 1000
            samples.append(elapsed_ms)
        except Exception:
            lost += 1
        time.sleep(0.2)

    if not samples:
        return {"min_ms": None, "mean_ms": None, "median_ms": None,
                "loss_pct": 100.0, "samples": []}

    return {
        "min_ms":    float(np.min(samples)),
        "mean_ms":   float(np.mean(samples)),
        "median_ms": float(np.median(samples)),
        "loss_pct":  (lost / probes) * 100,
        "samples":   samples,
    }
    return {}  # placeholder


# ─────────────────────────────────────────────
# TASK 2 — HAVERSINE + INEFFICIENCY
# ─────────────────────────────────────────────

def great_circle_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_my_location() -> tuple[float, float, str]:
    """Return (lat, lon, city) for this machine's public IP."""
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5).json()
        lat, lon = map(float, r["loc"].split(","))
        return lat, lon, r.get("city", "Your Location")
    except Exception:
        print("Could not auto-detect location. Defaulting to Boston.")
        return 42.3601, -71.0589, "Boston"


def compute_inefficiency(results: dict, src_lat: float, src_lon: float) -> dict:
    """
    Annotate each city in results with:
        "distance_km"        — great-circle distance from source
        "theoretical_min_ms" — 2 * (distance / FIBER_SPEED_KM_S) * 1000
        "inefficiency_ratio" — median_ms / theoretical_min_ms
        "high_inefficiency"  — True if ratio > 3.0

    TODO:
        1. For each city, unpack coords and call great_circle_km().
        2. Compute theoretical_min_ms (* 2 for round-trip, * 1000 for ms).
        3. Compute ratio. If median_ms is None, set ratio to None.
        4. Annotate results[city] in place.
    """
    for city, data in results.items():
        lat2, lon2 = data["coords"]
        dist = great_circle_km(src_lat, src_lon, lat2, lon2)
        theor = (dist / FIBER_SPEED_KM_S) * 2 * 1000
        med = data.get("median_ms")
        ratio = (med / theor) if (med is not None and theor > 0) else None
        data["distance_km"] = dist
        data["theoretical_min_ms"] = theor
        data["inefficiency_ratio"] = ratio
        data["high_inefficiency"] = (ratio is not None and ratio > 3.0)
    return results


# ─────────────────────────────────────────────
# TASK 3 — PLOTS
# ─────────────────────────────────────────────

def make_plots(results: dict):
    """
    Produce two figures saved to FIGURES_DIR/.

    Figure 1 — fig1_rtt_comparison.png
        Grouped bar chart: measured median RTT vs. theoretical min RTT per city.
        Sort cities by distance_km ascending.
        Label axes, add legend and title.

    Figure 2 — fig2_distance_scatter.png
        Scatter: x = distance_km, y = measured median RTT.
        Draw a dashed line for theoretical minimum.
        Label each point with city name.
        Color by continent using CONTINENT_COLORS.
        Add continent legend and title.

    TODO: implement both figures.
    Hints:
        fig, ax = plt.subplots(figsize=(11, 6))
        ax.bar() / ax.scatter()
        plt.tight_layout()
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
    """
    os.makedirs(FIGURES_DIR, exist_ok=True)
    valid  = {c: d for c, d in results.items() if d.get("median_ms") is not None}
    cities = sorted(valid, key=lambda c: valid[c]["distance_km"])

    # ── Figure 1 ──────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(cities))
    width = 0.35
    medians = [valid[c]["median_ms"] for c in cities]
    theorys = [valid[c]["theoretical_min_ms"] for c in cities]
    ax.bar(x - width/2, medians, width, label="Measured Median RTT", color="#e63946")
    ax.bar(x + width/2, theorys, width, label="Theoretical Min RTT", color="#457b9d")
    ax.set_xticks(x)
    ax.set_xticklabels(cities, rotation=15, ha="right")
    ax.set_ylabel("RTT (ms)")
    ax.set_title("Measured vs. Theoretical Minimum RTT by City")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/fig1_rtt_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()

    # ── Figure 2 ──────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 7))
    distances = [valid[c]["distance_km"] for c in cities]
    medians2  = [valid[c]["median_ms"] for c in cities]
    theorys2  = [valid[c]["theoretical_min_ms"] for c in cities]
    colors    = [CONTINENT_COLORS[valid[c]["continent"]] for c in cities]
    ax.scatter(distances, medians2, c=colors, s=100, zorder=5)
    for i, city in enumerate(cities):
        ax.annotate(city, (distances[i], medians2[i]), textcoords="offset points", xytext=(6, 4))
    ax.plot(distances, theorys2, "k--", label="Theoretical minimum")
    patches = [mpatches.Patch(color=v, label=k) for k, v in CONTINENT_COLORS.items()]
    ax.legend(handles=patches + [plt.Line2D([0],[0], linestyle="--", color="k", label="Theoretical min")])
    ax.set_xlabel("Great-Circle Distance (km)")
    ax.set_ylabel("Measured Median RTT (ms)")
    ax.set_title("Distance vs. RTT with Theoretical Minimum")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/fig2_distance_scatter.png", dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Figures saved to {FIGURES_DIR}/")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    src_lat, src_lon, src_city = get_my_location()
    print(f"Your location: {src_city} ({src_lat:.4f}, {src_lon:.4f})\n")

    results = {}
    for city, info in TARGETS.items():
        print(f"Probing {city} ({info['url']}) ...", end=" ", flush=True)
        stats = measure_rtt(info["url"])
        results[city] = {**stats, "coords": info["coords"], "continent": info["continent"]}
        med = stats.get("median_ms")
        print(f"median={med:.1f} ms  loss={stats['loss_pct']:.0f}%" if med else "unreachable")

    results = compute_inefficiency(results, src_lat, src_lon)

    print(f"\n{'City':<14} {'Dist km':>8} {'Median ms':>10} {'Theor. ms':>10} {'Ratio':>7}")
    print("─" * 55)
    for city, d in sorted(results.items(), key=lambda x: x[1].get("distance_km", 0)):
        dist  = d.get("distance_km", 0)
        med   = d.get("median_ms")
        theor = d.get("theoretical_min_ms")
        ratio = d.get("inefficiency_ratio")
        flag  = " ⚠️" if d.get("high_inefficiency") else ""
        print(f"{city:<14} {dist:>8.0f} "
              f"{(f'{med:.1f}' if med else 'N/A'):>10} "
              f"{(f'{theor:.1f}' if theor else 'N/A'):>10} "
              f"{(f'{ratio:.2f}' if ratio else 'N/A'):>7}{flag}")

    make_plots(results)

if __name__ == "__main__":
    main()
