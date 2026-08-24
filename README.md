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
| iOS | `iPad16,3` | `utsname.machine` / [DeviceKit](https://github.com/devicekit/DeviceKit) `Device.identifier` |
| Android | `SM-X910` | `Build.MODEL` |

## Repository layout

```
.
├── schema.sql              # SQLite DDL + seed / catalog INSERTs
├── build_data.py           # Rebuilds SQLite, JSON, XML, CSV from schema.sql
├── sync_sources.py         # Monthly DeviceKit + Google Play identifier sync
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
| `market_name` | TEXT | Marketing name, e.g. `iPad Pro 11-inch (M4)` |
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

1. Fetch [DeviceKit `Device.generated.swift`](https://github.com/devicekit/DeviceKit/blob/master/Source/Device.generated.swift) and add any new iPad identifiers.
2. Fetch Google Play's supported-devices list and add Galaxy Tab models whose family uses a long-edge camera.
3. Infer `camera_position_portrait` for **new** identifiers; leave curated rows unchanged.
4. Rebuild `/output` and open a pull request.

Run the same sync locally:

```bash
python sync_sources.py
python build_data.py
```

Camera placement is not published by DeviceKit. New product families are classified with naming heuristics (Air M2+, Pro M4+, standard iPad 10th generation+, Galaxy Tab S7+). Review those rows in the monthly PR before merging.

## Using the data

JSON:

```json
{
  "id": 1,
  "model_id": "iPad16,3",
  "market_name": "iPad Pro 11-inch (M4)",
  "platform": "iOS",
  "camera_position_portrait": "RIGHT",
  "updated_at": "2026-08-24T00:00:00Z"
}
```

Look up by `model_id`. If a device is missing, treat camera position as unknown rather than assuming `TOP`.

## Credits

iPad hardware strings are derived from [DeviceKit](https://github.com/devicekit/DeviceKit) (MIT). Samsung model codes are seeded from public Tab S8/S9/S10 SKUs and refreshed from Google Play's public supported-devices catalog.
