import subprocess
import keyboard
import ctypes
import json


class AudioControl:
  APPCOMMAND_MICROPHONE_MUTE = 0x180000
  WM_APPCOMMAND = 0x319

  def __init__(self):
    self.user32 = ctypes.windll.user32

  def toggle_microphone(self):
    hwnd = self.user32.GetForegroundWindow()
    self.user32.SendMessageW(hwnd, self.WM_APPCOMMAND, hwnd, self.APPCOMMAND_MICROPHONE_MUTE)


audio_control = AudioControl()


@app.route("/hotkeys/runAction", methods=["POST"])
def hotkeys_runAction():
  if request.args.get('password') == PASSWORD:
    actionType, actionContext = request.get_json()["action"].split("=:=")

    if actionType == "cmd":
      subprocess.run(actionContext.replace("'", '"'), shell=True)
    if actionType == "hotkey":
      keyboard.press_and_release(actionContext)
    if actionType == "mic":
      audio_control.toggle_microphone()
  return ""


def load():
  rows = getSetting("Rows")
  columns = getSetting("Columns")
  try:
    keys = json.loads(getSetting("!Key Actions"))
  except json.JSONDecodeError:
    keys = []

  buttons = ""

  for i in keys:
    buttons += f"""
    <div class="grid-item">
      <img onclick="hotkeys_runAction(`{i["action"]}`)" src="data:image/png;base64,{i["image"]}" style="width: 100%; border-radius: 16px;">
    </div>"""

  return """
    <script>
      function hotkeys_runAction(action) {
        fetch(`/hotkeys/runAction?password=${([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{[curr[0]]:curr[1]})),{})["password"]}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ action: action })
        })
      }
    </script>
    <div class="parent">
      <div class="grid-container">
        <buttonElements>
      </div>
    </div>

    <style>
      .parent {
        border: 30px solid transparent;
        border-top: 10px solid transparent;
        height: calc(100vh - 60px);
        width: calc(100vw - 60px);
        display: flex;
        justify-content: center;
        align-items: center;
      }
    
      .grid-container {
        display: grid;
        gap: 10px;
        width: calc((100vh - 60px) / <y> * <x>);
        height: calc(100vh - 60px);
        max-width: calc(100vw - 60px);
        max-height: calc((100vw - 60px) / <x> * <y>);
        grid-template-columns: repeat(<x>, 1fr);
        grid-template-rows: repeat(<y>, 1fr);
      }
    
      .grid-item {
        display: flex;
        align-items: center;
        justify-content: center;
      }
    
      @media (max-aspect-ratio: <x>/<y>) {
        .grid-container {
          width: 100%;
          height: calc((100vw - 60px) / <x> * <y>);
        }
      }

      @media (min-aspect-ratio: <x>/<y>) {
        .grid-container {
          width: calc((100vh - 60px) / <y> * <x>);
          height: 100%;
        }
      }
    </style>
  """.replace("<buttonElements>", buttons).replace("<x>", str(columns)).replace("<y>", str(rows))
