from pocketflow import Node, BatchNode
from utils import call_llm, get_transcript, generate_html, save_html, validate_url
import yaml

class ValidateURLNode(Node):
    """Validates the YouTube URL provided by the user."""
    
    def prep(self, shared):
        return shared.get("youtube_url", "")
        
    def exec(self, youtube_url):
        is_valid, error_message = validate_url(youtube_url)
        return {"is_valid": is_valid, "error_message": error_message}
        
    def post(self, shared, prep_res, exec_res):
        if exec_res["is_valid"]:
            return "success"
        else:
            shared["error"] = exec_res["error_message"]
            return "error"

class GetTranscriptNode(Node):
    """Retrieves the transcript and metadata from a YouTube video."""
    
    def prep(self, shared):
        return shared["youtube_url"]
        
    def exec(self, youtube_url):
        return get_transcript(youtube_url)
        
    def post(self, shared, prep_res, exec_res):
        # Store transcript and video info in shared store
        shared["transcript"] = exec_res["transcript"]
        shared["video_info"] = {
            "title": exec_res["title"],
            "duration": exec_res["duration"],
            "thumbnail_url": exec_res["thumbnail_url"]
        }
        
        # Check if there was an error
        if "Sorry, couldn't get transcript" in exec_res["transcript"]:
            shared["error"] = f"Failed to process video: {shared['transcript']}"
            return "error"
            
        return "default"

class GenerateTopicsNode(Node):
    """Identifies the main topics from the video transcript."""
    
    def prep(self, shared):
        return shared["transcript"]
        
    def exec(self, transcript):
        prompt = f"""
You are analyzing a YouTube video transcript to identify the main topics discussed.

TRANSCRIPT:
{transcript}  # Use the whole transcript

TASK:
1. Identify 3-5 main topics or themes discussed in this video.
2. For each topic, extract the relevant part of the transcript.
3. Format your response as YAML following this structure:

```yaml
topics:
  - id: 1
    name: "First Topic Name"
    content: "Relevant transcript section for this topic"
  - id: 2
    name: "Second Topic Name"
    content: "Relevant transcript section for this topic"
```

Only include the YAML in your response.
"""
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.strip()
        if "```yaml" in yaml_content:
            yaml_content = yaml_content.split("```yaml")[1].split("```")[0].strip()
        elif "```" in yaml_content:
            yaml_content = yaml_content.split("```")[1].strip()
            
        # Parse YAML
        try:
            topics_data = yaml.safe_load(yaml_content)
            # Add IDs if they're not already present
            for i, topic in enumerate(topics_data["topics"]):
                if "id" not in topic:
                    topic["id"] = i + 1
            return topics_data["topics"]
        except Exception as e:
            # Fallback in case YAML parsing fails
            return [{"id": 1, "name": "General Content", "content": transcript[:5000]}]
        
    def post(self, shared, prep_res, exec_res):
        shared["topics"] = exec_res
        return "default"

class TopicProcessorNode(BatchNode):
    """Map phase - Processes each topic independently to generate Q&A pairs and explanations."""
    
    def prep(self, shared):
        return shared["topics"]
        
    def exec(self, topic):
        prompt = f"""
You are creating a child-friendly explanation and Q&A for a YouTube video topic.
The explanation should be suitable for a 5-year-old to understand.

TOPIC: {topic["name"]}

CONTENT: 
{topic["content"]}

TASK:
1. Create a very simple summary of this topic that a 5-year-old would understand.
   Use simple words, analogies, and a friendly tone.
   
2. Create a detailed explanation of this topic in simple terms.
   Break down complex concepts into easy-to-understand ideas.
   
3. Create 2-3 question and answer pairs about this topic.
   Questions should be things a curious child might ask.
   Answers should be simple, educational, and engaging.

Format your response as YAML:

```yaml
summary: "Your child-friendly summary here"
explanation: "Your detailed but simple explanation here"
qa_pairs:
  - question: "First question?"
    answer: "Simple answer for the first question"
  - question: "Second question?"
    answer: "Simple answer for the second question"
```

Only include the YAML in your response.
"""
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.strip()
        if "```yaml" in yaml_content:
            yaml_content = yaml_content.split("```yaml")[1].split("```")[0].strip()
        elif "```" in yaml_content:
            yaml_content = yaml_content.split("```")[1].strip()
            
        # Parse YAML
        try:
            qa_data = yaml.safe_load(yaml_content)
            # Add the qa data to the topic
            processed_topic = {
                "id": topic.get("id", 0),
                "name": topic["name"],
                "content": topic["content"],
                "summary": qa_data.get("summary", ""),
                "explanation": qa_data.get("explanation", ""),
                "qa_pairs": qa_data.get("qa_pairs", [])
            }
            return processed_topic
        except Exception as e:
            # Fallback in case YAML parsing fails
            fallback = {
                "id": topic.get("id", 0),
                "name": topic["name"],
                "content": topic["content"],
                "summary": "This part talks about " + topic["name"],
                "explanation": "This is about " + topic["name"],
                "qa_pairs": [
                    {"question": f"What is {topic['name']}?", 
                     "answer": "It's something interesting in the video!"}
                ]
            }
            return fallback
        
    def post(self, shared, prep_res, exec_res_list):
        # Store the processed topics in the shared store
        shared["processed_topics"] = exec_res_list
        return "default"

class CombineTopicsNode(Node):
    """Reduce phase - Combines results from all topic processing."""
    
    def prep(self, shared):
        return {
            "video_title": shared["video_info"]["title"],
            "processed_topics": shared["processed_topics"]
        }
        
    def exec(self, data):
        # Extract topic information for the prompt
        topic_info = "\n".join([
            f"TOPIC {topic['id']}: {topic['name']}\nSUMMARY: {topic['summary']}"
            for topic in data["processed_topics"]
        ])
        
        prompt = f"""
You are reviewing and refining child-friendly explanations of topics from a YouTube video.
Your task is to ensure consistency and quality across all topics.

VIDEO TITLE: {data["video_title"]}

TOPICS OVERVIEW:
{topic_info}

TASK:
1. Review the topics and their summaries listed above.
2. Create connections between the topics to form a cohesive narrative.
3. Ensure all topics are explained at the same level of simplicity.
4. Provide a ranking of the topics by importance (most to least important).

Format your response as YAML:

```yaml
connections:
  - "Transition or connection between topics 1 and 2..."
  - "Another transition between topics..."
ranking:
  - topic_id: 1
    importance: "high/medium/low"
    reason: "Why this topic is important"
  - topic_id: 2
    importance: "high/medium/low"
    reason: "Why this topic is important"
```

Only include the YAML in your response.
"""
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.strip()
        if "```yaml" in yaml_content:
            yaml_content = yaml_content.split("```yaml")[1].split("```")[0].strip()
        elif "```" in yaml_content:
            yaml_content = yaml_content.split("```")[1].strip()
            
        # Parse YAML and return the combined info
        try:
            combined_data = yaml.safe_load(yaml_content)
            # Return both the processed topics and the connections/ranking
            return {
                "processed_topics": data["processed_topics"],
                "connections": combined_data.get("connections", []),
                "ranking": combined_data.get("ranking", [])
            }
        except Exception as e:
            # Fallback in case YAML parsing fails
            return {
                "processed_topics": data["processed_topics"],
                "connections": [],
                "ranking": []
            }
        
    def post(self, shared, prep_res, exec_res):
        # Update the processed topics with connections and ranking
        shared["processed_topics"] = exec_res["processed_topics"]
        shared["topic_connections"] = exec_res.get("connections", [])
        shared["topic_ranking"] = exec_res.get("ranking", [])
        return "default"

class CreateSummaryNode(Node):
    """Creates an overall child-friendly summary of the video."""
    
    def prep(self, shared):
        # Get topic summaries and connections
        topic_summaries = [f"- {topic['name']}: {topic['summary']}" 
                          for topic in shared["processed_topics"]]
        topic_text = "\n".join(topic_summaries)
        
        connections = "\n".join([f"- {conn}" for conn in shared.get("topic_connections", [])])
        
        return {
            "video_title": shared["video_info"]["title"],
            "topic_summaries": topic_text,
            "topic_connections": connections
        }
        
    def exec(self, data):
        prompt = f"""
You are creating a simple overall summary of a YouTube video for children.
The summary should be suitable for a 5-year-old to understand.

VIDEO TITLE: {data["video_title"]}

TOPIC SUMMARIES:
{data["topic_summaries"]}

CONNECTIONS BETWEEN TOPICS:
{data["topic_connections"] or "No specific connections identified."}

TASK:
Create a very simple, engaging overall summary of this video that a 5-year-old would understand.
Use simple words, fun analogies, and a friendly, enthusiastic tone.
Connect the topics in a way that tells a story.
Keep it to 4-5 sentences.

Your summary:
"""
        return call_llm(prompt)
        
    def post(self, shared, prep_res, exec_res):
        shared["summary"] = exec_res
        return "default"

class CreateHTMLNode(Node):
    """Generates HTML content from the processed data."""
    
    def prep(self, shared):
        return {
            "title": shared["video_info"]["title"],
            "processed_topics": shared["processed_topics"],
            "summary": shared["summary"],
            "thumbnail_url": shared["video_info"]["thumbnail_url"],
            "topic_connections": shared.get("topic_connections", [])
        }
        
    def exec(self, data):
        return generate_html(
            data["title"],
            data["processed_topics"],
            data["summary"],
            data["thumbnail_url"],
            data.get("topic_connections", [])
        )
        
    def post(self, shared, prep_res, exec_res):
        shared["html_content"] = exec_res
        return "default"

class SaveHTMLNode(Node):
    """Saves the HTML content to a file."""
    
    def prep(self, shared):
        # Create a safe filename from the video title
        safe_title = shared["video_info"]["title"].replace(" ", "_")[:30]
        filename = f"{safe_title}.html"
        
        return {
            "html_content": shared["html_content"],
            "filename": filename
        }
        
    def exec(self, data):
        return save_html(data["html_content"], data["filename"])
        
    def post(self, shared, prep_res, exec_res):
        shared["output_path"] = exec_res
        return "default"