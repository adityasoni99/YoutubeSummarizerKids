import os

def save_html(html_content, filename=None):
    """
    Saves HTML content to a file.
    
    Args:
        html_content (str): The HTML content to save
        filename (str, optional): Custom filename for the HTML file.
                                 If not provided, a default name is used.
        
    Returns:
        str: The path to the saved HTML file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # If no filename provided, use a default
        if not filename:
            filename = "youtube_summary.html"
        
        # Ensure filename has .html extension
        if not filename.lower().endswith('.html'):
            filename += '.html'
        
        # Create the file path
        file_path = os.path.join('output', filename)
        
        # Write the HTML content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML file saved to: {file_path}")
        return file_path
        
    except Exception as e:
        raise Exception(f"Error saving HTML file: {str(e)}")

if __name__ == "__main__":
    # Test the function
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test HTML</title>
    </head>
    <body>
        <h1>Test HTML File</h1>
        <p>This is a test HTML file to verify the save_html function works correctly.</p>
    </body>
    </html>
    """
    
    file_path = save_html(test_html, "test_output")
    print(f"Test HTML saved to: {file_path}")
