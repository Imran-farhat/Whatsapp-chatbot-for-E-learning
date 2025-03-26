
# E-Learning WhatsApp Chat Interface

A WhatsApp-themed chat interface for an e-learning virtual tutor assistant, powered by Google Gemini AI.

![Screenshot of the WhatsApp-themed E-Learning Chat Interface](https://via.placeholder.com/400x700/075E54/FFFFFF?text=E-Learning+WhatsApp+Chat)

## Features

- **WhatsApp-like UI**: Familiar chat interface with message bubbles, timestamps, and read receipts
- **Virtual Tutor Assistant**: AI-powered responses for academic questions across multiple subjects
- **Subject Categories**: Quick suggestions for math, science, English, languages, and exam prep
- **Markdown Support**: Format messages with markdown for better readability
- **Conversation History**: View and reference previous messages
- **Typing Indicators**: Visual feedback when the bot is "typing"
- **Responsive Design**: Works on both desktop and mobile devices

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python with Flask
- **AI**: Google Gemini API
- **Libraries**: 
  - Marked.js (for markdown parsing)
  - Animate.css (for UI animations)
  - Font Awesome (for icons)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/e-learning-whatsapp-chat.git
   cd e-learning-whatsapp-chat
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Configuration

You can customize the following aspects of the application:

- **Subjects**: Modify the `LEARNING_DOMAINS` list in `app.py` to add or remove subjects
- **System Prompt**: Edit the `system_prompt` in `app.py` to change the AI's behavior
- **UI Styling**: Adjust the CSS in `whatsapp-theme.css` or the inline styles in `script.js`
- **Quick Suggestions**: Update the `tutoringTopics` object in `script.js` to change the suggested questions

## Usage

1. Type your academic question in the input field and press Enter or click the send button
2. Use the category chips to get quick question suggestions
3. Format your messages with markdown for better readability
4. Click "Clear Chat" to start a new conversation

## Markdown Support

The chat supports the following markdown syntax:

| Syntax      | Description           |
|-------------|-----------------------|
| `*italic*`  | Italic text           |
| `**bold**`  | Bold text             |
| `# Heading` | Heading (level 1-6)   |
| `[Link](url)` | Hyperlink           |
| `` `code` `` | Inline code          |
| ```code block``` | Code block      |
| `> quote`    | Blockquote           |
| `- item`     | List item            |
| `1. item`    | Numbered list        |
| `---`        | Horizontal rule      |

## Screenshots

![Category Suggestions](https://via.placeholder.com/400x700/075E54/FFFFFF?text=Category+Suggestions)
![Markdown Help](https://via.placeholder.com/400x700/075E54/FFFFFF?text=Markdown+Help)
![Math Question](https://via.placeholder.com/400x700/075E54/FFFFFF?text=Math+Question)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
```

This README includes:
1. Project title and description
2. Key features
3. Technology stack
4. Installation instructions
5. Configuration options
6. Usage guide
7. Markdown support details
8. Placeholder images (you should replace these with actual screenshots)
9. License information
10. Contribution guidelines

You can customize it further by:
- Adding actual screenshots
- Including a demo link if you deploy it
- Adding more detailed documentation if needed
- Listing known issues or future enhancements
