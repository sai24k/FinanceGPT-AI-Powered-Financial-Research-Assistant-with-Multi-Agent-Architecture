# Beginner's Guide - Groq Version

## 🎯 Super Simple Guide for Beginners

### What is This?
An AI assistant that can:
- Tell you stock prices (FAST!)
- Search the web for news
- Give you analyst recommendations
- Uses cloud AI (Groq) for super fast responses

### ⚠️ Important Note
This version has some limitations with complex queries. For best results, ask simple questions!

---

## 🚀 Setup (One Time Only)

### Step 1: Get API Keys
1. **Groq API Key**: Go to https://console.groq.com/ and sign up
2. **Phidata API Key**: Go to https://www.phidata.com/ and sign up

### Step 2: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 3: Add Your API Keys
1. Copy `.env.example` to `.env`
2. Edit `.env` file
3. Add both API keys:
```
PHIDATA_API_KEY=your_phidata_key_here
GROQ_API_KEY=your_groq_key_here
```

Done! ✅

---

## 💻 How to Run Queries

### Open Terminal
1. Press `Windows Key + R`
2. Type `powershell`
3. Press Enter
4. Go to project folder:
```bash
cd C:\Users\HP\OneDrive\Desktop\NLP\groq_version
```

### Run a Query
Copy and paste this:
```bash
python financial_agent.py --query "What is the current price of AAPL?" --agent financial
```

Press Enter and wait 2-5 seconds!

---

## 📝 Easy Examples to Try (THESE WORK GREAT!)

### Get Stock Prices ✅
```bash
python financial_agent.py --query "What is the price of AAPL?" --agent financial
```

```bash
python financial_agent.py --query "What is the price of TSLA?" --agent financial
```

### Get News ✅
```bash
python financial_agent.py --query "Latest Tesla news" --agent web
```

```bash
python financial_agent.py --query "What is happening with AI?" --agent web
```

### Get Analyst Recommendations ✅
```bash
python financial_agent.py --query "Show me analyst ratings for NVIDIA" --agent financial
```

---

## ⚠️ What to Avoid

### DON'T Use Multi-Agent (May Fail)
```bash
# This might not work:
python financial_agent.py --query "Analyze NVIDIA stock and news" --agent multi
```

**Instead, ask separately:**
```bash
# First get stock info:
python financial_agent.py --query "NVIDIA stock price and recommendations" --agent financial

# Then get news:
python financial_agent.py --query "Latest NVIDIA news" --agent web
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
  - `financial` = For stock stuff ✅ WORKS GREAT
  - `web` = For news/searches ✅ WORKS GREAT
  - `multi` = For both ⚠️ MAY FAIL (use Ollama version)

---

## 📊 Common Stock Tickers

| Company | Ticker | Example Query |
|---------|--------|---------------|
| Apple | AAPL | "What is the price of AAPL?" |
| Tesla | TSLA | "What is the price of TSLA?" |
| NVIDIA | NVDA | "What is the price of NVDA?" |
| Amazon | AMZN | "What is the price of AMZN?" |
| Google | GOOGL | "What is the price of GOOGL?" |

---

## ✅ Tips for Success

### DO:
- ✅ Use `--agent financial` for stock questions
- ✅ Use `--agent web` for news questions
- ✅ Keep questions simple
- ✅ Put your question in quotes
- ✅ Use stock ticker symbols

### DON'T:
- ❌ Use `--agent multi` (has issues)
- ❌ Ask very complex questions
- ❌ Forget the quotes
- ❌ Expect multi-agent coordination to work

---

## 🆘 Common Problems

### "Invalid API Key"
**Fix:** Check your Groq API key at https://console.groq.com/keys

### "tool_use_failed" Error
**This is normal for Groq!** 
**Fix:** Use simpler queries or switch to Ollama version

### Query Fails for Some Tickers
**Fix:** Try again or use a different ticker

---

## 🎯 Practice Exercises

Try these (they work great!):

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
python financial_agent.py --query "Show me analyst ratings for Tesla" --agent financial
```

---

## 🌟 Why Groq Version is Great

### ✅ Pros
- **Super Fast** - Responses in 2-5 seconds!
- **High Quality** - Very smart AI
- **No Installation** - Just need API key
- **Cloud-Based** - Doesn't use your computer

### ⚠️ Cons
- **Multi-Agent Limited** - Can't combine agents well
- **API Costs** - Free tier then paid (very cheap though)
- **Needs Internet** - Must be online

---

## 💡 When to Use Groq vs Ollama

### Use Groq (This Version) For:
- ✅ Simple stock price queries
- ✅ Quick web searches
- ✅ Fast responses needed
- ✅ Single-agent questions

### Use Ollama Version For:
- ✅ Multi-agent queries
- ✅ Complex questions
- ✅ 100% free operation
- ✅ Privacy concerns

---

## 📞 Quick Reference

```
┌─────────────────────────────────────────┐
│  QUICK COMMAND (GROQ)                   │
├─────────────────────────────────────────┤
│                                         │
│  python financial_agent.py \            │
│    --query "YOUR QUESTION" \            │
│    --agent TYPE                         │
│                                         │
│  TYPE (What Works):                     │
│    financial ✅ GREAT                   │
│    web ✅ GREAT                         │
│    multi ⚠️ USE OLLAMA                  │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎉 You're Ready!

Remember:
1. Use `financial` or `web` agents (not `multi`)
2. Keep questions simple
3. Enjoy super fast responses!

**For complex multi-agent queries, use the Ollama version!**

Have fun! ⚡
