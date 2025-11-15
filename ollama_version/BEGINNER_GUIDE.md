# Beginner's Guide - Ollama Version

## 🎯 Super Simple Guide for Beginners

### What is This?
An AI assistant that can:
- Tell you stock prices
- Search the web for news
- Give you analyst recommendations
- All running on YOUR computer (free!)

---

## 🚀 Setup (One Time Only)

### Step 1: Install Ollama
```bash
# Download and install from:
https://ollama.com/download

# Or use Windows command:
winget install Ollama.Ollama
```

### Step 2: Get the AI Model
Open a NEW terminal and run:
```bash
ollama pull llama3.2
```
(This downloads 2GB - takes a few minutes)

### Step 3: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 4: Add Your API Key
1. Copy `.env.example` to `.env`
2. Edit `.env` file
3. Add your Phidata API key

Done! ✅

---

## 💻 How to Run Queries

### Open Terminal
1. Press `Windows Key + R`
2. Type `powershell`
3. Press Enter
4. Go to project folder:
```bash
cd C:\Users\HP\OneDrive\Desktop\NLP\ollama_version
```

### Run a Query
Copy and paste this:
```bash
python financial_agent.py --query "What is the current price of AAPL?" --agent financial
```

Press Enter and wait 5-10 seconds!

---

## 📝 Easy Examples to Try

### Get Stock Prices
```bash
python financial_agent.py --query "What is the price of AAPL?" --agent financial
```

```bash
python financial_agent.py --query "What is the price of TSLA?" --agent financial
```

```bash
python financial_agent.py --query "What is the price of MSFT?" --agent financial
```

### Get News
```bash
python financial_agent.py --query "Latest Tesla news" --agent web
```

```bash
python financial_agent.py --query "What is happening with AI?" --agent web
```

### Get Analyst Recommendations
```bash
python financial_agent.py --query "Show me analyst ratings for Apple" --agent financial
```

### Ask Complex Questions
```bash
python financial_agent.py --query "Tell me about NVIDIA stock and latest AI news" --agent multi
```

---

## 🎓 Understanding the Command

```
python financial_agent.py --query "YOUR QUESTION" --agent TYPE
```

**Parts:**
- `python financial_agent.py` = Run the program
- `--query "..."` = Your question (in quotes!)
- `--agent TYPE` = Which helper to use:
  - `financial` = For stock stuff
  - `web` = For news/searches
  - `multi` = For both together

---

## 📊 Common Stock Tickers

| Company | Ticker | Example Query |
|---------|--------|---------------|
| Apple | AAPL | "What is the price of AAPL?" |
| Tesla | TSLA | "What is the price of TSLA?" |
| Microsoft | MSFT | "What is the price of MSFT?" |
| NVIDIA | NVDA | "What is the price of NVDA?" |
| Amazon | AMZN | "What is the price of AMZN?" |
| Google | GOOGL | "What is the price of GOOGL?" |

---

## ✅ Tips for Success

### DO:
- ✅ Put your question in quotes
- ✅ Use stock ticker symbols (AAPL, TSLA, etc.)
- ✅ Keep questions simple
- ✅ Wait 5-10 seconds for response
- ✅ Make sure Ollama is running

### DON'T:
- ❌ Forget the quotes around your question
- ❌ Use full company names for stock prices
- ❌ Make questions too complicated
- ❌ Expect instant responses (AI takes time!)

---

## 🆘 Common Problems

### "ollama: command not found"
**Fix:** Restart your terminal after installing Ollama

### "Model not found"
**Fix:** Run `ollama pull llama3.2`

### Query takes forever
**Normal!** First query loads the model (slow). Next queries are faster.

### "Configuration Error"
**Fix:** Make sure `.env` file has your Phidata API key

---

## 🎯 Practice Exercises

Try these in order:

1. **Easy:** Get Apple's stock price
```bash
python financial_agent.py --query "What is the price of AAPL?" --agent financial
```

2. **Medium:** Search for AI news
```bash
python financial_agent.py --query "Latest AI news" --agent web
```

3. **Advanced:** Get analyst recommendations
```bash
python financial_agent.py --query "Show me analyst ratings for NVIDIA" --agent financial
```

4. **Expert:** Multi-agent query
```bash
python financial_agent.py --query "Analyze Tesla stock and latest news" --agent multi
```

---

## 🌟 Why Ollama Version is Great

- ✅ **100% Free** - No costs ever!
- ✅ **Private** - Everything stays on your computer
- ✅ **Works Offline** - No internet needed for AI (only for stock data)
- ✅ **No Limits** - Use as much as you want
- ✅ **Multi-Agent Works** - Can combine financial + web search

---

## 📞 Quick Reference

```
┌─────────────────────────────────────────┐
│  QUICK COMMAND                          │
├─────────────────────────────────────────┤
│                                         │
│  python financial_agent.py \            │
│    --query "YOUR QUESTION" \            │
│    --agent TYPE                         │
│                                         │
│  TYPE:                                  │
│    financial = stocks                   │
│    web = news/search                    │
│    multi = both                         │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎉 You're Ready!

Just remember:
1. Open terminal
2. Go to project folder
3. Copy a command from above
4. Change the question to what you want
5. Press Enter!

**That's it!** Have fun! 🚀
