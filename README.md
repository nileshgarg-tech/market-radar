# Market Radar 

> Turn financial news chaos into actionable intelligence

Automated pipeline that collects, filters, and ranks market-moving news 
from multiple sources using LLM-powered analysis.

## 🛠 Status
- **Phase 1 (Done)**: RSS Ingestion Engine with US/Central time and smart cleaning.
- **Phase 2 (Done)**: Autonomous Ranking Agent (GPT-OSS 120B) for institutional signal detection.
- **Phase 3 (Next)**: Supabase Integration & Orchestration.

## 🧠 The Agent
Our ranking engine is calibrated for **High-Conviction Alpha**:
- **9-10**: Hard Corporate Data (Earnings/Transcripts)
- **8**: Systemic Macro (Geopolitics/Central Banks)
- **6-7**: Institutional Activity (M&A/Sector Trends)
- **1-3**: Retail Junk (Personal Finance/Clickbait)


## 🚀 Quick Start
```powershell
# Create & Activate Environment
python -m venv .venv
.venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Collector
python -m src.ingestion
```
