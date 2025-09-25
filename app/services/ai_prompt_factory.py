from typing import List, Optional

# This module centralizes the creation of prompts for various AI tasks.

def create_hashtag_suggestion_prompt(text: str, platforms: List[str]) -> str:
    """Creates a prompt to ask the AI for hashtag suggestions."""
    return f"""Suggest 5-7 relevant and concise hashtags for a social media post about '{text}' targeting platforms: {', '.join(platforms)}. 
Return only a JSON array of strings. For example: ["#example1", "#example2"]"""

def create_content_analysis_prompt(text: str) -> str:
    """Creates a prompt to ask the AI to analyze content quality."""
    return f"""Analyze the following social media post content. 
Return a JSON object with two keys: 'score' (an integer from 0-100 representing quality) and 'suggestions' (a list of 2-3 short, actionable strings for improvement).

Content: {text}"""

def create_insight_generation_prompt(query: Optional[str]) -> str:
    """Creates a prompt to ask the AI for a performance insight."""
    return f"""Generate a short, actionable insight for a social media manager based on this query: '{query or 'general performance'}'. 
The insight should be a single, impactful sentence."""

def create_best_posting_time_prompt(platforms: List[str], audience_description: Optional[str]) -> str:
    """Creates a prompt to ask the AI for the best time to post."""
    return f"""Based on the target platforms ({', '.join(platforms)}) and the audience ('{audience_description or 'a general audience'}'), what are the 3 best times to post for maximum engagement? 
Return a JSON object with a key 'suggestions' containing a list of strings. For example: {{"suggestions": ["Weekday mornings (9-11 AM)", "Weekends after 6 PM"]}}"""
