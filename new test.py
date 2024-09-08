import gradio as gr
import openai
import base64
from PIL import Image
import io
from dotenv import load_dotenv
import os
load_dotenv()
key = os.environ.get("OPENAI_API_KEY")
import requests

def generate_summary(image,text):
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"You are provided with an image and you have to describe testing instructions for any digital product's features, based on the screenshots.Output should describe a detailed, step-by-step guide on how to test each functionality. Each test case should include: Description: What the test case is about. Pre-conditions: What needs to be set up or ensured before testing. Testing Steps: Clear, step-by-step instructions on how to perform the test. Expected Result: What should happen if the feature works correctly.. Also some additional info on the image is : {text}"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    resp = response.json()
    print (resp)
    return resp['choices'][0]['message']['content']

iface = gr.Interface(
    fn=generate_summary,
    inputs= [ gr.Image(type="pil"),gr.Textbox(lines=2, placeholder="Enter text here...")],
    outputs="text",
    title="Tool Functionality Summarizer",
    description="Upload an image to get a summary of the tool's functionality.",
    allow_flagging= "never"
)

iface.launch(debug=True)
