from pocketflow import Flow
from nodes import (
    ValidateURLNode,
    GetTranscriptNode,
    GenerateTopicsNode,
    TopicProcessorNode,
    CombineTopicsNode,
    CreateSummaryNode,
    CreateHTMLNode,
    SaveHTMLNode
)

def create_youtube_summarizer_flow():
    """Create and return a YouTube video summarizer flow with Map Reduce pattern."""
    # Create nodes
    validate_url_node = ValidateURLNode()
    get_transcript_node = GetTranscriptNode()
    generate_topics_node = GenerateTopicsNode()
    
    # Map phase - process each topic independently
    topic_processor_node = TopicProcessorNode()
    
    # Reduce phase - combine results
    combine_topics_node = CombineTopicsNode()
    
    # Create summary and output
    create_summary_node = CreateSummaryNode()
    create_html_node = CreateHTMLNode()
    save_html_node = SaveHTMLNode()
    
    # Connect nodes with actions
    validate_url_node - "success" >> get_transcript_node
    get_transcript_node >> generate_topics_node
    
    # Map-Reduce pattern
    generate_topics_node >> topic_processor_node  # Map: distribute topics
    topic_processor_node >> combine_topics_node   # Reduce: combine results
    
    # Final processing
    combine_topics_node >> create_summary_node
    create_summary_node >> create_html_node
    create_html_node >> save_html_node
    
    # Create flow starting with input validation
    return Flow(start=validate_url_node)

# Create the flow
youtube_summarizer_flow = create_youtube_summarizer_flow()