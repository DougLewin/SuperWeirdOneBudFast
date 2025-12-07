# Chatbot Setup Guide

## Overview
The application now includes an AI-powered surf forecasting chatbot using Google's Gemini API. The chatbot appears as a floating 🌊 button in the bottom-left corner of the page and persists across all views.

## Features
- **Persistent floating interface**: Chat button always visible in bottom-left corner
- **Popover design**: Chat opens in a styled popover overlay
- **Session persistence**: Chat history maintained during your session
- **Responsive design**: Adapts to mobile and desktop screens
- **Surf-focused AI assistant**: Specialized for surf and weather forecasting
- **Multi-source forecasts**: Checks 4 different surf forecast sources

## Forecast Sources
The chatbot is configured to ONLY use these 4 sources:
1. **Seabreeze** - https://www.seabreeze.com.au
2. **Surfline** - https://www.surfline.com/
3. **Windy** - https://www.windy.com/-Waves-waves
4. **BOM** (Bureau of Meteorology) - https://www.bom.gov.au/

## Response Format
The chatbot provides:
- **Wind**: Speed (knots) and direction for each source
- **Swell**: Size (meters) and direction for each source
- **Tide**: Height and timing (when available)
- **Comparison**: Shows what each website predicts (often differ)
- **Concise**: Under 100 words per response

## Usage
1. Click the 🌊 button in the bottom-left corner
2. **IMPORTANT**: Include location and specific time in your question
   - ✅ Good: "Rottnest Island conditions Monday 2pm"
   - ✅ Good: "What's the surf like at Strickland Bay tomorrow morning?"
   - ❌ Bad: "What's the weather like?"
3. The AI will check all 4 forecast sources
4. You'll get a concise summary comparing all sources
5. Click "🗑️ Clear Chat" to reset the conversation

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
- **Model**: `gemini-2.5-flash` (Google's latest flash model)
- **Google Search Grounding**: Enabled - allows real-time access to live forecast data
- **System Prompt**: Custom surf forecasting instructions
- **Sources**: Seabreeze, Surfline, Windy, BOM only
- **Response Length**: Max 100 words (enforced by system prompt)
- **Chat History**: Stored in Streamlit session state
- **UI Component**: `st.popover()` with custom CSS styling
- **Position**: Fixed bottom-left with z-index 999 for persistent visibility

### How It Works
The chatbot uses **Google Search Grounding** to:
- Access real-time data from the 4 surf forecast websites
- Look up current conditions when you ask
- Retrieve live wind, swell, and tide information
- Compare forecasts across multiple sources
- Provide up-to-date predictions (not cached or outdated data)

### CSS Customization
The chatbot button and popover are styled to match the app's color scheme:
- Button: 🌊 wave emoji in bottom-left corner
- Gradient background: Teal/cyan colors matching surf theme
- Border: Matches the app's accent color (#2eecb5)
- Popover: Dark theme consistent with the main interface
- Responsive: Adjusts size and position on mobile devices
- Position: Bottom-left to avoid conflicts with other UI elements

## System Prompt
The chatbot uses a specialized system prompt that:
- Restricts responses to the 4 approved forecast sources only
- Enforces 100-word limit for concise responses
- Requires wind, swell, and tide information
- Mandates comparison across all 4 sources
- Prompts users to include location and time if missing

## Future Enhancements
- Integration with app data (surf conditions from tracker)
- Historical condition comparisons
- Spot-specific recommendations based on past logs
- Automated alerts for favorable conditions
- Voice input/output capabilities

## Troubleshooting

### Chatbot Not Available
If you see "❌ Chatbot is not available", check:
1. GEMINI_API_KEY is set in secrets
2. API key is valid and active
3. Internet connection is working

### "Cannot Access Real-Time Data" Error
This error should NOT appear anymore as we've enabled Google Search Grounding. If you still see it:
1. Restart the Streamlit app to reload the model configuration
2. Verify your API key has access to grounding features
3. Check that you're using `gemini-2.5-flash` model

### API Errors
- **Quota exceeded**: You've hit the free tier limit (wait or upgrade)
- **Invalid API key**: Double-check your key in secrets
- **Network errors**: Check your internet connection
- **Grounding errors**: Ensure your API key supports the google_search_retrieval tool

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
