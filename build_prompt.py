def build_mcp_prompt(system, tools, query, memory=[]):
    prompt = ""

    prompt += f"System:\n{system}\n\n"
    prompt += f"Available Tool:\n{tools}\n\n"

    if memory:
        prompt += "Memory:\n" + "\n".join(memory) + "\n\n"
    prompt += f"User Query:\n{query}\n\n"

    prompt += (
        "Instructions:\n"
        "If the query is about weather, response ONLY with a code block like this:\n"
        "'''tool_code\nget_weather(city='CityName')\n'''\n"
        "Instructions:\n"
        "If the query is about current exchange rate, respond ONLY with a code block like this:\n"
        "'''tool_code\nget_exchange_rate(from_currency='USD', to_currency='NPR')\n'''\n"
        "use multiple tools whenever necessary"
        "Otherwise, reply normally.\n"
    )

    return prompt