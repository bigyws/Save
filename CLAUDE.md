# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Two independent, dependency-free static web projects. There is no build step, package manager, linter, or test suite: open the HTML files in a browser (or serve the repo root, e.g. `python3 -m http.server`). User-facing text and docs are in Korean; keep it that way.

- `whack-a-mole/index.html`: a single-file browser game (HTML, CSS and JS all inline). The best score is kept in `localStorage` under `whack-best`.
- `nfc-keyring/`: "콕태그", a product site for an acrylic pet keyring with an embedded NFC chip that opens a pet memory album. `nfc-keyring/README.md` is the owner-facing guide (deployment via GitHub Pages, payments, chip writing). Update it when behavior it describes changes.

## nfc-keyring architecture

Pages are plain HTML that load shared scripts with `<script src>` tags in this order: `art.js`, then `data.js`, then (for pages that need it) `store.js`. Each script is an IIFE that sets a global:

- `art.js` → `window.KokArt`: draws every illustration as an SVG string (characters `petArt`, keyring faces `keyringSVG(kind, side, opts)`, and the sample "photos" `photoSVG(kind, scene, opts)`). There are no image assets for the samples; a photo entry with `scene: "park"` is drawn by `photoSVG`, while a real customer photo uses `src: "photos/<id>/01.jpg"` instead.
- `data.js` → `window.KOK`: the single source of truth for pets (`KOK.pets.<id>`) and shop pricing (`KOK.shop`: products, plans, engraving, shipping, free-shipping threshold). `index.html` and `app.html` both read prices from it.
- `store.js` → `window.KokStore`: user-uploaded photos/videos kept in IndexedDB (`kok-memories`), and like counts kept in `localStorage`. This is a browser-only placeholder; replacing it with a real backend (Firebase or Supabase) should only require changing this file and keeping its API (`list`, `add`, `remove`, `likes`, `like`).

`art.js` and `data.js` also export through `module.exports`, so they can be `require`d from Node.

Pages:
- `memory.html?pet=<id>`: the album an NFC tag opens. The `pet` query parameter selects `KOK.pets[id]`. Samples are `choco` (dog) and `nabi` (cat).
- `index.html`: web-style shop page with a live engraving preview and order form. The order form is a preview only: no payment is wired up.
- `app.html`: app-style version, installable via `manifest.json`. Its "내 키링" tab writes the album URL to an NFC chip with Web NFC (`NDEFReader`), which only works on Android Chrome.
- `designs.html`: design sheet and manufacturing specs, rendered from `art.js`.

`designs/*.svg` are the print files sent to the keyring maker. They are `KokArt.keyringSVG(kind, side, { id: "p" })` output (kind `dog`/`cat`, side `front`/`back`) wrapped in a standalone SVG file. If you change the keyring art in `art.js`, regenerate them with Node so the print files stay in sync with the site.

Adding a customer means adding an entry under `KOK.pets` in `data.js` (see the example in `nfc-keyring/README.md`). The NFC chip URL is `https://<site>/nfc-keyring/memory.html?pet=<id>`.
