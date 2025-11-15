# Financial AI Agent System - Groq Version

## 🎯 Project Description

A multi-agent AI system that provides real-time financial data and web search capabilities using Groq's cloud-based LLM (llama-3.3-70b-versatile). This system combines three specialized agents to answer financial queries with fast, high-quality AI responses.

### Key Features
- 📊 **Financial Agent**: Real-time stock prices, analyst recommendations, company fundamentals
- 🔍 **Web Search Agent**: Latest news, market trends, company information
- 🤝 **Multi-Agent System**: Coordinates both agents (with limitations - see below)
- ⚡ **Fast Cloud AI**: Uses Groq's optimized infrastructure
- 🎯 **High Quality**: Powered by llama-3.3-70b-versatile model
- 🌐 **FastAPI Deployment**: REST API with interactive Swagger documentation

---

## ⚠️ Known Limitations

### Groq API Limitations

**Multi-Agent Coordination Issues:**
- ❌ Complex multi-agent queries may fail with `tool_use_failed` error
- ❌ Some function calling scenarios not fully supported by Groq API
- ✅ **Workaround**: Use individual agents separately

**What Works:**
- ✅ Single Financial Agent queries (stock prices, recommendations)
- ✅ Single Web Search Agent queries (news, searches)
- ✅ Simple queries with one tool call

**What May Fail:**
- ❌ Multi-agent queries requiring coordination
- ❌ Complex queries with multiple tool calls
- ❌ Some stock tickers (intermittent API issues)

**Recommendation:** For multi-agent queries, use the **Ollama version** instead.

---

## ✅ Tasks Completed

### 1. Web Search Agent ✅
- Implemented DuckDuckGo search integration
- Markdown-formatted results with source citations
- Real-time web information retrieval
- **Works perfectly with Groq**

### 2. Financial Agent ✅
- YFinance integration for stock data
- Analyst recommendations retrieval
- Company fundamentals and metrics
- Real-time stock prices
- **Works well for most queries**

### 3. Multi-Agent Coordinator ⚠️
- Intelligent query routing
- Agent coordination (limited by Groq API)
- **Use Ollama version for multi-agent queries**

### 4. Configuration & Error Handling ✅
- Environment variable management
- Comprehensive error handling
- Detailed logging system
- User-friendly error messages

### 5. FastAPI Deployment ✅
- REST API endpoints
- Interactive Swagger UI documentation
- Hot reload for development
- Production-ready deployment

### 6. Testing & Validation ✅
- End-to-end test suite
- 4/5 tests passing (multi-agent has known issues)
- Comprehensive documentation

---

## 🚀 Quick Start

### Prerequisites
1. **Python 3.12+**
2. **Groq API key** (free tier available)
3. **Phidata API key**

### Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Get API keys
# Groq: https://console.groq.com/
# Phidata: https://www.phidata.com/

# 3. Configure environment
copy .env.example .env
# Edit .env and add:
#   PHIDATA_API_KEY=your_phidata_key
#   GROQ_API_KEY=your_groq_key
```

### Running Queries

```bash
# Get stock price (WORKS GREAT)
python financial_agent.py --query "What is the current price of AAPL?" --agent financial

# Search the web (WORKS GREAT)
python financial_agent.py --query "Latest AI news" --agent web

# Multi-agent query (MAY FAIL - use Ollama version instead)
python financial_agent.py --query "Analyze NVIDIA stock and latest news" --agent multi
```

---

## 📋 Sample Query Outputs

### Example 1: Stock Price Query ✅ WORKS

**Query:**
```bash
python financial_agent.py --query "What is the current price of TSLA?" --agent financial
```

**Output:**
```
================================================================================
  Financial AI Agent System - Local Test
================================================================================

[*] Loading configuration...
[+] Configuration loaded successfully

[*] Initializing agents...
  - Web Search Agent: Ready
  - Financial Agent: Ready
  - Multi-Agent System: Ready

================================================================================
CUSTOM QUERY EXECUTION
================================================================================

[*] Using: Financial Agent
[?] Query: What is the current price of TSLA?
--------------------------------------------------------------------------------

[RESPONSE]:
--------------------------------------------------------------------------------

Running:
 - get_current_stock_price(symbol=TSLA)

The current price of TSLA is $404.35.
--------------------------------------------------------------------------------

[+] Query completed successfully!
```

### Example 2: Analyst Recommendations ✅ WORKS

**Query:**
```bash
python financial_agent.py --query "Get analyst recommendations for NVIDIA" --agent financial
```

**Output:**
```
[RESPONSE]:
--------------------------------------------------------------------------------

Running:
 - get_analyst_recommendations(symbol=NVDA)

Here are the analyst recommendations for NVIDIA:

| Period | Strong Buy | Buy | Hold | Sell | Strong Sell |
|--------|-----------|-----|------|------|-------------|
| 0m     | 10        | 12  | 4    | 1    | 0           |
| -1m    | 10        | 11  | 4    | 1    | 0           |
| -2m    | 10        | 10  | 4    | 1    | 0           |
| -3m    | 10        | 9   | 6    | 1    | 0           |

The majority of analysts recommend buying NVIDIA stock.
--------------------------------------------------------------------------------
```

### Example 3: Web Search ✅ WORKS

**Query:**
```bash
python financial_agent.py --query "Latest Tesla news" --agent web
```

**Output:**
```
[RESPONSE]:
--------------------------------------------------------------------------------

Running:
 - duckduckgo_search(query=Latest Tesla news)

## Latest Tesla News

1. **Tesla Announces New Model**
   - Details about upcoming vehicle
   - Source: https://tesla.com/...

2. **Stock Performance Update**
   - Recent market movements
   - Source: https://finance.yahoo.com/...

3. **Industry Analysis**
   - Expert opinions on Tesla's future
   - Source: https://reuters.com/...
--------------------------------------------------------------------------------
```

### Example 4: Multi-Agent Query ❌ MAY FAIL

**Query:**
```bash
python financial_agent.py --query "Analyze NVIDIA stock and latest news" --agent multi
```

**Possible Error:**
```
Error occurred: BadRequestError: Error code: 400 - {'error': {'message': 
"Failed to call a function. Please adjust your prompt.", 'type': 
'invalid_request_error', 'code': 'tool_use_failed'}}
```

**Workaround - Use Individual Agents:**
```bash
# Get financial data
python financial_agent.py --query "NVIDIA stock price and recommendations" --agent financial

# Get news separately
python financial_agent.py --query "Latest NVIDIA news" --agent web
```

---

## 🎓 Beginner's Guide

### Basic Command Structure
```bash
python financial_agent.py --query "YOUR QUESTION" --agent TYPE
```

**Agent Types:**
- `financial` - Stock prices, analyst data, fundamentals ✅ WORKS WELL
- `web` - Web searches, news, general information ✅ WORKS WELL
- `multi` - Complex queries ⚠️ USE OLLAMA VERSION

### Common Stock Tickers
| Company | Ticker |
|---------|--------|
| Apple | AAPL |
| Tesla | TSLA |
| NVIDIA | NVDA |
| Amazon | AMZN |
| Google | GOOGL |
| Microsoft | MSFT |

### Recommended Queries (That Work Well)

**Get stock prices:**
```bash
python financial_agent.py --query "What is the price of AAPL?" --agent financial
python financial_agent.py --query "What is the price of TSLA?" --agent financial
```

**Search for news:**
```bash
python financial_agent.py --query "Latest AI news" --agent web
python financial_agent.py --query "Tesla news today" --agent web
```

**Get recommendations:**
```bash
python financial_agent.py --query "Show me analyst ratings for NVIDIA" --agent financial
```

### Queries to Avoid
❌ Multi-agent queries (use Ollama version)
❌ Very complex queries with multiple steps
❌ Queries requiring extensive tool coordination

---

## 🌟 Advantages & Disadvantages

### ✅ Pros
- **Very Fast** - Cloud-optimized infrastructure
- **High Quality** - Powerful 70B parameter model
- **No Installation** - Just need API key
- **No Local Resources** - Runs in the cloud

### ❌ Cons
- **API Limitations** - Multi-agent coordination issues
- **Requires Internet** - Cloud-based processing
- **API Costs** - Free tier then paid (though very cheap)
- **Less Privacy** - Data sent to Groq servers

### 💡 When to Use Groq
- ✅ Single-agent queries
- ✅ Need fast responses
- ✅ Want high-quality AI
- ✅ Simple financial or web queries

### 💡 When to Use Ollama Instead
- ✅ Multi-agent queries
- ✅ Complex coordination needed
- ✅ Want 100% free
- ✅ Privacy concerns

---

## 🔧 Technical Details

### Architecture
```
User Query → Phidata Framework → Groq API (llama-3.3-70b) → Tools:
                                                             ├─ YFinance (stock data)
                                                             └─ DuckDuckGo (web search)
```

### Components
- **Phidata**: Agent orchestration framework
- **Groq**: Cloud LLM API
- **llama-3.3-70b-versatile**: 70B parameter language model
- **YFinance**: Stock market data API
- **DuckDuckGo**: Web search API

### Requirements
- Python 3.12+
- Valid Groq API key
- Valid Phidata API key
- Internet connection

---

## 📊 Test Results

### Local Script Tests: 4/5 ⚠️
- Financial query (AAPL price) ✅
- Web search query (AI news) ✅
- Multi-agent query (NVIDIA analysis) ❌ (Known Groq limitation)
- Invalid ticker error handling ✅
- Response formatting validation ✅

### FastAPI Tests: 6/6 ✅
- Server startup ✅
- Swagger UI access ✅
- API key validation ✅
- Health check ✅
- OpenAPI schema ✅
- Hot reload functionality ✅

---

## 📁 Project Structure

```
groq_version/
├── web_search_agent.py          # Web search agent (Groq)
├── financial_agent_module.py    # Financial agent (Groq)
├── multi_agent.py                # Multi-agent coordinator (Groq - limited)
├── financial_agent.py            # Main CLI interface
├── playground.py                 # FastAPI deployment
├── config.py                     # Configuration management
├── error_handler.py              # Error handling
├── logger.py                     # Logging system
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 🆘 Troubleshooting

### "Invalid API Key" Error
```bash
# Verify your Groq API key at:
https://console.groq.com/keys

# Make sure it's active and not expired
# Update .env file with valid key
```

### "tool_use_failed" Error
```
This is a known Groq API limitation.

Solution:
1. Use individual agents instead of multi-agent
2. Or switch to Ollama version for multi-agent queries
```

### Query Fails for Specific Ticker
```
Some tickers may fail intermittently due to Groq API issues.

Workaround:
- Try again (may work on retry)
- Use a different ticker
- Switch to Ollama version
```

---

## 🔄 Switching to Ollama Version

If you need multi-agent functionality:

1. Navigate to `ollama_version` directory
2. Follow the README there
3. Install Ollama
4. Enjoy full multi-agent capabilities!

---

## 🎉 Summary

**Groq Version Status:**
- ✅ Fast and powerful for single-agent queries
- ⚠️ Limited multi-agent support (Groq API issue)
- ✅ Great for simple financial and web queries
- 💡 Use Ollama version for complex multi-agent needs

**Best Use Cases:**
- Quick stock price checks
- Fast web searches
- Simple analyst recommendations
- Individual agent queries

Enjoy your cloud-powered AI financial agent! ⚡
