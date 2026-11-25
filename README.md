# mc-server-pack

"한원탁의 놀이터" 서버 리소스팩 저장소. 플러그인이 만든 아이템에만 새 그림을 입힌다.

- 마인크래프트 26.3 (리소스팩 pack format 97.1)
- 네임스페이스 `hanolter`
- 그림은 **CC0 또는 직접 만든 것만** — 파일마다 [`CREDITS.md`](CREDITS.md)에 출처·라이선스를 적는다

## 그림을 입히는 방식

플러그인은 자기가 만든 아이템에 `custom_model_data` 문자열(예: `hanolter:golden_watering_can`)을 붙인다.
리소스팩은 바탕 바닐라 아이템의 아이템 정의에서 그 문자열일 때만 새 모델을 고르고, 아니면 **원래 바닐라 모델(fallback)**을 그대로 쓴다.
그래서 제작대에서 만든 금괭이는 금괭이 그림 그대로이고, 리소스팩 없이 접속해도 빈 그림이 나오지 않는다.

```
pack.mcmeta
assets/
  minecraft/items/<바탕 아이템>.json     ← custom_model_data 로 고르기 + fallback 은 바닐라 모델
  hanolter/models/item/<이름>.json       ← 모델
  hanolter/textures/item/<이름>.png      ← 16×16 그림
CREDITS.md                               ← 그림마다 출처·라이선스
tools/validate.py                        ← 리소스팩 검사
tools/make_textures.py                   ← 직접 만든 도트 그림의 원본 (글자 격자)
tools/vanilla_items/<바탕 아이템>.json   ← 단순 모델이 아닌 바탕의 바닐라 아이템 정의 (fallback 비교용)
```

바닐라 그림·모델 자체는 바꾸지 않는다. `assets/minecraft/` 아래에는 `items/*.json`만 둔다.

## 지금 들어 있는 그림

| 아이템 | `custom_model_data` 값 | 바탕 아이템 |
| --- | --- | --- |
| 황금 물뿌리개 | `hanolter:golden_watering_can` | `golden_hoe` |
| 지폐 | `hanolter:banknote` | `paper` |
| 강화석 | `hanolter:reinforce_stone` | `amethyst_shard` |
| 불씨석 | `hanolter:ember_stone` | `blaze_powder` |
| 녹청 꽃돌 | `hanolter:verdigris_bloom` | `green_dye` |
| 강철 심 | `hanolter:steel_core` | `netherite_scrap` |
| 붉은 맥석 | `hanolter:red_vein` | `nether_wart` |
| 쪽빛 결정 | `hanolter:azure_crystal` | `prismarine_crystals` |
| 사금 덩이 | `hanolter:gold_grain` | `gold_nugget` |
| 맑은 핵 | `hanolter:clear_core` | `ghast_tear` |
| 초록 별조각 | `hanolter:green_shard` | `prismarine_shard` |
| 토기 조각 | `hanolter:relic_pottery_shard` | `brick` |
| 돌 화살촉 | `hanolter:relic_stone_arrowhead` | `flint` |
| 옛 동전 | `hanolter:relic_old_coin` | `gold_nugget` |
| 녹슨 열쇠 | `hanolter:relic_rusty_key` | `iron_nugget` |
| 점토 인장 | `hanolter:relic_clay_seal` | `clay_ball` |
| 화석 뼈 | `hanolter:relic_fossil_bone` | `bone` |
| 조개 장신구 | `hanolter:relic_shell_ornament` | `nautilus_shell` |
| 수정 조각 | `hanolter:relic_crystal_shard` | `amethyst_shard` |
| 전설 유물 — 별의 눈물 | `hanolter:legend_star_tear` | `nether_star` |
| 전설 유물 — 잠든 바다의 진주 | `hanolter:legend_deep_pearl` | `heart_of_the_sea` |
| 전설 유물 — 잊힌 왕의 메아리 | `hanolter:legend_king_echo` | `echo_shard` |
| 향신료 | `hanolter:spice` | `glowstone_dust` |
| 야생 버섯 | `hanolter:wild_mushroom` | `brown_mushroom` |
| 꿀 | `hanolter:honey` | `honey_bottle` |
| 광맥 지도 | `hanolter:vein_map` | `map` |
| 특수 미끼 | `hanolter:special_bait` | `fermented_spider_eye` |
| 레시피 쪽지 | `hanolter:recipe_note` | `paper` |
| 비전 레시피 (일반) | `hanolter:secret_recipe_normal` | `flower_banner_pattern` |
| 비전 레시피 (희귀) | `hanolter:secret_recipe_rare` | `flower_banner_pattern` |
| 비전 레시피 (전설) | `hanolter:secret_recipe_legend` | `flower_banner_pattern` |
| 고대 도면 조각 | `hanolter:blueprint_piece` | `disc_fragment_5` |
| 고대 도면 (일반) | `hanolter:blueprint_normal` | `paper` |
| 고대 도면 (희귀) | `hanolter:blueprint_rare` | `paper` |
| 고대 도면 (전설) | `hanolter:blueprint_legend` | `paper` |
| 보물 지도 조각 | `hanolter:treasure_map_piece` | `globe_banner_pattern` |
| 보물 지도 | `hanolter:treasure_map` | `filled_map` |
| 지폐 1~9탁 (작은 동전) | `hanolter:money_coin_small` | `paper` |
| 지폐 10~99탁 (큰 동전) | `hanolter:money_coin_large` | `paper` |
| 지폐 100~999탁 (깔끔한 동전) | `hanolter:money_coin_fine` | `paper` |
| 지폐 10,000~99,999탁 (수표) | `hanolter:money_check` | `paper` |
| 지폐 100,000탁 이상 (돈 보따리) | `hanolter:money_bag` | `paper` |
| 탐사 나침반 | `hanolter:explorer_compass` (그림 `explorer_compass_00`~`31`, 바늘 방향마다 한 장) | `compass` |

## 그림 추가 방법

1. **그림 넣기** — 16×16 PNG를 `assets/hanolter/textures/item/<이름>.png`에 넣는다. 이름은 영어 소문자·숫자·밑줄.
   - 직접 도트로 그릴 때는 `tools/make_textures.py`의 `ART`에 글자 격자를 추가하고 `python3 tools/make_textures.py`를 실행해도 된다.
2. **모델 만들기** — `assets/hanolter/models/item/<이름>.json`

   ```json
   {
     "parent": "minecraft:item/generated",
     "textures": { "layer0": "hanolter:item/<이름>" }
   }
   ```

   손에 드는 도구 모양이면 `minecraft:item/handheld`.
3. **바탕 아이템에 연결** — `assets/minecraft/items/<바탕 아이템>.json`의 `cases`에 한 줄 추가. 파일이 없으면 아래처럼 새로 만든다 (`fallback`은 꼭 그 아이템의 원래 바닐라 모델).

   ```json
   {
     "model": {
       "type": "minecraft:select",
       "property": "minecraft:custom_model_data",
       "cases": [
         { "when": "hanolter:<이름>", "model": { "type": "minecraft:model", "model": "hanolter:item/<이름>" } }
       ],
       "fallback": { "type": "minecraft:model", "model": "minecraft:item/<바탕 아이템>" }
     }
   }
   ```

   바닐라 아이템 정의가 단순 모델이 아닌 아이템(활·나침반·색이 입혀지는 아이템 등)은 `fallback`에 바닐라 정의 전체를 그대로 넣어야 한다.
   그 바닐라 정의(마인크래프트 26.3)를 `tools/vanilla_items/<바탕 아이템>.json`에 그대로 두면, 검사가 `fallback`이 그 파일과 똑같은지 확인한다 (지금은 `compass`).
   탐사 나침반은 바닐라 나침반과 같은 구조(자석석 추적 여부 → 바늘 각도 32단계)에 그림만 `explorer_compass_00`~`31`로 바꿔 바늘이 그대로 움직인다.
4. **`CREDITS.md`에 적기** — 파일 경로, 출처 URL, 작가, 라이선스(CC0 또는 직접 제작), 수정 내용.
5. **검사** — `python3 tools/validate.py` (PR을 올리면 자동으로도 돈다).
6. 플러그인(`MC-server`) 쪽 YAML의 `model` 키에 `hanolter:<이름>`을 적는다 (별도 PR).

## 릴리스

main에 머지된 뒤 `v*` 태그를 올리면 GitHub Actions가 검사 → zip → GitHub 릴리스까지 한다. 검사가 실패하면 릴리스는 만들어지지 않는다.

```bash
git tag v0.1.0
```

```bash
git push origin v0.1.0
```

릴리스 설명에 **zip 직접 다운로드 주소와 SHA-1**이 적힌다. 운영자는 그 두 값을 `server.properties`의 `resource-pack`·`resource-pack-sha1`에 그대로 복사한다.
리소스팩을 고칠 때마다 새 태그(`v0.1.1` …)를 올리고 두 값을 바꾼다. 이미 올린 태그는 다시 쓰지 않는다 (주소가 같으면 클라이언트가 옛 파일을 계속 쓴다).
