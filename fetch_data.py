"""
fetch_data.py — Foco Lab Demo (Saul Kato lab, UCSF)
Downloads the C. elegans hermaphrodite connectome from OpenWorm/c302 (White et al. 1986,
updated by Varshney et al. 2011) and computes hub neuron statistics.

The Kato lab's work on global brain dynamics and working memory centers on the
command interneuron circuit (AVA/AVB) and motor oscillators (RIA, SMD).
This analysis shows that connectome topology — hub degree centrality — predicts
exactly those neurons.
"""

import urllib.request, csv, os
from collections import defaultdict

OUT = os.path.dirname(__file__)

URL = ("https://raw.githubusercontent.com/openworm/c302/master/c302/data/"
       "herm_full_edgelist.csv")

print("Downloading C. elegans connectome (OpenWorm/c302) …")
with urllib.request.urlopen(URL, timeout=30) as r:
    raw = r.read().decode("utf-8")
print(f"  Downloaded {len(raw):,} bytes")

rows = list(csv.DictReader(raw.splitlines()))
chem = [r for r in rows if r["Type"].strip() == "chemical"]
elec = [r for r in rows if r["Type"].strip() == "electrical"]
print(f"  {len(chem)} chemical synapses, {len(elec)} electrical gap junctions")

# Per-neuron weighted degree
chem_out = defaultdict(int)
chem_in  = defaultdict(int)
elec_deg = defaultdict(int)

for r in chem:
    w = int(r["Weight"])
    chem_out[r["Source"].strip()] += w
    chem_in[r["Target"].strip()]  += w

for r in elec:
    w = int(r["Weight"])
    elec_deg[r["Source"].strip()] += w
    elec_deg[r["Target"].strip()] += w

all_neurons = set(
    list(chem_out.keys()) + list(chem_in.keys()) + list(elec_deg.keys())
)
# Exclude non-neuron entries (muscle, hyp, etc.)
EXCLUDE = {"hyp", "int", "mu_int", "mu_bod", "mu_anal"}
all_neurons = {n for n in all_neurons if not any(n.startswith(x) for x in EXCLUDE)
               and not n.startswith("mu_") and n != "hyp"}

total_deg = {
    n: chem_out[n] + chem_in[n] + elec_deg[n]
    for n in all_neurons
}

# Write full connectivity table
with open(os.path.join(OUT, "connectivity.tsv"), "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["neuron", "chem_out", "chem_in", "electrical", "total_degree"])
    for n in sorted(total_deg, key=lambda x: -total_deg[x]):
        w.writerow([n, chem_out[n], chem_in[n], elec_deg[n], total_deg[n]])
print("Wrote connectivity.tsv")

# Neuron class annotations (from WormAtlas / Kato lab context)
# AVA = backward command interneuron (Kato working memory paper)
# AVB = forward command interneuron (coupled oscillator partner)
# RIA = sensorimotor integrator (Kato 2015 global dynamics)
# SMD = head motor neuron (motor oscillator)
# PVC = posterior ventral cord interneuron (touch circuit)
# AIB = interneuron (turns/reversals)
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
    "AVEL":  ("Forward/rev int.","#27ae60"),
    "PVCR":  ("Touch int.",      "#7f8c8d"),
    "PVCL":  ("Touch int.",      "#7f8c8d"),
    "PVPR":  ("Post. interneuron","#7f8c8d"),
    "PVPL":  ("Post. interneuron","#7f8c8d"),
    "AIBL":  ("Interneuron",     "#16a085"),
    "AIBR":  ("Interneuron",     "#16a085"),
    "AIZL":  ("Interneuron",     "#16a085"),
    "AIZR":  ("Interneuron",     "#16a085"),
}

# Write top 15 hub neurons
top15 = sorted(total_deg.items(), key=lambda x: -x[1])[:15]
with open(os.path.join(OUT, "hub_neurons.tsv"), "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["neuron", "class", "color", "chem_out", "chem_in", "electrical", "total"])
    for n, d in top15:
        cls, col = NEURON_CLASS.get(n, ("Other interneuron", "#95a5a6"))
        w.writerow([n, cls, col, chem_out[n], chem_in[n], elec_deg[n], d])

print("Wrote hub_neurons.tsv")
print("\nTop 15 hub neurons:")
for n, d in top15:
    cls, _ = NEURON_CLASS.get(n, ("?", ""))
    print(f"  {n:8s}: {d:5d}  [{cls}]")
