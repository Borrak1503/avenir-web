#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, os
OUT="/root/avenir-web/public/files"; os.makedirs(OUT,exist_ok=True)
STR={
"fr":{"lang_tag":"Français","doc_title":"Exercice et corrigé","subtitle":"Mesures de risque : VaR, ES & volatilité",
 "module":"Financial Risk Management · Modèles d'évaluation & de risque · Mesures de risque",
 "intro":"Quatre parties pour maîtriser les mesures de queue : calculer VaR et ES dans les cas usuels, lire un cas discret, montrer que la VaR punit parfois la diversification, et mettre à jour la volatilité qui les nourrit. Traitez chaque partie avant de lire la solution.",
 "statement":"Énoncé","solution":"Solution",
 "parts":[
  ("Partie A · VaR et ES, cas normal",
   "Les pertes suivent N(−20, 30) (en M). Avec z₉₉ = 2,326 et φ(2,326) = 0,02665, calculez (a) la VaR 99 %, (b) l'ES 99 %, et vérifiez la relation entre les deux.",
   ["(a) VaR = µ + σ·z = −20 + 30 × 2,326 = <b>49,79 M</b>.",
    "(b) ES = µ + σ·φ(z)/(1 − X) = −20 + 30 × 0,02665/0,01 = −20 + 79,95 = <b>59,96 M</b>. On a bien ES ≥ VaR : l'ES moyenne des pertes toutes supérieures à la VaR. Piège : ne pas oublier le terme de moyenne −20, et diviser φ(z) par (1 − X) = 0,01."]),
  ("Partie B · Cas discret",
   "Un portefeuille subit des pertes de 2, 5 ou 8 M avec des probabilités 88 %, 10 % et 2 %. Calculez la VaR 99 %, la VaR 97 % et l'ES 97 %.",
   ["Probabilités cumulées : [0-88] → 2 M, [88-98] → 5 M, [98-100] → 8 M. VaR 99 % : le percentile 99 tombe dans [98 ; 100], donc <b>8 M</b>. VaR 97 % : le percentile 97 tombe dans [88 ; 98], donc <b>5 M</b>.",
    "ES 97 % : la queue de 3 % contient 8 M (2 %) et 5 M (1 %), renormalisées à 2/3 et 1/3. ES = (2/3) × 8 + (1/3) × 5 = <b>7 M</b> > VaR 97 %. À la frontière exacte 98 %, la VaR est ambiguë et la convention prend la moyenne (6,5 M)."]),
  ("Partie C · La VaR punit la diversification",
   "Deux contrats d'assurance indépendants : chacun subit 20 M avec probabilité 0,8 %, sinon 1 M. (a) VaR 99 % d'un contrat ? (b) VaR 99 % du portefeuille des deux ? (c) Conclusion ?",
   ["(a) La perte de 20 M (0,8 %) est sous le seuil de 1 % : elle échappe à la VaR 99 %, qui vaut seulement <b>1 M</b>.",
    "(b) Par indépendance : 2 M (98,4064 %), 21 M (1,5872 %), 40 M (0,0064 %). La probabilité d'au moins une grosse perte (1,5936 %) dépasse 1 %, donc le percentile 99 tombe sur 21 M : <b>VaR 99 % = 21 M</b>.",
    "(c) 21 > 1 + 1 : la VaR du portefeuille diversifié dépasse la somme des VaR, alors que rien n'a changé économiquement. C'est une violation de la sous-additivité : la VaR n'est pas cohérente. L'ES, elle, reste sous-additive."]),
  ("Partie D · Volatilité EWMA et GARCH",
   "La volatilité EWMA d'hier est σₙ₋₁ = 1,5 % par jour (λ = 0,94). Le marché bouge de rₙ₋₁ = 3 %. (a) Nouvelle volatilité EWMA ? (b) En quoi un GARCH(1,1) diffère-t-il à long horizon ?",
   ["(a) σ²ₙ = 0,94 × 0,015² + 0,06 × 0,03² = 0,00021150 + 0,00005400 = 0,0002655, donc σₙ = <b>1,629 %</b>. Le choc a fait monter la volatilité de 1,5 % à 1,63 %.",
    "(b) L'EWMA laisse cette volatilité persister sans ancre. Le GARCH(1,1) ajoute un poids sur la variance de long terme V_L (σ²ₙ = ω + αr² + βσ², ω = γV_L) : sa prévision revient graduellement vers V_L (mean reversion), ce qui donne de meilleures prévisions à long horizon. Si la volatilité courante est au-dessus de V_L, le GARCH prévoit une baisse."]),
 ],
 "closing":"À retenir : VaR = percentile X des pertes (normal µ + σz, discret par paliers cumulés) ; ES = E[L | L > VaR] ≥ VaR (moyenne renormalisée de la queue) ; la VaR viole la sous-additivité alors que l'ES est cohérente, d'où FRTB → ES 97,5 % ; l'EWMA met à jour σ² = λσ² + (1−λ)r² et le GARCH ajoute une ancre de long terme et la mean reversion.",
 "footer":"Avenir · Exercice pédagogique · à des fins d'apprentissage uniquement"},
"en":{"lang_tag":"English","doc_title":"Exercise and worked solution","subtitle":"Risk measures: VaR, ES & volatility",
 "module":"Financial Risk Management · Valuation & Risk Models · Risk measures",
 "intro":"Four parts to master tail measures : compute VaR and ES in the usual cases, read a discrete case, show that VaR sometimes punishes diversification, and update the volatility that feeds them. Work through each part before reading the solution.",
 "statement":"Problem","solution":"Solution",
 "parts":[
  ("Part A · VaR and ES, normal case",
   "Losses follow N(−20, 30) (in M). With z₉₉ = 2.326 and φ(2.326) = 0.02665, compute (a) the 99% VaR, (b) the 99% ES, and check the relation between them.",
   ["(a) VaR = µ + σ·z = −20 + 30 × 2.326 = <b>49.79M</b>.",
    "(b) ES = µ + σ·φ(z)/(1 − X) = −20 + 30 × 0.02665/0.01 = −20 + 79.95 = <b>59.96M</b>. Indeed ES ≥ VaR: ES averages losses all above the VaR. Trap: do not forget the mean term −20, and divide φ(z) by (1 − X) = 0.01."]),
  ("Part B · Discrete case",
   "A portfolio suffers losses of 2, 5 or 8M with probabilities 88%, 10% and 2%. Compute the 99% VaR, the 97% VaR and the 97% ES.",
   ["Cumulative probabilities: [0-88] → 2M, [88-98] → 5M, [98-100] → 8M. 99% VaR: the 99 percentile falls in [98; 100], so <b>8M</b>. 97% VaR: the 97 percentile falls in [88; 98], so <b>5M</b>.",
    "97% ES: the 3% tail holds 8M (2%) and 5M (1%), renormalised to 2/3 and 1/3. ES = (2/3) × 8 + (1/3) × 5 = <b>7M</b> > 97% VaR. At the exact 98% boundary, VaR is ambiguous and the convention takes the average (6.5M)."]),
  ("Part C · VaR punishes diversification",
   "Two independent insurance contracts: each suffers 20M with probability 0.8%, otherwise 1M. (a) 99% VaR of one contract? (b) 99% VaR of the portfolio of both? (c) Conclusion?",
   ["(a) The 20M loss (0.8%) is below the 1% threshold: it escapes the 99% VaR, which is only <b>1M</b>.",
    "(b) By independence: 2M (98.4064%), 21M (1.5872%), 40M (0.0064%). The probability of at least one big loss (1.5936%) exceeds 1%, so the 99 percentile falls on 21M: <b>99% VaR = 21M</b>.",
    "(c) 21 > 1 + 1: the diversified portfolio's VaR exceeds the sum of the VaRs, though nothing changed economically. This is a subadditivity violation: VaR is not coherent. ES, by contrast, stays subadditive."]),
  ("Part D · EWMA and GARCH volatility",
   "Yesterday's EWMA volatility is σₙ₋₁ = 1.5% per day (λ = 0.94). The market moves by rₙ₋₁ = 3%. (a) New EWMA volatility? (b) How does a GARCH(1,1) differ at long horizon?",
   ["(a) σ²ₙ = 0.94 × 0.015² + 0.06 × 0.03² = 0.00021150 + 0.00005400 = 0.0002655, so σₙ = <b>1.629%</b>. The shock lifted volatility from 1.5% to 1.63%.",
    "(b) EWMA lets this volatility persist with no anchor. GARCH(1,1) adds a weight on the long-run variance V_L (σ²ₙ = ω + αr² + βσ², ω = γV_L): its forecast returns gradually toward V_L (mean reversion), giving better long-horizon forecasts. If current volatility is above V_L, GARCH forecasts a decline."]),
 ],
 "closing":"Key takeaways: VaR = X percentile of losses (normal µ + σz, discrete by cumulated bands); ES = E[L | L > VaR] ≥ VaR (renormalised tail average); VaR violates subadditivity while ES is coherent, hence FRTB → ES 97.5%; EWMA updates σ² = λσ² + (1−λ)r² and GARCH adds a long-run anchor and mean reversion.",
 "footer":"Avenir · Teaching exercise · for learning purposes only"},
"nl":{"lang_tag":"Nederlands","doc_title":"Oefening en uitgewerkte oplossing","subtitle":"Risicomaten: VaR, ES & volatiliteit",
 "module":"Financial Risk Management · Waarderings- & risicomodellen · Risicomaten",
 "intro":"Vier delen om staartmaten te beheersen : VaR en ES berekenen in de gebruikelijke gevallen, een discreet geval lezen, aantonen dat VaR soms diversificatie bestraft, en de volatiliteit bijwerken die ze voedt. Werk elk deel uit voordat u de oplossing leest.",
 "statement":"Opgave","solution":"Oplossing",
 "parts":[
  ("Deel A · VaR en ES, normaal geval",
   "Verliezen volgen N(−20, 30) (in M). Met z₉₉ = 2,326 en φ(2,326) = 0,02665, bereken (a) de 99% VaR, (b) de 99% ES, en controleer de relatie tussen beide.",
   ["(a) VaR = µ + σ·z = −20 + 30 × 2,326 = <b>49,79M</b>.",
    "(b) ES = µ + σ·φ(z)/(1 − X) = −20 + 30 × 0,02665/0,01 = −20 + 79,95 = <b>59,96M</b>. Inderdaad ES ≥ VaR: ES middelt verliezen die allemaal boven de VaR liggen. Valstrik: vergeet de gemiddelde-term −20 niet, en deel φ(z) door (1 − X) = 0,01."]),
  ("Deel B · Discreet geval",
   "Een portefeuille lijdt verliezen van 2, 5 of 8M met kansen 88%, 10% en 2%. Bereken de 99% VaR, de 97% VaR en de 97% ES.",
   ["Cumulatieve kansen: [0-88] → 2M, [88-98] → 5M, [98-100] → 8M. 99% VaR: het 99-percentiel valt in [98; 100], dus <b>8M</b>. 97% VaR: het 97-percentiel valt in [88; 98], dus <b>5M</b>.",
    "97% ES: de 3%-staart bevat 8M (2%) en 5M (1%), hernormaliseerd naar 2/3 en 1/3. ES = (2/3) × 8 + (1/3) × 5 = <b>7M</b> > 97% VaR. Op de exacte grens 98% is VaR dubbelzinnig en neemt de conventie het gemiddelde (6,5M)."]),
  ("Deel C · VaR bestraft diversificatie",
   "Twee onafhankelijke verzekeringscontracten: elk lijdt 20M met kans 0,8%, anders 1M. (a) 99% VaR van één contract? (b) 99% VaR van de portefeuille van beide? (c) Conclusie?",
   ["(a) Het verlies van 20M (0,8%) ligt onder de 1%-drempel: het ontsnapt aan de 99% VaR, die slechts <b>1M</b> is.",
    "(b) Door onafhankelijkheid: 2M (98,4064%), 21M (1,5872%), 40M (0,0064%). De kans op minstens één groot verlies (1,5936%) overschrijdt 1%, dus het 99-percentiel valt op 21M: <b>99% VaR = 21M</b>.",
    "(c) 21 > 1 + 1: de VaR van de gediversifieerde portefeuille overschrijdt de som van de VaR's, hoewel economisch niets veranderde. Dit is een schending van subadditiviteit: VaR is niet coherent. ES daarentegen blijft subadditief."]),
  ("Deel D · EWMA- en GARCH-volatiliteit",
   "De EWMA-volatiliteit van gisteren is σₙ₋₁ = 1,5% per dag (λ = 0,94). De markt beweegt met rₙ₋₁ = 3%. (a) Nieuwe EWMA-volatiliteit? (b) Hoe verschilt een GARCH(1,1) op lange horizon?",
   ["(a) σ²ₙ = 0,94 × 0,015² + 0,06 × 0,03² = 0,00021150 + 0,00005400 = 0,0002655, dus σₙ = <b>1,629%</b>. De schok tilde de volatiliteit van 1,5% naar 1,63%.",
    "(b) EWMA laat deze volatiliteit persisteren zonder anker. GARCH(1,1) voegt een gewicht toe op de langetermijnvariantie V_L (σ²ₙ = ω + αr² + βσ², ω = γV_L): zijn voorspelling keert geleidelijk terug naar V_L (mean reversion), wat betere langetermijnvoorspellingen geeft. Ligt de huidige volatiliteit boven V_L, dan voorspelt GARCH een daling."]),
 ],
 "closing":"Onthoud: VaR = X-percentiel van verliezen (normaal µ + σz, discreet via gecumuleerde banden); ES = E[L | L > VaR] ≥ VaR (hernormaliseerd staartgemiddelde); VaR schendt subadditiviteit terwijl ES coherent is, vandaar FRTB → ES 97,5%; EWMA werkt σ² = λσ² + (1−λ)r² bij en GARCH voegt een langetermijnanker en mean reversion toe.",
 "footer":"Avenir · Pedagogische oefening · uitsluitend voor leerdoeleinden"},
}
CSS="""
@page { size: A4; margin: 20mm 18mm 16mm 18mm; }
* { box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Arial, sans-serif; color:#1c2530; font-size:11pt; line-height:1.5; }
.brand { color:#13294b; font-weight:800; font-size:15pt; } .brand b { color:#2f7d7a; }
.tag { color:#66707a; font-size:8.5pt; text-transform:uppercase; letter-spacing:1px; margin-top:2px; }
.head { border-bottom:2px solid #13294b; padding-bottom:10px; margin-bottom:16px; }
.langtag { float:right; font-size:8.5pt; color:#66707a; border:1px solid #d9dee3; border-radius:20px; padding:2px 10px; }
h1 { color:#13294b; font-size:19pt; margin:14px 0 2px; }
.sub { color:#2f7d7a; font-weight:700; font-size:12.5pt; margin:0 0 8px; }
.intro { color:#3a4551; background:#f5f7f9; border-radius:8px; padding:11px 14px; font-size:10.5pt; margin-bottom:8px; }
.part { margin-top:16px; page-break-inside:avoid; }
.pt { color:#13294b; font-size:12.5pt; font-weight:800; border-left:4px solid #2f7d7a; padding-left:10px; margin-bottom:6px; }
.lbl { display:inline-block; font-size:8.5pt; font-weight:700; text-transform:uppercase; letter-spacing:.6px; color:#66707a; margin:6px 0 3px; }
.statement { background:#fbfcfd; border:1px solid #e5e9ed; border-radius:8px; padding:9px 13px; }
.sol { border-left:3px solid #13294b; background:#f7f9fb; border-radius:0 8px 8px 0; padding:6px 14px; margin-top:6px; }
.sol ol { margin:4px 0 4px 4px; padding-left:18px; } .sol li { margin:3px 0; }
b { color:#13294b; } sup { font-size:70%; }
.closing { margin-top:18px; background:#13294b; color:#eef2f6; border-radius:8px; padding:11px 14px; font-size:10.5pt; }
.footer { margin-top:14px; border-top:1px solid #e5e9ed; padding-top:6px; color:#8a939c; font-size:8pt; text-align:center; }
"""
def build(lang):
    s=STR[lang]; parts=""
    for (title,st,steps) in s["parts"]:
        lis="".join(f"<li>{x}</li>" for x in steps)
        parts+=f'<div class="part"><div class="pt">{title}</div><div class="lbl">{s["statement"]}</div><div class="statement">{st}</div><div class="lbl">{s["solution"]}</div><div class="sol"><ol>{lis}</ol></div></div>'
    return f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="head"><span class="langtag">{s["lang_tag"]}</span><div class="brand">Avenir<b>.</b></div><div class="tag">{s["module"]}</div></div><h1>{s["doc_title"]}</h1><div class="sub">{s["subtitle"]}</div><div class="intro">{s["intro"]}</div>{parts}<div class="closing">{s["closing"]}</div><div class="footer">{s["footer"]}</div></body></html>'
for lang in ("fr","en","nl"):
    hp=f"/tmp/vrm1_{lang}.html"; open(hp,"w",encoding="utf-8").write(build(lang))
    outp=f"{OUT}/vrm1-exercice-corrige-{lang}.pdf"
    subprocess.run(["wkhtmltopdf","--quiet","--encoding","utf-8",hp,outp],capture_output=True,text=True)
    ok=os.path.exists(outp) and os.path.getsize(outp)>2000
    print(lang,"->","OK" if ok else "FAIL", os.path.getsize(outp) if os.path.exists(outp) else 0)
