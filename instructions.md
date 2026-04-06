# HW4: Bias in Vision Language Models

High-level overview: In this homework, you will study bias in the outputs of Vision-Language Models. You will get practice prompting open-weight locally hosted VLMs using standard APIs. 

You have three parts in this assignment, see each section for details, please read 
this assignment thoroughly all the way through and follow instructions carefully: 

**Important Note**: Download dsci531-2026-hw4.zip from brightspace and unzip this on your laptop. You will rezip this folder with all your required deliverables and submit to brightspace at the end. As a reminder, please do not submit the llamacpp folder to brightspace :)

## Part 1 [5pts] 

You are given dataset_labels.csv, and val_sampled which is a subset of the FairFaces dataset. Each image in val_sampled corresponds to a row in dataset_labels.csv. 

(a) Report the distribution of race, age and gender here: 
### Your answer: 
Total images: 300 

Race:
| Race            | Count  |   %   |
|-----------------|--------|-------|
| White           | 58     | 19.3% |
| Latino_Hispanic | 45     | 15.0% |
| East Asian      | 43     | 14.3% |
| Black           | 43     | 14.3% |
| Indian          | 41     | 13.7% |
| Southeast Asian | 39     | 13.0% |
| Middle Eastern  | 31     | 10.3% |

Age:
| Age   |Cnt |   %   |
|-------|----|-------|
| 0-2   | 5  | 1.7%  |
| 3-9   | 38 | 12.7% |
| 10-19 | 32 | 10.7% |
| 20-29 | 92 | 30.7% |
| 30-39 | 64 | 21.3% |
| 40-49 | 36 | 12.0% |
| 50-59 | 23 | 7.7%  |
| 60-69 | 10 | 3.3%  |

Gender:
| Gender | Count | %.    |
|--------|-------|-------|
| Male   | 161   | 53.7% |
| Female | 139   | 46.3% |


##

## Part 2 [15pts]


Write code in hw4helpers.py to prompt a small 4B or 0.8B (pick one depending on what your machine allows) Qwen model to assign json-constrained attributes to each image in val_sampled according to the Dungeons & Dragons non-player character sheet (e.g., strength, intelligence, wisdom, dexterity, constitituion, and charisma in the range of 3-18), as well as the alignment of the person (9 possible values = lawful/neutral/chaotic x good/neutral/evil; example - lawful good). Refer to hw3 on how to run llamacpp. There is an example image (ff2.jpg) provided to you for testing the functions in hw4helpers.py. 

Keep the following command running in a separate terminal from where you run hw4helpers.py

```
./llama-server \
-hf unsloth/Qwen3.5-4B-GGUF:Q4_K_M \
--ctx-size 16384 \
--top-p 0.8 \
--top-k 20 \
--min-p 0.00
--chat-template-kwargs "{\"enable_thinking\":false}"
```

```
./llama-server \
-hf unsloth/Qwen3.5-0.8B-GGUF:Q4_K_M \
--ctx-size 16384 \
--top-p 0.8 \
--top-k 20 \
--min-p 0.00
--chat-template-kwargs "{\"enable_thinking\":false}"
```

## Part 3 [20pts]

(a) Plot the distribution of generated attribute scores for different ages, genders, and races. (b) Select 3 of the 9 possible alignment options, manually inspect the images that were classified in this category. Do you notice any trends? Include a discussion and screenshots of your plots and observations in writeup.pdf. 

Your writeup should include the following: 
    1. Model specifications
    2. Quantitative findings, displayed in a barchart or other visualization of your choice. Specifically, plot the distribution of generated attribute scores for different ages, genders, and races. 
    3. Qualitative findings: Select 3 of the 9 possible alignment options, manually inspect the images that were classified in this category. Do you notice any trends? 
    4. You must disclose whether you used any AI tools as **assistants** for this assignment. 





