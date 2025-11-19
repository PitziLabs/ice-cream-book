#!/bin/bash
# Recipe Renumbering Script - Difficulty-Based Order
# Run this from your recipes/ directory

echo "Renumbering recipe files to difficulty-based order..."
echo ""

# CHILL recipes (01-03)
mv 20_cardamom_pistachio_kulfi.md 01_cardamom_pistachio_kulfi.md
mv 26_vietnamese_avocado.md 02_vietnamese_avocado.md
mv 27_thai_coconut_pandan.md 03_thai_coconut_pandan.md

# LEGIT recipes (04-16)
mv 01_atole_de_anis.md 04_atole_de_anis.md
mv 02_chili_mango.md 05_chili_mango.md
mv 04_gochugaru_sesame.md 06_gochugaru_sesame.md
mv 05_golden_milk_fig.md 07_golden_milk_fig.md
mv 06_tarte_tatin.md 08_tarte_tatin.md
mv 08_miso_matcha.md 09_miso_matcha.md
mv 09_sfogliatelle.md 10_sfogliatelle.md
mv 10_sichuan_plum.md 11_sichuan_plum.md
mv 13_guava_coffee.md 12_guava_coffee.md
mv 14_wattleseed_macadamia.md 13_wattleseed_macadamia.md
mv 15_rum_banana.md 14_rum_banana.md
mv 21_horchata.md 15_horchata.md
mv 25_irish_brown_bread.md 16_irish_brown_bread.md

# THE REAL DEAL recipes (17-25)
mv 03_earl_grey_burnt_honey.md 17_earl_grey_burnt_honey.md
mv 07_lemon_rosemary_honey.md 18_lemon_rosemary_honey.md
mv 11_cashew_coconut_piri_piri.md 19_cashew_coconut_piri_piri.md
mv 16_pain_patate.md 20_pain_patate.md
mv 17_southern_brown_butter_pecan.md 21_southern_brown_butter_pecan.md
mv 18_southwest_red_chile_chocolate.md 22_southwest_red_chile_chocolate.md
mv 22_tahini_halva_rose.md 23_tahini_halva_rose.md
mv 23_coffee_berbere.md 24_coffee_berbere.md
mv 24_brigadeiro_passion_fruit.md 25_brigadeiro_passion_fruit.md

# A FUCKING ORDEAL recipes (26-27)
mv 12_appalachian_pawpaw_maple.md 26_appalachian_pawpaw_maple.md
mv 19_new_orleans_chicory_beignet.md 27_new_orleans_chicory_beignet.md

echo ""
echo "✅ Done! All recipes renumbered by difficulty."
echo ""
echo "New order:"
echo "  01-03: CHILL"
echo "  04-16: LEGIT"
echo "  17-25: THE REAL DEAL"
echo "  26-27: A FUCKING ORDEAL"
