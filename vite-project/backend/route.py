import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import random

# Configure the Google AI API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the Flask app
app = Flask(__name__)
CORS(app)  # Add CORS support

# Set the generation configuration
generation_config = {
    "temperature": 0.7,  # Adjusted for more coherent responses
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 150,  # Adjusted to limit response length
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
        
        # Format the response for a more conversational tone
        formatted_response = format_response(response.text)
        
        # Return the generated response
        return jsonify({'response': formatted_response})
    except Exception as e:
        # Log the error
        print(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

def format_response(response_text):
    """
    Formats the response to resemble ChatGPT or Claude style outputs.
    This function adds structure by breaking the response into paragraphs,
    using a conversational tone, and applying friendly language.
    """
    # Trim the response text
    formatted_response = response_text.strip()

    # Define delimiters for headings and bullet points
    headings = ["##", "#"]
    bullet_points = ["*"]

    # Initialize formatted response
    formatted_response_parts = []

    # Split text into paragraphs based on double new lines
    paragraphs = formatted_response.split("\n\n")

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        # Check for headings
        if any(paragraph.startswith(heading) for heading in headings):
            formatted_response_parts.append(paragraph)
        # Check for bullet points
        elif any(paragraph.startswith(bullet) for bullet in bullet_points):
            formatted_response_parts.append(paragraph)
        else:
            # Regular paragraph formatting
            formatted_response_parts.append(paragraph)

    # Join the formatted paragraphs with double new lines
    formatted_response = "\n\n".join(formatted_response_parts)

    # Add a friendly greeting or introduction
    greetings = [
        "Hi there! 😊",
        "Hello! How can I assist you today? 👋",
        "Hey! How can I help you? 👋"
    ]
    formatted_response = random.choice(greetings) + "\n\n" + formatted_response

    # Add a friendly closing statement
    closing_statements = [
        "I hope this helps! If you have any more questions, feel free to ask.",
        "Let me know if you need anything else. I'm here to help!",
        "Is there anything else I can assist you with? 😊"
    ]
    formatted_response += "\n\n" + random.choice(closing_statements)

    return formatted_response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))  # Default to port 3000 if not specified
    app.run(host='0.0.0.0', port=port)
