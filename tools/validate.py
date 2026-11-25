#!/usr/bin/env python3
"""리소스팩 파일 검사 (표준 라이브러리만 사용). 문제가 있으면 목록을 찍고 종료 코드 1.

검사하는 것
- 모든 .json / pack.mcmeta 의 JSON 문법
- assets/minecraft 아래에는 아이템 정의(items/*.json)만 있다 (바닐라 그림·모델 자체를 바꾸지 않는다)
- 바닐라 아이템 정의: custom_model_data 문자열로 고르고, fallback 은 그 아이템의 원래 바닐라 모델
  (단순 모델이 아닌 바탕은 tools/vanilla_items/<이름>.json 의 바닐라 정의와 똑같아야 한다)
- 아이템 정의가 참조한 모델 파일, 모델이 참조한 그림 파일이 있다
- 그림은 16x16 PNG 이고, 파일마다 CREDITS.md 에 적혀 있다
"""
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
NAMESPACE = "hanolter"
# 바닐라 정의가 단순 모델이 아닌 바탕 아이템의 바닐라 아이템 정의(마인크래프트 26.3 그대로). fallback 비교용.
VANILLA_ITEMS = ROOT / "tools" / "vanilla_items"
errors = []


def err(path, msg):
    where = path.relative_to(ROOT) if isinstance(path, Path) else path
    errors.append(f"{where}: {msg}")


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        err(path, f"JSON 문법 오류 — {e}")
        return None


def split(ref):
    ns, _, rest = ref.partition(":")
    return (ns, rest) if rest else ("minecraft", ns)


def model_refs(node):
    """아이템 정의 안의 모든 {"type": "minecraft:model", "model": ...} 참조를 모은다."""
    found = []
    if isinstance(node, dict):
        if node.get("type") in ("minecraft:model", "model") and isinstance(node.get("model"), str):
            found.append(node["model"])
        for value in node.values():
            found += model_refs(value)
    elif isinstance(node, list):
        for value in node:
            found += model_refs(value)
    return found


def check_pack_mcmeta():
    path = ROOT / "pack.mcmeta"
    if not path.is_file():
        err("pack.mcmeta", "파일이 없다")
        return
    data = load(path)
    if data is None:
        return
    pack = data.get("pack") if isinstance(data, dict) else None
    if not isinstance(pack, dict) or "description" not in pack:
        err(path, "pack.description 이 없다")
    elif "min_format" not in pack or "max_format" not in pack:
        err(path, "pack.min_format / pack.max_format 이 없다")


def check_model(ref, source):
    ns, name = split(ref)
    if ns == "minecraft":
        return  # 바닐라 모델은 게임에 들어 있다
    path = ASSETS / ns / "models" / f"{name}.json"
    if not path.is_file():
        err(source, f"모델 {ref} 의 파일이 없다 ({path.relative_to(ROOT)})")
        return
    data = load(path)
    if not isinstance(data, dict):
        return
    parent = data.get("parent")
    if isinstance(parent, str):
        check_model(parent, path)
    for tex in (data.get("textures") or {}).values():
        if not isinstance(tex, str) or tex.startswith("#"):
            continue
        tns, tname = split(tex)
        if tns == "minecraft":
            continue
        tpath = ASSETS / tns / "textures" / f"{tname}.png"
        if not tpath.is_file():
            err(path, f"그림 {tex} 의 파일이 없다 ({tpath.relative_to(ROOT)})")


def check_vanilla_item(path):
    data = load(path)
    if data is None:
        return
    model = data.get("model") if isinstance(data, dict) else None
    if not isinstance(model, dict):
        err(path, "model 이 없다")
        return
    if model.get("type") not in ("minecraft:select", "select") \
            or model.get("property") not in ("minecraft:custom_model_data", "custom_model_data"):
        err(path, "바닐라 아이템 정의는 custom_model_data 로 고르는 minecraft:select 여야 한다")
        return
    fallback = model.get("fallback")
    vanilla_path = VANILLA_ITEMS / path.name
    if vanilla_path.is_file():
        # 바닐라 정의가 단순 모델이 아닌 바탕(나침반 등): fallback 이 바닐라 정의와 완전히 같아야 한다.
        vanilla = load(vanilla_path)
        if not isinstance(vanilla, dict) or fallback != vanilla.get("model"):
            err(path, f"fallback 은 바닐라 정의({vanilla_path.relative_to(ROOT)})와 똑같아야 한다")
    else:
        expected = f"minecraft:item/{path.stem}"
        if not isinstance(fallback, dict) or fallback.get("type") not in ("minecraft:model", "model") \
                or "minecraft:" + split(str(fallback.get("model")))[1] != expected \
                or split(str(fallback.get("model")))[0] != "minecraft" \
                or set(fallback) != {"type", "model"}:
            err(path, f"fallback 은 원래 바닐라 모델({expected})이어야 한다")
    cases = model.get("cases")
    if not isinstance(cases, list) or not cases:
        err(path, "cases 가 비어 있다")
        return
    seen = set()
    for case in cases:
        whens = case.get("when") if isinstance(case, dict) else None
        whens = whens if isinstance(whens, list) else [whens]
        for when in whens:
            if not isinstance(when, str) or not when.startswith(NAMESPACE + ":"):
                err(path, f"when 값은 '{NAMESPACE}:이름' 문자열이어야 한다 (지금: {when!r})")
            elif when in seen:
                err(path, f"when 값 {when!r} 이 두 번 적혀 있다 (뒤의 것은 쓰이지 않는다)")
            else:
                seen.add(when)
    for ref in model_refs(model):
        check_model(ref, path)


def check_textures():
    credits_path = ROOT / "CREDITS.md"
    credits = credits_path.read_text(encoding="utf-8") if credits_path.is_file() else ""
    if not credits:
        err("CREDITS.md", "파일이 없다")
    for path in sorted(ASSETS.rglob("*.png")):
        head = path.read_bytes()[:24]
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            err(path, "PNG 파일이 아니다")
        elif struct.unpack(">II", head[16:24]) != (16, 16):
            err(path, "그림 크기가 16x16 이 아니다")
        rel = path.relative_to(ROOT).as_posix()
        if credits and f"`{rel}`" not in credits:
            err(path, "CREDITS.md 에 출처·라이선스가 적혀 있지 않다")


def main():
    check_pack_mcmeta()
    if not ASSETS.is_dir():
        err("assets", "폴더가 없다")
    else:
        for path in sorted(ASSETS.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ASSETS).parts
            if rel[0] == "minecraft":
                if len(rel) == 3 and rel[1] == "items" and path.suffix == ".json":
                    check_vanilla_item(path)
                else:
                    err(path, "assets/minecraft 아래에는 items/*.json 만 둘 수 있다 (바닐라 그림·모델을 바꾸지 않는다)")
            elif path.suffix in (".json", ".mcmeta"):
                data = load(path)
                if data is not None and len(rel) > 1 and rel[1] == "models":
                    check_model(f"{rel[0]}:{'/'.join(rel[2:])[:-5]}", path)
        check_textures()
    if errors:
        print(f"리소스팩 검사 실패 ({len(errors)}건)")
        for line in errors:
            print(" - " + line)
        sys.exit(1)
    print("리소스팩 검사 통과")


if __name__ == "__main__":
    main()
