import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyCee4qW4DrJ9dDQDVx0cCtNaL0maVVj03M"))

def call_llm(prompt):    
    # Load the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content
    response = model.generate_content(prompt)
    
    return response.text
    
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    print(call_llm(prompt))
