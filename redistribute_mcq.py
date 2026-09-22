#!/usr/bin/env python3
"""Vary the correct-answer position (A/B/C) across the 3-option MCQ blocks
so the correct answer is no longer almost always option A.

For each question we keep the three <button class="opt"> lines but reorder
them so the correct one (the button carrying data-correct / avenirAnswer(this,true))
lands at a target position given by a balanced, non-repeating sequence.
The true/false and data-correct attributes stay attached to their own button,
so correctness is preserved — only the display order changes.
"""
import sys, re

# offset per module so the pattern differs between files
FILES = [
    ("/root/avenir/modules/am2-portefeuille.html", 0),
    ("/root/avenir/modules/am1-fondamentaux.html", 1),
    ("/root/avenir/modules/var.html", 2),
    ("/root/avenir/modules/frm3-volatilite.html", 1),
    ("/root/avenir/modules/frm4-taux-duration.html", 0),
    ("/root/avenir/modules/frm5-greeks.html", 2),
    ("/root/avenir/modules/frm6-credit.html", 1),
    ("/root/avenir/modules/frm7-stress-testing.html", 2),
    ("/root/avenir/modules/frm8-reglementation-capital.html", 1),
    ("/root/avenir/modules/am4-actions.html", 0),
    ("/root/avenir/modules/am4-obligations.html", 1),
    ("/root/avenir/modules/am4-immobilier.html", 2),
    ("/root/avenir/modules/am4-matieres.html", 0),
    ("/root/avenir/modules/am4-monetaire.html", 1),
    ("/root/avenir/modules/qa1-probabilites.html", 2),
    ("/root/avenir/modules/qa2-echantillons.html", 0),
    ("/root/avenir/modules/qa3-regression.html", 1),
    ("/root/avenir/modules/qa4-series-temporelles.html", 2),
    ("/root/avenir/modules/qa5-simulation-ml.html", 0),
    ("/root/avenir/modules/fmp1-institutions.html", 1),
    ("/root/avenir/modules/fmp2-derives.html", 2),
    ("/root/avenir/modules/fmp3-futures-forwards.html", 0),
    ("/root/avenir/modules/fmp4-options-strategies.html", 1),
    ("/root/avenir/modules/fmp5-taux-obligations-swaps.html", 2),
    ("/root/avenir/modules/vrm1-mesures-risque-var.html", 0),
]

def target_pos(i, offset):
    # 2*i cycles 0,2,1 -> balanced across A/B/C, never two identical in a row
    return (2 * i + offset) % 3

def process(path, offset):
    lines = open(path, encoding="utf-8").read().split("\n")
    # find runs of consecutive button.opt lines
    is_btn = [bool(re.match(r'\s*<button class="opt"', ln)) for ln in lines]
    i = 0
    q_index = 0
    dist = {0: 0, 1: 0, 2: 0}
    n = len(lines)
    while i < n:
        if is_btn[i]:
            j = i
            while j < n and is_btn[j]:
                j += 1
            run = lines[i:j]
            if len(run) == 3:
                # identify correct button
                correct_idx = next((k for k, ln in enumerate(run)
                                    if "data-correct" in ln), None)
                if correct_idx is not None:
                    tgt = target_pos(q_index, offset)
                    wrongs = [run[k] for k in range(3) if k != correct_idx]
                    new = [None, None, None]
                    new[tgt] = run[correct_idx]
                    w = 0
                    for k in range(3):
                        if new[k] is None:
                            new[k] = wrongs[w]; w += 1
                    lines[i:j] = new
                    dist[tgt] += 1
                    q_index += 1
            i = j
        else:
            i += 1
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    letters = {0: "A", 1: "B", 2: "C"}
    return q_index, {letters[k]: v for k, v in dist.items()}

for path, off in FILES:
    nq, dist = process(path, off)
    print(f"{path.split('/')[-1]}: {nq} questions -> distribution {dist}")
