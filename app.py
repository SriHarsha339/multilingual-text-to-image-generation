from googletrans import Translator
from diffusers import StableDiffusionPipeline
from huggingface_hub import login
from flask import Flask, request, jsonify, render_template_string
import torch 
import io
import base64
from PIL import Image


# Initialize Flask app
app = Flask(__name__)

# Function to translate the input text
def get_translation(text, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest_lang)
    return translated_text.text


class CFG:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    seed = 42
    image_gen_steps = 35
    image_gen_model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
    image_gen_size = (600, 600)
    image_gen_guidance_scale = 9
    # Add your Hugging Face API key here or use environment variables
    api_key = "Hugging Face API"

# Login to Hugging Face Hub using the API key
login(CFG.api_key)

# Load the model using the Hugging Face Hub
pipe = StableDiffusionPipeline.from_pretrained(
    CFG.image_gen_model_id,
    torch_dtype=torch.float16,
    use_auth_token=True  # This will use the API key
)

# Move the model to the appropriate device
pipe = pipe.to(CFG.device)

# Function to generate multiple images
def generate_images(prompt, model, num_images=3):
    images = []
    for _ in range(num_images):
        image = model(
            prompt,
            num_inference_steps=CFG.image_gen_steps,
            guidance_scale=CFG.image_gen_guidance_scale
        ).images[0]

        # Resize the image if needed
        image = image.resize(CFG.image_gen_size)
        images.append(image)
    return images

# HTML structure embedded in the Python script
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multilingual Image Generation</title>
    <style>
        body {
    font-family: Arial, sans-serif;
    background-color: #f7f8fc;
    margin: 0;
    padding: 20px;
    color: #333;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #fff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease-in-out;
}

.container:hover {
    transform: scale(1.02);
}

h1 {
    text-align: center;
    font-size: 28px;
    color: #4CAF50;
}

label {
    display: block;
    margin-top: 20px;
    font-size: 18px;
    color: #555;
}

input[type="text"], select {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    margin-bottom: 20px;
    border: 2px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
}

button {
    width: 100%;
    padding: 12px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
}

button:hover {
    background-color: #45a049;
}

.output-images {
    display: flex;
    justify-content: space-between;
    gap: 30px; /* Adds space between image blocks */
    margin-top: 30px;
}

.output-images div {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 30%; /* Adjusts width for each image block */
    transition: transform 0.2s ease;
}

.output-images div:hover {
    transform: scale(1.05);
}

.output-images img {
    max-width: 100%;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 12px; /* Adds space between the image and the download button */
}

.download-btn {
    display: block;
    margin-top: 10px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    text-align: center;
    border-radius: 8px;
    text-decoration: none;
    font-size: 16px;
    transition: background-color 0.3s ease-in-out;
}

.download-btn:hover {
    background-color: #0056b3;
}

.loading {
    display: none;
    text-align: center;
    margin-top: 20px;
}

.loading .spinner {
    border: 8px solid #f3f3f3; /* Light grey */
    border-top: 8px solid #4CAF50; /* Green */
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

    </style>
</head>
<body>

<div class="container">
    <h1>Multilingual Image Generation</h1>
    
    <label for="textPrompt">Enter Text Prompt:</label>
    <input type="text" id="textPrompt" placeholder="Type your prompt here..." required>

    <label for="languageSelect">Select Language:</label>
    <select id="languageSelect">
        <option value="en">English</option>
    </select>

    <button onclick="generateImages()">Generate Images</button>

    <div class="loading" id="loading">Generating images, please wait...</div>

    <div class="output-images" id="outputImages">
        <!-- Generated images will appear here -->
    </div>
</div>

<script>
    function generateImages() {
        const prompt = document.getElementById('textPrompt').value;
        const language = document.getElementById('languageSelect').value;

        if (prompt === "") {
            alert("Please enter a prompt.");
            return;
        }

        document.getElementById('loading').style.display = 'block';
        document.getElementById('outputImages').innerHTML = '';

        fetch('/generate-images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt, language: language }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').style.display = 'none';

            data.images.forEach((image, index) => {
                const imgElement = `<div>
                    <img src="data:image/png;base64,${image}" alt="Generated Image ${index+1}">
                    <a href="data:image/png;base64,${image}" download="generated_image_${index+1}.png" class="download-btn">Download Image ${index+1}</a>
                </div>`;
                document.getElementById('outputImages').innerHTML += imgElement;
            });
        })
        .catch(error => {
            document.getElementById('loading').style.display = 'none';
            console.error('Error:', error);
        });
    }
</script>

</body>
</html>
"""

# Flask route to serve the HTML page
@app.route('/')
def index():
    return render_template_string(html_code)

# Flask route to handle the image generation
@app.route('/generate-images', methods=['POST'])
def generate_images_endpoint():
    data = request.json
    prompt = data['prompt']
    language = data['language']

    # Translate the prompt to English
    translated_prompt = get_translation(prompt, "en")

    # Generate 3 images using Stable Diffusion
    images = generate_images(translated_prompt, pipe, num_images=3)

    # Convert images to base64
    image_data = []
    for image in images:
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
        image_data.append(img_base64)

    return jsonify({'images': image_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
