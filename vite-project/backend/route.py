import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

# Configure the Google AI API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the Flask app
app = Flask(__name__)
CORS(app)  # Add CORS support

# Set the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/backend/route', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('input')
        
        # Create a new chat session
        chat_session = model.start_chat(history=[])
        
        # Send the user input to the model
        response = chat_session.send_message(user_input)
        
        # Return the generated response
        return jsonify({'response': response.text})
    except Exception as e:
        # Log the error
        print(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))  # Default to port 3000 if not specified
    app.run(host='0.0.0.0', port=port)
