
---

# 🌐 Multilingual Text to Image Generation

A Flask-based web application that leverages NLP translation and Stable Diffusion image generation to create images from multilingual text prompts. Perfect for quickly visualizing ideas in different languages using cutting-edge AI technologies.

---

## 🔍 Overview

**Multilingual Text to Image Generation** is designed to transform your text prompts into visual art seamlessly. The application performs the following key tasks:

- Translates non-English prompts to English using **googletrans**.
- Generates images based on the translated prompt using the **Stable Diffusion** model provided by [diffusers](https://github.com/huggingface/diffusers) on the Hugging Face Hub.
- Serves a modern, responsive front-end via a Flask web server.
- Provides downloadable images in PNG format.

This project combines state-of-the-art translation and image generation to deliver visually engaging and multilingual outputs.

---

## ✨ Features

- **🌏 Multilingual Support:** Translate user prompts to English to enable image generation from texts in any language.
- **🎨 Image Generation:** Uses the Stable Diffusion model to generate art from text, with customizable inference parameters.
- **🔒 Secure API Integration:** Leverages Hugging Face Hub for secure and authenticated model access.
- **🖼️ Interactive Web Interface:** A clean, responsive HTML interface with real-time progress feedback and image downloads.
- **🚀 Scalable Architecture:** Easily extendable and customizable for additional features or models.

---

## 🚀 Installation

1. **Clone the Repository:**

   ```bash
   gh repo clone SriHarsha339/multilingual-text-to-image-generation
   cd multilingual-text-to-image-generation


2. **Install Dependencies:**

   Ensure you have Python 3.7+ installed. Then, install the required libraries using:

   ```bash
   pip install -r requirements.txt
   ```

   *(The `requirements.txt` includes packages like `googletrans==4.0.0-rc1`, `diffusers`, `huggingface_hub`, `Flask`, `torch`, and `Pillow`.)*

3. **Configure API Keys:**

   - Open `app.py` and replace the placeholder API keys with your own:
     - **Hugging Face API Key:** Replace the value of `CFG.api_key`.
     - **Additional configuration** can be done via environment variables if desired.

---

## 🎬 Usage

1. **Run the Application:**

   Start the Flask server by running:

   ```bash
   python app.py
   ```

2. **Access the Web Interface:**

   Open your browser and navigate to [http://0.0.0.0:5000](http://0.0.0.0:5000). You will see the interface where you can:
   
   - Input your **text prompt**.
   - Choose a **language** (currently, only English is enabled, though you can extend this functionality).
   - Click on "Generate Images" to view and download generated images.

3. **Download Images:**

   Each generated image comes with a download button, allowing you to save the image locally.

---

## 💻 Code Overview

- **Translation:**

  ```python
  from googletrans import Translator
  
  def get_translation(text, dest_lang):
      translator = Translator()
      translated_text = translator.translate(text, dest=dest_lang)
      return translated_text.text
  ```
  
  Translates the input text into English (or another specified language).

- **Image Generation:**

  ```python
  from diffusers import StableDiffusionPipeline
  from huggingface_hub import login
  import torch
  
  # Model configuration and device setup inside CFG class.
  # Login and load the pipeline:
  login(CFG.api_key)
  pipe = StableDiffusionPipeline.from_pretrained(
      CFG.image_gen_model_id,
      torch_dtype=torch.float16,
      use_auth_token=True
  ).to(CFG.device)
  ```
  
  Uses the Stable Diffusion model to generate images based on the translated prompt.

- **Flask Web Server:**

  The Flask routes serve the HTML interface and handle POST requests to generate images, converting them to base64 for seamless inline display.

- **HTML Interface:**

  The embedded HTML (served using `render_template_string`) provides a modern UI with input fields, loading animations, and download options.

For full details, review the `app.py` file in this repository.

---

## 🤝 Contributing

Contributions are very welcome! If you'd like to help improve the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add new features'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Submit a pull request.

---

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

For questions, suggestions, or feedback, please contact:

**Gowtham Sri Harsha**  
Email: [harshakota339@gmail.com](mailto:harshakota339@gmail.com)  
[LinkedIn](https://www.linkedin.com/in/gowthamsriharsha)  
[GitHub](https://github.com/SriHarsha339)

---

Happy generating and translating! 🚀
```
