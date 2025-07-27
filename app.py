import streamlit as st
try:
    import openai
    from openai import OpenAI
except ImportError:
    st.error("OpenAI library not found. Please install it using: pip install openai")
    st.stop()
import json

# Set page configuration
st.set_page_config(
    page_title="AI Prompt Enhancer",
    page_icon="🚀",
    layout="wide"
)

# Title and description
st.title("🚀 AI Prompt Enhancer")
st.markdown("Transform your basic prompts into powerful, structured instructions that get better AI responses!")

# Sidebar for API key
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password", help="Your API key will not be stored")
    
    if api_key:
        st.success("API Key provided!")
    else:
        st.warning("Please enter your OpenAI API Key to use the app")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Your Prompt Components")
    
    # Input fields
    role = st.text_area(
        "Role:", 
        placeholder="e.g., You are an experienced marketing strategist...",
        help="Define who the AI should act as"
    )
    
    context = st.text_area(
        "Context:", 
        placeholder="e.g., I'm launching a new SaaS product for small businesses...",
        help="Provide background information and situation"
    )
    
    task = st.text_area(
        "Task:", 
        placeholder="e.g., Create a comprehensive marketing plan...",
        help="Specify exactly what you want the AI to do"
    )
    
    # Additional options
    st.subheader("🎯 Enhancement Options")
    include_examples = st.checkbox("Request examples in the response", value=True)
    include_steps = st.checkbox("Ask for step-by-step breakdown", value=True)
    response_length = st.selectbox(
        "Preferred response length:",
        ["Concise", "Detailed", "Comprehensive"]
    )

with col2:
    st.header("✨ Enhanced Prompt")
    
    if st.button("🔄 Enhance Prompt", type="primary"):
        if not api_key:
            st.error("Please provide your OpenAI API Key in the sidebar!")
        elif not all([role, context, task]):
            st.error("Please fill in all required fields (Role, Context, Task)")
        else:
            try:
                # Initialize OpenAI client
                client = OpenAI(api_key=api_key)
                
                # Create the enhancement prompt
                enhancement_prompt = f"""
You are an expert prompt engineer. Your task is to take the basic prompt components below and transform them into a highly effective, structured prompt that will get better AI responses.

Original Components:
- Role: {role}
- Context: {context}
- Task: {task}

Enhancement Requirements:
1. Create a clear, structured prompt that combines all components effectively
2. Include specific formatting instructions for the AI's response
3. Add a requirement for the AI to clarify any assumptions before responding
4. Make the prompt more specific and actionable
5. Include relevant constraints and guidelines
{'6. Request examples in the response' if include_examples else ''}
{'7. Ask for a step-by-step approach' if include_steps else ''}
8. Set expectations for a {response_length.lower()} response

Please return ONLY the enhanced prompt, ready to be used with an AI assistant. The enhanced prompt should be comprehensive but clear, and should significantly improve the quality of responses compared to the original components.
"""
                
                # Call OpenAI API
                with st.spinner("Enhancing your prompt..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert prompt engineer who creates highly effective AI prompts."},
                            {"role": "user", "content": enhancement_prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.7
                    )
                
                enhanced_prompt = response.choices[0].message.content
                
                # Display the enhanced prompt
                st.text_area(
                    "Your Enhanced Prompt:",
                    value=enhanced_prompt,
                    height=400,
                    help="Copy this enhanced prompt to use with any AI assistant"
                )
                
                # Copy button (using st.code for easy copying)
                st.subheader("📋 Copy-Ready Format")
                st.code(enhanced_prompt, language="text")
                
                # Success message
                st.success("✅ Prompt enhanced successfully! Copy the text above to use it.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure your API key is valid and you have sufficient credits.")

# Footer with instructions
st.markdown("---")
st.markdown("""
### 📚 How to Use:
1. **Enter your OpenAI API Key** in the sidebar
2. **Fill in the Role**: Define who the AI should act as (expert, assistant, etc.)
3. **Provide Context**: Give background information about your situation or project
4. **Specify the Task**: Clearly state what you want the AI to accomplish
5. **Choose enhancement options** to customize the output
6. **Click "Enhance Prompt"** to get your improved prompt
7. **Copy the enhanced prompt** and use it with any AI assistant

### 💡 Tips:
- Be specific in your role definition (include expertise level, background)
- Provide relevant context that helps the AI understand your situation
- Make your task clear and actionable
- The enhanced prompt will work with GPT, Claude, or other AI assistants
""")

# Information about API usage
with st.expander("ℹ️ About API Usage"):
    st.markdown("""
    - This app uses OpenAI's GPT-3.5-turbo model for prompt enhancement
    - Your API key is not stored and is only used for this session
    - Each enhancement typically costs less than $0.01 in API credits
    - You can get an API key from https://platform.openai.com/api-keys
    """)