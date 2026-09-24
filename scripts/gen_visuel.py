# -*- coding: utf-8 -*-
"""Génération de visuels marketing via OpenRouter (clé OPENROUTER_API_KEY).

Usage:
  python3 gen_visuel.py --prompt "..." --out visuel.png [--ratio 1:1|4:5|9:16|16:9]
                        [--model google/gemini-2.5-flash-image|google/gemini-3-pro-image]
                        [--n 1] [--ref image.png]

Sortie: chemin(s) du/des fichier(s) écrits, imprimé sur stdout.
"""
import os, sys, json, base64, argparse, urllib.request, urllib.error
from pathlib import Path

API = "https://openrouter.ai/api/v1/chat/completions"
MODELS = {
    "rapide": "google/gemini-2.5-flash-image",
    "pro": "google/gemini-3-pro-image",
    "openai": "openai/gpt-5-image",
}
RATIO_HINT = {
    "1:1": "format carré 1:1",
    "4:5": "format portrait 4:5 (Instagram feed)",
    "9:16": "format vertical 9:16 (Reels / TikTok / Stories)",
    "16:9": "format paysage 16:9 (YouTube / bannière)",
}


def key():
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k:
        env = Path.home() / ".hermes" / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("ERREUR: OPENROUTER_API_KEY introuvable")
    return k


def b64ify(path):
    ext = Path(path).suffix.lstrip(".").lower() or "png"
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def generate(prompt, model, ratio, n=1, ref=None):
    content = []
    full = prompt
    if ratio in RATIO_HINT:
        full += f" — cadre le visuel en {RATIO_HINT[ratio]}."
    content.append({"type": "text", "text": full})
    if ref:
        content.append({"type": "image_url", "image_url": {"url": b64ify(ref)}})

    body = {"model": model, "messages": [{"role": "user", "content": content}],
            "modalities": ["image", "text"], "n": n}
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERREUR HTTP {e.code}: {e.read().decode(errors='replace')[:600]}")
    msg = data["choices"][0]["message"]
    return [i["image_url"]["url"] for i in (msg.get("images") or [])], msg.get("content") or ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--ratio", default="1:1", choices=list(RATIO_HINT))
    p.add_argument("--model", default=MODELS["rapide"])
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--ref", default=None)
    a = p.parse_args()

    urls, _ = generate(a.prompt, a.model, a.ratio, a.n, a.ref)
    if not urls:
        sys.exit("ERREUR: aucune image renvoyée (le modèle a refusé ou n'a produit que du texte)")

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for idx, u in enumerate(urls):
        raw = base64.b64decode(u.split(",", 1)[1])
        target = out if idx == 0 else out.with_name(f"{out.stem}_{idx}{out.suffix}")
        target.write_bytes(raw)
        written.append(str(target))
        print(f"{target}  ({len(raw)} octets)")


if __name__ == "__main__":
    main()
