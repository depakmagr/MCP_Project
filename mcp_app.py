import re 
import streamlit as st
import google.generativeai as genai
from tools import get_weather, get_exchange_rate
from build_prompt import build_mcp_prompt

genai.configure(api_key="AIzaSyCmuOyyZRF6BJZCK0g0Z-EHl07WAqQCuQs")

model = genai.GenerativeModel("gemini-2.0-flash-lite")

st.markdown("""
    <style>
    .main { background-color: #F9FAFC; }
    .stChatMessage { font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Google_Gemini_logo.svg/512px-Google_Gemini_logo.svg.png", width=50)
st.title("🧠 Gemini-Powered Multi-Command Processor")
st.subheader("Ask about weather, currency, and more with real-time tools.")

# # Replace st.chat_message blocks
# if msg["role"] == "user":
#     with st.chat_message("user", avatar="👤"):
#         st.markdown(msg["content"])
# else:
#     with st.chat_message("assistant", avatar="🤖"):
#         st.markdown(msg["content"])

# if tools_used:
#     st.markdown("#### 🔧 Tools Used")
#     for title, output in tools_used:
#         st.success(f"**{title}**: {output}")



#MCP Context
system = "You are a helpful assistant. Use tools when needed."
tools = ("get_weather(city): Gets weather using wttr.in. Call only when asked about weather.\n"
         "get_exchange_rate(from_currency,to_currency): Gets currency exchange rate using Frankfurther API. Call only when asked about exchange rate." 
         )


memory = []

def handl_tool_call(response):
    weather_pattern = r"```tool_code\s*\nget_weather\(city=['\"](.*?)['\"]\)\s*```"
    exchange_pattern = r"```tool_code\s*\nget_exchange_rate\(from_currency=['\"](.*?)['\"],\s*to_currency=['\"](.*?)['\"]\)\s*```"
    
    weather_match = re.search(weather_pattern, response, re.DOTALL)

    result=[]
    if weather_match:
        city = weather_match.group(1).strip()
        print(f"[Tool] Getting weather for: {city}")
        result.append(get_weather(city))
    
    exchange_match = re.search(exchange_pattern, response, re.DOTALL)
    if exchange_match:
        from_currency = exchange_match.group(1).strip()
        to_currency = exchange_match.group(2).strip()
        print(f"[Tool] Getting exchange rate: {from_currency} to {to_currency}")
        result.append(get_exchange_rate(from_currency, to_currency))

    if result:
        return "\n".join(result)

    return None

# Main loop
if __name__ == "__main__":
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        prompt = build_mcp_prompt(system, tools, user_input, memory)
        response = model.generate_content(prompt).text

        tool_output = handl_tool_call(response)

        if tool_output:
            followup_prompt = (
                f"The user asked: {user_input}\n"
                f"The tool returned: {tool_output}\n"
                f"Respond to the user naturally using this result.")
            final_response = model.generate_content(followup_prompt).text

            print("\nGemini:", final_response)
            memory.append(f"User: {user_input}")
            memory.append(f"AI: {final_response}")
        
        else:
            print("\nGemini:", response)
            memory.append(f"User: {user_input}")
            memory.append(f"AI: {response}")