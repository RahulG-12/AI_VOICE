from openai import OpenAI, AsyncOpenAI
import speech_recognition as sr
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, Field
from typing import Optional
import os
from openai.helpers import LocalAudioPlayer
import asyncio
import json

# ---------------- LOOP ----------------
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ---------------- ENV ----------------
load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


# ---------------- TTS ----------------
async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="ALWAYS WITH HIGH ENGERGY AND SPEAK LIKE HUMAN TONE",
        input=speech,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


# ---------------- TOOLS ----------------
def run_cmd(cmd: str):
    try:
        # Force normal Windows Desktop (NOT OneDrive)
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")

        cmd_lower = cmd.lower()

        # Extract folder name after mkdir
        if "mkdir" in cmd_lower:
            parts = cmd.split("mkdir")
            folder_name = parts[-1].strip().strip('"').strip("'")

            full_path = os.path.join(desktop, folder_name)

            os.makedirs(full_path, exist_ok=True)

            return f"Folder created successfully at {full_path}"

        # If not mkdir → run normally
        result = os.system(cmd)

        if result == 0:
            return "Command executed successfully"
        else:
            return f"Command failed with code {result}"

    except Exception as e:
        return str(e)

def get_weather(city: str):
    try:
        import requests

        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            current = data["current_condition"][0]

            temp = current["temp_C"]
            desc = current["weatherDesc"][0]["value"]

            return f"The weather in {city} is {desc} with temperature {temp}°C"

    except Exception:
        pass   # ignore error and fallback

    # ---------- FALLBACK ----------
    return f"The weather in {city} is around 30°C with partly cloudy skies (demo data)"


available_Tools = {
    "get_weather": get_weather,
    "run_cmd": run_cmd
}


# ---------------- STRONG PROMPT ----------------
SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.

You work on START, PLAN, TOOL, OBSERVE and OUTPUT steps.

If the user asks to perform any system action like:
- create folder
- open app
- run command
- file operations

You MUST call the TOOL run_cmd.

Never give instructions if you can execute using tool.

Always wait for OBSERVE after tool call.

available tools:
- get_weather(city:str)
- run_cmd(cmd:str)

Output JSON Format:
{
 "step": "START" | "PLAN" | "OUTPUT" | "TOOL",
 "content": "string",
 "tool": "string",
 "input": "string"
}
"""


class OP_Format(BaseModel):
    step: str = Field(...)
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None


message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


# ---------------- MAIN LOOP ----------------
def start_voice_loop(ui):

    r = sr.Recognizer()

    while True:

        with sr.Microphone() as source:

            ui.info("🎤 Speak Something...")
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 2
            audio = r.listen(source)

        ui.info("Processing Audio....(STT)")

        try:
            stt = r.recognize_google(audio)
        except Exception:
            ui.error("Could not understand")
            continue

        user_query = stt
        ui.success(f"🧑 You: {user_query}")

        message_history.append({"role": "user", "content": user_query})

        while True:

            response = client.chat.completions.parse(
                model="gpt-4o",
                response_format=OP_Format,
                messages=message_history
            )

            raw_result = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": raw_result})

            parsed_result = response.choices[0].message.parsed

            # ---------- START ----------
            if parsed_result.step == "START":
                ui.write(f"🔥 START: {parsed_result.content}")
                continue

            # ---------- PLAN ----------
            if parsed_result.step == "PLAN":
                ui.write(f"🧠 PLAN: {parsed_result.content}")
                continue

            # ---------- TOOL ----------
            if parsed_result.step == "TOOL":

                tool_to_call = parsed_result.tool
                tool_input = parsed_result.input

                ui.warning(f"🛠 TOOL CALL → {tool_to_call}({tool_input})")

                tool_response = available_Tools[tool_to_call](tool_input)

                ui.info(f"🔍 OBSERVE → {tool_response}")

                message_history.append({
                    "role": "developer",
                    "content": json.dumps({
                        "step": "OBSERVE",
                        "tool": tool_to_call,
                        "input": tool_input,
                        "output": tool_response
                    })
                })

                continue

            # ---------- OUTPUT ----------
            if parsed_result.step == "OUTPUT":

                ui.success(f"🤖 OUTPUT: {parsed_result.content}")
                loop.run_until_complete(tts(parsed_result.content))
                break