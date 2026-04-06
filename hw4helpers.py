"""
Preliminaries: Assumes you have a folder named dsci-531-2026-hw4 on your machine where this hw4helpers.py file is stored. 
You must have a **different** terminal open with the following command running otherwise, this will not work.

./llama-server -hf unsloth/Qwen3.5-0.8B-GGUF:Q4_K_M \
--ctx-size 16384 \
--top-p 0.8 \
--top-k 20 \
--min-p 0.00 \
--chat-template-kwargs "{\"enable_thinking\":false}", 

Open a new terminal and do the following: 

> cd dsci-531-2026-hw4
> pip install uv
> uv init
> uv add requests

> uv run hw3helpers.py 

Note: You may need to uncomment the print statements below to call the functions
"""

import requests
import base64
from PIL import Image  # uv add Pillow
import io

DEFAULT_URL = "http://127.0.0.1:8080"
DEFAULT_HEADERS = {"Content-Type": "application/json"}

# Part 1: Simple image query


def image_load_scale_base64_url(image_path, scale=1.0):
    img = Image.open(image_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")  # handle .png
    resized_image = img.resize(
        (int(img.width * scale), int(img.height * scale)),
        resample=Image.Resampling.BICUBIC,
    )
    buffered = io.BytesIO()
    resized_image.save(buffered, format="JPEG")
    return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"


def ask_image(image_path, prompt, scale=1.0):
    image_base64_url = image_load_scale_base64_url(image_path, scale=scale)
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_base64_url}},
                ],
            },
        ]
    }
    response = requests.post(
        f"{DEFAULT_URL}/v1/chat/completions", headers=DEFAULT_HEADERS, json=data
    )
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"].strip()
    return text


# print(ask_image("ff2.jpg", "What is this thing?", scale=3.0))

# Part 2: JSON-schema constrained generation for images

import json


def ask_image_schema(image_path, prompt, schema, scale=1.0):
    image_base64_url = image_load_scale_base64_url(image_path, scale=scale)
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_base64_url}},
                ],
            },
        ],
        "response_format": {"type": "json_object", "schema": schema},
    }
    response = requests.post(
        f"{DEFAULT_URL}/v1/chat/completions",
        headers=DEFAULT_HEADERS,
        json=data,
        timeout=60,
    )
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"].strip()
    obj = json.loads(text)
    return obj


YES_NO_SCHEMA = {"type": "string", "enum": ["yes", "no"]}

# print(ask_image_schema("image.png", "Does this look like a pizza to you?", YES_NO_SCHEMA))


# Part 2: D&D character sheet for each image in val_sampled

DND_SCHEMA = {
    "type": "object",
    "properties": {
        "strength": {"type": "integer"},
        "intelligence": {"type": "integer"},
        "wisdom": {"type": "integer"},
        "dexterity": {"type": "integer"},
        "constitution": {"type": "integer"},
        "charisma": {"type": "integer"},
        "alignment": {
            "type": "string",
            "enum": [
                "lawful good",
                "lawful neutral",
                "lawful evil",
                "neutral good",
                "true neutral",
                "neutral evil",
                "chaotic good",
                "chaotic neutral",
                "chaotic evil",
            ],
        },
    },
    "required": [
        "strength",
        "intelligence",
        "wisdom",
        "dexterity",
        "constitution",
        "charisma",
        "alignment",
    ],
}

DND_PROMPT = (
    "You are assigning a Dungeons & Dragons Non-Player Character sheet to the person in this image. "
    "Assign integer scores from 3 to 18 for each attribute (strength, intelligence, wisdom, dexterity, "
    "constitution, charisma) based on the person's appearance, and choose one of the nine alignments "
    "(lawful good, lawful neutral, lawful evil, neutral good, true neutral, neutral evil, "
    "chaotic good, chaotic neutral, chaotic evil). "
    "Return only the JSON object."
)


def score_image(image_path, scale=0.5):
    """Return D&D attribute dict for a single image."""
    return ask_image_schema(image_path, DND_PROMPT, DND_SCHEMA, scale=scale)


import os
import csv


def score_all_images(
    val_sampled_dir="val_sampled", output_csv="results.csv", scale=1.0
):
    """Score every image in val_sampled_dir and save results to output_csv."""
    image_files = sorted(
        f for f in os.listdir(val_sampled_dir) if f.lower().endswith(".jpg")
    )
    fields = [
        "file",
        "strength",
        "intelligence",
        "wisdom",
        "dexterity",
        "constitution",
        "charisma",
        "alignment",
    ]

    done = set()
    if os.path.exists(output_csv):
        with open(output_csv, newline="") as f:
            for row in csv.DictReader(f):
                done.add(row["file"])

    mode = "a" if done else "w"
    with open(output_csv, mode, newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields)
        if not done:
            writer.writeheader()
        for i, fname in enumerate(image_files):
            if fname in done:
                continue
            image_path = os.path.join(val_sampled_dir, fname)
            try:
                attrs = score_image(image_path, scale=scale)
                attrs["file"] = fname
                writer.writerow({k: attrs.get(k, "") for k in fields})
                out.flush()
                print(f"[{i+1}/{len(image_files)}] {fname}: {attrs}")
            except Exception as e:
                print(f"[{i+1}/{len(image_files)}] ERROR on {fname}: {e}")

    print(f"Done. Results saved to {output_csv}")


# Test on the example image
# print(score_image("ff2.jpg"))

# Run on all images
score_all_images()
