#!/usr/bin/env python3
"""직접 만든 16x16 도트 그림을 PNG로 만든다 (표준 라이브러리만 사용).

그림을 고치려면 아래 ART의 글자 격자를 고치고 `python3 tools/make_textures.py`를 실행한다.
격자의 글자 하나가 픽셀 하나이고, '.'은 투명이다.
"""
import math
import struct
import sys
import zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "hanolter" / "textures" / "item"

# 여러 그림이 같이 쓰는 팔레트·격자 (등급만 다른 그림은 격자 하나에 색만 바꾼다)
PARCH = {"O": "#3a2a14", "P": "#e3cf9a", "Q": "#c2aa72", "D": "#7a6644"}

SCROLL = [
    "................",
    "................",
    "..OOO......OOO..",
    ".OPPPOOOOOOPPPO.",
    ".OPQPPPPPPPPQPO.",
    ".OPPPPPPPPPPPPO.",
    "..OPDDDPPDDDPO..",
    "..OPPPPAAPPPPO..",
    "..OPDDABBADDPO..",
    "..OPPPABBAPPPO..",
    "..OPDDDAADDDPO..",
    ".OPPPPPPPPPPPPO.",
    ".OPQPPPPPPPPQPO.",
    ".OPPPOOOOOOPPPO.",
    "..OOO......OOO..",
    "................",
]

SHEET = [
    "................",
    ".OOOOOOOOOOOOOO.",
    ".OAAAAAAAAAAAAO.",
    ".OABBBBBBBBBBAO.",
    ".OABWWWWBBBWBAO.",
    ".OABWBBWBBWWBAO.",
    ".OABWBBWBBBWBAO.",
    ".OABWWWWBBBWBAO.",
    ".OABBBBBBBBBBAO.",
    ".OABWBWBWWWWBAO.",
    ".OABBBBBBBBBBAO.",
    ".OABWWWBBWWBBAO.",
    ".OABBBBBBBBBBAO.",
    ".OAAAAAAAAAAAAO.",
    ".OOOOOOOOOOOOOO.",
    "................",
]

# 이름: (팔레트, 16줄 격자)
ART = {
    "golden_watering_can": (
        {"O": "#5a3a0a", "D": "#b8860b", "Y": "#f2c12e", "L": "#fff3a0", "W": "#4aa8e8"},
        [
            "................",
            "................",
            ".OO.............",
            "OLYO.....OOOO...",
            "OYDO....O....O..",
            ".OYYO..OOOOOOOO.",
            "..OYYO.OLLYYYDOO",
            "...OYYOOLYYYYDO.",
            "....OYYYYYYYYDOO",
            ".W...OOYYYYYYDO.",
            "......OYYYYYDDO.",
            "W.W...OYYYYDDDO.",
            "......OYDDDDDDO.",
            ".W.....OOOOOOO..",
            "................",
            "................",
        ],
    ),
    "banknote": (
        {"O": "#2f5a36", "G": "#7fbf7a", "L": "#c9ecc0", "D": "#4d8f55", "S": "#f2e6a8", "E": "#b89b3c"},
        [
            "................",
            "................",
            "................",
            "OOOOOOOOOOOOOOOO",
            "OLLLLLLLLLLLLLLO",
            "OLDGGGGEEGGGGDLO",
            "OLGGGGESSEGGGGLO",
            "OLGDGESEESEGDGLO",
            "OLGDGESEESEGDGLO",
            "OLGGGGESSEGGGGLO",
            "OLDGGGGEEGGGGDLO",
            "OGGGGGGGGGGGGGGO",
            "OOOOOOOOOOOOOOOO",
            "................",
            "................",
            "................",
        ],
    ),
    "reinforce_stone": (
        {"O": "#2a2340", "D": "#5b4a9a", "M": "#8a78d6", "L": "#c4b8ff", "W": "#ffffff"},
        [
            "................",
            "......OOOO......",
            ".....OLLMMO.....",
            "....OLWLMMDO....",
            "...OLWWLMMDDO...",
            "..OLLWLMMMDDDO..",
            "..OLLLMMMMDDDO..",
            "..OMMMMMMDDDDO..",
            "..OMMMMMDDDDDO..",
            "..OMMMDDDDDDDO..",
            "...OMDDDDDDDO...",
            "....ODDDDDDO....",
            ".....ODDDDO.....",
            "......OOOO......",
            "................",
            "................",
        ],
    ),
    "ember_stone": (
        {"O": "#1a1210", "D": "#3a2a26", "M": "#5a4640", "R": "#e2521c", "Y": "#ffc233"},
        [
            "................",
            "................",
            "......OOOO......",
            "....OOMMMDOO....",
            "...OMMMRMDDDO...",
            "..OMMMRYRDDDDO..",
            "..OMMDDRDDDRDO..",
            ".OMMDDDDDDRYRDO.",
            ".OMRDDDDDDDRDDO.",
            ".ORYRDDDRDDDDDO.",
            ".ODRDDDRYRDDDDO.",
            "..ODDDDDRDDDDO..",
            "...OODDDDDDOO...",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "verdigris_bloom": (
        {"O": "#123f3a", "G": "#2f9c8a", "L": "#7fe0c8", "C": "#b5652f", "K": "#5e2f12", "W": "#e6fff6"},
        [
            "................",
            "......OOO.......",
            ".....OLLGO......",
            "..OO.OLGGO.OO...",
            ".OLLOOGGGOOLGO..",
            ".OLGGGOCOGGGGO..",
            "..OGGOCWCOGGO...",
            "..OOGGOCOGGOO...",
            ".OLGGOOGOOGGGO..",
            ".OLGGO.OGO.OGGO.",
            "..OOO..OGO..OO..",
            "......KOGOK.....",
            ".....KCCGCCK....",
            "....KCCCCCCCK...",
            ".....KKKKKKK....",
            "................",
        ],
    ),
    "steel_core": (
        {"O": "#1c2026", "D": "#4a525e", "M": "#7d8896", "L": "#b9c4d0", "W": "#f4f8fb", "B": "#2e6fb0"},
        [
            "................",
            "................",
            ".....OOOOOO.....",
            "....OLLLLMMO....",
            "...OLWWLMMMDO...",
            "..OLWLOOOOMDDO..",
            "..OLLOBBBBOMDO..",
            "..OLMOBWBBODDO..",
            "..OMMOBBBBODDO..",
            "..OMMOBBBBODDO..",
            "..OMMMOOOODDDO..",
            "...OMDDDDDDDO...",
            "....ODDDDDDO....",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "red_vein": (
        {"O": "#22191a", "D": "#57494a", "M": "#857576", "L": "#a99a9a", "R": "#d81f2a", "P": "#ff6b6b"},
        [
            "................",
            "................",
            "....OOOOOO......",
            "...OLLMMMROO....",
            "..OLLMMMRPMMO...",
            ".OLMMMRRMMMMDO..",
            ".OMMRRPMMMDDDO..",
            ".OMRPMMMMDDRDO..",
            ".ORMMMMDDDRPDO..",
            ".OMMMDDRRRPDDO..",
            ".OMDDDRPDDDDDO..",
            "..ODDRDDDDDDO...",
            "...OODDDDDOO....",
            ".....OOOOO......",
            "................",
            "................",
        ],
    ),
    "azure_crystal": (
        {"O": "#0f1d4a", "D": "#2443a8", "M": "#3f74e6", "L": "#8fc0ff", "W": "#eaf6ff"},
        [
            "................",
            ".......OO.......",
            "......OLMO......",
            "......OWMO......",
            ".....OLWMDO.....",
            "..O..OLMMDO.....",
            ".OLO.OLMMDO..O..",
            ".OLMOOLMMDO.OLO.",
            ".OLMOOLMMDOOLMO.",
            "OLWMDOLMMDOLWMDO",
            "OLMMDOLMMDOLMMDO",
            "OLMMDOMMDDOLMDDO",
            ".OMDDOMDDDOMDDO.",
            "..OOOOOOOOOOOO..",
            "................",
            "................",
        ],
    ),
    "gold_grain": (
        {"O": "#5a3a0a", "D": "#b8860b", "Y": "#f2c12e", "L": "#fff3a0"},
        [
            "................",
            "................",
            "................",
            "................",
            "......OOO.......",
            ".....OLYYO......",
            ".....OYYDO.OO...",
            "..OO..OOO.OLYO..",
            ".OLYO.OOO.OYDO..",
            ".OYDOOLLYO.OO...",
            "..OOOLYYYDO.OO..",
            ".OOOOYYYDDOOLYO.",
            "OLYYOOYDDOOYYDDO",
            "OYYDDOOOOOOYDDDO",
            ".OOOO......OOOO.",
            "................",
        ],
    ),
    "clear_core": (
        {"O": "#4a6a86", "D": "#9fc4dc", "M": "#cfe8f5", "L": "#eefaff", "W": "#ffffff", "S": "#7fd6ff"},
        [
            "................",
            "...W............",
            "..WSW..OOOO.....",
            "...W.OOLLMMOO...",
            "....OLLWWLMMDO..",
            "...OLLWWLLMMDDO.",
            "...OLWWLLSMMDDO.",
            "..OLLWLLSSSMMDDO",
            "..OLLLLSSWSSMDDO",
            "..OMLLLLSSSMMDDO",
            "...OMMLLLSMMDDO.",
            "...OMMMMMMMDDDO.",
            "....ODMMMMDDDO..",
            ".....OODDDDOO.W.",
            ".......OOOO..WSW",
            "..............W.",
        ],
    ),
    "green_shard": (
        {"O": "#0d3d1c", "D": "#1f8a3d", "M": "#3fcf62", "L": "#a8ffb4", "W": "#f2fff2"},
        [
            "................",
            ".......OO.......",
            "......OLMO......",
            "......OLMO......",
            ".....OLWMDO.....",
            ".OOOOOLWMDOOOO..",
            ".OLLLLWWMMMMDDO.",
            "..OLMMWMMMMDDO..",
            "...OMMMMMMDDO...",
            "....OMMMMDDO....",
            "...OMMMDMMDDO...",
            "...OMMDOODDDO...",
            "..OMMDO..ODDDO..",
            "..OMDO....ODDO..",
            "..OOO......OOO..",
            "................",
        ],
    ),
    # ---- 유물 8종 ----
    "relic_pottery_shard": (
        {"O": "#3b1f14", "D": "#8a4a2e", "M": "#b8683f", "L": "#d98c5f", "W": "#f0d9b0"},
        [
            "................",
            "................",
            ".....OOOO.......",
            "....OLLMMOO.....",
            "...OLMMMMMDO....",
            "..OLMMWMMMMDO...",
            "..OMMWMWMMMMDO..",
            ".OMMMMWMMWMMDO..",
            ".OMMMMMMWMWMDO..",
            ".OMDMMMMMWMDDO..",
            "..ODDMMMMMDDO...",
            "...OODDMDDDO....",
            ".....OODDOO.....",
            ".......OO.......",
            "................",
            "................",
        ],
    ),
    "relic_stone_arrowhead": (
        {"O": "#1e1e22", "D": "#55575e", "M": "#82858d", "L": "#b4b8c0", "B": "#7a5230"},
        [
            "................",
            "...........OOO..",
            ".........OOLLO..",
            "........OLLMMO..",
            ".......OLLMMDO..",
            "......OLLMMDO...",
            ".....OLLMMMDO...",
            "....OLLMMMDO....",
            "...OLMMMMDDO....",
            "...OMMMDDDO.....",
            "....OMDDOO......",
            "...OBOOO........",
            "..OBBO..........",
            "..OBO...........",
            "...O............",
            "................",
        ],
    ),
    "relic_old_coin": (
        {"O": "#3d2a08", "D": "#8f6a1c", "M": "#c49a32", "L": "#e8cf6a", "G": "#5f8f6a"},
        [
            "................",
            "................",
            ".....OOOOOO.....",
            "...OOLLLLMMOO...",
            "..OLLMMMMMGDDO..",
            "..OLMMOOOOMMDO..",
            ".OLMMMO..OMMMDO.",
            ".OLMGMO..OMMMDO.",
            ".OLMMMO..OMMMDO.",
            ".OLMMMO..OMGMDO.",
            "..OMMMOOOOMMDO..",
            "..OMGMMMMMDDDO..",
            "...OODDDDDDOO...",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "relic_rusty_key": (
        {"O": "#2b1a12", "D": "#7a3b1e", "R": "#b5622f", "L": "#d98a4e"},
        [
            "................",
            "................",
            "..........OOOO..",
            ".........OLRRRO.",
            "........OLRO.ORO",
            "........ORO...OO",
            "........ORRO.ORO",
            ".......OLRRRRRO.",
            "......OLRDOOOO..",
            ".....OLRDO......",
            "....OLRDO.......",
            "...OLRDOO.......",
            "..OLRDORO.......",
            "..ORDOORO.......",
            "...OO..O........",
            "................",
        ],
    ),
    "relic_clay_seal": (
        {"O": "#3a2c22", "D": "#8b6f58", "M": "#b89a7e", "L": "#d9c2a6"},
        [
            "................",
            "................",
            ".....OOOOOO.....",
            "...OOLLLLLMOO...",
            "..OLLMMMMMMMDO..",
            "..OLMDDDDDDMDO..",
            ".OLMMDMMMMDMMDO.",
            ".OLMMDMDDMDMMDO.",
            ".OLMMDMDDMDMMDO.",
            ".OLMMDMMMMDMMDO.",
            "..OMMDDDDDDMDO..",
            "..OMMMMMMMMDDO..",
            "...OODDDDDDOO...",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "relic_fossil_bone": (
        {"O": "#24211d", "D": "#5e574d", "M": "#8c8375", "L": "#b0a797", "W": "#e9e2cf"},
        [
            "................",
            "................",
            "....OOOOOOO.....",
            "...OMMMMMMLOO...",
            "..OMMWWWWMMLLO..",
            "..OMWMMMMWMMLO..",
            ".OMMWMWWMMWMMO..",
            ".OMMWMWMWMWMMDO.",
            ".OMMWMWMMMWMMDO.",
            ".OMMMWMWWWMMDDO.",
            "..OMMMWMMMMDDO..",
            "..ODMMMWWWDDDO..",
            "...ODDDDDDDOO...",
            "....OOOOOOO.....",
            "................",
            "................",
        ],
    ),
    "relic_shell_ornament": (
        {"O": "#4a2f3a", "P": "#e8a7b5", "L": "#fbe3e6", "D": "#b56f80"},
        [
            "................",
            ".......OO.......",
            "......O..O......",
            "......O..O......",
            ".......OO.......",
            ".....OOPPOO.....",
            "....OPLPPLPO....",
            "...OPLPLLPLPO...",
            "..OPLPLPPLPLPO..",
            "..OPLPLPPLPLPO..",
            "..OPPLPLLPLPPO..",
            "...OPPLPPLPPO...",
            "....OPPPPPPO....",
            ".....OODDOO.....",
            ".......OO.......",
            "................",
        ],
    ),
    "relic_crystal_shard": (
        {"O": "#0e2f3a", "D": "#1f7f96", "M": "#3fbcd6", "L": "#9be8f5", "W": "#ffffff"},
        [
            "................",
            ".......OO.......",
            "......OWLO......",
            "......OWLO..O...",
            ".....OWLLMO.OO..",
            ".....OWLMMOOLMO.",
            "..O..OWLMMOLMMO.",
            ".OLO.OLLMMOLMDO.",
            ".OLMOOLMMDOLMDO.",
            ".OLMMOLMMDOMDDO.",
            "..OMMOMMDDOMDO..",
            "..OMDDOMDDODDO..",
            "...ODDDODDDDO...",
            "....OOOOOOOO....",
            "................",
            "................",
        ],
    ),
    # ---- 전설 유물 3종 ----
    "legend_star_tear": (
        {"O": "#5a3d00", "G": "#d99a1e", "Y": "#ffd54a", "L": "#fff2a8", "W": "#ffffff"},
        [
            ".......OO.......",
            "......OWWO......",
            "......OWLO......",
            ".....OWLLYO.....",
            ".....OWLYYO.....",
            "....OWLLYYYO....",
            "...OWLLYWYYGO...",
            "..OWLLYWWWYGGO..",
            "..OWLYWWWWWGGO..",
            "..OLLYYWWWYGGO..",
            "..OLYYYYWYGGGO..",
            "..OYYYYYYGGGGO..",
            "...OYYYGGGGGO...",
            "....OOGGGGOO....",
            "......OOOO......",
            "................",
        ],
    ),
    "legend_deep_pearl": (
        {"O": "#050a2a", "B": "#0f1d5c", "D": "#1f3a9c", "M": "#3f6ad6", "L": "#8fb4ff", "W": "#ffffff"},
        [
            "................",
            "................",
            ".....OOOOOO.....",
            "...OOLLLMMMOO...",
            "..OLLWWLMMMDDO..",
            "..OLWWLMMMMDDO..",
            ".OLLWLMMMMDDDDO.",
            ".OLLLMMMMMDDDBO.",
            ".OLMMMMMMDDDBBO.",
            ".OMMMMMMDDDDBBO.",
            "..OMMMDDDDDBBO..",
            "..ODDDDDDBBBBO..",
            "...OODDBBBBOO...",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "legend_king_echo": (
        {"O": "#02080d", "J": "#0a2b33", "K": "#12414d", "L": "#2b8a99", "T": "#3fe0d0", "W": "#e8fffb"},
        [
            "................",
            "................",
            "..O....OO....O..",
            ".OTO..OTTO..OTO.",
            ".OTO..OTTO..OTO.",
            ".OKKO.OKKO.OKKO.",
            ".OKKKOKKKKOKKKO.",
            ".OKKKKKKKKKKKKO.",
            ".OKLKKKTTKKKLKO.",
            ".OKKKKTWWTKKKKO.",
            ".OKKKKKTTKKKKKO.",
            ".OJJJJJJJJJJJJO.",
            ".OJTJJTJJTJJTJO.",
            "..OOOOOOOOOOOO..",
            "................",
            "................",
        ],
    ),
    # ---- 채집 재료 3종 ----
    "spice": (
        {"O": "#3a1206", "D": "#9c3412", "R": "#d9571e", "Y": "#f6b03a", "G": "#5f9e3a", "L": "#9ed36a"},
        [
            "................",
            "................",
            "................",
            ".......OO.......",
            "......OGGO......",
            ".....OGGLO......",
            "......OOO.......",
            ".....ORRYO......",
            "....ORYRRRO.....",
            "...ORRRRYRRO....",
            "..ORRYRRRRRDO...",
            ".ORRRRRYRRDDDO..",
            ".ODRRRRRRDDDDO..",
            "..OODDDDDDDOO...",
            "....OOOOOOO.....",
            "................",
        ],
    ),
    "wild_mushroom": (
        {"O": "#2e1a10", "C": "#c9462a", "D": "#8f2a18", "W": "#f3e2b8", "S": "#efe6d0", "T": "#c9bba0"},
        [
            "................",
            "................",
            ".....OOOOOO.....",
            "...OOCCWCCCOO...",
            "..OCCCCCCWWCCO..",
            ".OCWWCCCCWWCCDO.",
            ".OCWWCCCCCCCDDO.",
            ".OCCCCCWCCCDDDO.",
            "..OOOOOSSOOOOO..",
            "......OSSTO.....",
            "......OSSTO.....",
            ".....OSSSTO.....",
            ".....OSSTTO.....",
            ".....OSSTTO.....",
            "......OOOO......",
            "................",
        ],
    ),
    "honey": (
        {"O": "#5a3200", "D": "#c9820e", "Y": "#f5b921", "H": "#ffe27a"},
        [
            "................",
            "................",
            "...OOOO..OOOO...",
            "..OYYYYOOYYYYO..",
            ".OYHHHYYYHHHYYO.",
            ".OYHHHYYYHHHYDO.",
            ".OYYYYOOYYYYDDO.",
            "..OYYOYYOYYDDO..",
            "..OYOYHHYOYDDO..",
            "..OYOYHHYOYDO...",
            "...OYOYYOYDDO...",
            "...OYYOOYYDO....",
            "....OYYYYDOO....",
            ".....OOYDO......",
            ".......OYO......",
            "........O.......",
        ],
    ),
    # ---- 소모품 ----
    "vein_map": (
        {"O": "#24262b", "P": "#c3c6cd", "Q": "#8d9099", "D": "#5c5f68", "G": "#3fae5a", "B": "#3f7fd6",
         "R": "#d63f3f", "C": "#5fd9e0", "Y": "#e8c53f"},
        [
            "................",
            ".OOOOOOOOOOOOOO.",
            ".OPPPPPPPPPPPPO.",
            ".OPGGPPPPPPBBPO.",
            ".OPGGGPPPPBBPPO.",
            ".OPPGPPDDPPPPPO.",
            ".OPPPPDPPDPPPPO.",
            ".OPPPDPPPPDPRPO.",
            ".OPDDPPPPPPRRPO.",
            ".OPPPPPCCPPPRPO.",
            ".OPPPPCCCPPPPPO.",
            ".OPYYPPCPPPPPPO.",
            ".OPYPPPPPPPPPPO.",
            ".OQQQQQQQQQQQQO.",
            ".OOOOOOOOOOOOOO.",
            "................",
        ],
    ),
    "special_bait": (
        {"O": "#1c1420", "S": "#c9ced6", "R": "#e04a5a", "W": "#ffffff", "P": "#f08ac0", "B": "#2a2a2a",
         "Y": "#ffd94a"},
        [
            "................",
            "..........OO....",
            ".........OSSO...",
            "........OSO.....",
            "........OSO.....",
            ".......OOSOO....",
            "......ORRRRRO...",
            ".....ORRWWRRRO..",
            ".....ORWBWRRRO..",
            ".....ORRWWRRYO..",
            "....OPORRRRYYO..",
            "...OPPPORRYYO...",
            "..OPPOPPOOOO....",
            "..OPO.OPPO......",
            "...O...OO.......",
            "................",
        ],
    ),
    "recipe_note": (
        {"O": "#4a3a22", "W": "#f7efd8", "D": "#9a8660", "R": "#d9571e", "S": "#d8c9a0"},
        [
            "................",
            "..OOOOOOOOOOOO..",
            "..OWWWWWWWWWWO..",
            "..OWRRWWWWWWWO..",
            "..OWRRWDDDDDWO..",
            "..OWWWWWWWWWWO..",
            "..OWDDDDDDDDWO..",
            "..OWWWWWWWWWWO..",
            "..OWDDDDDDWWWO..",
            "..OWWWWWWWWWWO..",
            "..OWDDDDDDDDWO..",
            "..OWWWWWWWWWOO..",
            "..OWDDDDWWWOSO..",
            "..OWWWWWWWOSO...",
            "..OOOOOOOOOO....",
            "................",
        ],
    ),
    "secret_recipe_normal": ({**PARCH, "A": "#6e6e6e", "B": "#b0b0b0"}, SCROLL),
    "secret_recipe_rare": ({**PARCH, "O": "#14244a", "A": "#1f4fb0", "B": "#6faaff"}, SCROLL),
    "secret_recipe_legend": ({**PARCH, "O": "#5a2a00", "P": "#f7e3a0", "A": "#c8302a", "B": "#ffd94a"}, SCROLL),
    "blueprint_piece": (
        {"O": "#0d1f4a", "B": "#2f5fc4", "W": "#dfeaff"},
        [
            "................",
            "................",
            "...OOOOOO.......",
            "..OBBBBBBOO.....",
            "..OBWWWBBBBO....",
            "..OBWBBBWBBBO...",
            "...OBWBBWBBBO...",
            "...OBBWWBBWBO...",
            "..OBBBBBBWWBO...",
            "..OBWWWWBBBO....",
            "...OBBBBBBO.....",
            "....OBBWBBO.....",
            ".....OBBBO......",
            "......OOO.......",
            "................",
            "................",
        ],
    ),
    "blueprint_normal": ({"O": "#0d1f4a", "A": "#2f5fc4", "B": "#2f5fc4", "W": "#dfeaff"}, SHEET),
    "blueprint_rare": ({"O": "#0d1f4a", "A": "#7fe3ff", "B": "#1f4a9c", "W": "#dfeaff"}, SHEET),
    "blueprint_legend": ({"O": "#3a2600", "A": "#ffd94a", "B": "#4a2f9c", "W": "#fff6d0"}, SHEET),
    "treasure_map_piece": (
        {**PARCH, "R": "#c8302a"},
        [
            "................",
            "................",
            "..OOOOOOOO......",
            "..OPPPPPPPOO....",
            "..OPDPPPPPPPO...",
            "..OPPDPPRPRPO...",
            "...OPPDPPRPPO...",
            "...OPPPPRPRPO...",
            "..OPPDDPPPPPO...",
            "..OPPPPPPPPPO...",
            "...OPPPPDPPO....",
            "....OPQQPPO.....",
            ".....OQQOO......",
            "......OO........",
            "................",
            "................",
        ],
    ),
    "treasure_map": (
        {**PARCH, "R": "#c8302a", "G": "#5f9e3a", "B": "#4a8fd6"},
        [
            "................",
            ".OOOOOOOOOOOOOO.",
            ".OQPPPPPPPPPPQO.",
            ".OPPGGPPPPPPPPO.",
            ".OPGGGPPPDDPPPO.",
            ".OPPGPPPDPPDPPO.",
            ".OPPPPPDPPPPDPO.",
            ".OPDDPDPPPRPRPO.",
            ".OPPPDPPPPPRPPO.",
            ".OPPPPPPBPRPRPO.",
            ".OPPBBPBBPPPPPO.",
            ".OPBBBBBPPPPPPO.",
            ".OQPPPPPPPPPPQO.",
            ".OOOOOOOOOOOOOO.",
            "................",
            "................",
        ],
    ),
    # ---- 지폐 금액 구간 (banknote 는 위에 이미 있다) ----
    "money_coin_small": (
        {"O": "#3a1a0a", "D": "#8a4a22", "M": "#c4733a", "L": "#eaa76a"},
        [
            "................",
            "................",
            "................",
            "................",
            ".....OOOOOO.....",
            "....OLLLMMMO....",
            "...OLLMMMMMDO...",
            "...OLMMDDMMDO...",
            "...OLMDMMDMDO...",
            "...OMMDMMDMDO...",
            "...OMMMDDMDDO...",
            "....OMMDDDDO....",
            ".....OOOOOO.....",
            "................",
            "................",
            "................",
        ],
    ),
    "money_coin_large": (
        {"O": "#23262e", "D": "#6f7684", "M": "#a9b0bd", "L": "#e3e8f0"},
        [
            "................",
            "....OOOOOOOO....",
            "..OOLLLLLMMMOO..",
            ".OLLLMMMMMMMDDO.",
            ".OLLMMDDDDMMMDO.",
            "OLLMMDMMMMDMMDDO",
            "OLMMDMMDDMMDMMDO",
            "OLMMDMDMMDMDMMDO",
            "OLMMDMDMMDMDMMDO",
            "OLMMDMMDDMMDMMDO",
            "OMMMMDMMMMDMMDDO",
            ".OMMMMDDDDMMDDO.",
            ".OMDMMMMMMMDDDO.",
            "..OODDDDDDDDOO..",
            "....OOOOOOOO....",
            "................",
        ],
    ),
    "money_coin_fine": (
        {"O": "#5a3d00", "D": "#c98f14", "M": "#f5c530", "L": "#ffe98a", "W": "#ffffff", "S": "#b87a0a"},
        [
            ".............W..",
            "....OOOOOOO.WWW.",
            "..OOLLLLMMMOOW..",
            ".OLLWWMMMMMMDO..",
            ".OLWWMMSMMMMDDO.",
            "OLLWMMMSMMMMMDO.",
            "OLMMSSSSSSSMMDDO",
            "OLMMMSSSSSMMMDDO",
            "OLMMMMSSSMMMMDDO",
            "OLMMMSSMSSMMMDDO",
            ".OMMMSMMMSMMDDO.",
            ".OMMMMMMMMMDDDO.",
            "..OODDDDDDDDOO..",
            "....OOOOOOOO....",
            "................",
            "................",
        ],
    ),
    "money_check": (
        {"O": "#1f3a5a", "W": "#f4f8ff", "B": "#2f5fc4", "D": "#9aa7b8", "R": "#d63f3f", "S": "#1f1f1f",
         "C": "#b9d4f5"},
        [
            "................",
            "................",
            "................",
            "OOOOOOOOOOOOOOOO",
            "OWWWWWWWWWWWWWWO",
            "OWBBBBBWWWWRRWWO",
            "OWWWWWWWWWRWWRWO",
            "OWDDDDDDDWRWWRWO",
            "OWWWWWWWWWWRRWWO",
            "OWDDDDWWWWWWWWWO",
            "OWWWWWWSSSSSSSWO",
            "OCCCCCCCCCCCCCCO",
            "OOOOOOOOOOOOOOOO",
            "................",
            "................",
            "................",
        ],
    ),
    "money_bag": (
        {"O": "#2e1c0c", "D": "#7a5226", "M": "#a8763a", "L": "#cf9d5c", "R": "#c8302a", "Y": "#ffd94a"},
        [
            "................",
            ".....OO..OO.....",
            "....OMMOOMMO....",
            ".....OMMMMO.....",
            "......ORRO......",
            ".....OMMMMO.....",
            "....OLMMMMMO....",
            "...OLMMYYMMDO...",
            "..OLMMYMMYMMDO..",
            "..OLMMYMMMMMDO..",
            "..OLMMYMMYMDDO..",
            "..OMMMMYYMMDDO..",
            "..OMMMMMMMDDDO..",
            "...OMDDDDDDDO...",
            "....OOOOOOOO....",
            "................",
        ],
    ),
}

# ---- 요리·대장장이·공통 아이템 (이슈 MC-server#221) ----
# 여러 그림이 같이 쓰는 격자: 색만 바꾸거나(도시락·특별 음식), 표지 책 바탕에 무늬를 찍는다(stamp).


def faded(palette, amount=0.55):
    """비상 음식용: 같은 그림의 흐린 판 — 색을 회색 쪽으로 섞는다."""
    out = {}
    for key, color in palette.items():
        r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
        gray = (r * 3 + g * 6 + b) // 10
        mix = [round(c + (gray + 40 - c) * amount) for c in (r, g, b)]
        out[key] = "#" + "".join(f"{max(0, min(255, c)):02x}" for c in mix)
    return out


def stamp(base, marks):
    """바탕 격자에 (x, y, 줄 목록) 무늬를 찍는다. 무늬의 '.' 은 바탕을 그대로 둔다."""
    rows = [list(r) for r in base]
    for x, y, lines in marks:
        for dy, line in enumerate(lines):
            for dx, ch in enumerate(line):
                if ch != ".":
                    rows[y + dy][x + dx] = ch
    return ["".join(r) for r in rows]


LUNCHBOX = [
    "................",
    "................",
    ".OOOOOOOOOOOOOO.",
    ".OBBBBBBBBBBBBO.",
    ".OBRRRRRBAAAABO.",
    ".OBRRGRRBAACABO.",
    ".OBRRRRRBACAABO.",
    ".OBRGRRRBAAAABO.",
    ".OBBBBBBBBBBBBO.",
    ".OBCCCCBGGGGGBO.",
    ".OBCACCBGAGGGBO.",
    ".OBCCCCBGGGAGBO.",
    ".OBBBBBBBBBBBBO.",
    ".ObbbbbbbbbbbbO.",
    ".OOOOOOOOOOOOOO.",
    "................",
]
HARVEST_BOX = {"O": "#3a2412", "B": "#b5834a", "b": "#8a5f30", "R": "#f4f0e0", "A": "#f08a2a",
               "C": "#e6c35a", "G": "#5fae3a"}

FISH_SOUP_PALETTE = {"O": "#2a1e16", "B": "#5a4636", "D": "#3e2f24", "W": "#8a705a", "S": "#efe6cf",
                     "G": "#58b04a", "R": "#d8402c", "F": "#7aa6c8", "H": "#e8eef2"}
FISH_SOUP = [
    "......H...H.....",
    ".....H...H......",
    "......H...H.....",
    "..........FF....",
    "..OOOOOOOFFOOO..",
    ".OWWWWWWFFWWWWO.",
    ".OWSSGSSFSSRSWO.",
    ".OWSRSSSSSGSSWO.",
    "..OWSSGSSRSSWO..",
    "..OBWWWWWWWWBO..",
    "...OBBBBBBBBO...",
    "...OBDBBBBDBO...",
    "....OBBBBBBO....",
    ".....OOOOOO.....",
    "................",
    "................",
]

RICEBALL_PALETTE = {"O": "#3a3428", "W": "#f7f4ea", "S": "#d6d0bf", "N": "#1f2a24", "K": "#2b2b2b"}
RICEBALL = [
    "................",
    "................",
    ".......OO.......",
    "......OWWO......",
    ".....OWWWWO.....",
    ".....OWWWWO.....",
    "....OWWWKWWO....",
    "....OWWWWWWO....",
    "...OWWKWWWWWO...",
    "...OWWNNNNWWO...",
    "..OWWWNNNNWWWO..",
    "..OWWWNNNNWWSO..",
    "..OSWWNNNNWSSO..",
    "...OOOOOOOOOO...",
    "................",
    "................",
]

# 특별 음식: 종류(농부·어부·광부·탐험가)마다 덮개 색만 다르다. 등급은 아이템 이름 색으로 구분한다.
SPECIAL_DISH = [
    "................",
    ".......YY.......",
    "......OYYO......",
    "....OOOOOOOO....",
    "...OCCCCCCCCO...",
    "..OCCLCCCCCCCO..",
    "..OCLCCCSCCCCO..",
    ".OCCLCCSSSCCCCO.",
    ".OCCCCCCSCCCCCO.",
    ".OCCCCCCCCCCCCO.",
    "OOOOOOOOOOOOOOOO",
    "OYYYYYYYYYYYYYYO",
    ".OYYDDDDDDDDYYO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
]


def special_dish(cover, light):
    return ({"O": "#2a1e0a", "Y": "#f2c12e", "D": "#b8860b", "S": "#ffffff", "C": cover, "L": light},
            SPECIAL_DISH)


# 표지 책 바탕. 표지 한가운데(5,4)에 5x5 무늬를 찍는다.
BOOK = [
    "................",
    "..OOOOOOOOOOO...",
    ".OCCCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCLCCCCCCCCPO..",
    ".OCDDDDDDDDDPO..",
    ".OCCCCCCCCCCPO..",
    ".OPPPPPPPPPPPO..",
    "..OOOOOOOOOOO...",
    "................",
    "................",
]
MARK_PICKAXE = ["MMMM.", "...MM", "..S.M", ".S..M", "S...."]
MARK_HOOK = ["...S.", "...S.", "M..S.", "M..S.", ".MM.."]
MARK_CROSS = ["..M..", "..M..", "MMMMM", "..M..", "..M.."]
MARK_CROWN = ["M.M.M", "M.M.M", "MMMMM", "MMMMM", "....."]
# 낡은 책: 바랜 색 + 얼룩(T) + 찢어진 귀퉁이. 대장장이 책: 선명한 색 + 금 모서리 장식(G).
WORN_SPOTS = [(9, 3, ["T"]), (4, 9, ["TT"]), (10, 8, ["T"]), (11, 1, ["..", "T."]), (12, 2, ["."])]
SMITH_STUDS = [(2, 2, ["G"]), (11, 2, ["G"]), (2, 11, ["G"]), (11, 11, ["G"])]
WORN_BOOK = {"O": "#2e2418", "C": "#8a7458", "L": "#a08a6c", "D": "#5e4e3a", "P": "#cfc3a0",
             "M": "#4a3e2e", "S": "#4a3e2e", "T": "#6a583f"}


def smith_book(cover, light, dark):
    return {"O": "#10162e", "C": cover, "L": light, "D": dark, "P": "#f2ead2", "M": "#ffd94a",
            "S": "#c9a36a", "G": "#ffd94a"}


ART.update({
    # ---- 요리 8종 ----
    "meal_harvest_box": (HARVEST_BOX, LUNCHBOX),
    "meal_fish_soup": (FISH_SOUP_PALETTE, FISH_SOUP),
    "meal_miner_rice": (RICEBALL_PALETTE, RICEBALL),
    "meal_pumpkin_stew": (
        {"O": "#3a2a1a", "B": "#c9c2b5", "W": "#f2ede2", "S": "#e58a1f", "P": "#ffb347", "C": "#b8601a",
         "G": "#6fae3c", "L": "#a8763a"},
        [
            "................",
            "............OO..",
            "...........OLO..",
            "..........OLO...",
            "..OOOOOOOOLOOO..",
            ".OWWWWWWWLWWWWO.",
            ".OWSSPPSSSSCSWO.",
            ".OWSPPSSGSSSSWO.",
            "..OWSSSCSSPSWO..",
            "..OBWWWWWWWWBO..",
            "...OBBBBBBBBO...",
            "...OBBBBBBBBO...",
            "....OBBBBBBO....",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "meal_sea_bream_feast": (
        {"O": "#3a2a22", "R": "#e0503a", "P": "#f08a70", "D": "#a8301f", "E": "#1a1a1a", "W": "#f2f2f2",
         "L": "#d6e06a", "Y": "#fff27a"},
        [
            "................",
            "................",
            "................",
            "....OOOOO.......",
            "...ORRRRROO..O..",
            "..ORPRRRRRROORO.",
            ".OREPRRDRRRRRRO.",
            ".ORRPRRRRDRRRO..",
            "..ORRRRDRRRORO..",
            "...OOORRRROO.O..",
            ".OOOOOOOOOOOOOO.",
            "OWWWWWWLLWWWWWWO",
            ".OWWWWLYYLWWWWO.",
            "..OOOOOOOOOOOO..",
            "................",
            "................",
        ],
    ),
    "meal_explorer_lunchbox": (
        {"O": "#16261c", "B": "#4f7a5a", "b": "#365a40", "R": "#d9b98a", "A": "#9a6a3a", "C": "#d6452a",
         "G": "#a8c04a"},
        LUNCHBOX,
    ),
    "meal_honey_pork_stew": (
        {"O": "#141418", "K": "#3a3a40", "D": "#25252a", "M": "#9a4a2a", "Y": "#f5b921", "G": "#6fae3c",
         "H": "#e8eef2"},
        [
            "....H....H......",
            ".....H....H.....",
            "....H....H......",
            "................",
            "..OOOOOOOOOOOO..",
            ".OKMMYMMMYMMGKO.",
            "OOKMYYMMYYMMMKOO",
            "OKKKKKKKKKKKKKKO",
            ".OKKKKKKKKKKKKO.",
            ".OKDKKKKKKKKDKO.",
            "..OKKKKKKKKKKO..",
            "...OOOOOOOOOO...",
            "................",
            "................",
            "................",
            "................",
        ],
    ),
    "meal_spice_grilled_fish": (
        {"O": "#3a2412", "B": "#c9772e", "S": "#d8341f", "T": "#c9a36a", "E": "#1a1a1a"},
        [
            "................",
            ".............OO.",
            "............OTO.",
            "..........OOTO..",
            "........OOBBO...",
            "......OOBSBBO...",
            ".....OBBBBSBO...",
            "....OBSBBBBO....",
            "...OBBBBSBO.....",
            "..OEBBSBBO......",
            "..OBBBBOO.......",
            ".OTOBOO.........",
            "OTO.OO..........",
            "OO..............",
            "................",
            "................",
        ],
    ),
    # ---- 특별 음식 4종 (종류별 1장) ----
    "meal_special_farmer": special_dish("#5fae3a", "#a8e07a"),
    "meal_special_fisher": special_dish("#3f8fd6", "#9fd0ff"),
    "meal_special_miner": special_dish("#7a7f92", "#c5c9d6"),
    "meal_special_explorer": special_dish("#c9772e", "#f0b070"),
    # ---- 비상 음식 3종 (같은 요리 그림의 흐린 판) ----
    "meal_emergency_harvest_box": (faded(HARVEST_BOX), LUNCHBOX),
    "meal_emergency_fish_soup": (faded(FISH_SOUP_PALETTE), FISH_SOUP),
    "meal_emergency_miner_rice": (faded(RICEBALL_PALETTE), RICEBALL),
    # ---- 정체불명의 죽·요리사 도구 ----
    "mystery_porridge": (
        {"O": "#2a1e16", "B": "#6a5240", "W": "#9a7e64", "S": "#7a6a8a", "U": "#a892c0", "E": "#3a2e44",
         "G": "#9ad06a"},
        [
            "................",
            "................",
            ".....G..........",
            "..........G.....",
            "..OOOOOOOOOOOO..",
            ".OWWWWWWWWWWWWO.",
            ".OWSSSUSSSSSSWO.",
            ".OWSUSSSSEESSWO.",
            "..OWSSSUSSSSWO..",
            "..OBWWWWWWWWBO..",
            "...OBBBBBBBBO...",
            "...OBBBBBBBBO...",
            "....OBBBBBBO....",
            ".....OOOOOO.....",
            "................",
            "................",
        ],
    ),
    "emergency_bandage": (
        {"O": "#4a4438", "W": "#f6f3ea", "G": "#cfc9b8", "S": "#e2dccb", "R": "#d8342c"},
        [
            "................",
            "................",
            "....OOOOOOOO....",
            "...OWWWWWWWWO...",
            "..OWWWWWWWWWWO..",
            "..OWSSWRRWWWWO..",
            "..OWSOSRRWWWWO..",
            "..OWSSRRRRRRWO..",
            "..OWWWRRRRRRWO..",
            "..OWWWWWRRWWWO..",
            "..OGWWWWRRWWWOOO",
            "...OGGGGGGGGOWWO",
            "....OOOOOOOOOGGO",
            ".............OO.",
            "................",
            "................",
        ],
    ),
    "aging_jar": (
        {"O": "#24140a", "B": "#7a4a2a", "L": "#b07a4a", "D": "#4e2e18"},
        [
            "................",
            ".....OOOOOO.....",
            "....OLLLLLLO....",
            "...OOOOOOOOOO...",
            "....ODDDDDDO....",
            "...OBBBBBBBBO...",
            "..OBLBBBBBBBBO..",
            ".OBLLBBBBBBBBBO.",
            ".OBLBBBBBBBBBDO.",
            ".OBLBBBBBBBBBDO.",
            ".OBBBBBBBBBBDDO.",
            ".OBBBBBBBBBBDDO.",
            "..OBBBBBBBBDDO..",
            "...OBBBBBBDDO...",
            "....OOOOOOOO....",
            "................",
        ],
    ),
    # ---- 인챈트 북 5종 ----
    "worn_enchant_book_tool": (WORN_BOOK, stamp(BOOK, [(5, 4, MARK_PICKAXE)] + WORN_SPOTS)),
    "worn_enchant_book_rod": (WORN_BOOK, stamp(BOOK, [(5, 4, MARK_HOOK)] + WORN_SPOTS)),
    "smith_enchant_book_tool": (smith_book("#2f4f9a", "#5a7fd0", "#1e3470"),
                                stamp(BOOK, [(5, 4, MARK_PICKAXE)] + SMITH_STUDS)),
    "smith_enchant_book_rod": (smith_book("#1f7a78", "#4fb8b0", "#125250"),
                               stamp(BOOK, [(5, 4, MARK_HOOK)] + SMITH_STUDS)),
    "mending_book": (smith_book("#2f8a4a", "#6fc88a", "#1c5a30"),
                     stamp(BOOK, [(5, 4, MARK_CROSS)] + SMITH_STUDS)),
    # ---- 공통 ----
    "chest_lock": (
        {"O": "#2a2010", "S": "#b8bec8", "Y": "#e8b830", "L": "#fff0a0", "D": "#a87a18"},
        [
            "................",
            "................",
            ".....OOOOOO.....",
            "....OSSSSSSO....",
            "...OSSOOOOSSO...",
            "...OSO....OSO...",
            "...OSO....OSO...",
            "..OOOOOOOOOOOO..",
            "..OYYYYYYYYYYO..",
            "..OYLYYOOYYYDO..",
            "..OYLYYOOYYYDO..",
            "..OYYYYYOYYYDO..",
            "..OYYYYYOYYDDO..",
            "..OYDDDDDDDDDO..",
            "..OOOOOOOOOOOO..",
            "................",
        ],
    ),
    "title_book": (
        {"O": "#1e102e", "C": "#6a3fa8", "L": "#9a70d8", "D": "#45247a", "P": "#f2ead2", "M": "#ffd94a",
         "R": "#d8342c"},
        stamp(BOOK, [(5, 4, MARK_CROWN), (9, 12, ["R", "R", "R"])]),
    ),
})


# 탐사 나침반: 바늘 방향 32장. 바닐라 나침반과 같은 순서다 (00 = 아래, 08 = 왼쪽, 16 = 위, 24 = 오른쪽).
COMPASS_PALETTE = {"O": "#1a0f06", "B": "#c08a44", "C": "#7a4e22", "F": "#123c44", "T": "#2b8a99",
                   "R": "#ff4a4a", "W": "#e8fffb"}
COMPASS_BASE = [
    "................",
    "................",
    ".....OOOOOO.....",
    "...OOBBBBBBOO...",
    "..OBBFFTTFFBBO..",
    "..OBFFFFFFFFBO..",
    ".OBFFFFFFFFFFBO.",
    ".OBTFFFFFFFFTBO.",
    ".OBTFFFFFFFFTBO.",
    ".OBFFFFFFFFFFBO.",
    "..OBFFFFFFFFBO..",
    "..OCBFFTTFFBCO..",
    "...OOCCCCCCOO...",
    ".....OOOOOO.....",
    "................",
    "................",
]


def compass_frames():
    """탐사 나침반 32장: 바탕 격자 위에 빨간 바늘(가리키는 쪽)과 흰 꼬리(반대쪽)를 각도마다 그린다."""
    frames = {}
    for k in range(32):
        angle = math.radians(k * 360 / 32)  # 아래(00)에서 시계 방향
        dx, dy = -math.sin(angle), math.cos(angle)
        rows = [list(r) for r in COMPASS_BASE]
        for ch, sign, length in (("W", -1, 2.5), ("R", 1, 3.5)):
            t = 0.5
            while t <= length:
                x, y = int(8 + sign * dx * t), int(8 + sign * dy * t)
                if 8 + sign * dx * t < 0 or 8 + sign * dy * t < 0:
                    x, y = -1, -1
                if 0 <= x < 16 and 0 <= y < 16 and rows[y][x] in "FTWR":
                    rows[y][x] = ch
                t += 0.25
        frames[f"explorer_compass_{k:02d}"] = (COMPASS_PALETTE, ["".join(r) for r in rows])
    return frames



def png(rows, palette):
    raw = bytearray()
    for row in rows:
        raw.append(0)
        for ch in row:
            if ch == ".":
                raw += b"\x00\x00\x00\x00"
            else:
                c = palette[ch].lstrip("#")
                raw += bytes.fromhex(c) + b"\xff"

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (palette, rows) in {**ART, **compass_frames()}.items():
        if len(rows) != 16 or any(len(r) != 16 for r in rows):
            sys.exit(f"{name}: 격자는 16줄 x 16글자여야 한다")
        (OUT / f"{name}.png").write_bytes(png(rows, palette))
        print(f"만듦: {name}.png")


if __name__ == "__main__":
    main()
