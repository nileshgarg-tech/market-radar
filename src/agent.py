from openai import OpenAI
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from config.models import OPENROUTER_BASE_URL, DEFAULT_MODEL

# Load environment variables from .env
load_dotenv()

class NewsRanker:
    """
    Ranks news articles using OpenRouter SLMs.
    Designed for Sovereign Wealth analysis focusing on macro-impact.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set.")
        
        self.client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/nileshgarg-tech/market-radar",
                "X-Title": "Market Radar Ingestor",
            }
        )

    def analyze_article(self, title: str, summary: str) -> Dict[str, Any]:
        """
        Calculates an impact score (1-10), category, and reasoning in strict JSON format.
        """
        system_prompt = (
            "You are an autonomous High-Conviction Investment Analyst. "
            "Your objective: Identify actionable market alpha and filter out retail noise. "
            
            "\n\nINVESTMENT PRIORITIES (Weighted):"
            "\n- High Priority: Hard Corporate Data (Earnings, transcripts, filings). These provide the highest clarity of signal for investment opportunities."
            "\n- High Priority: Systemic Macro (Central Bank shifts, Geopolitical catalysts with massive economic tail-risks)."
            "\n- Medium Priority: Institutional Activity (Large stock moves, M&A, sector-wide shifts in strategic industries like AI, Energy, Tech)."
            "\n- Zero Priority: Retail Junk (Personal financial advice, retirement tips, family affairs, 'Best Stocks for $1000' clickbait)."

            "\n\nAUTONOMY DIRECTIVES:"
            "\n1. Signal Quality: Prefer hard facts and transcripts over speculative narratives or general news."
            "\n2. Magnitude vs. Opportunity: A niche company with a massive earnings beat can be as 'actionable' as a macro shift. Do not ignore individual stock alpha just because it isn't global."
            "\n3. Scoring Philosophy: Use a 1-10 scale for 'Signal Strength'. High-conviction signals (8-10), relevant context (4-7), and pure noise (1-3)."

            "\n\nSTRICT OUTPUT RULES:"
            "\nYou must respond with a single JSON object. Do not include any text outside the JSON."
            "\nJSON Schema: "
            "{\"score\": int, \"category\": \"string\", \"reasoning\": \"string\", \"is_structural\": bool}"
        )

        try:
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Title: {title}\nSummary: {summary}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Robust parsing for JSON responses
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            return {
                "score": 0, 
                "reasoning": f"Analysis failed: {str(e)}"
            }

if __name__ == "__main__":
    # Integration Test
    ranker = NewsRanker()
    
    test_cases = [
        {
            "title": "My husband, 73, wants to sell our $300K rental and buy an annuity. Is that wise?",
            "summary": "Personal finance question regarding retirement planning and annuity purchases."
        },
        {
            "title": "Blackbaud, Inc. (BLKB) Q4 2025 Earnings Call Transcript",
            "summary": "Full text of the final quarterly earnings call for fiscal year 2025 including revenue guidance."
        },
        {
            "title": "Why Gilat Satellite Stock Just Crashed 15% Today",
            "summary": "Explaining the fundamental reasons behind the double-digit drop in share price."
        }
    ]
    
    print(f"[*] Testing Agent with model: {DEFAULT_MODEL}\n")

    for case in test_cases:
        print(f"--- Analyzing: {case['title']} ---")
        result = ranker.analyze_article(case['title'], case['summary'])
        print(f"Score: {result.get('score')}")
        print(f"Category: {result.get('category')}")
        print(f"Structural: {result.get('is_structural')}")
        print(f"Reasoning: {result.get('reasoning')}\n")
