import openai

# Read the OpenAI API key from the txt file
with open("openai_key.txt") as f:
    openai.api_key = f.read().strip()

def stream_recipe_from_gpt(ingredients, meal, cuisine, time):
    prompt = (
        f"Suggest a detailed recipe for {meal} using the following ingredients: {ingredients}.\n"
        f"The cuisine should be {cuisine or 'any'} and the total cooking time should be {time}.\n"
        "Please provide a catchy recipe name, list of ingredients with quantities, and step-by-step instructions."
    )
    stream = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful chef."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and getattr(delta, 'content', None):
            yield delta.content

def get_recipe_mock(ingredients, meal, cuisine, time):
    return (
        f"### Sample {cuisine or 'Any'} {meal} Recipe\n\n"
        f"**Ingredients:** {ingredients}\n\n"
        "**Instructions:**\n1. Step one...\n2. Step two...\n3. Enjoy!"
    )
