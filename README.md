# Homework 4 - A vision language model for tux

In this homework, we will train (fine-tune) two vision-language models on the SuperTuxKart data [here](https://utexas.box.com/shared/static/qubjm5isldqvyimfj9rsmbnvnbezwcv4.zip).
The first is a generative model, as known the Multimodal Large Language Model (MLLM); the second is a contrastive model, which is a simplified version of the Contrastive Language-Image Model (CLIP).
In the first part, we will focus on the most important aspect of the VLM pipeline: The data-pipeline.
We will use vision labels of the SuperTuxKart dataset to produce question/answer labels for the same set of images.
In the second part, we will focus on building a toy CLIP model and finetune it to do multi-choice question answering.
To fuel this, we will use the the SuperTuxKart dataset to generate some paired image-captions data.
your submission might be counted as invalid.

