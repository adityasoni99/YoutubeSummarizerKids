from jinja2 import Template

def generate_html(title, topics, summary, thumbnail_url, connections=None):
    """
    Generates an HTML page to visualize the video summary.
    
    Args:
        title (str): The title of the video
        topics (list): List of dictionaries with topic details including 'name', 'summary', 'explanation', and 'qa_pairs'
        summary (str): Overall summary of the video
        thumbnail_url (str): URL to the video thumbnail
        connections (list): Optional list of connections between topics
        
    Returns:
        str: HTML content as a string
    """
    
    # Create a Jinja2 template for the HTML
    template_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }} - Kid-Friendly Summary</title>
        <style>
            body {
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }
            h1 {
                color: #ff6b6b;
                text-align: center;
            }
            h2 {
                color: #4ecdc4;
                border-bottom: 2px solid #4ecdc4;
                padding-bottom: 5px;
            }
            h3 {
                color: #ff9f43;
            }
            .thumbnail {
                display: block;
                margin: 20px auto;
                max-width: 100%;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .summary {
                background-color: #ffe8d6;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .topic {
                background-color: #e8f4f8;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .qa {
                background-color: #fff;
                padding: 10px 15px;
                border-radius: 8px;
                margin-bottom: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .question {
                font-weight: bold;
                color: #6a6a6a;
            }
            .answer {
                margin-top: 5px;
                color: #2d2d2d;
            }
            .connections {
                background-color: #e0f7fa;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .explanation {
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 8px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <img src="{{ thumbnail_url }}" alt="Video Thumbnail" class="thumbnail">
        
        <div class="summary">
            <h2>Simple Summary</h2>
            <p>{{ summary }}</p>
        </div>
        
        {% if connections %}
        <div class="connections">
            <h2>How Topics Connect</h2>
            <ul>
                {% for connection in connections %}
                <li>{{ connection }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <h2>Interesting Topics</h2>
        {% for topic in topics %}
        <div class="topic">
            <h3>{{ topic.name }}</h3>
            <p>{{ topic.summary }}</p>
            
            <div class="explanation">
                <h4>Simple Explanation:</h4>
                <p>{{ topic.explanation }}</p>
            </div>
            
            <h4>Questions & Answers:</h4>
            {% for qa in topic.qa_pairs %}
            <div class="qa">
                <div class="question">Q: {{ qa.question }}</div>
                <div class="answer">A: {{ qa.answer }}</div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </body>
    </html>
    """
    
    # Render the template
    template = Template(template_str)
    html_content = template.render(
        title=title,
        topics=topics,
        summary=summary,
        thumbnail_url=thumbnail_url,
        connections=connections
    )
    
    return html_content

if __name__ == "__main__":
    # Test the function
    test_data = {
        "title": "How Rainbows Form",
        "topics": [
            {
                "name": "Sunlight and Water Droplets",
                "summary": "Rainbows happen when sunlight meets water drops in the air. The light splits into different colors like magic!",
                "qa": [
                    {"question": "What makes the colors in a rainbow?", "answer": "Sunlight splits into different colors when it goes through water drops."},
                    {"question": "When can we see rainbows?", "answer": "We can see rainbows when the sun is behind us and it's raining in front of us."}
                ]
            },
            {
                "name": "Rainbow Colors",
                "summary": "Rainbows always have the same colors in the same order: red, orange, yellow, green, blue, indigo, and violet.",
                "qa": [
                    {"question": "How many colors are in a rainbow?", "answer": "There are 7 main colors in a rainbow."},
                    {"question": "What's the first color in a rainbow?", "answer": "Red is the first color at the top of the rainbow."}
                ]
            }
        ],
        "summary": "Rainbows are beautiful arcs of color in the sky. They appear when sunshine and rain happen at the same time. The water drops in the air work like tiny prisms that split sunlight into all the colors we can see!",
        "thumbnail_url": "https://example.com/rainbow.jpg"
    }
    
    html_content = generate_html(
        test_data["title"], 
        test_data["topics"], 
        test_data["summary"], 
        test_data["thumbnail_url"]
    )
    
    print("HTML content generated successfully!")
    print(f"HTML length: {len(html_content)} characters")
