# Storybook Edge Blender

## Purpose

AI-generated illustrations (ChatGPT/DALL-E, Midjourney, etc.) usually come as
a picture on a flat background with a hard, rectangular cutoff. Dropped
straight into a children's storybook page, that sharp edge looks jarring -
like a sticker slapped on top of the page instead of artwork that belongs
there.

This tool batch-processes a folder of images and softens their edges -
blurring them and fading them out - so they sit naturally on a page instead
of ending in a sudden, straight line.

It is deliberately built as a small CLI script rather than a one-off, since
the "right" amount of softening differs from image to image, and new
strategies for handling edges are expected to be added over time (see
[Modes](#modes) below).

## Requirements

- Python 3.9+
- Pillow, numpy (see `requirements.txt`)

```bash
pip install -r requirements.txt
```

## Usage

By default, the script reads every image from a folder named `Input` in the
current directory, and writes the processed PNGs into a folder named
`Output` (both are created/used relative to where you run the script from).

```bash
python feather_edges.py
```

Custom folders:

```bash
python feather_edges.py --input-dir path/to/my_images --output-dir path/to/result
```

Choosing a mode and its strength:

```bash
python feather_edges.py --mode fade --fade-percent 20
python feather_edges.py --mode mirror-fade --mirror-percent 12
```

Output is always written as PNG with an alpha (transparency) channel,
regardless of the input format, since transparency is what makes the edge
blend into the page.

## Arguments

| Argument | Default | Used by | Description |
|---|---|---|---|
| `--input-dir`, `-i` | `Input` | all modes | Folder to read source images from. |
| `--output-dir`, `-o` | `Output` | all modes | Folder to write processed PNGs to. |
| `--mode`, `-m` | `fade` | - | Which edge-handling strategy to use: `fade` or `mirror-fade`. |
| `--fade-percent` | `15` | `fade` | % of the image's shorter side used as the fade zone near each edge. Higher = more of the picture fades out. |
| `--mirror-percent` | `12` | `mirror-fade` | % of the image's shorter side that gets mirror-extended outward before fading. |
| `--blur-radius` | auto | all modes | Gaussian blur radius in pixels. If not given, it's derived automatically from the fade/mirror percent. |

## Modes

### `fade` (default)

The straightforward approach:

1. The image's own edges are blurred (Gaussian blur).
2. A soft mask is built that is fully opaque in the center and smoothly
   fades to fully transparent within a border zone (`--fade-percent` of the
   shorter image side).
3. Near the edge, the picture is both blurred *and* faded to transparency,
   so there is no sudden color change and no hard cutoff line - the image
   simply dissolves into the page.

**Known limitation:** this mode does not know or care what is drawn near
the border. If a character's hand, a tree branch, or any other important
detail sits inside that fade zone, it will visibly fade out along with the
background. In other words: the more aggressive the fade percentage, the
smoother the blend, but the more of the actual illustration you risk
losing near the edges. `--fade-percent` is exactly the knob to balance that
trade-off per image - there's no single value that will look perfect for
every picture, which is why it's exposed as a parameter rather than
hardcoded.

### `mirror-fade` (experimental)

This mode exists specifically to attack the content-loss problem above. The
idea, still being refined:

1. Instead of fading the original border pixels straight to transparency,
   the border strip is first **mirrored (reflected) outward**, extending the
   canvas. This means the area just past the original edge isn't empty or a
   flat blur - it's an echo of the artwork itself.
2. That mirrored strip is then blurred and faded out using the same
   mask-based approach as `fade`.

The intent is that the transition reads as a soft vignette / halo made of
"related" content, rather than the picture being visibly cut off. This is a
first working version, not a finished algorithm - the reflection approach
is a reasonable starting point, but it can look odd on images with strong
directional detail near the edge (text, straight lines, faces cut close to
the border, etc.). Treat its parameters and even its overall approach as
subject to change.

## Known limitations / roadmap

- `fade` mode can cut off illustration content that sits close to the
  image border - see above.
- `mirror-fade` is experimental: reflection can look unnatural on some
  images (e.g. faces or text near the edge); it hasn't been tuned yet
  beyond a first working version.
- Both modes use a single global fade/mirror percentage for the whole
  image; there's no per-side or content-aware adjustment yet.
- No automatic detection of "busy" vs. "already blank" edges - the same
  percentage is applied uniformly regardless of what's actually near the
  border.

This README is kept up to date as the goal, feature set, and available
modes evolve.
