# Financial AI Agent System

## 🎯 Overview

A production-ready multi-agent AI system for financial analysis and market research. Choose between local (Ollama) or cloud (Groq) AI backends based on your needs.

---

## 📁 Project Structure

```
Financial-AI-Agent/
│
├── ollama_version/              # 🏠 Local AI (Recommended)
│   ├── README.md               # Full documentation
│   ├── BEGINNER_GUIDE.md       # Simple guide
│   ├── test_end_to_end.py      # Test suite
│   └── [all agent files]       # Complete working system
│
├── groq_version/                # ⚡ Cloud AI (Fast)
│   ├── README.md               # Full documentation + limitations
│   ├── BEGINNER_GUIDE.md       # Simple guide
│   ├── test_end_to_end.py      # Test suite
│   └── [all agent files]       # Complete working system
│
├── PROJECT_README.md            # Detailed project info
└── README.md                    # This file
```

---

## 🚀 Quick Start

### 1. Choose Your Version

| Version | Best For | Status |
|---------|----------|--------|
| **Ollama** | Beginners, Privacy, Multi-agent | ✅ Fully Working |
| **Groq** | Speed, Cloud, Simple queries | ✅ Works (with limitations) |

### 2. Navigate to Your Choice

```bash
# For local AI (recommended):
cd ollama_version

# For cloud AI (fast):
cd groq_version
```

### 3. Follow the README

Each version has complete documentation:
- `README.md` - Technical details
- `BEGINNER_GUIDE.md` - Simple step-by-step guide

---

## ✨ Features

### Financial Agent
- 📊 Real-time stock prices
- 📈 Analyst recommendations
- 💼 Company fundamentals
- 📰 Company news

### Web Search Agent
- 🔍 Web search capabilities
- 📰 Latest news
- 🌐 Market information
- 📊 Industry trends

### Multi-Agent System
- 🤝 Coordinates both agents
- 🧠 Intelligent query routing
- 📋 Comprehensive analysis
- ✅ Works perfectly in Ollama version
- ⚠️ Limited in Groq version

---

## 📊 Version Comparison

| Feature | Ollama | Groq |
|---------|--------|------|
| Cost | Free | Free tier |
| Speed | Moderate | Very Fast |
| Privacy | 100% Local | Cloud |
| Multi-Agent | ✅ Works | ⚠️ Limited |
| Setup | Install Ollama | Get API key |
| Quality | Good | Excellent |

---

## 🎓 Usage Example

```bash
# Get stock price
python financial_agent.py --query "What is the current price of AAPL?" --agent financial

# Search news
python financial_agent.py --query "Latest AI news" --agent web

# Multi-agent (Ollama only)
python financial_agent.py --query "Analyze NVIDIA stock and news" --agent multi
```

---

## 📚 Documentation

- **PROJECT_README.md** - Complete project overview
- **ollama_version/README.md** - Ollama documentation
- **groq_version/README.md** - Groq documentation
- **BEGINNER_GUIDE.md** - In each version folder

---

## ✅ Project Status

**Status**: Production Ready ✅

- ✅ All features implemented
- ✅ Comprehensive testing completed
- ✅ Full documentation provided
- ✅ Two working versions available

---

## 🎯 Recommendation

**Start with Ollama version** for:
- Full functionality
- No API costs
- Privacy
- Multi-agent capabilities

**Switch to Groq** if you need:
- Faster responses
- Cloud-based processing
- Simple single-agent queries

---

## 🚀 Get Started Now!

```bash
# Choose your version
cd ollama_version
# or
cd groq_version

# Read the README
cat README.md

# Follow the beginner guide
cat BEGINNER_GUIDE.md
```

---

**Built for financial analysis and AI exploration** 🎉
