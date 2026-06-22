#!/usr/bin/env python3
"""
build_people.py — regenerates people.html from people.yaml

Usage:
    python3 build_people.py

Reads:   people.yaml
Writes:  people.html  (the entire file is replaced; only people.yaml
                       needs to be hand-edited going forward)

Requirements: pip install pyyaml
"""

import html as html_module
import sys
from pathlib import Path

import yaml

SITE_ROOT = Path(__file__).parent
YAML_PATH = SITE_ROOT / "people.yaml"
OUTPUT_PATH = SITE_ROOT / "people.html"
PHOTO_DIR = SITE_ROOT / "images" / "people"


def esc(s):
    """Escape a plain-text field for safe HTML embedding. Does NOT escape
    fields that are allowed to contain raw HTML (like headline/bio, which
    may legitimately use <br> or similar)."""
    return html_module.escape(s, quote=False) if s else ""


def load_data():
    if not YAML_PATH.exists():
        print(f"  people.yaml not found at {YAML_PATH}")
        sys.exit(1)
    with open(YAML_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def photo_exists_on_disk(photo_filename):
    if not photo_filename:
        return False
    return (PHOTO_DIR / photo_filename).exists()


def render_photo_cell(person):
    photo = person.get("photo", "")
    name = esc(person["name"])

    if photo and not photo_exists_on_disk(photo):
        print(f"  WARNING: images/people/{photo} not found on disk — using placeholder for {person['name']}")

    if photo and photo_exists_on_disk(photo):
        return f'<td align="center"><img src="/images/people/{photo}" alt="{name}" style="max-width:100%;height:200px;" width=auto height="200"></td>'
    else:
        # No photo on file - render a simple placeholder cell instead of
        # silently reusing someone else's photo (the old page did this by
        # accident for two different people sharing KVD.jpg), or showing a
        # broken image icon for a typo'd filename.
        return (
            '<td align="center">'
            '<div style="width:100%;max-width:160px;height:200px;margin:0 auto;background:#eaf3f8;'
            'border:1px solid #b9d3e2;display:flex;align-items:center;justify-content:center;'
            'font-family:Arial,sans-serif;color:#143c55;font-size:13px;text-align:center;padding:8px;">'
            f"{name}<br>(photo coming soon)"
            "</div></td>"
        )


def render_info_cell(person):
    name = esc(person["name"])
    role = esc(person.get("role", ""))

    links = []
    pubmed_url = person.get("pubmed_url", "")
    if pubmed_url:
        links.append(f'<a href="{pubmed_url}" target="_blank">Publications</a>')

    email = person.get("email", "")
    if email:
        links.append(f'<a href="mailto:{email}">Email</a>')

    resume_pdf = person.get("resume_pdf", "")
    if resume_pdf:
        links.append(f'<a target="_blank" href="{resume_pdf}" download> Resume</a>')

    link_line = " | ".join(links)

    bio = (person.get("bio") or "").strip()
    bio_html = f'<p align="justify">{esc(bio)}</p>' if bio else ""

    return (
        '<td align="center">\n'
        f"<p><strong>{name}</strong><br><strong>{role}</strong><br>\n"
        f"{link_line}\n"
        f"{bio_html}\n"
        "</td>"
    )


def render_member_rows(members):
    """Pair members two-per-row, exactly matching the site's existing layout."""
    rows = []
    for i in range(0, len(members), 2):
        pair = members[i:i + 2]

        photo_cells = "\n    \t".join(render_photo_cell(p) for p in pair)
        info_cells = "\n    \t".join(render_info_cell(p) for p in pair)

        rows.append(
            f"   <tr>\n    \t{photo_cells}\n   </tr>\n\n"
            f"\t<tr>\n    \t{info_cells}\n\t</tr>\n"
        )
    return "\n".join(rows)


def render_alumni_item(entry):
    text = entry["text"]
    link_text = entry.get("link_text")
    link_url = entry.get("link_url")

    if link_text and link_url:
        linked = f'<a href="{link_url}" target="_blank">{esc(link_text)}</a>'
        text = text.replace(link_text, linked)
        return f"<li>{text}</li>"
    else:
        return f"<li>{esc(text)}</li>"


def build():
    print("Building people.html from people.yaml...")
    data = load_data()

    members = data.get("current_members", [])
    alumni = data.get("alumni", [])
    group_photo = data.get("group_photo", "")
    group_photo_alt = data.get("group_photo_alt", "")
    headline = data.get("headline", "")

    if group_photo and not photo_exists_on_disk(group_photo):
        print(f"  WARNING: images/people/{group_photo} (group photo) not found on disk")

    member_rows_html = render_member_rows(members)
    alumni_html = "\n".join(render_alumni_item(a) for a in alumni)

    html = f"""---
layout: default
title: The Van Doorslaer lab at the University of Arizona
permalink: /people
---

<body>
<div id="wrap">
  <div id="masthead">
    <h1>{{{{page.title}}}}</h1>
  </div>
  <div id="menucontainer">
    {{% include nav.html %}}
  </div>
\t{{% include sidebar.html %}}
    <div id="content", style="margin: 0 auto;">

<h3>{headline}</h3>
<br>
<img class="normal" src="/images/people/{group_photo}" style="max-width:730px;width:100%;height:auto;" alt="{group_photo_alt}"/>

<br><br><br>

<table cellspacing="0" cellpadding="10" class="people-table">
{member_rows_html}
</table>

</div>

<h4><a id="KVD Lab alumni"></a>KVD Lab alumni</h4>
<ul>
{alumni_html}
</ul>

  </div>
</div>
"""

    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"\n✅ Done → {OUTPUT_PATH}")
    print(f"   {len(members)} current members, {len(alumni)} alumni")


if __name__ == "__main__":
    build()
