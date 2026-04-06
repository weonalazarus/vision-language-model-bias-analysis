# Bias in Vision-Language Models — DSCI 531 HW4

A study of demographic bias in the outputs of a locally-hosted Vision-Language Model (VLM). Each face image from the FairFace dataset was prompted to produce a D&D Non-Player Character sheet, revealing how the model assigns attributes and moral alignment based on appearance.

---

## Model

| Setting | Value |
|---------|-------|
| Model | Qwen3.5-0.8B (GGUF, Q4_K_M quantization) |
| Server | llama-server (llama.cpp) |
| Context | 16,384 tokens |
| Sampling | top-p=0.8, top-k=20, min-p=0.0 |
| Output | JSON-constrained schema |
| Images | 300 (FairFace val_sampled) |

---

## Dataset (Part 1)

300 images from the FairFace validation set.

**Race distribution**
| Race | Count | % |
|------|-------|---|
| White | 58 | 19.3% |
| Latino/Hispanic | 45 | 15.0% |
| East Asian | 43 | 14.3% |
| Black | 43 | 14.3% |
| Indian | 41 | 13.7% |
| Southeast Asian | 39 | 13.0% |
| Middle Eastern | 31 | 10.3% |

**Age distribution**
| Age | Count | % |
|-----|-------|---|
| 0-2 | 5 | 1.7% |
| 3-9 | 38 | 12.7% |
| 10-19 | 32 | 10.7% |
| 20-29 | 92 | 30.7% |
| 30-39 | 64 | 21.3% |
| 40-49 | 36 | 12.0% |
| 50-59 | 23 | 7.7% |
| 60-69 | 10 | 3.3% |

**Gender distribution**
| Gender | Count | % |
|--------|-------|---|
| Male | 161 | 53.7% |
| Female | 139 | 46.3% |

---

## Quantitative Findings (Part 3a)

### Overall mean attribute scores (across all 300 images)

| Attribute | Mean |
|-----------|------|
| Strength | 10.72 |
| Intelligence | 10.87 |
| Wisdom | 10.50 |
| Dexterity | 9.82 |
| Constitution | 10.22 |
| Charisma | 10.06 |

Scores cluster tightly around 10-11, close to the statistical average for a 3-18 range (10.5). The model shows little variance, suggesting it defaults to average values regardless of image content.

### By Gender

| Attribute | Male | Female |
|-----------|------|--------|
| Strength | 10.76 | 10.67 |
| Intelligence | 10.86 | 10.87 |
| Wisdom | 10.41 | 10.61 |
| Dexterity | 9.89 | 9.73 |
| Constitution | 10.35 | 10.08 |
| Charisma | 9.98 | 10.14 |

Gender differences are minimal across all attributes. Female subjects scored marginally higher in wisdom and charisma; male subjects slightly higher in strength and constitution — reflecting common D&D gender tropes.

### By Race (Strength / Intelligence / Charisma)

| Race | Strength | Intelligence | Charisma |
|------|----------|-------------|---------|
| Black | 11.14 | 10.63 | 9.93 |
| East Asian | 11.21 | 10.84 | 10.14 |
| Indian | 10.61 | 10.90 | 10.29 |
| Latino/Hispanic | 9.58 | 10.49 | 9.78 |
| Middle Eastern | 11.00 | 11.39 | 10.23 |
| Southeast Asian | 11.08 | 11.08 | 10.36 |
| White | 10.60 | 10.91 | 9.84 |

Notable: Latino/Hispanic subjects received the lowest mean strength (9.58) and charisma (9.78). Middle Eastern subjects received the highest mean intelligence (11.39). These patterns likely reflect biases encoded in the model's training data.

### By Age (All Attributes)

| Age | Str | Int | Wis | Dex | Con | Cha |
|-----|-----|-----|-----|-----|-----|-----|
| 0-2 | 10.2 | 7.2 | 7.0 | 8.2 | 9.0 | 5.8 |
| 3-9 | 10.89 | 10.66 | 10.34 | 9.74 | 9.89 | 10.05 |
| 10-19 | 10.38 | 10.59 | 10.34 | 9.50 | 9.47 | 9.69 |
| 20-29 | 11.21 | 11.36 | 11.01 | 10.27 | 10.62 | 10.60 |
| 30-39 | 10.36 | 10.69 | 10.17 | 9.83 | 10.14 | 10.25 |
| 40-49 | 10.44 | 11.22 | 10.50 | 9.72 | 10.75 | 10.39 |
| 50-59 | 10.39 | 10.70 | 10.70 | 9.35 | 10.04 | 9.43 |
| 60-69 | 10.90 | 10.10 | 10.40 | 9.10 | 9.90 | 7.40 |

The strongest bias is in **charisma by age**: infants (0-2) score 5.8 and elderly (60-69) score 7.4, while young adults (20-29) peak at 10.6. Intelligence follows a similar arc. This suggests the model associates youth and middle adulthood with higher social and mental attributes.

---

## Alignment Findings (Part 3b)

### Distribution

| Alignment | Count | % |
|-----------|-------|---|
| Lawful Good | 201 | 67.0% |
| Lawful Neutral | 59 | 19.7% |
| Neutral Good | 18 | 6.0% |
| Lawful Evil | 7 | 2.3% |
| Chaotic Neutral | 7 | 2.3% |
| Chaotic Good | 4 | 1.3% |
| Neutral Evil | 2 | 0.7% |
| Chaotic Evil | 2 | 0.7% |

**Key finding:** 67% of all images were assigned "lawful good" — a dramatic positive bias. Evil alignments appear in fewer than 4% of cases combined. This is a strong "halo effect": the model defaults to flattering moral descriptions of human faces regardless of demographic characteristics.

### Top 3 Alignments — Observations

**Lawful Good (n=201):** The dominant alignment across all demographic groups. No single race, gender, or age group was disproportionately excluded. The model appears to assign this as a near-default for human faces.

**Lawful Neutral (n=59):** The second most common alignment. Appeared more frequently for older subjects and images with more neutral/expressionless faces. Suggests the model interprets stoic or aged appearances as less "good" but still orderly.

**Neutral Good (n=18):** A smaller group with a slight skew toward younger and female subjects, possibly because the model associates youth and femininity with warmth but less structure.

---

## Key Takeaways

1. **Positive alignment bias:** The model overwhelmingly assigns lawful/good alignments to human faces. This "halo effect" makes bias detection in alignment harder since almost everyone is rated positively.
2. **Age is the strongest demographic signal:** Charisma and intelligence scores drop significantly for very young and elderly subjects — the model penalizes age in social/mental attributes.
3. **Race differences are subtle but present:** Latino/Hispanic subjects consistently scored lower in strength and charisma; Middle Eastern subjects scored higher in intelligence. These patterns likely reflect stereotypes in training data.
4. **Gender differences are minimal:** Attribute scores differ by less than 0.5 points on average between male and female subjects.

---

## AI Tool Disclosure

Claude Code (claude-sonnet-4-6) was used as an assistant to write and debug Python code, troubleshoot llama-server setup, and generate the writeup. All analysis and conclusions were reviewed by the student.
