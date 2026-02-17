"""Generate the OG cover image for superuserlabs.org.

Renders at 2x and downscales for sharp antialiasing.
Requires: Pillow (pip install Pillow)
Usage: python scripts/generate_og_cover.py
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "media"

SCALE = 2
W, H = 1200 * SCALE, 630 * SCALE
BG_COLOR = (2, 6, 23)  # slate-950


def main():
    img = Image.new("RGBA", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    s = SCALE
    font_bold = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 54 * s)
    font_tagline = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22 * s)
    font_label = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15 * s)
    font_url = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15 * s)

    # --- Load and fix logo background to match page bg ---
    logo_full = Image.open(BASE / "superuserlabs-logo.png").convert("RGBA")
    lw, lh = logo_full.size
    pixels = logo_full.load()

    for y in range(lh):
        for x in range(lw):
            r, g, b, a = pixels[x, y]
            if r < 15 and g < 15 and b < 15:
                pixels[x, y] = (BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], a)

    # Find SU text bounds (white pixels, not the green cursor)
    min_y_su, max_y_su = lh, 0
    for y in range(lh):
        for x in range(lw):
            r, g, b, a = pixels[x, y]
            if r > 120 and b > 120:
                min_y_su = min(min_y_su, y)
                max_y_su = max(max_y_su, y)

    su_content_h = max_y_su - min_y_su
    su_top_frac = min_y_su / lh

    # --- Measure text ---
    bbox = draw.textbbox((0, 0), "Superuser Labs", font=font_bold)
    text_w = bbox[2] - bbox[0]
    bbox_cap = draw.textbbox((0, 0), "S", font=font_bold)
    cap_h = bbox_cap[3] - bbox_cap[1]

    # Size logo so SU text matches cap height
    logo_size = int(cap_h * 1.15 * lh / su_content_h)
    logo = logo_full.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    gap = 18 * s
    total_w = logo_size + gap + text_w

    # --- Vertical layout ---
    tagline = "Free and open-source software that empowers you"
    bbox_t = draw.textbbox((0, 0), tagline, font=font_tagline)
    tagline_h = bbox_t[3] - bbox_t[1]
    tw_t = bbox_t[2] - bbox_t[0]

    proj_size = 52 * s
    proj_label_h = 30 * s

    gap_to_tagline = 18 * s
    gap_to_divider = 44 * s
    gap_to_projects = 28 * s
    total_content = (
        logo_size
        + gap_to_tagline
        + tagline_h
        + gap_to_divider
        + gap_to_projects
        + proj_size
        + proj_label_h
    )

    content_top = (H - total_content) // 2 - 15 * s

    # --- Heading (logo + text) ---
    start_x = (W - total_w) // 2
    name_y = content_top + int(su_top_frac * logo_size) - int(bbox[1])
    logo_y = content_top

    img.paste(logo, (start_x, logo_y), logo)

    text_x = start_x + logo_size + gap
    bbox_su = draw.textbbox((0, 0), "Superuser ", font=font_bold)
    su_w = bbox_su[2] - bbox_su[0]
    draw.text((text_x, name_y), "Superuser ", fill=(255, 255, 255), font=font_bold)
    draw.text((text_x + su_w, name_y), "Labs", fill=(100, 116, 139), font=font_bold)

    # --- Tagline ---
    tagline_y = logo_y + logo_size + gap_to_tagline
    lockup_center = start_x + total_w // 2
    page_center = W // 2
    tagline_center = (lockup_center + page_center) // 2
    draw.text(
        (tagline_center - tw_t // 2, tagline_y),
        tagline,
        fill=(148, 163, 184),
        font=font_tagline,
    )

    # --- Divider ---
    line_y = tagline_y + tagline_h + gap_to_divider
    draw.line(
        [(page_center - 100 * s, line_y), (page_center + 100 * s, line_y)],
        fill=(51, 65, 85),
        width=s,
    )

    # --- Projects ---
    projects = [
        ("activitywatch-logo.png", "ActivityWatch"),
        ("gptme-logo.png", "gptme"),
    ]
    proj_gap = 95 * s
    proj_y = line_y + gap_to_projects
    total_pw = len(projects) * proj_size + (len(projects) - 1) * proj_gap
    pstart_x = (W - total_pw) // 2

    for i, (fname, label) in enumerate(projects):
        p = (
            Image.open(BASE / fname)
            .convert("RGBA")
            .resize((proj_size, proj_size), Image.Resampling.LANCZOS)
        )
        px = pstart_x + i * (proj_size + proj_gap)
        img.paste(p, (px, proj_y), p)
        bbox_l = draw.textbbox((0, 0), label, font=font_label)
        lbw = bbox_l[2] - bbox_l[0]
        draw.text(
            (px + (proj_size - lbw) // 2, proj_y + proj_size + 8 * s),
            label,
            fill=(148, 163, 184),
            font=font_label,
        )

    # --- URL ---
    url = "superuserlabs.org"
    bbox_u = draw.textbbox((0, 0), url, font=font_url)
    uw = bbox_u[2] - bbox_u[0]
    draw.text(((W - uw) // 2, H - 36 * s), url, fill=(148, 163, 184), font=font_url)

    # --- Downscale and save ---
    final = img.resize((1200, 630), Image.Resampling.LANCZOS)
    out = BASE / "og-cover.png"
    final.save(out, format="PNG")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
