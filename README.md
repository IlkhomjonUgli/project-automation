# project-automation

Static asset host for the EduSync Instagram carousel schedule.
Served over GitHub Pages so Instagram's Graph API can fetch the images server-side.

## Layout

    edusync/dayNN/slotN/NN.jpg    748 carousel slides (JPEG 1080x1350)
    captions/dayNN-slotN.txt      124 captions; the whole file is the caption

- `slot1` = ertalab (08:00), `slot2` = kechqurun (20:00), Asia/Tashkent
- Days 1-2 have 7 slides per carousel, days 3-62 have 6
- JPEG only — the Instagram API rejects PNG
- Edit any caption directly in GitHub's web editor; n8n reads the live file
