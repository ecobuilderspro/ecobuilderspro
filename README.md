# EcoBuilders site

Static site served by GitHub Pages. Everything here goes at the repo root.

## What's in here

| File | What it is |
|---|---|
| `index.html` | Home page |
| `services/*.html` | Six service pages |
| `styles.css` | All styling for every page |
| `site.js` | Theme toggle, mobile nav, phone reveal, gallery |
| `assets/` | Photos, logos, badges |
| `build.py` | Generates the HTML. Optional — see below |

## Installing

Replace the old files with these. Then **delete** the following from the repo,
they are no longer used:

```
gallery.js
assets/cubix-megapack-crane.jpg      assets/kaiser-diamond-bar.jpg
assets/getty-center.jpg              assets/ups-fleet-depot.jpg
assets/domaine-carneros-solar.jpg    assets/domaine-ground-mount.jpg
assets/sanford-aerial.jpg            assets/edge-ems.jpg
assets/commissioning-rope-ct.jpg     assets/om-ev-charging.jpg
assets/om-iv-tracer.png              assets/solar-ground.jpg
assets/solar-rooftop.jpg             assets/functional-testing.jpg
```

Those were renamed to neutral filenames (the old ones named clients in the URL)
or dropped because nothing used them.

## Adding a project later

All project content lives in one place: the `P = { ... }` block near the top of
`build.py`. One entry per project:

```python
 "mf-somewhere": dict(
    title="12 Pedestals · Somewhere, CA",       # what it is + city
    specs="12 pedestals · Level 2",             # the numbers
    note="One line about the scope.",
    images=[("multifamily-somewhere.jpg", "Caption for this photo."),
            ("multifamily-somewhere-2.jpg", "Caption for the second photo.")]),
```

Then add the key to the right section in `SERVICES` further down, drop the
photos in `assets/`, and run:

```
python3 build.py
```

That rewrites `index.html` and all six service pages. Commit the result.

You never have to touch the HTML by hand — and because every page is generated
from the same partials, the header, footer and gallery can't drift apart.

If you'd rather not run Python, the generated HTML is perfectly editable
directly; just remember a change to the header has to be made in all seven files.

## Theme

Colours are defined once as tokens at the top of `styles.css` — `--bg`,
`--surface`, `--text`, `--muted`, `--border`. Dark mode re-declares the same
names under `[data-theme="dark"]`. Change a colour there and it changes
everywhere, in both themes.

The theme follows the visitor's system setting until they click the sun/moon
button, after which their choice is remembered. A small script in each page's
`<head>` sets it before the page paints, so dark-mode visitors never see a
white flash.

## Photos

Captions describe the real job. Where a photo is standing in for a site you
don't have a picture of yet, swap the file in `assets/` and keep the caption.

Images are resized to 1600px wide and compressed. If you drop in a new one
straight off a phone, run it through the same treatment or the page gets slow.

## Still to do

- Photos for San Francisco, Bay Point, Camden NJ, Canoga Park, and the JPI
  Riverside site — those five projects are parked, not in the site.
- A favicon (browsers currently request one and get a 404).
- Crops noted during review: truck-door logo on the corridor drone shots,
  charger-face lettering on the Torrance photo, fuel-canopy branding at
  Chula Vista, building signage on the Irwindale aerial.
