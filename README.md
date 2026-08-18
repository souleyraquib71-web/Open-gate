# 🚪 Open Gate: Autonomous Opportunity Scout for Students
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Hackathon](https://img.shields.io/badge/AWS-Agents_for_Humans-orange.svg)](https://agentsforhumans.devpost.com/)
> **Open Gate** is a proactive, background AI agent that continuously monitors, filters, and analyzes academic scholarships and educational opportunities for students—surfacing only high-match opportunities and automating application preparation.
---
## 🎯 1. The Problem
Every year, thousands of students miss life-changing scholarship deadlines or spend hundreds of exhausting hours manually searching across dozens of disjointed websites. Most opportunities are irrelevant, restricted by nationality, or already expired.
## 💡 2. The Solution: An "Everyday Agent" for Students
Built for the **AWS Agents for Humans Hackathon** under the **Everyday Agents** track, **Open Gate** acts as an autonomous background scout:
1. **Background Discovery:** Silently monitors opportunity feeds and scholarship databases.
2. **Intelligent Matching:** Compares student criteria (study level, field of interest, nationality, availability) against eligibility requirements using generative AI reasoning.
3. **Human-in-the-Loop Decision:** Surfaces *only* high-confidence opportunities (>90% match) and requests a simple user decision.
4. **Autonomous Action:** Upon approval, opens the application portal and generates a custom `to-do` document checklist.
---
## 🏗️ Architecture & Workflow
[ 👤 Student Profile ] │ ▼ [ 🗃️ Opportunities Feed (data/opportunities.json) ] │ ▼ [ 🤖 Open Gate AI Engine (Strands SDK / LLM) ] ── (Filters out incompatible offers) │ ▼ (Matches > 90%) [ 🔔 Human-in-the-Loop Prompt ] ├── [ Option 1: Apply ] ──► Opens Portal + Generates To-Do Checklist 📝 └── [ Option 2: Archive ] ──► Remains in background monitoring 💤



---
## 🚀 Quick Start Guide
### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Git
### 1. Clone the repository
```bash
git clone https://github.com/souleyraquib71-web/Open-gate.git
cd Open-gate
2. Set up virtual environment
bash


# On Windows
py -3.11 -m venv GateHome
GateHome\Scripts\activate
3. Install dependencies
bash


pip install -r requirements.txt
4. Configure API Keys
Create a .env file at the root of the project:

env


GEMINI_API_KEY=your_api_key_here
5. Run the Agent
bash


python agent.py
🗺️ Roadmap
 Background opportunity analyzer MVP
 Interactive human-in-the-loop decision system
 Automated browser portal launcher & checklist generator
 Direct WhatsApp / Telegram bot notifications
 AWS Bedrock integration with live web-scraping pipelines
📄 License
This project is open-source under the 
MIT License.