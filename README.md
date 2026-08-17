# project-automation

Static asset host for the EduSync Instagram carousel schedule.
Served over GitHub Pages so Instagram's Graph API can fetch the images server-side.

## Layout

    edusync/dayNN/slotN/NN.jpg    748 carousel slides (JPEG 1080x1350)
    captions/dayNN-slotN.txt      124 captions; the whole file is the caption
    manifests/edusync.json        the schedule n8n reads on every run
    manifests/verify.py           checks a manifest against the files in this repo

- `slot1` = ertalab (08:00), `slot2` = kechqurun (20:00), Asia/Tashkent
- Days 1-2 have 7 slides per carousel, days 3-62 have 6
- JPEG only — the Instagram API rejects PNG
- Edit any caption directly in GitHub's web editor; n8n reads the live file

## The manifest

`manifests/edusync.json` holds everything the workflow used to hardcode: the account,
the start date, and which slots exist with how many slides. n8n fetches it fresh on
every run, so this repo — not the workflow — decides what gets posted.

    "posts": { "1": { "1": 7, "2": 7 }, "2": { "1": 7, "2": 6 } }
              day 1: slot1 7 slides, slot2 7 slides ...

## Adding a day past the campaign

1. Commit `edusync/day63/slot1/01.jpg …` and `captions/day63-slot1.txt`
2. Add `"63": { "1": 6, "2": 6 }` to `posts` in the manifest
3. `python3 manifests/verify.py`

That is the whole process — no n8n edit, no restart. A day missing from `posts` is
simply skipped, so gaps and one-slot days are fine.

## Fields to fill before going live

`igUserId` and `startDate` are placeholders. The workflow refuses to run until both
are real, rather than posting to the wrong account.
