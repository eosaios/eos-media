# EOS Media — Local Media Toolbox

> Batch convert, compress and watermark images, video and documents — in one native app, without your files ever leaving your machine.

**EOS Media** is a local-first media toolbox from the [EOS AI OS](https://eosaios.com) family: 25 feature pages in the GUI plus a full CLI sharing the same Rust core. No accounts, no uploads, no cloud dependency.

- ✓ **Images** — compress (with a never-larger guarantee), resize with platform presets, crop, watermark, EXIF removal, ICO export
- ✓ **Video & audio** — compress, trim, GIF export, cover extraction, audio conversion
- ✓ **Documents** — Markdown → DOCX/PDF/PNG, PDF → images, images → PDF
- ✓ **Batch pipelines** — queues with honest progress, cancellable tasks, output anti-overwrite
- ✓ **100% local** — everything runs on your machine; privacy-sensitive material stays private

## Download

**Current maturity ceiling: Beta.** Stable publication is disabled by `release-policy.json`. The source repository has an independent preparation/build gate. Moving reviewed code to `main` before launch does not authorize a stable release. Future stable enablement requires explicit review of both policies and the workflow dispatch options after native acceptance.

Choose an installer from [Releases](../../releases) and check its channel and platform. **Dev** is for development, **Beta** is for testing, and a version without a prerelease suffix is stable. Dev and Beta use separate application names and data directories in newly built releases. Historical beta.1–beta.3 packages used the plain EOS Media identity.

New releases include per-platform manifests (version, channel, source commit) and SHA256SUMS.txt. Existing published assets are never replaced. Dev/Beta releases are marked as prereleases and do not become stable Latest.

FFmpeg and PDFium runtimes are downloaded automatically by the app on first use — or you can use your own system installation.

## Pricing

**EOS Media is free while in beta testing** — every feature works, no sign-up required. Pricing for the 1.0 release will be announced later.

## License

Copyright (c) 2026 EOS AI OS (legal@eosaios.com). Released under the [EOS Non-Commercial License v1.1](LICENSE) — free for personal and non-commercial use; commercial use requires a separate license from the copyright holder.

## The EOS AI OS family

| Product | Form |
|---|---|
| [EOS App](https://github.com/eosaios/eos-app) | Desktop AI coding workspace |
| [EOS CLI](https://github.com/eosaios/eos) | Terminal AI coding agent |
| **EOS Media** | Local media toolbox (this repo) |

Family home: <https://eosaios.com>
