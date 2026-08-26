# 전면 카메라 위치 검증 레퍼런스

**검증일**: 2026-08-26
**범위**: 규칙 기반 추론으로 `RIGHT`가 부여됐던 비(非)삼성 Android 태블릿 130행 / 83개 제품 전수.
(iPhone·iPad는 Apple 공식 제품 사양으로 확정, Galaxy Tab S7 이상 91행은 삼성의 공식 가로 배치 전환으로 확정이라 본 문서 범위에서 제외.)

**방법**: 제품별로 공식 제품 페이지·공식 매뉴얼(FCC 제출본 포함)·주요 매체 리뷰의 제품 이미지/명시 문구로
전면 카메라가 **긴 변(LONG, 가로형)** 인지 **짧은 변(SHORT, 세로형)** 인지 확인.
LONG → DB 값 `RIGHT`, SHORT → DB 값 `TOP`.

## 결과 요약

- 검증 83개 제품 중 **76개 LONG(RIGHT 유지)**, **7개 SHORT(오분류)** → DB 10행 `RIGHT`→`TOP` 교정.
- UNVERIFIED 0건.

### 교정된 행 (RIGHT → TOP)

| Build.MODEL | 제품 | 사유 |
|---|---|---|
| `JMS-W09` | HONOR Pad X7 | 8.7" 폰 스타일, 짧은 변 카메라 |
| `OPD2515` | Oppo Pad Mini | 짧은 변 펀치홀 (iPad mini와 동일 배치) |
| `24075RP89G` | Redmi Pad SE 8.7 | 짧은 변 카메라 |
| `24076RP19G` | Redmi Pad SE 8.7 4G | 동일 기기 (Wi-Fi/4G 단일 디자인) |
| `24076RP19I` | Redmi Pad SE 4G | = Redmi Pad SE 8.7 인도판 (GSMArena 명시) |
| `21051182C`, `21051182G` | Xiaomi Pad 5 | 짧은 변 카메라 (가로 배치는 Pad 6부터) |
| `M2105K81AC` | Xiaomi Pad 5 Pro (11") | 짧은 변 카메라 |
| `M2105K81C` | Xiaomi Pad 5 Pro 5G | 짧은 변 카메라 |
| `25079RPDCG` | Xiaomi Pad Mini | 짧은 변 카메라, 세로 우선 (Expert Reviews 명시) |

주의: `22081281AC`는 이름이 "Xiaomi Pad 5 Pro"지만 실제로는 **Pad 5 Pro 12.4**(2022)로, 전면 카메라가 긴 변에 있어 `RIGHT`를 유지합니다 ([Tencent News 리뷰](https://news.qq.com/rain/a/20220815A07Y3Y00)).

---

## 브랜드별 근거

표기: **edge** = LONG(긴 변) / SHORT(짧은 변), **DB** = 최종 `camera_position_portrait`.

### Google / Lenovo

| 제품 | Build.MODEL | edge | DB | 근거 |
|---|---|---|---|---|
| Google Pixel Tablet | `Pixel Tablet` | LONG | RIGHT | [Thurrott 리뷰](https://www.thurrott.com/mobile/android/284925/google-pixel-tablet-review) "webcam in the upper right center of the top bezel (in landscape mode)"; [HotHardware](https://hothardware.com/reviews/google-pixel-tablet-review) |
| Lenovo Tab P11 | `Lenovo TB-J606F/L` | LONG | RIGHT | [Lenovo 공식 QSG 다이어그램](https://objects.icecat.biz/objects/mmo_89285766_1614859703_024_23669.pdf) — 랜드스케이프 도면 상단 긴 변에 전면 카메라 |
| Lenovo Tab P11 5G | `Lenovo TB-J607Z` | LONG | RIGHT | [au(KDDI) 공식 LET01 매뉴얼](https://www.au.com/content/dam/au-com/support/service/mobile/guide/manual/let01/pdf/let01_torisetsu_shousai.pdf) p.14 부품 도면 |
| Lenovo Tab P11 Plus | `Lenovo TB-J616F/X` | LONG | RIGHT | [FCC 제출 공식 QSG](https://fcc.report/FCC-ID/O57TBJ616F/5273035.pdf) — 카메라 콜아웃이 랜드스케이프 상단 중앙 |
| Lenovo Tab P11 (2nd Gen) | `TB350FU/XU` | LONG | RIGHT | [FCC 제출 공식 QSG](https://fcc.report/FCC-ID/O57TB350XU/6089397.pdf) |
| Lenovo Tab P11 Pro | `Lenovo TB-J706F/L` | LONG | RIGHT | [FCC 제출 공식 QSG](https://fccid.io/O57TBJ706F/User-Manual/User-manual-4855857) — 듀얼 전면 카메라가 긴 변 |
| Lenovo Tab P11 Pro (2nd Gen) | `TB132FU` | LONG | RIGHT | [XDA 리뷰](https://www.xda-developers.com/lenovo-tab-p11-pro-gen-2-review/) — 랜드스케이프 상단 중앙 |
| Lenovo Tab P12 | `TB370FU` | LONG | RIGHT | [Trusted Reviews](https://www.trustedreviews.com/reviews/lenovo-tab-p12) "front camera, correctly positioned against the long side" |
| Lenovo Tab P12 Pro | `Lenovo TB-Q706F/Z` | LONG | RIGHT | [FCC 제출 공식 QSG](https://fccid.io/O57TBQ706F/User-Manual/Lenovo-TB-Q706F-QSG-updated-5392995) |

### OnePlus

| 제품 | Build.MODEL | edge | DB | 근거 |
|---|---|---|---|---|
| OnePlus Pad | `OPD2203`, `OPD2407` | LONG | RIGHT | [Digital Trends](https://www.digitaltrends.com/mobile/oneplus-pad-great-design-except-for-odd-camera/), [GSMArena 리뷰](https://m.gsmarena.com/oneplus_pad-review-2563p2.php) — 긴 변 배치 명시 |
| OnePlus Pad 2 | `OPD2403` | LONG | RIGHT | [Uswitch](https://www.uswitch.com/mobiles/reviews/oneplus-pad-2/), [Tom's Guide](https://www.tomsguide.com/tablets/android-tablets/oneplus-pad-2-review) |
| OnePlus Pad 3 | `OPD2415` | LONG | RIGHT | [Uswitch](https://www.uswitch.com/mobiles/reviews/oneplus-pad-3/), [GSMArena 리뷰](https://m.gsmarena.com/oneplus_pad_3-review-2854p4.php) |
| OnePlus Pad 4 | `OPD2514` | LONG | RIGHT | [GSMArena 공식 이미지](https://www.gsmarena.com/oneplus_pad_4-pictures-14630.php) |
| OnePlus Pad Go | `OPD2304` | LONG | RIGHT | [Trusted Reviews](https://www.trustedreviews.com/reviews/oneplus-pad-go) "selfie camera sitting above the long edge" |
| OnePlus Pad Go 2 | `OPD2504`, `OPD2505` | LONG | RIGHT | [HotHardware](https://hothardware.com/reviews/oneplus-pad-go-2-review-scaled-back-with-compromises), [BGR](https://www.bgr.com/2056376/oneplus-pad-go-2-review/) |
| OnePlus Pad Lite | `OPD2480`, `OPD2481` | LONG | RIGHT | [Trusted Reviews](https://www.trustedreviews.com/reviews/oneplus-pad-lite), [Uswitch](https://www.uswitch.com/mobiles/reviews/oneplus-pad-lite/) |

### OPPO

| 제품 | Build.MODEL | edge | DB | 근거 |
|---|---|---|---|---|
| OPPO Pad | `OPD2101` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad-pictures-11322.php) — 포트레이트 기준 긴 변 중앙 |
| OPPO Pad 2 | `OPD2201`, `OPD2202` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_2-pictures-12177.php) |
| OPPO Pad 3 | `OPD2405`, `OPD2406` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_3-pictures-13516.php) |
| OPPO Pad 3 Pro | `OPD2401`, `OPD2402` | LONG | RIGHT | [GSMArena](https://www.gsmarena.com/oppo_pad_3_pro-pictures-13085.php), [T3 리뷰](https://www.t3.com/tech/tablets/oppo-pad-3-pro-review) |
| Oppo Pad 4 Pro | `OPD2409` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_4_pro-pictures-13786.php) |
| OPPO Pad 5 | `OPD2506` (+ `OPD2502/3`) | LONG | RIGHT | [GSMArena](https://www.gsmarena.com/oppo_pad_5-pictures-14236.php) |
| Oppo Pad 5 Pro | `OPD2511` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_5_pro-pictures-14621.php) |
| OPPO Pad 6 | `OPD2601` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_6-pictures-14690.php) |
| OPPO Pad Air | `OPD2102` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_air-pictures-11544.php) |
| Oppo Pad Air5 | `OPD2501`, `OPD2510` | LONG | RIGHT | [GSMArena](https://www.gsmarena.com/oppo_pad_air5-14382.php) — 중국판 Air5 = 글로벌 Pad 5 Matte Display |
| OPPO Pad Neo | `OPD2302`, `OPD2303` | LONG | RIGHT | [GadgetGuy 리뷰](https://www.gadgetguy.com.au/oppo-pad-neo-review-tablet/) "Unlike an iPad, the front camera is located in the centre of the long edge" |
| Oppo Pad SE | `OPD2417/9/20` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_se-pictures-13867.php) |
| **Oppo Pad Mini** | `OPD2515` | **SHORT** | **TOP** | [GSMArena 공식 렌더](https://www.gsmarena.com/oppo_pad_mini-pictures-14624.php), [3E Life 리뷰](https://m.3elife.net/Art/test/202604/22/107526_0.html) — 짧은 변 중앙 펀치홀 |

### Honor

| 제품 | Build.MODEL | edge | DB | 근거 |
|---|---|---|---|---|
| HONOR MagicPad2 | `ROD2-W09` | LONG | RIGHT | [Android Central](https://www.androidcentral.com/tablets/honor-magicpad-2-review), [GSMArena 리뷰](https://www.gsmarena.com/honor_magicpad_2-review-2762p2.php) |
| HONOR MagicPad3 | `CGA-W00` | LONG | RIGHT | [Tech Advisor](https://www.techadvisor.com/article/2891191/honor-magicpad-3-review.html), [Android Headlines](https://www.androidheadlines.com/honor-magicpad-3-review) |
| Honor MagicPad3 Pro 13.3 | `YLP-W00` | LONG | RIGHT | [GSMArena 공식 이미지](https://www.gsmarena.com/honor_magicpad_3_pro-pictures-14243.php) |
| HONOR MagicPad4 | `YLE-W09` | LONG | RIGHT | [TechRadar](https://www.techradar.com/tablets/honor-magic-pad-4-review), [Stuff](https://www.stuff.tv/review/honor-magicpad-4-review/) |
| HONOR Pad 8 | `HEY-W09` | LONG | RIGHT | [Android Central](https://www.androidcentral.com/tablets/honor-pad-8-review), [GSMArena 리뷰](https://m.gsmarena.com/honor_pad_8-review-2490.php) |
| HONOR Pad 9 | `HEY2-W09`, `HEY2-N09` | LONG | RIGHT | [GSMArena 리뷰](https://m.gsmarena.com/honor_pad_9-review-2693p5.php) "set in one of the long bezels" |
| HONOR Pad 10 | `HEY3-W00`, `HEY3-N09` | LONG | RIGHT | [Expert Reviews](https://www.expertreviews.co.uk/technology/phones/honor-pad-10-review), [Creative Bloq](https://www.creativebloq.com/tech/phones-tablets/i-tested-honors-latest-budget-tablet-and-it-feels-surprisingly-premium) |
| HONOR Pad 20 | `HEY4-W09`, `HEY4-N09` | LONG | RIGHT | [GSMArena 공식 이미지](https://www.gsmarena.com/honor_pad_20-pictures-14663.php) |
| HONOR Pad 20 Pro | `MLA-W09` | LONG | RIGHT | [Honor 공식 제품 페이지](https://www.honor.com/global/tablets/honor-pad-20-pro/) 렌더 |
| HONOR Pad V9 | `ROL-W00` | LONG | RIGHT | [PhoneArena](https://www.phonearena.com/reviews/honor-pad-v9-review_id7082), [Tech Advisor](https://www.techadvisor.com/article/2777535/honor-pad-v9-review-2.html) |
| **HONOR Pad X7** | `JMS-W09` | **SHORT** | **TOP** | [GSMArena 공식 이미지](https://www.gsmarena.com/honor_pad_x7-pictures-14026.php) — 8.7" 포트레이트 상단 짧은 변, 폰 스타일 |
| HONOR Pad X8 | `AGM3-W09HN`, `AGM3-AL09HN` | LONG | RIGHT | [Creative Bloq 리뷰](https://www.creativebloq.com/reviews/honor-pad-x8) "positioned halfway down the long edge" |
| HONOR Pad X8 Lite | `AGM-W09HN` | LONG | RIGHT | [GSMArena 공식 이미지](https://www.gsmarena.com/honor_pad_x8_lite-pictures-11890.php) |
| HONOR Pad X8a | `NDL-W09/L09/L03` | LONG | RIGHT | [MyNextTablet 리뷰](https://mynexttablet.com/honor-pad-x8a-test/) |
| HONOR Pad X8b | `NDL2-W09/L09/L03` | LONG | RIGHT | [Honor 공식 제품 페이지](https://www.honor.com/ph/tablets/honor-pad-x8b/) 렌더 |
| HONOR Pad X9 | `ELN-W09/L09/L03` | LONG | RIGHT | [GSMArena 리뷰](https://www.gsmarena.com/honor_pad_x9-review-2638.php) — 긴 변 웹캠 스타일 |
| HONOR Pad X9a | `ELN2-W29/L29/L23` | LONG | RIGHT | [TechReviewer](https://en.techreviewer.de/honor-pad-x9a-test/), [NoypiGeeks](https://www.noypigeeks.com/android/honor-pad-x9a-review/) |
| HONOR Pad X9b Max | `YAG-W09`, `YAG-W19` | LONG | RIGHT | [Honor 공식 제품 페이지](https://www.honor.com/global/tablets/honor-pad-x9b-max/) 렌더 |

### Xiaomi

| 제품 | Build.MODEL | edge | DB | 근거 |
|---|---|---|---|---|
| **Xiaomi Pad 5** | `21051182C`, `21051182G` | **SHORT** | **TOP** | [GSMArena 리뷰](https://www.gsmarena.com/xiaomi_pad_5-review-2317p2.php) "If you hold the Pad 5 in portrait mode, you can spot the 8MP front camera above the screen" |
| **Xiaomi Pad 5 Pro (11")** | `M2105K81AC` | **SHORT** | **TOP** | [GSMArena 공식 렌더](https://www.gsmarena.com/xiaomi_pad_5_pro-pictures-11043.php) — 포트레이트 상단 중앙 |
| Xiaomi Pad 5 Pro 12.4 | `22081281AC` | LONG | RIGHT | [Tencent News 리뷰](https://news.qq.com/rain/a/20220815A07Y3Y00) — 12.4형만 긴 변으로 이동 (소스 이름은 "Xiaomi Pad 5 Pro"로 동일하니 주의) |
| **Xiaomi Pad 5 Pro 5G** | `M2105K81C` | **SHORT** | **TOP** | [GSMArena](https://www.gsmarena.com/xiaomi_pad_5_pro-11043.php) — 11" Pad 5 Pro와 동일 바디 |
| Xiaomi Pad 6 | `23043RP34C/G/I` | LONG | RIGHT | [GSMArena 리뷰](https://www.gsmarena.com/xiaomi_pad_6-review-2596p2.php) "on the correct (i.e. long edge)" |
| Xiaomi pad 6 Pro | `23046RP50C` | LONG | RIGHT | [GSMArena 렌더](https://www.gsmarena.com/xiaomi_pad_6_pro-pictures-12238.php), [zh.wikipedia 小米平板6](https://zh.wikipedia.org/zh-hans/%E5%B0%8F%E7%B1%B3%E5%B9%B3%E6%9D%BF6) "由短边中心移至长边中心" |
| Xiaomi Pad 6 Max 14 | `2307BRPDCC` | LONG | RIGHT | [GSMArena 발표 기사](https://www.gsmarena.com/xiaomi_pad_6_max_debuts_with_14_display_and_sd_8_gen_1_smart_band_8_pro_also_unveiled-news-59547.php) "placed in the middle of the long side" |
| Xiaomi Pad 6S Pro 12.4 | `24018RPACG` | LONG | RIGHT | [GSMArena 리뷰](https://www.gsmarena.com/xiaomi_pad_6s_pro_12_4-review-2707p2.php) |
| Xiaomi Pad 7 | `2410CRP4CC/G/I` | LONG | RIGHT | [GSMArena 핸즈온](https://www.gsmarena.com/xiaomi_pad_7_handson-review-2792p2.php), [공식 사진](https://www.gsmarena.com/xiaomi_pad_7-pictures-13475.php) |
| Xiaomi Pad 7 Pro | `24091RPADC/G` | LONG | RIGHT | [Stuff 리뷰](https://www.stuff.tv/review/xiaomi-pad-7-pro-review/) "in the centre of the tablet's longer edge" |
| Xiaomi Pad 7 Ultra | `25032RP42C` | LONG | RIGHT | [NotebookCheck 리뷰](https://www.notebookcheck.net/The-best-Android-tablet-isn-t-from-Samsung-Xiaomi-Pad-7-Ultra-review.1043674.0.html), [GSMArena](https://www.gsmarena.com/xiaomi_pad_7_ultra-13896.php) — 긴 변 노치 |
| Xiaomi Pad 7S Pro 12.5 | `25053RP5CC` | LONG | RIGHT | [GSMArena 공식 이미지](https://www.gsmarena.com/xiaomi_pad_7s_pro_12_5-pictures-13968.php) |
| Xiaomi Pad 8 | `25097RP43C` | LONG | RIGHT | [GSMArena 렌더](https://www.gsmarena.com/xiaomi_pad_8-pictures-14184.php), [ITHome](https://www.ithome.com/0/885/838.htm) "靠近前置摄像头的长边中框" |
| Xiaomi Pad 8 Pro | `25091RP04C` | LONG | RIGHT | [GSMArena 렌더](https://www.gsmarena.com/xiaomi_pad_8_pro-pictures-14183.php), [T3 리뷰](https://www.t3.com/tech/tablets/xiaomi-pad-8-pro-review) |
| **Xiaomi Pad Mini** | `25079RPDCG` | **SHORT** | **TOP** | [Expert Reviews](https://www.expertreviews.co.uk/technology/tablets-ereaders/xiaomi-pad-mini-review) "set into the short bezel ... favour portrait use", [GSMArena 렌더](https://www.gsmarena.com/xiaomi_pad_mini-pictures-14179.php) |

### Redmi / POCO

| 제품 | Build.MODEL | edge | DB | 근거 |
|---|---|---|---|---|
| Redmi Pad | `22081283G` | LONG | RIGHT | [GSMArena 공식 렌더](https://www.gsmarena.com/xiaomi_redmi_pad-pictures-11911.php) |
| Redmi Pad SE | `23073RPBFC/G/L` | LONG | RIGHT | [GSMArena 렌더](https://www.gsmarena.com/xiaomi_redmi_pad_se-pictures-12466.php), [Business Standard 리뷰](https://www.business-standard.com/technology/tech-news/xiaomi-redmi-pad-se-review-budget-tablet-good-for-learning-entertainment-124052000361_1.html) |
| **Redmi Pad SE 4G** | `24076RP19I` | **SHORT** | **TOP** | [GSMArena](https://www.gsmarena.com/xiaomi_redmi_pad_se_8_7-13225.php) "Also known as Redmi Pad SE 4G in India" — 즉 SE 8.7과 동일 기기, [FoneArena](https://www.fonearena.com/blog/430501/redmi-pad-se-4g-price-india-specifications.html) |
| **Redmi Pad SE 8.7** | `24075RP89G` | **SHORT** | **TOP** | [GSMArena 공식 렌더](https://www.gsmarena.com/xiaomi_redmi_pad_se_8_7-pictures-13225.php) — 포트레이트 상단 짧은 변 |
| **Redmi Pad SE 8.7 4G** | `24076RP19G` | **SHORT** | **TOP** | [GSMArena](https://www.gsmarena.com/xiaomi_redmi_pad_se_8_7-13225.php), [MyNextTablet 리뷰](https://mynexttablet.com/xiaomi-redmi-pad-se-8-7-review/) — Wi-Fi/4G 단일 디자인 |
| Redmi Pad Pro | `2405CRPFDC/G/I` | LONG | RIGHT | [GSMArena 리뷰](https://m.gsmarena.com/xiaomi_redmi_pad_pro-review-2718p2.php) "embedded in the top bezel (landscape orientation)" |
| Redmi Pad Pro 5G | `24074RPD2C/G` | LONG | RIGHT | [GSMArena](https://m.gsmarena.com/xiaomi_redmi_pad_pro_5g-ampp-13071.php) — Pad Pro와 동일 섀시 |
| Redmi Pad 2 | `25040RP0AC/AE/AG/AI/AL` | LONG | RIGHT | [Tech Advisor 리뷰](https://www.techadvisor.com/article/2828351/xiaomi-redmi-pad-2-review.html) "placement of the front-facing camera on the longer edge", [GSMArena 렌더](https://www.gsmarena.com/xiaomi_redmi_pad_2-pictures-13908.php) |
| Redmi Pad 2 4G / Wi-Fi + Cellular | `2505DRP06E/G/I` | LONG | RIGHT | [GSMArena](https://www.gsmarena.com/xiaomi_redmi_pad_2-13908.php), [mi.com 4G 스펙](https://www.mi.com/global/product/redmi-pad-2-4g/specs/) — 11" 단일 바디 |
| REDMI Pad 2 Pro (+5G) | `25099RP13C/G/I`, `2509BRP2DG/I` | LONG | RIGHT | [GSMArena 렌더](https://www.gsmarena.com/xiaomi_redmi_pad_2_pro-pictures-14174.php), [리뷰](https://www.gsmarena.com/xiaomi_redmi_pad_2_pro-review-2891.php) |
| REDMI Pad 2 9.7 (+4G) | `2603ARP14G`, `2604ERP4DG` | LONG | RIGHT | [GSMArena 렌더](https://www.gsmarena.com/xiaomi_redmi_pad_2_9_7-pictures-14636.php), [WalasTech 리뷰](https://walastech.com/reviews/redmi-pad-2-9-7-review-philippines/) — 9.7"지만 긴 변 배치 |
| REDMI Pad 2 SE (+4G) | `2603ARP14C`, `2604ERP4DC` | LONG | RIGHT | [GSMArena](https://www.gsmarena.com/xiaomi_redmi_pad_2_9_7-14636.php) "Also known as Xiaomi Redmi Pad 2 SE ... in China only" — Pad 2 9.7과 동일 기기 |
| POCO Pad | `2405CPCFBG` | LONG | RIGHT | [GSMArena 리뷰](https://m.gsmarena.com/poco_pad-review-2721p2.php) "placed half-way along the tablet's longer side" |
| POCO Pad C1 | `2603APC14G` | LONG | RIGHT | [GSMArena](https://www.gsmarena.com/xiaomi_poco_pad_c1-14682.php) — Redmi Pad 2 9.7 리브랜드 |
| POCO Pad M1 | `2509ARPBDG` | LONG | RIGHT | [GSMArena 리뷰](https://www.gsmarena.com/poco_pad_m1-review-2916p2.php), [Stuff](https://www.stuff.tv/review/poco-pad-m1-review/) |

---

## 검증에서 도출된 규칙 변경 (sync_sources.py)

향후 신규 변종이 같은 오류로 유입되지 않도록 `classify_android()`에 반영:

| 패턴 | 결과 | 근거 |
|---|---|---|
| `pad mini` | TOP | Oppo/Xiaomi Pad Mini — 8.x" 세로 우선 |
| `xiaomi pad 5` | TOP | Pad 5 세대는 짧은 변, 긴 변 전환은 Pad 6부터 (기존 `22081281AC` RIGHT 행은 sync가 보존) |
| `redmi pad se 8.7` / `redmi pad se 4g` | TOP | 8.7" SE 라인은 폰 스타일 |
| `honor pad x7` | TOP | 8.7" 폰 스타일 |

경향 요약: **~9인치 미만 소형 태블릿은 세로 우선(짧은 변)으로 회귀하는 사례가 반복됨** (iPad mini, Oppo Pad Mini, Xiaomi Pad Mini, Redmi Pad SE 8.7, Honor Pad X7). 신규 소형 태블릿 추가 시 개별 확인 권장.
