# 🎤 AI Voice Agent with Tool Execution and Memory

An intelligent **voice-enabled AI assistant** capable of executing system commands using **LLM reasoning, tool orchestration, and conversational memory**.

The system integrates **Speech Recognition, Large Language Models, and automation workflows** to create a real-time interactive AI assistant capable of understanding voice commands and executing tools dynamically.

This project demonstrates how **modern AI agents combine reasoning, tools, and memory to automate real-world workflows.**

---

# 🚀 Features

• Voice-based interaction using **Speech-to-Text (STT)**  
• Real-time **Text-to-Speech (TTS)** responses  
• Structured reasoning pipeline (**PLAN → TOOL → OBSERVE → OUTPUT**)  
• Memory-enabled conversational interactions  
• Dynamic **tool execution for system commands**  
• Modular and extensible architecture  
• **Docker container support** for deployment  

---

# 🧠 System Architecture

```
User Voice
     │
     ▼
Speech-to-Text (STT)
     │
     ▼
LLM Reasoning Engine
     │
     ▼
Tool Selection & Execution
     │
     ▼
Result Processing
     │
     ▼
Text-to-Speech (TTS)
     │
     ▼
Voice Response to User
```

The system follows a **structured reasoning pipeline** ensuring reliable and explainable tool invocation.

---

# 🛠️ Tech Stack

## Programming
Python

## AI / LLM
OpenAI API  
Prompt Engineering

## Speech Processing
SpeechRecognition  
Text-to-Speech libraries

## Backend
FastAPI (optional API server)

## Concurrency
AsyncIO

## Deployment
Docker

---

# 📂 Project Structure

```
voice-agent
│
├── app.py
├── agent.py
├── requirements.txt
├── Dockerfile
└── README.md
```

### File Description

**app.py**  
Main application entry point handling voice interaction loop.

**agent.py**  
Core AI agent logic including reasoning, memory, and tool orchestration.

**requirements.txt**  
Project dependencies.

**Dockerfile**  
Container configuration for deployment.

---

# ⚙️ Installation

Clone the repository

```
git clone https://github.com/yourusername/voice-agent
cd voice-agent
```

Install dependencies

```
pip install -r requirements.txt
```

Run the voice agent

```
python app.py
```

---

# 🧪 Example Workflow

Example user command:

```
"Open calculator"
```

The AI agent will:

1. Convert voice to text
2. Analyze intent using the LLM
3. Select the appropriate system tool
4. Execute the command
5. Respond via voice output

---

# 🎥 Demo

Due to microphone and system access requirements, the project is demonstrated through a recorded execution.

🔗 Demo Video

https://drive.google.com/drive/folders/1ymbUSTtKHmJd2NcwfFDdLg03L1BkvTgp

---

# 🔮 Future Improvements

Possible enhancements include:

• Multi-tool orchestration  
• Integration with external APIs  
• Persistent memory storage  
• Voice authentication  
• Deployment as a cloud AI assistant  

---

# 👨‍💻 Author

Rahul Giri  
AI / ML Engineer  
Mumbai, India

GitHub  
https://github.com/RahulG-12

---

# 📄 License

This project is intended for **educational and research purposes**.
