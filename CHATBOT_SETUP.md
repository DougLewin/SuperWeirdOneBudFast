# Chatbot Setup Guide

## Overview
The application now includes an AI-powered chatbot using Google's Gemini API. The chatbot appears as a floating button in the bottom-right corner of the page and persists across all views.

## Features
- **Persistent floating interface**: Chat button always visible in bottom-right corner
- **Popover design**: Chat opens in a styled popover overlay
- **Session persistence**: Chat history maintained during your session
- **Responsive design**: Adapts to mobile and desktop screens
- **Generic AI assistant**: Currently answers any questions (will be restricted to weather/forecasting in future updates)

## Configuration

### Local Development
1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.streamlit/secrets.toml` file in your project root if it doesn't exist
3. Add your API key:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### Streamlit Cloud Deployment
1. Go to your app settings in Streamlit Cloud
2. Navigate to the "Secrets" section
3. Add the following:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

## Usage
1. Click the 💬 button in the bottom-right corner
2. Type your question in the chat input
3. Press Enter to send
4. The AI will respond based on Google Gemini's knowledge
5. Click "🗑️ Clear Chat" to reset the conversation
6. Click outside the popover or the 💬 button again to close

## Technical Details

### Dependencies
- `google-generativeai`: Official Python SDK for Google Gemini API
- Already added to `requirements.txt`

### Implementation
- **Model**: `gemini-pro` (Google's text generation model)
- **Chat History**: Stored in Streamlit session state
- **UI Component**: `st.popover()` with custom CSS styling
- **Position**: Fixed positioning with z-index 999 for persistent visibility

### CSS Customization
The chatbot button and popover are styled to match the app's color scheme:
- Button: Gradient background with teal/cyan colors
- Border: Matches the app's accent color (#2eecb5)
- Popover: Dark theme consistent with the main interface
- Responsive: Adjusts size and position on mobile devices

## Future Enhancements
- Restrict responses to weather and forecasting topics
- Integration with app data (surf conditions, forecasts, etc.)
- Suggested prompts based on current view
- Enhanced context awareness about Rottnest Island conditions
- Voice input/output capabilities

## Troubleshooting

### Chatbot Not Available
If you see "❌ Chatbot is not available", check:
1. GEMINI_API_KEY is set in secrets
2. API key is valid and active
3. Internet connection is working

### API Errors
- **Quota exceeded**: You've hit the free tier limit (wait or upgrade)
- **Invalid API key**: Double-check your key in secrets
- **Network errors**: Check your internet connection

### UI Issues
- **Button not visible**: Check if CSS is loading properly
- **Popover not styled**: Clear browser cache and reload
- **Mobile display issues**: Try different viewport sizes

## Cost Considerations
- Gemini API has a generous free tier
- Monitor usage at [Google AI Studio](https://makersuite.google.com/)
- Consider rate limiting for production use

## Security Notes
- Never commit API keys to version control
- Use Streamlit secrets for secure storage
- Rotate keys periodically
- Monitor API usage for unexpected spikes
