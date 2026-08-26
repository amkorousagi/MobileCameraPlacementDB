# MobileCameraPlacementDB

모바일 기기(폰/태블릿)의 **전면 카메라 위치**를 포트레이트 기준으로 매핑한 언어 비종속 카탈로그입니다.
소스 오브 트루스는 [`schema.sql`](schema.sql) 하나이며, 여기서 SQLite / JSON / XML / CSV / 최소 CSV 5종을 생성합니다. MIT 라이선스.

화상통화·시선 보정·카메라 UI 힌트처럼 "전면 카메라가 어느 변에 붙어 있는가"가 필요한
앱에서 런타임 식별자만으로 조회할 수 있습니다.

- iOS 조회 키: `utsname.machine` (예: `iPad16,3`, `iPhone17,1`)
- Android 조회 키: `Build.MODEL` (예: `SM-X910`, `SM-X200`)

## 카메라 위치 값 정의

| 값 | 의미 |
|---|---|
| `RIGHT` | **긴 변**에 카메라. 포트레이트에서 오른쪽, 랜드스케이프 화상통화에서 위쪽 (최근 랜드스케이프 우선 태블릿) |
| `TOP` | **짧은 변**에 카메라. 모든 폰, 구형 태블릿, iPad mini |
| `LEFT` | 반대쪽 긴 변. 예약값 (현재 해당 기기 0개) |

## 데이터 소스

| 플랫폼 | Primary | Fallback | 선택 이유 |
|---|---|---|---|
| iOS | [AppleDB](https://github.com/littlebyteorg/appledb) `main.json.gz` (MIT) | [DeviceKit](https://github.com/devicekit/DeviceKit) `Device.generated.swift` | AppleDB는 식별자별로 Wi-Fi/Cellular를 구분한 이름·SoC·출시일을 제공. DeviceKit은 Swift enum이라 Wi-Fi/Cellular가 한 이름으로 묶이고 iPad 수가 적어 fallback 전용 |
| Android | [androidtrackers/certified-android-devices](https://github.com/androidtrackers/certified-android-devices) `by_model.json` | [Google Play supported_devices.csv](https://storage.googleapis.com/play_public/supported_devices.csv) (UTF-16) | Google 공식 인증 기기 CSV의 일일 UTF-8 JSON 미러이며 키가 정확히 `Build.MODEL`. 공식 CSV는 UTF-16 파싱이 필요해 fallback |

**쓰지 않는 소스**: `KHwang9883/MobileModels` — 라이선스가 CC BY-NC-SA라서 본 저장소의 MIT와 충돌합니다.

참고: Huawei는 2019년 이후 Play 인증 대상이 아니어서 MatePad 계열은 현재 소스에 사실상 없습니다
(규칙은 코드에 유지, 브랜드 검증으로 서드파티 짝퉁 오탐 방지).

## 카메라 위치 추론 규칙

### iOS

| 기기 | 규칙 |
|---|---|
| iPhone, iPod touch | 전부 `TOP` |
| iPad mini 전체 | `TOP` (A17 Pro 포함) |
| iPad Air | M2 이상 `RIGHT`, 그 이전 `TOP` |
| iPad Pro | M4 이상 `RIGHT`, 그 이전 `TOP` — 11형 3세대(`iPad13,4–7`)·4세대(`iPad14,3–4`)는 `TOP` |
| iPad(무印) | 10세대(`iPad13,18/19`)·iPad (A16)(`iPad15,7/8`)부터 `RIGHT`, 9세대까지 `TOP` |

판별 힌트: SoC 필드(M2+/M4+/A16+)와 이름의 `"(M2)"`, `"10th generation"`, `"iPad (A16)"` 패턴.

### Android

| 기기 | 규칙 |
|---|---|
| 폰 전체 | `TOP` (폴더블 내부 카메라는 예외일 수 있으나 `Build.MODEL` 단위 관례상 `TOP`) |
| Galaxy Tab S7 이상 (S8/S9/S10/…, +/Ultra/FE/Lite 포함) | `RIGHT` |
| Pixel Tablet, OnePlus Pad, OPPO Pad, Xiaomi/Redmi/POCO Pad, Honor Pad/MagicPad, Huawei MatePad Pro, Lenovo Tab P11/P12 | `RIGHT` |
| 위 패밀리 중 검증된 예외: Oppo/Xiaomi **Pad Mini**, **Xiaomi Pad 5 세대**(12.4 제외), **Redmi Pad SE 8.7/SE 4G**, **Honor Pad X7** | `TOP` |
| 그 외 태블릿 (Tab A8, A7, S6, Active 등) | `TOP` |

규칙으로 추론된 비삼성 Android 태블릿 130행(83개 제품)은 공식 제품 페이지·매뉴얼·주요 매체 리뷰 이미지로 전수 검증했습니다.
제품별 근거 링크는 [docs/camera-position-references.md](docs/camera-position-references.md) 참조.
~9인치 미만 소형 태블릿은 세로 우선(짧은 변)으로 회귀하는 경향이 있어 신규 소형 기기는 개별 확인이 필요합니다.

## iPad의 RIGHT(가로 우선) 전환 경향

| 출시연도 | RIGHT 비율 | 비고 |
|---|---|---|
| 2010–2021 | 0% | 전 모델 짧은 변(`TOP`) |
| 2022 | ~25% | iPad 10세대만 전환 |
| 2023 | — | 신형 iPad 없음 |
| 2024 | ~80% | Air M2 + Pro M4 전환, mini(A17 Pro)만 `TOP` 유지 |
| 2025– | 사실상 100% | mini를 제외한 전 라인 전환 |

Android는 Galaxy Tab S7(2020)이 같은 전환을 더 일찍 시작했고, 폰은 전환이 없습니다.
연도별 실측 수치는 [`output/stats.json`](output/stats.json)의 `ipad_by_release_year` 참조.

## 사용법

```bash
# schema.sql -> output/devices.{db,json,xml,csv,min.csv}  (표준 라이브러리만, 결정적 빌드)
python build_data.py

# 소스 동기화: 신규 model_id만 schema.sql에 추가, 기존 카메라 위치 보존,
# output/stats.json 갱신 (매월 1일 GitHub Actions로 자동 실행)
python sync_sources.py
```

조회 예 (SQLite):

```sql
SELECT camera_position_portrait FROM devices WHERE model_id = 'iPad16,3';  -- RIGHT
SELECT camera_position_portrait FROM devices WHERE model_id = 'SM-X200';   -- TOP
```

### 앱 임베드용 최소 CSV (`output/devices.min.csv`)

앱 번들에 넣어 메모리 부담 없이 로드할 수 있는 최소 룩업 테이블입니다.

- 헤더 없음, 2열: `model_id,camera_position` (행 순서는 다른 출력과 동일)
- 카메라 위치는 단일 대문자: `T`=TOP, `R`=RIGHT, `L`=LEFT
- 전체 CSV 대비 약 1/3 크기

```csv
"iPad16,3",R
SM-X200,T
```

주의: iOS 식별자는 `model_id` 자체에 콤마가 있어(`iPad16,3`) CSV 규칙대로 큰따옴표로 감싸집니다.
표준 CSV 파서를 사용하거나, 직접 파싱한다면 "마지막 콤마 뒤 1글자 = 위치, 그 앞 전체(따옴표 제거) = model_id"로 처리하세요.

## 유지보수 규칙

- `schema.sql`이 유일한 소스 오브 트루스. `output/`은 전부 생성물.
- sync는 **신규 model_id만 INSERT**하고, 기존 행의 `camera_position_portrait`는 절대 덮어쓰지 않음. marketing name만 primary 소스가 더 정확할 때 갱신.
- `updated_at`은 INSERT에 ISO-8601 UTC 리터럴로 고정 → 재빌드가 바이트 단위로 결정적 (CI 무한 커밋 방지).
- INSERT는 200행 단위 청크.

## License

MIT — see [LICENSE](LICENSE).
