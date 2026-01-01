# Code-In-The-Middle – v27
# Make human hands move continuously (not only when Prompt blinks)

import os, shutil, math
import matplotlib.pyplot as plt
from moviepy.editor import ImageSequenceClip
from matplotlib.patches import Circle, Rectangle, Polygon

FPS = 8
DURATION_SEC = 15
N_FRAMES = FPS * DURATION_SEC

OUT_MP4 = "/mnt/data/Code-In-The-Middle_15s_centered_boxes_video_layers_visual_human_75pct_hands_always_moving.mp4"
FRAMES_DIR = "/mnt/data/_frames_code_middle_human_hands_always"

PROMPTS = [
    "Create a short video that explains Kubernetes pod autoscaling using clear visuals.",
    "Move the pods to the left and make scaling events easier to understand visually.",
    "Add a queue based scaling example with producer and consumer behavior.",
    "Fix visual overlaps and improve layout consistency across frames.",
    "Enhance animations to clearly show continuous iteration and improvement."
]

CODE_STEPS = [
    ["draw_pods(x=10)"],
    ["draw_pods(x=4)"],
    ["draw_queue()", "scale_by_queue()"],
    ["adjust_layout()", "fix_overlaps()"],
    ["add_animation()", "polish_visuals()"]
]

def phase_index(i):
    return min(len(PROMPTS) - 1, int((i / N_FRAMES) * len(PROMPTS)))

def split_two_words_per_line(text):
    words = text.split()
    lines, i = [], 0
    while i < len(words):
        w1 = words[i]; i += 1
        w2 = words[i] if i < len(words) else ""
        if w2: i += 1
        line_words = [w1] + ([w2] if w2 else [])
        if line_words and len(line_words[-1]) == 1 and i < len(words):
            line_words.append(words[i]); i += 1
        if i < len(words) and len(words[i]) == 1:
            line_words.append(words[i]); i += 1
        lines.append(" ".join(line_words))
    return lines

def draw_typing_user(ax, cx, cy, scale=1.75, t=0):
    ax.add_patch(Circle((cx, cy + 0.45*scale), 0.18*scale,
                        facecolor="#f1c7a6", edgecolor="#333333", linewidth=1.2))
    ax.add_patch(Rectangle((cx - 0.25*scale, cy - 0.05*scale),
                           0.5*scale, 0.35*scale,
                           facecolor="#ffffff", edgecolor="#333333", linewidth=1.2))
    ax.add_patch(Rectangle((cx - 0.35*scale, cy - 0.25*scale),
                           0.7*scale, 0.12*scale,
                           facecolor="#d9d9d9", edgecolor="#333333", linewidth=1.2))
    ax.add_patch(Rectangle((cx - 0.30*scale, cy - 0.05*scale),
                           0.6*scale, 0.20*scale,
                           facecolor="#eeeeee", edgecolor="#333333", linewidth=1.2))

    # Always-moving hands (continuous sinusoidal motion)
    offset = 0.06 * math.sin(t * 0.9)
    hand_color = "#ff8c00"
    ax.add_patch(Rectangle((cx - 0.22*scale, cy - 0.10*scale + offset),
                           0.12*scale, 0.06*scale,
                           facecolor=hand_color, edgecolor="none"))
    ax.add_patch(Rectangle((cx + 0.10*scale, cy - 0.10*scale - offset),
                           0.12*scale, 0.06*scale,
                           facecolor=hand_color, edgecolor="none"))

def draw_box(ax, x, y, w, h, label, color, blink=False, blink_strength=0.0):
    if blink:
        ax.add_patch(Rectangle((x - 0.25, y - 0.25),
                               w + 0.5, h + 0.5,
                               fill=False,
                               edgecolor=color,
                               linewidth=4 + 2 * blink_strength,
                               alpha=0.6))
    ax.add_patch(Rectangle((x, y), w, h,
                           facecolor=color,
                           edgecolor="#222222",
                           linewidth=2.5))
    ax.text(x + w/2, y + h - 0.4, label,
            ha="center", va="top",
            fontsize=13, weight="bold")

def draw_video_layer(ax, x, y, w, idx, active=False):
    base_y = y + 0.4 + idx * 0.65
    ax.add_patch(Rectangle((x + 0.15, base_y),
                           w - 0.3, 0.5,
                           facecolor="#ffffff",
                           edgecolor="#666666",
                           linewidth=1.2))
    ax.add_patch(Rectangle((x + 0.18, base_y + 0.06),
                           (w - 0.36) * (0.3 + 0.15 * idx),
                           0.06,
                           facecolor="#7b61ff",
                           edgecolor="none"))
    tri = Polygon([
        (x + w - 0.45, base_y + 0.12),
        (x + w - 0.25, base_y + 0.25),
        (x + w - 0.45, base_y + 0.38)
    ], closed=True, facecolor="#7b61ff", edgecolor="none")
    ax.add_patch(tri)
    if active:
        ax.add_patch(Rectangle((x + 0.12, base_y - 0.03),
                               w - 0.24, 0.56,
                               fill=False,
                               edgecolor="#7b61ff",
                               linewidth=2))

def render_frame(path, i):
    idx = phase_index(i)
    cycle = (i // 8) % 2
    blink_prompt = cycle == 0
    blink_code = cycle == 1
    blink_strength = abs(math.sin(i * 0.6))

    fig = plt.figure(figsize=(9.6, 5.4), dpi=90)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8, 8.3, "Code-In-The-Middle", ha="center",
            fontsize=16, weight="bold")
    ax.text(
        8, 7.8,
        "Instead of generating videos directly, we iterate on code.\n"
        "Prompts refine Python. Python regenerates visuals.\n"
        "This loop makes results controllable, debuggable, and reusable.",
        ha="center", va="top", fontsize=11
    )

    bw, bh = 2.6, 4.6
    y = 1.4
    total_width = bw * 3 + 1.6 * 2
    start_x = (16 - total_width) / 2
    prompt_x = start_x
    code_x = start_x + bw + 1.6
    video_x = start_x + 2 * (bw + 1.6)

    draw_box(ax, prompt_x, y, bw, bh, "Prompt", "#fde2e2", blink_prompt, blink_strength)
    draw_box(ax, code_x, y, bw, bh, "Python Code", "#e2f0cb", blink_code, blink_strength)
    draw_box(ax, video_x, y, bw, bh, "Video", "#e8d9ff")

    prompt_lines = split_two_words_per_line(PROMPTS[idx])
    top_text_y = y + bh - 1.1
    bottom_text_y = y + 0.5
    step = min((top_text_y - bottom_text_y) / max(len(prompt_lines) - 1, 1), 0.32)
    start_y = top_text_y
    for line in prompt_lines:
        if start_y < bottom_text_y + 1.6:
            break
        ax.text(prompt_x + bw/2, start_y,
                line, ha="center", va="center", fontsize=7.6)
        start_y -= step

    draw_typing_user(ax, prompt_x + bw/2, y + 0.6, scale=1.75, t=i)

    all_code = []
    for k in range(idx + 1):
        all_code.extend(CODE_STEPS[k])

    code_y = top_text_y
    for line in all_code:
        if code_y < bottom_text_y:
            break
        ax.text(code_x + bw/2, code_y,
                line, ha="center", va="center",
                fontsize=9, family="monospace")
        code_y -= step

    for k in range(idx + 1):
        draw_video_layer(ax, video_x, y, bw, k, active=(k == idx))

    ay = y + bh/2
    ax.annotate("", xy=(code_x, ay), xytext=(prompt_x + bw, ay),
                arrowprops=dict(arrowstyle="->", linewidth=2))
    ax.annotate("", xy=(video_x, ay), xytext=(code_x + bw, ay),
                arrowprops=dict(arrowstyle="->", linewidth=2))

    pulse = 0.5 + 0.5 * math.sin(i * 0.4)
    ax.annotate("", xy=(prompt_x + bw/2, y - 0.4),
                xytext=(code_x + bw/2, y - 0.4),
                arrowprops=dict(arrowstyle="<->",
                                linewidth=3 + pulse * 2,
                                linestyle="dashed"))

    ax.text((prompt_x + code_x + bw)/2, y - 0.9,
            "iterate", ha="center", va="center",
            fontsize=12, weight="bold")

    fig.savefig(path)
    plt.close(fig)

if os.path.exists(FRAMES_DIR):
    shutil.rmtree(FRAMES_DIR)
os.makedirs(FRAMES_DIR, exist_ok=True)

frames = []
for i in range(N_FRAMES):
    p = os.path.join(FRAMES_DIR, f"frame_{i:04d}.png")
    render_frame(p, i)
    frames.append(p)

clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile(OUT_MP4, fps=FPS, codec="libx264",
                     audio=False, preset="ultrafast", bitrate="1200k")

shutil.rmtree(FRAMES_DIR)
OUT_MP4
