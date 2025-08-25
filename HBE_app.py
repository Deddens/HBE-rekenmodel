# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 15:02:17 2025

@author: Maartend
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Streamlit configuratie
st.set_page_config(page_title="HBE Blendprijs Rekenmodel", layout="centered")

st.title("🔄 HBE Blendprijs Rekenmodel – Volledige Berekening")

# Invoer
volume = st.number_input("Totaal volume (MT)", min_value=0.0, value=100.0)
bio_percentage = st.slider("Aandeel Bio (%)", min_value=0, max_value=100, value=30)
fossiel_percentage = 100 - bio_percentage

lhv_bio = st.number_input("LHV Bio (GJ/MT)", min_value=0.0, value=37.0)
lhv_fossiel = st.number_input("LHV Fossiel (GJ/MT)", min_value=0.0, value=42.0)

hbe_waarde = st.number_input("HBE-marktwaarde (€/GJ)", min_value=0.0, value=15.0)
multiplier = 0.8  # Vast

prijs_bio = st.number_input("Prijs Bio (€/MT)", min_value=0.0, value=1200.0)
prijs_fossiel = st.number_input("Prijs Fossiel (€/MT)", min_value=0.0, value=900.0)

# Berekeningen
bio_frac = bio_percentage / 100
fossiel_frac = fossiel_percentage / 100

hbe_kosten_gj = hbe_waarde * multiplier
hbe_kosten_mt = hbe_kosten_gj * lhv_bio
hbe_kosten_totaal = hbe_kosten_mt * volume * bio_frac

blendprijs_totaal = volume * (bio_frac * prijs_bio + fossiel_frac * prijs_fossiel)
blendprijs_mt = blendprijs_totaal / volume
hbe_korting_mt = hbe_kosten_totaal / volume
netto_mt = blendprijs_mt - hbe_korting_mt

# Resultaten
st.subheader("📊 Resultaten")
st.write(f"**Aandeel Fossiel:** {fossiel_percentage:.1f}%")
st.write(f"**HBE-kosten (€/GJ):** €{hbe_kosten_gj:.2f}")
st.write(f"**HBE-kosten (€/MT):** €{hbe_kosten_mt:.2f}")
st.write(f"**HBE-kosten totaal (€):** €{hbe_kosten_totaal:,.2f}")

st.write(f"**Prijs Blend totaal (€):** €{blendprijs_totaal:,.2f}")
st.write(f"**Prijs Blend (€/MT):** €{blendprijs_mt:.2f}")
st.write(f"**HBE-korting (€/MT):** €{hbe_korting_mt:.2f}")
st.write(f"**Totaal (€/MT):** €{netto_mt:.2f}")

# Toevoegen van grafiek
bio_range = np.arange(0, 101, 1)
blendprijzen = []
netto_prijzen = []

for pct in bio_range:
    bio_frac_loop = pct / 100
    fossiel_frac_loop = 1 - bio_frac_loop
    blendprijs_loop = bio_frac_loop * prijs_bio + fossiel_frac_loop * prijs_fossiel
    hbe_korting_loop = bio_frac_loop * hbe_waarde * multiplier * lhv_bio
    netto_loop = blendprijs_loop - hbe_korting_loop
    blendprijzen.append(blendprijs_loop)
    netto_prijzen.append(netto_loop)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(bio_range, blendprijzen, label='Blendprijs (€/MT)', color='blue')
ax.plot(bio_range, netto_prijzen, label='Netto prijs (€/MT)', color='green')
ax.axvline(bio_percentage, color='gray', linestyle='--')
ax.set_xlabel('Bio-percentage (%)')
ax.set_ylabel('Prijs (€/MT)')
ax.set_title('Blendprijs en Netto prijs vs. Bio-percentage')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Gemaakt door Maarten Deddens – Volledige HBE Berekening volgens Excel-logica")
