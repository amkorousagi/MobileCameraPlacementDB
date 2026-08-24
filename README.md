# Mobile Camera Placement DB

Language-agnostic hardware database of **tablet front-camera location** in portrait orientation (`RIGHT`, `TOP`, or `LEFT`). Apps that pin a camera preview, punch-hole overlay, or video-call layout can look up a device by its hardware identifier without depending on a specific SDK.

License: [MIT](LICENSE).

## Camera positions

Values describe where the front camera sits when the tablet is held **in portrait** (short edges at top and bottom):

| Value | Meaning |
| --- | --- |
| `RIGHT` | Camera is on the long edge — the right side in portrait, which becomes the top edge in landscape video calls. |
| `TOP` | Camera is on the short edge (classic iPad / older tablet placement). |
| `LEFT` | Reserved for the opposite long edge. |

Modern landscape-first tablets (iPad 10th generation and later standard iPads, iPad Air M2+, iPad Pro M4+, Galaxy Tab S7+ flagships) use `RIGHT`.

## Identifiers

| Platform | `model_id` example | How to read it at runtime |
| --- | --- | --- |
| iOS | `iPad16,3` | `utsname.machine` |
| Android | `SM-X910` | `Build.MODEL` |

## Identifier sources

`sync_sources.py` pulls catalog rows from structured public databases rather than scraping vendor HTML.

| Platform | Primary source | Why this one | Fallback |
| --- | --- | --- | --- |
| iOS | [AppleDB](https://appledb.dev) (`api.appledb.dev/device/main.json.gz`, MIT) | Identifier-keyed JSON with Wi-Fi vs Cellular names, device type, and SoC. Covers more iPad hardware strings than DeviceKit or Xcode identifier dumps. | [DeviceKit](https://github.com/devicekit/DeviceKit) `Device.generated.swift` |
| Android | [androidtrackers/certified-android-devices](https://github.com/androidtrackers/certified-android-devices) `by_model.json` (MIT) | Daily UTF-8 JSON of Google Play's official certified-device list, keyed by `Build.MODEL`. | [Google Play supported_devices.csv](https://storage.googleapis.com/play_public/supported_devices.csv) |

Not used: [KHwang9883/MobileModels](https://github.com/KHwang9883/MobileModels) (CC BY-NC-SA 4.0, incompatible with this MIT catalog) and DeviceKit as the primary iOS source (Swift enums collapse Wi-Fi/Cellular variants and lag AppleDB).

## Repository layout

```
.
├── schema.sql              # SQLite DDL + seed / catalog INSERTs
├── build_data.py           # Rebuilds SQLite, JSON, XML, CSV from schema.sql
├── sync_sources.py         # Monthly AppleDB + Google Play identifier sync
├── output/
│   ├── devices.db
│   ├── devices.json
│   ├── devices.xml
│   └── devices.csv
├── LICENSE
└── .github/workflows/
    ├── build.yml           # Rebuild artifacts on push to main
    └── monthly-update.yml  # 1st of each month: sync new devices, open a PR
```

## Schema

`devices`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | INTEGER | Primary key |
| `model_id` | TEXT | Unique hardware identifier |
| `market_name` | TEXT | Marketing name, e.g. `iPad Pro 11-inch (M4) Wi-Fi` |
| `platform` | TEXT | `iOS` or `Android` |
| `camera_position_portrait` | TEXT | `RIGHT`, `TOP`, or `LEFT` |
| `updated_at` | TEXT | ISO-8601 UTC; stable across rebuilds |

## Build locally

Python 3.9+ with no third-party packages:

```bash
python build_data.py
```

This reads `schema.sql`, writes `output/devices.db`, and exports the same rows to JSON (indent 2), CSV, and XML (`<devices>` / `<device>`).

## Monthly auto-update

`.github/workflows/monthly-update.yml` runs on the 1st of each month (and via `workflow_dispatch`):

1. Fetch [AppleDB](https://api.appledb.dev/device/main.json.gz) and add any new iPad identifiers (names include Wi-Fi vs Cellular).
2. Fetch [androidtrackers `by_model.json`](https://github.com/androidtrackers/certified-android-devices) (Google Play certified devices) and add Galaxy Tab models whose family uses a long-edge camera.
3. Refresh marketing names from those sources. Infer `camera_position_portrait` for **new** identifiers; leave curated positions unchanged.
4. Rebuild `/output` and open a pull request.

Run the same sync locally:

```bash
python sync_sources.py
python build_data.py
```

Camera placement is not published by AppleDB or Google Play. New product families are classified with naming heuristics (Air M2+, Pro M4+, standard iPad 10th generation+, Galaxy Tab S7+). Review those rows in the monthly PR before merging.

## Using the data

JSON:

```json
{
  "id": 1,
  "model_id": "iPad16,3",
  "market_name": "iPad Pro 11-inch (M4) Wi-Fi",
  "platform": "iOS",
  "camera_position_portrait": "RIGHT",
  "updated_at": "2026-08-24T00:00:00Z"
}
```

Look up by `model_id`. If a device is missing, treat camera position as unknown rather than assuming `TOP`.

## Credits

iPad hardware identifiers and names come from [AppleDB](https://github.com/littlebyteorg/appledb) (MIT). Android `Build.MODEL` codes come from [Google Play's certified-device list](https://support.google.com/googleplay/android-developer/answer/1727131), consumed as UTF-8 JSON via [androidtrackers/certified-android-devices](https://github.com/androidtrackers/certified-android-devices) (MIT).
