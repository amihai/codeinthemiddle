# Code-In-The-Middle 
**Code-In-The-Middle Prompt Engineering Technique to Create Editable, Coherent Content**

What if, instead of generating content such as videos or images directly with AI, we first generate Python code that produces that content?

So instead of editing the video directly, we use AI to edit the Python code that generates the video.

[Code In The Middle](https://youtu.be/NGY_J58c7nk?si=rogKp1_uWriFM_sr)

## Benefits

This approach has multiple benefits:

- **Coherence and determinism**  
  We can iterate many times on the content editing while preserving consistency across edits.

- **Control**  
  We can fine-tune or modify any aspect of the video without impacting the rest, because we are modifying the intermediary code.

- **Cost reduction**  
  Generating code is much cheaper than generating videos directly.

- **Explainability and debugging**  
  By using intermediary Python code, we can clearly see how the video is generated and manually adjust specific aspects such as text, colors, or frames.

These Code-In-The-Middle techniques can be applied on top of any DSL (Domain-Specific Language). The power of this method lies in using AI only to create and edit the DSL code, and then relying on deterministic, non-AI methods to generate the actual content.

## How It Works

First, start with a prompt like:

```text
I want to create a short video (15 seconds) about Kubernetes pod autoscaling.
First, create Python code that generates the video.
Use any Python libraries you prefer to generate diagrams and merge them into a short video frame by frame.
Run the code and provide the resulting video.
```
After we get the first iteration of the video/image we continue editing specific parts in a Chatbot conversation mode.

