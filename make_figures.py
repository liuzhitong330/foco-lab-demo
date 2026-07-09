"""
make_figures.py — Foco Lab Demo
Figure 1: Top hub neurons by total weighted degree, colored by functional class
Figure 2: Chemical vs electrical synapse scatter, highlighting command circuit
"""

import csv, os

OUT = os.path.dirname(__file__)

# Load hub neuron data
hubs = []
with open(os.path.join(OUT, "hub_neurons.tsv")) as f:
    for row in csv.DictReader(f, delimiter="\t"):
        hubs.append(row)

# Load full connectivity for scatter
conn = []
with open(os.path.join(OUT, "connectivity.tsv")) as f:
    for row in csv.DictReader(f, delimiter="\t"):
        conn.append(row)

NEURON_CLASS = {
    "AVAR": ("Backward command", "#c0392b"),
    "AVAL": ("Backward command", "#c0392b"),
    "AVBR": ("Forward command",  "#1a5c8a"),
    "AVBL": ("Forward command",  "#1a5c8a"),
    "RIAR": ("Sensorimotor int.", "#e67e22"),
    "RIAL": ("Sensorimotor int.", "#e67e22"),
    "SMDVR": ("Head motor",      "#8e44ad"),
    "SMDVL": ("Head motor",      "#8e44ad"),
    "SABD":  ("Motor neuron",    "#8e44ad"),
    "AVER":  ("Forward/rev int.","#27ae60"),
    "PVPR":  ("Post. interneuron","#7f8c8d"),
    "PVPL":  ("Post. interneuron","#7f8c8d"),
    "PVCR":  ("Touch int.",      "#7f8c8d"),
    "PVCL":  ("Touch int.",      "#7f8c8d"),
    "AIZL":  ("Interneuron",     "#16a085"),
}

# ── Figure 1: Hub neuron bar chart ────────────────────────────────────────────
FW, FH = 700, 440
PAD_L = 80
PAD_R = 200
PAD_T = 75
PAD_B = 55
AW = FW - PAD_L - PAD_R
AH = FH - PAD_T - PAD_B

max_total = int(hubs[0]["total"])

bars1 = ""
for i, h in enumerate(hubs):
    n       = h["neuron"]
    total   = int(h["total"])
    chem_o  = int(h["chem_out"])
    chem_i  = int(h["chem_in"])
    elec    = int(h["electrical"])
    col     = h["color"]
    cls     = h["class"]

    y = PAD_T + i * (AH / len(hubs))
    bar_h = AH / len(hubs) * 0.72

    # Stacked bar: chem_out | chem_in | electrical
    scale = AW / max_total
    w_co = chem_o * scale
    w_ci = chem_i * scale
    w_el = elec * scale
    x0 = PAD_L

    # chemical outgoing (solid color)
    bars1 += (f'<rect x="{x0:.1f}" y="{y:.1f}" width="{w_co:.1f}" height="{bar_h:.1f}" '
              f'fill="{col}" opacity="0.9" rx="1"/>')
    # chemical incoming (lighter)
    bars1 += (f'<rect x="{x0+w_co:.1f}" y="{y:.1f}" width="{w_ci:.1f}" height="{bar_h:.1f}" '
              f'fill="{col}" opacity="0.5" rx="1"/>')
    # electrical (gray-ish)
    bars1 += (f'<rect x="{x0+w_co+w_ci:.1f}" y="{y:.1f}" width="{w_el:.1f}" height="{bar_h:.1f}" '
              f'fill="{col}" opacity="0.25" rx="1"/>')

    # Neuron label left
    bars1 += (f'<text x="{PAD_L - 8}" y="{y + bar_h/2 + 4:.1f}" '
              f'text-anchor="end" font-size="11" fill="{col}" font-weight="700">{n}</text>')
    # Class label right
    bars1 += (f'<text x="{PAD_L + AW + 10}" y="{y + bar_h/2 + 4:.1f}" '
              f'font-size="9.5" fill="{col}">{cls}</text>')
    # Total value
    bars1 += (f'<text x="{PAD_L + total*scale + 5:.1f}" y="{y + bar_h/2 + 4:.1f}" '
              f'font-size="9" fill="{col}" font-weight="600">{total}</text>')

# X-axis ticks
xticks1 = ""
for v in [0, 300, 600, 900, 1200]:
    tx = PAD_L + v / max_total * AW
    xticks1 += (f'<line x1="{tx:.1f}" y1="{PAD_T}" x2="{tx:.1f}" y2="{PAD_T+AH}" '
                f'stroke="#eee" stroke-width="1"/>'
                f'<text x="{tx:.1f}" y="{PAD_T+AH+16}" text-anchor="middle" '
                f'font-size="9" fill="#888">{v}</text>')
axis1 = (f'<line x1="{PAD_L}" y1="{PAD_T}" x2="{PAD_L}" y2="{PAD_T+AH}" '
         f'stroke="#ccc" stroke-width="1"/>')

# Legend
leg_x = PAD_L + 20
leg_y = PAD_T + AH + 28
leg1 = ""
items = [("Dark = chem. outgoing", "#555"), ("Medium = chem. incoming", "#999"),
         ("Light = electrical (gap junctions)", "#bbb")]
for i, (lbl, col) in enumerate(items):
    lx = leg_x + i * 200
    leg1 += (f'<rect x="{lx}" y="{leg_y}" width="12" height="10" fill="{col}" rx="1"/>'
             f'<text x="{lx+16}" y="{leg_y+9}" font-size="9" fill="#666">{lbl}</text>')

svg1 = f"""<svg viewBox="0 0 {FW} {FH}" xmlns="http://www.w3.org/2000/svg"
     style="font-family:-apple-system,system-ui,sans-serif;background:white;">
  <text x="{FW//2}" y="22" text-anchor="middle" font-size="13" font-weight="600" fill="#222">
    C. elegans Connectome Hub Neurons — Top 15 by Weighted Degree
  </text>
  <text x="{FW//2}" y="40" text-anchor="middle" font-size="10" fill="#666">
    Chemical (outgoing + incoming) and electrical synapse weights · White et al. 1986 · OpenWorm/c302
  </text>
  <text x="{FW//2}" y="56" text-anchor="middle" font-size="10" fill="#c0392b">
    AVA (backward command) and AVB (forward command) are the top hubs — the working memory circuit
  </text>
  <text x="{PAD_L + AW/2:.0f}" y="{PAD_T+AH+44}" text-anchor="middle"
        font-size="10" fill="#555">Total weighted degree (synapse counts)</text>
  {axis1}{xticks1}{bars1}{leg1}
</svg>"""

with open(os.path.join(OUT, "hub_neurons.svg"), "w") as f:
    f.write(svg1)
print("Wrote hub_neurons.svg")


# ── Figure 2: Chemical vs electrical scatter for top 60 neurons ──────────────
FW2, FH2 = 640, 500
PAD_L2 = 70
PAD_R2 = 40
PAD_T2 = 75
PAD_B2 = 65
AW2 = FW2 - PAD_L2 - PAD_R2
AH2 = FH2 - PAD_T2 - PAD_B2

# Use top 60 neurons for background scatter
top60 = conn[:60]
max_chem = max(int(r["chem_out"]) + int(r["chem_in"]) for r in top60) * 1.1
max_elec = max(int(r["electrical"]) for r in top60) * 1.1

HIGHLIGHT = {"AVAR", "AVAL", "AVBL", "AVBR", "RIAR", "RIAL", "SMDVL", "SMDVR", "SABD"}
LABEL_OFFSET = {
    "AVAR": (8, -8), "AVAL": (8, 10), "AVBL": (-8, -8), "AVBR": (8, 8),
    "RIAR": (8, -8), "RIAL": (8, 8), "SMDVL": (8, -8), "SMDVR": (8, 8),
    "SABD": (8, -8),
}

def sx(chem_total):
    return PAD_L2 + chem_total / max_chem * AW2

def sy(elec):
    return PAD_T2 + AH2 - elec / max_elec * AH2

dots2 = ""
labels2 = ""
for r in top60:
    n = r["neuron"]
    chem_t = int(r["chem_out"]) + int(r["chem_in"])
    elec_v = int(r["electrical"])
    x = sx(chem_t)
    y = sy(elec_v)
    cls, col = NEURON_CLASS.get(n, ("Other", "#bdc3c7"))
    is_hi = n in HIGHLIGHT
    radius = 7 if is_hi else 4
    opacity = "0.9" if is_hi else "0.4"
    dots2 += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" '
              f'fill="{col}" opacity="{opacity}"/>')
    if is_hi:
        ox, oy = LABEL_OFFSET.get(n, (8, -8))
        anc = "start" if ox > 0 else "end"
        labels2 += (f'<text x="{x+ox:.1f}" y="{y+oy:.1f}" font-size="10" '
                    f'fill="{col}" font-weight="700" text-anchor="{anc}">{n}</text>')

# Axes
xtick2, ytick2 = "", ""
for v in [0, 300, 600, 900, 1200, 1500]:
    tx = sx(v)
    if tx > PAD_L2 + AW2: break
    xtick2 += (f'<line x1="{tx:.1f}" y1="{PAD_T2}" x2="{tx:.1f}" y2="{PAD_T2+AH2}" '
               f'stroke="#eee" stroke-width="1"/>'
               f'<text x="{tx:.1f}" y="{PAD_T2+AH2+16}" text-anchor="middle" '
               f'font-size="9" fill="#888">{v}</text>')
for v in [0, 150, 300, 450, 600]:
    ty = sy(v)
    ytick2 += (f'<line x1="{PAD_L2}" y1="{ty:.1f}" x2="{PAD_L2+AW2}" y2="{ty:.1f}" '
               f'stroke="#eee" stroke-width="1"/>'
               f'<text x="{PAD_L2-8}" y="{ty+4:.1f}" text-anchor="end" '
               f'font-size="9" fill="#888">{v}</text>')
axis2 = (f'<line x1="{PAD_L2}" y1="{PAD_T2}" x2="{PAD_L2}" y2="{PAD_T2+AH2}" '
         f'stroke="#ccc" stroke-width="1"/>'
         f'<line x1="{PAD_L2}" y1="{PAD_T2+AH2}" x2="{PAD_L2+AW2}" y2="{PAD_T2+AH2}" '
         f'stroke="#ccc" stroke-width="1"/>')
xlabel2 = (f'<text x="{PAD_L2+AW2/2:.0f}" y="{PAD_T2+AH2+34}" text-anchor="middle" '
           f'font-size="10" fill="#555">Total chemical synapse weight</text>')
ylabel2 = (f'<text transform="rotate(-90,18,{PAD_T2+AH2/2:.0f})" '
           f'x="18" y="{PAD_T2+AH2/2:.0f}" text-anchor="middle" '
           f'font-size="10" fill="#555">Electrical (gap junction) weight</text>')

# Color legend
leg2 = ""
legend_items = [
    ("AVA — Backward command", "#c0392b"),
    ("AVB — Forward command",  "#1a5c8a"),
    ("RIA — Sensorimotor",     "#e67e22"),
    ("SMD/SABD — Motor",       "#8e44ad"),
    ("Other top neurons",      "#bdc3c7"),
]
lx2, ly2 = PAD_L2 + AW2 * 0.55, PAD_T2 + 12
for i, (lbl, col) in enumerate(legend_items):
    leg2 += (f'<circle cx="{lx2 + 6}" cy="{ly2 + i*20 + 5}" r="5" fill="{col}" opacity="0.85"/>'
             f'<text x="{lx2 + 16}" y="{ly2 + i*20 + 10}" font-size="9.5" fill="{col}" '
             f'font-weight="600">{lbl}</text>')

svg2 = f"""<svg viewBox="0 0 {FW2} {FH2}" xmlns="http://www.w3.org/2000/svg"
     style="font-family:-apple-system,system-ui,sans-serif;background:white;">
  <text x="{FW2//2}" y="22" text-anchor="middle" font-size="13" font-weight="600" fill="#222">
    Two Modes of Hub Connectivity: Chemical vs. Electrical Synapses
  </text>
  <text x="{FW2//2}" y="40" text-anchor="middle" font-size="10" fill="#666">
    Top 60 neurons by total degree · White et al. 1986 · OpenWorm/c302
  </text>
  <text x="{FW2//2}" y="56" text-anchor="middle" font-size="10" fill="#444">
    AVA/AVB dominate chemical synapses; PVCR/PVP combine strong electrical coupling with moderate chemical
  </text>
  {axis2}{xtick2}{ytick2}{xlabel2}{ylabel2}{dots2}{labels2}{leg2}
</svg>"""

with open(os.path.join(OUT, "synapse_scatter.svg"), "w") as f:
    f.write(svg2)
print("Wrote synapse_scatter.svg")
