from flask import Flask, request, jsonify, render_template, session
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import logging
import re
import random
import uuid

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # For session management

# Get Google Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize the Gemini client
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    logger.error("Google Gemini API key is not set! Make sure you have a .env file with GEMINI_API_KEY")
    client = None

# Store conversation history in memory only (will be cleared on server restart)
conversation_history = {}

# E-learning focused topics 
LEARNING_DOMAINS = [
    "math", "mathematics", "algebra", "calculus", "geometry", "trigonometry", "statistics",
    "science", "physics", "chemistry", "biology", "anatomy", "astronomy", "geology",
    "english", "literature", "grammar", "writing", "essay", "poetry", "reading",
    "history", "geography", "social studies", "civics", "economics", "politics",
    "computer", "programming", "coding", "python", "javascript", "html", "css",
    "language", "spanish", "french", "german", "italian", "chinese", "japanese",
    "study", "exam", "test", "quiz", "homework", "assignment", "project",
    "learn", "education", "course", "class", "school", "college", "university",
    "academic", "tutor", "teaching", "student", "professor", "instructor", "curriculum"
]

@app.route('/')
def home():
    # Create a unique session ID if not exists - but don't persist history
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        # Initialize an empty conversation history for this session
        conversation_history[session['session_id']] = []
        
    return app.send_static_file('index.html')

def is_learning_query(query):
    """Check if the query is related to learning or chat functionality."""
    query_lower = query.lower()
    
    # Accept chat history and self-reference queries
    chat_patterns = [
        r"(previous|last|earlier) (message|prompt|question)",
        r"what (did|was) (i|you) (say|ask|told|tell)",
        r"(show|display|get|fetch) (my|the) (history|conversation)",
        r"what (is|was) my",
        r"can you (remember|recall)",
        r"who (am i|are you)"
    ]
    
    for pattern in chat_patterns:
        if re.search(pattern, query_lower):
            return True
    
    # Check for e-learning keywords
    for domain in LEARNING_DOMAINS:
        if domain in query_lower:
            return True
            
    # Check for learning question patterns
    learning_patterns = [
        r"how (to|do|does|can) .+\?",
        r"what (is|are|was|were) .+\?",
        r"where (is|are|can) .+\?",
        r"when (did|was|should|can|will) .+\?",
        r"why (is|are|does|do) .+\?",
        r"explain .+",
        r"define .+",
        r"solve .+",
        r"help .+",
        r"teach .+"
    ]
    
    for pattern in learning_patterns:
        if re.search(pattern, query_lower):
            return True
            
    return False

@app.route('/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY or not client:
        logger.error("Google Gemini API key is missing or client initialization failed")
        return jsonify({"error": "Google Gemini API key not set. Please check your .env file."}), 500

    try:
        # Get user input from the request
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400

        user_input = data.get('message')
        logger.debug(f"Received user input: {user_input}")
        
        if not user_input:
            logger.error("No message provided in request")
            return jsonify({"error": "No message provided"}), 400
            
        # Get or create session ID
        session_id = session.get('session_id')
        if not session_id or session_id not in conversation_history:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            conversation_history[session_id] = []
        
        # Add user message to history
        conversation_history[session_id].append({
            "role": "user",
            "content": user_input
        })

        # Check if the query is learning related
        if not is_learning_query(user_input):
            bot_response = "I'm your virtual tutor assistant and can help with subjects like math, science, languages, history, and more. Could you please ask me something related to your studies?"
            
            # Add bot response to history
            conversation_history[session_id].append({
                "role": "assistant",
                "content": bot_response
            })
            
            # Limit history size (keep last 20 messages)
            if len(conversation_history[session_id]) > 20:
                conversation_history[session_id] = conversation_history[session_id][-20:]
                
            return jsonify({
                "reply": bot_response,
                "history": conversation_history[session_id]
            })
        
        # Craft a more flexible system prompt that allows chat functionality
        system_prompt = """You are EduTutor, a friendly and knowledgeable e-learning assistant focused on helping students with their academic questions while maintaining a natural conversation.

Your primary focus is educational content, but you should also:
1. Be able to respond to questions about the conversation history
2. Answer when users ask about their previous messages or prompts
3. Remember and reference previous questions and answers when relevant

When explaining educational concepts:
- Break down complex ideas using simple language
- Use examples to illustrate points (e.g., math problems, science concepts)
- Provide step-by-step explanations for problem-solving
- Suggest additional resources for learning when appropriate
- Format content to be engaging and easy to understand

If someone asks to see their previous message or what they asked before, show them their previous prompt.
Maintain a conversational, WhatsApp-like friendly tone while being informative and helpful.

If you're not sure about a specific fact or concept, acknowledge the uncertainty rather than providing potentially incorrect information."""

        # Prepare the content structure with conversation history
        contents = []
        
        # Add system prompt as the first message
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=system_prompt)]
            )
        )
        
        # Add previous conversation history (limited to last few exchanges for context)
        history_to_include = conversation_history[session_id][-10:] if len(conversation_history[session_id]) > 5 else conversation_history[session_id]
        
        for message in history_to_include:
            role = "user" if message["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=message["content"])]
                )
            )
            
        # Configure the content generation
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=1024,
            response_mime_type="text/plain",
        )

        # Make the API call
        logger.debug("Sending request to Gemini 2.0 Flash")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=generate_content_config,
        )
        
        # Extract the bot's reply
        bot_reply = response.text
        
        # Add bot response to history
        conversation_history[session_id].append({
            "role": "assistant",
            "content": bot_reply
        })
        
        # Limit history size (keep last 20 messages)
        if len(conversation_history[session_id]) > 20:
            conversation_history[session_id] = conversation_history[session_id][-20:]
            
        logger.debug(f"Received response from Google Gemini: {bot_reply[:100]}...")
        return jsonify({
            "reply": bot_reply, 
            "history": conversation_history[session_id]
        })

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to fetch conversation history
@app.route('/history', methods=['GET'])
def get_history():
    session_id = session.get('session_id')
    if not session_id or session_id not in conversation_history:
        return jsonify({"history": []})
    
    return jsonify({"history": conversation_history[session_id]})

# Route to clear conversation history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session_id = session.get('session_id')
    if session_id and session_id in conversation_history:
        conversation_history[session_id] = []
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)