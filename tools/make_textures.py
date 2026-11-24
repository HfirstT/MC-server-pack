#!/usr/bin/env python3
"""직접 만든 16x16 도트 그림을 PNG로 만든다 (표준 라이브러리만 사용).

그림을 고치려면 아래 ART의 글자 격자를 고치고 `python3 tools/make_textures.py`를 실행한다.
격자의 글자 하나가 픽셀 하나이고, '.'은 투명이다.
"""
import struct
import sys
import zlib
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "hanolter" / "textures" / "item"

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
}


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
    for name, (palette, rows) in ART.items():
        if len(rows) != 16 or any(len(r) != 16 for r in rows):
            sys.exit(f"{name}: 격자는 16줄 x 16글자여야 한다")
        (OUT / f"{name}.png").write_bytes(png(rows, palette))
        print(f"만듦: {name}.png")


if __name__ == "__main__":
    main()
