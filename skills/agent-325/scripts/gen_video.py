# -*- coding: utf-8 -*-
"""AGENT 325 — Générateur de vidéos courtes verticales (TikTok / Reels / Shorts).

Assemble une vraie vidéo MP4 1080x1920 à partir d'un scénario JSON :
voix off française (edge-tts, gratuit, sans clé) + images (IA ou fournies)
+ mouvement Ken Burns + texte incrusté + logo en filigrane.

Usage :
  python3 gen_video.py --spec scenario.json --out video.mp4 [--work dossier]

Format du scénario JSON :
{
  "voix": "fr-FR-HenriNeural",
  "debit": "+8%",
  "logo": "logo.png",
  "scenes": [
    {"fond": "img1.png", "duree_min": 3.0, "zoom": "in",
     "texte": "GROS TITRE", "sous_titre": "ligne secondaire",
     "voix": "Texte prononce par la voix off."}
  ]
}

Contraintes : ffmpeg (zoompan, drawtext, libx264, aac), Pillow, edge-tts.
"""
import argparse, asyncio, json, os, shutil, subprocess, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ORANGE = (232, 114, 28)
NAVY = (20, 48, 79)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"ECHEC: {' '.join(str(c) for c in cmd[:6])}...\n{r.stderr[-1500:]}")
    return r


def probe_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)])
    return float(r.stdout.strip())


def tts(text, out_mp3, voice, rate):
    import edge_tts

    async def go():
        await edge_tts.Communicate(text, voice, rate=rate).save(str(out_mp3))
    asyncio.run(go())
    return probe_duration(out_mp3)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_overlay(scene, path, logo=None):
    """PNG transparent 1080x1920 : titre + sous-titre DANS la meme bande + logo."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    titre = (scene.get("texte") or "").strip()
    sous = (scene.get("sous_titre") or "").strip()

    # polices reduites si le titre est long, pour eviter un pave de 4 lignes
    taille_t = 92 if len(titre) <= 34 else 78
    ft = ImageFont.truetype(FONT_BOLD, taille_t)
    fs = ImageFont.truetype(FONT_REG, 48)

    tl = wrap(d, titre, ft, int(W * 0.84)) if titre else []
    sl = wrap(d, sous, fs, int(W * 0.80)) if sous else []

    lh_t = int(taille_t * 1.16)
    lh_s = 60
    gap = 20 if (tl and sl) else 0
    block_h = lh_t * len(tl) + gap + lh_s * len(sl)

    # la bande sombre englobe titre ET sous-titre -> lisibilite garantie
    # meme sur un fond tres sombre (contre-jour, silhouette, nuit)
    pad = 42
    top = int(H * 0.40) - block_h // 2
    d.rounded_rectangle(
        [int(W * 0.05), top - pad, int(W * 0.95), top + block_h + pad],
        radius=24, fill=(10, 20, 34, 185))

    y = top
    for ln in tl:
        tw = d.textlength(ln, font=ft)
        d.text(((W - tw) / 2 + 3, y + 3), ln, font=ft, fill=(0, 0, 0, 210))
        d.text(((W - tw) / 2, y), ln, font=ft, fill=(255, 255, 255, 255))
        y += lh_t
    y += gap
    for ln in sl:
        tw = d.textlength(ln, font=fs)
        d.text(((W - tw) / 2 + 2, y + 2), ln, font=fs, fill=(0, 0, 0, 200))
        d.text(((W - tw) / 2, y), ln, font=fs, fill=ORANGE + (255,))
        y += lh_s

    if logo and Path(logo).exists():
        lg = Image.open(logo).convert("RGBA")
        size = 150
        lg = lg.resize((size, size), Image.LANCZOS)
        img.alpha_composite(lg, (int(W * 0.07), int(H * 0.055)))

    img.save(path)
    return path


def make_signature(scene, path, logo=None):
    """Layout de cloture : logo centre + nom de marque + slogan + CTA."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    marque = (scene.get("marque") or "").strip()
    slogan = (scene.get("slogan") or "").strip()
    cta = (scene.get("cta") or "").strip()

    f_m = ImageFont.truetype(FONT_BOLD, 66)
    f_s = ImageFont.truetype(FONT_REG, 54)
    f_c = ImageFont.truetype(FONT_BOLD, 46)

    ml = wrap(d, marque, f_m, int(W * 0.86)) if marque else []
    sl = wrap(d, slogan, f_s, int(W * 0.82)) if slogan else []
    cl = wrap(d, cta, f_c, int(W * 0.80)) if cta else []

    LOGO, lh_m, lh_s, lh_c = 370, 82, 72, 62
    g1, g2, g3 = 44, 26, 36
    block_h = LOGO + g1 + lh_m * len(ml) + g2 + lh_s * len(sl) + g3 + lh_c * len(cl)
    pad = 56
    top = int(H * 0.50) - block_h // 2
    d.rounded_rectangle([int(W * 0.05), top - pad, int(W * 0.95), top + block_h + pad],
                        radius=30, fill=(10, 20, 34, 196))

    y = top
    if logo and Path(logo).exists():
        lg = Image.open(logo).convert("RGBA").resize((LOGO, LOGO), Image.LANCZOS)
        img.alpha_composite(lg, ((W - LOGO) // 2, y))
    y += LOGO + g1

    for ln in ml:
        tw = d.textlength(ln, font=f_m)
        d.text(((W - tw) / 2 + 3, y + 3), ln, font=f_m, fill=(0, 0, 0, 210))
        d.text(((W - tw) / 2, y), ln, font=f_m, fill=(255, 255, 255, 255))
        y += lh_m
    y += g2
    for ln in sl:
        tw = d.textlength(ln, font=f_s)
        d.text(((W - tw) / 2 + 2, y + 2), ln, font=f_s, fill=(0, 0, 0, 200))
        d.text(((W - tw) / 2, y), ln, font=f_s, fill=ORANGE + (255,))
        y += lh_s
    y += g3
    for ln in cl:
        tw = d.textlength(ln, font=f_c)
        d.text(((W - tw) / 2 + 2, y + 2), ln, font=f_c, fill=(0, 0, 0, 200))
        d.text(((W - tw) / 2, y), ln, font=f_c, fill=(255, 255, 255, 255))
        y += lh_c

    img.save(path)
    return path


def make_background(src, path):
    """Fond 1080x1920 : image fournie recadree, ou degrade de marque."""
    if src and Path(src).exists():
        im = Image.open(src).convert("RGB")
        # recadrage "cover"
        ratio = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * ratio) + 1, int(im.height * ratio) + 1), Image.LANCZOS)
        left = (im.width - W) // 2
        top = (im.height - H) // 2
        im = im.crop((left, top, left + W, top + H))
        im.save(path)
        return path
    # degrade bleu nuit -> orange
    base = Image.new("RGB", (W, H))
    px = base.load()
    for y in range(H):
        t = y / H
        r = int(NAVY[0] + (ORANGE[0] - NAVY[0]) * t * t)
        g = int(NAVY[1] + (ORANGE[1] - NAVY[1]) * t * t)
        b = int(NAVY[2] + (ORANGE[2] - NAVY[2]) * t * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    base = base.filter(ImageFilter.GaussianBlur(2))
    base.save(path)
    return path


def render_scene(idx, scene, work, logo, voice_default, rate):
    bg_src = scene.get("fond")
    bg = make_background(bg_src, work / f"bg_{idx}.png")
    if scene.get("style") == "signature":
        ov = make_signature(scene, work / f"ov_{idx}.png", logo)
    else:
        ov = make_overlay(scene, work / f"ov_{idx}.png", logo)

    voice_txt = (scene.get("voix") or scene.get("texte") or scene.get("slogan") or "").strip()
    mp3 = work / f"voix_{idx}.mp3"
    vdur = tts(voice_txt, mp3, scene.get("voix_id", voice_default), rate) if voice_txt else 0.0
    dur = max(float(scene.get("duree_min", 3.0)), vdur + 0.32)

    frames = int(dur * FPS)
    z = scene.get("zoom", "in")
    if z == "out":
        zp = f"z='if(eq(on,1),1.28,max(zoom-0.0006,1.0))'"
    elif z == "none":
        zp = "z='1.0'"
    else:
        zp = "z='min(zoom+0.0006,1.28)'"

    seg = work / f"seg_{idx}.mp4"
    vf = (
        f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,"
        f"crop={W*2}:{H*2},"
        f"zoompan={zp}:d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={W}x{H}:fps={FPS},setsar=1[bg];"
        f"[bg][1:v]overlay=0:0:format=auto[v]"
    )
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(bg), "-i", str(ov), "-t", f"{dur:.3f}"]
    if voice_txt:
        cmd += ["-i", str(mp3)]
        cmd += ["-filter_complex",
                vf + f";[2:a]apad,atrim=0:{dur:.3f},asetpts=N/SR/TB[a]",
                "-map", "[v]", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-filter_complex", vf, "-map", "[v]", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-shortest", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-t", f"{dur:.3f}", str(seg)]
    run(cmd)
    return seg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()

    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    scenes = spec.get("scenes") or []
    if not scenes:
        sys.exit("ERREUR: aucune scene dans le scenario")

    work = Path(a.work or (Path(a.out).parent / (Path(a.out).stem + "_work")))
    work.mkdir(parents=True, exist_ok=True)
    voice = spec.get("voix", "fr-FR-HenriNeural")
    rate = spec.get("debit", "+8%")
    logo = spec.get("logo")

    segs = []
    for i, sc in enumerate(scenes):
        print(f"  scene {i+1}/{len(scenes)}...", flush=True)
        segs.append(render_scene(i, sc, work, logo, voice, rate))

    lst = work / "liste.txt"
    lst.write_text("".join(f"file '{s.resolve()}'\n" for s in segs), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(a.out)])

    d = probe_duration(a.out)
    print(f"OK {a.out}  ({d:.1f}s, {os.path.getsize(a.out)//1024} Ko)")


if __name__ == "__main__":
    main()
