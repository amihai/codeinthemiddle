# Code-In-The-Middle 
**Code-In-The-Middle is a Prompt Engineering Technique to Create Editable, Coherent Content**

Instead of generating content such as videos or images directly with AI, we first generate Python code that produces (render) that content.

So instead of editing the video directly, we use AI to edit the Python code that will be rendered as video.

The Code is the determinitistc contract between the AI Assistant and Final Artifact rendering (video/image/etc). The Code can be Python code or any executable Domain-Specific Language (DSL).

![Code In The Middle](CodeInTheMiddle.png)



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

The power of this method lies in using **AI only to create and edit the DSL code, and then relying on deterministic, non-AI methods to render the actual content**.

## How It Works

### In ChatGPT 

First, start with a prompt like:

```text
I want to create a short video (15 seconds) about Kubernetes pod autoscaling.
First, create Python code that generates the video.
Use any Python libraries you prefer to generate diagrams and merge them into a short video frame by frame.
Run the code and provide the resulting video.
```

After we get the first iteration of the video/image we continue editing specific parts in a Chatbot conversation mode (Ai Assistant).

Example of Result: [https://youtu.be/NGY_J58c7nk?si=F_4n3IyNqfcsJ04O](https://youtu.be/NGY_J58c7nk?si=F_4n3IyNqfcsJ04O) 

## As an AGENT

WORK IN PROGRESS: Develop an agent that abstracts the prompt-engineering layer and provides a more reliable DSL for generating videos and images. Follow the progress on [Github andreimihai](https://github.com/amihai/codeinthemiddle)

## Limitations

This method works only if we have a DSL (Domain-Specific Language) for a task. For example, we already have Python libraries for generating images and videos. However, we need to develop many more DSLs so that we can generate more diverse and complex content.


# Author

[Andrei Mihai](https://www.linkedin.com/in/andrei1985/)

