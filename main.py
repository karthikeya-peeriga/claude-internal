import anthropic

client = anthropic.Anthropic(
    # API key
    api_key="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"
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="You are a world-class poet. Respond only with short poems.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the ocean salty?"
                }
            ]
        }
    ]
)
print(message.content)
