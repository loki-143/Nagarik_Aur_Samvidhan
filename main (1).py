from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import time

app = Flask(__name__)

# Configure the generative AI model with your API key
genai.configure(api_key="AIzaSyCV7pLU5IN8btkJ72BjLxK547cMc1lJOGY")

# Upload the file once and store the file reference
def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Wait for the files to be active
def wait_for_files_active(files):
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Configure the generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# Upload the file only once when the app starts
uploaded_files = [upload_to_gemini(r"C:\Users\annep\OneDrive\Desktop\web development\COI.pdf", mime_type="application/pdf")]
wait_for_files_active(uploaded_files)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.json
    question = data.get('question')

    # Assuming you no longer need the age group as you removed it in the form
    prompt = f"{question} without any extra information."

    # Start a new chat session with the model and the uploaded file
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    uploaded_files[0],  # Reusing the already uploaded file
                    "When a user asks about a concept from the provided PDF, explain it in a simplified and concise manner. Adapt the explanation to the age of the person, ensuring it's appropriate for their level of understanding.\n",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Please provide me with the concept you want explained, and I'll do my best to give a simplified answer appropriate for the age of the person you've specified.\n",
                ],
            },
        ]
    )

    # Send the user's question as a prompt to the model
    response = chat_session.send_message(prompt)

    # Return the generated response as JSON
    return jsonify({'answer': response.text})

if __name__ == '__main__':
    app.run(port=5000)
