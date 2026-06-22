# Updating the People page

## The short version

1. Edit `people.yaml`
2. Run `python3 build_people.py`
3. `git add people.html people.yaml && git commit -m "Update people" && git push`

That's it. You never need to touch `people.html` directly again.

---

## Adding a new lab member

Open `people.yaml`. Under `current_members:`, copy one of the existing
entries and fill in the new person's details:

```yaml
  - name: Jane Smith
    role: Postdoctoral Fellow
    photo: jane.jpg
    email: janesmith@arizona.edu
    pubmed_url: "https://pubmed.ncbi.nlm.nih.gov/?term=..."
    bio: |
      A sentence or two about Jane's research focus and background.
```

- `photo` must match a filename already in `images/people/`. Add the photo
  file there first.
- If you don't have a photo yet, leave `photo: ""` — the page will show a
  placeholder box with their name instead of breaking or showing the wrong
  photo.
- `bio` can be left as `bio: ""` if there's nothing to say yet.
- `pubmed_url` and `resume_pdf` are optional — leave them as `""` to omit
  that link entirely.

People are displayed two-per-row, in the order they appear in the file.

Then run:
```bash
python3 build_people.py
```

This regenerates `people.html` completely. Don't hand-edit `people.html` —
the next build will overwrite whatever you typed there.

---

## Moving someone to alumni

1. Delete (or cut) their block from `current_members:`
2. Add one line under `alumni:` at the bottom:

```yaml
  - text: "Jane Smith, PhD - currently postdoc at Stanford"
```

If their entry needs a clickable link inside the text (like the KEYS or
NSURP program links), use the longer form:

```yaml
  - text: "Jane Smith (KEYS high school student) - currently at UofA"
    link_text: "(KEYS high school student)"
    link_url: "https://bio5.org/impact/engaging-students/keys-research-internship-program"
```

The script finds `link_text` inside `text` and turns just that part into a
link — everything else stays plain text.

3. Run `python3 build_people.py`

---

## Removing someone entirely

Delete their block from `current_members:` (or their line from `alumni:`)
and run the build script. Nothing else to do.

---

## Changing the group photo or headline

Both are at the very bottom of `people.yaml`:

```yaml
group_photo: group.jpeg
group_photo_alt: "lab celebrating the first R01"
headline: "In the Van Doorslaer Lab, we depend on your whole self <br> to tackle the genomic challenges of HPV cancers."
```

`headline` allows the `<br>` tag if you want a line break in a specific
place, same as the original page.

---

## What the build script checks for you

Every time you run `build_people.py`, it warns you (without failing) if:
- A `photo:` filename doesn't actually exist in `images/people/`

It does NOT validate email addresses or URLs — a quick visual check of the
generated `people.html`, or the live site after deploying, is still worth
doing for anything unusual.

---

## If something looks wrong after building

- **A person's photo shows a placeholder box instead of their real photo**:
  check that the filename in `people.yaml` exactly matches the file in
  `images/people/`, including capitalization (`Jane.jpg` ≠ `jane.jpg` on
  GitHub Pages, even though it might work locally on a Mac).
- **The page looks broken/unstyled**: make sure you committed both
  `people.html` AND any new photo files in the same push.
- **You want to go back to how it looked before**: `git log` and
  `git checkout <commit> -- people.html people.yaml` to revert just these
  two files.
