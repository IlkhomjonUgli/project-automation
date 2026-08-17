#!/usr/bin/env python3
"""Check manifests/*.json against what is actually in the repo.

Run this after adding a campaign day:  python3 manifests/verify.py
Exits non-zero if the manifest promises a post the repo cannot serve.
"""
import json, os, sys, glob
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def day_for(start: str, today: date) -> int:
    """Mirror of the workflow's day maths, kept here so it is testable."""
    y, m, d = (int(x) for x in start.split('-'))
    return (today - date(y, m, d)).days + 1


def check(path):
    m = json.load(open(path))
    name = os.path.basename(path)
    errs = []

    img = m['imageBase'].split('/project-automation/', 1)[1]
    cap = m['captionBase'].split('/project-automation/', 1)[1]

    for day, slots in m['posts'].items():
        for slot, count in slots.items():
            dd = f"day{int(day):02d}"
            folder = os.path.join(ROOT, img, dd, f"slot{slot}")
            caption = os.path.join(ROOT, cap, f"{dd}-slot{slot}.txt")

            found = sorted(f for f in os.listdir(folder) if f.endswith('.jpg')) \
                if os.path.isdir(folder) else []
            want = [f"{i:02d}.jpg" for i in range(1, count + 1)]
            if found != want:
                errs.append(f"{dd}/slot{slot}: manifest says {count} slides, repo has {len(found)}")
            if not (2 <= count <= 10):
                errs.append(f"{dd}/slot{slot}: {count} slides - Instagram allows 2-10")
            if not os.path.isfile(caption):
                errs.append(f"{dd}/slot{slot}: missing {cap}/{dd}-slot{slot}.txt")
            elif not open(caption, encoding='utf-8').read().strip():
                errs.append(f"{dd}/slot{slot}: caption is empty")

    slots_total = sum(len(v) for v in m['posts'].values())
    print(f"{name}: {len(m['posts'])} days, {slots_total} slots, "
          f"{sum(n for v in m['posts'].values() for n in v.values())} slides")
    for e in errs:
        print("  FAIL", e)
    return errs


def self_test():
    assert day_for('2026-09-01', date(2026, 9, 1)) == 1
    assert day_for('2026-09-01', date(2026, 9, 2)) == 2
    assert day_for('2026-09-01', date(2026, 11, 1)) == 62   # 62-day campaign ends here
    assert day_for('2026-09-01', date(2026, 8, 31)) == 0    # before start -> no post


if __name__ == '__main__':
    self_test()
    bad = sum(len(check(p)) for p in sorted(glob.glob(os.path.join(ROOT, 'manifests', '*.json'))))
    print("OK" if not bad else f"{bad} problem(s)")
    sys.exit(1 if bad else 0)
