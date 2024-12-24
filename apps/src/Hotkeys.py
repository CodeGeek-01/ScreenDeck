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
    actionType, actionContext = request.get_json()["action"].split("-=:=-")

    if actionType == "Command":
      subprocess.run(actionContext.replace("'", '"'), shell=True)
    if actionType == "Hotkey":
      keyboard.press_and_release(actionContext)
    if actionType == "Microphone":
      audio_control.toggle_microphone()
  return ""


@app.route("/hotkeys/saveLayout", methods=["POST"])
def hotkeys_saveLayout():
  if request.args.get('password') == PASSWORD:
    buttons = request.get_json()["data"]

    with open('settings.json', 'r') as file:
      data = json.load(file)
      data['yPNIETrAqfDMmpFaXZgJcuvOCohewmwQ']['!Key Actions'] = str(buttons).replace("'", '\"')
      with open('settings.json', 'w') as file:
        json.dump(data, file)
  return ""


def editButtonsPage():
  try:
    buttons = json.loads(getSetting("!Key Actions", "yPNIETrAqfDMmpFaXZgJcuvOCohewmwQ"))
  except:
    buttons = []
  
  button_inputs = ""
  for button in buttons:
    button_inputs += f"""
    <div class="input-group">
      <input style="display: none" type="file" accept="image/*" />
      <img id="icon-preview" src="{button['image']}" style="height: 50px; width: 50px; padding: 0;" />
      <div class="select">
        <select>
          <option value="Hotkey" {'selected' if 'Hotkey' in button['action'] else ''}>Hotkey</option>
          <option value="Command" {'selected' if 'Command' in button['action'] else ''}>Command</option>
          <option value="Microphone" {'selected' if 'Microphone' in button['action'] else ''}>Microphone</option>
        </select>
      </div>
      <input id="Hotkey" type="text" placeholder="Key combination" value="{button['action'].split('-=:=-')[1] if 'Hotkey' in button['action'] else ''}" style="{'display: block' if 'Hotkey' in button['action'] else 'display: none'}" />
      <input id="Command" type="text" placeholder="Enter command" value="{button['action'].split('-=:=-')[1] if 'Command' in button['action'] else ''}" style="{'display: block' if 'Command' in button['action'] else 'display: none'}" />
      <input id="Microphone" type="text" placeholder="Toggle microphone" disabled style="{'display: block' if 'Microphone' in button['action'] else 'display: none'}" />
      <button class="button-9" style="background-color: #ED3419;" onclick="this.parentElement.remove()">Delete</button>
    </div>
    """
  
  return """
  <style>
    :root {
      --primary: #0077FF;
      --dark: white;
    }

    #editPage {
      width: 100%;
      height: 100%;
    }
    
    #editPage #inputs-container {
      margin-bottom: 20px;
    }

    #editPage .input-group {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      gap: 10px;
    }

    #editPage input[type="file"] {
      display: block;
    }

    #editPage button {
      cursor: pointer;
    }

    #editPage button:hover {
      background-color: #f0f0f0;
    }

    #editPage #icon-preview {
      max-width: 100px;
      display: block;
    }

    #editPage label {
      display: block;
      margin-top: 10px;
    }

    #editPage input[type="text"] {
      flex-grow: 1;
    }

    #editPage .input-group {
      padding: 10px;
      border-radius: 5px;
    }

    #editPage .inp {
      position: relative;
      margin: 0 auto;
      width: 100%;
      max-width: 280px;
      border-radius: 3px;
      overflow: hidden;
      background: rgba(255,255,255,0.1);
      box-shadow: inset 0 -2px 0 rgba(255, 255, 255, 0.2);
    }

    #editPage .inp .label {
      position: absolute;
      top: 20px;
      left: 12px;
      font-size: 16px;
      color: rgba(var(--dark), .5);
      font-weight: 500;
      transform-origin: 0 0;
      transform: translate3d(0, 0, 0);
      transition: all .2s ease;
      pointer-events: none;
    }

    #editPage .inp .focus-bg {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(var(--dark), .05);
      z-index: -1;
      transform: scaleX(0);
      transform-origin: left;
    }

    #editPage .inp input {
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      border: 0;
      padding: 16px 12px 0 12px;
      height: 56px;
      font-size: 16px;
      font-weight: 400;
      background: rgba(var(--dark), .02);
      box-shadow: inset 0 -1px 0 rgba(var(--dark), .3);
      color: var(--dark);
      transition: all .15s ease;
    }

    #editPage .inp input:hover {
      background: rgba(var(--dark), .04);
      box-shadow: inset 0 -1px 0 rgba(var(--dark), .5);
    }

    #editPage .inp input:not(:placeholder-shown) + .label {
      color: rgba(var(--dark), .5);
      transform: translate3d(0, -12px, 0) scale(.75);
    }

    #editPage .inp input:focus {
      background: rgba(var(--dark), .05);
      outline: none;
      box-shadow: inset 0 -2px 0 var(--primary);
    }

    #editPage .inp input:focus + .label {
      color: var(--primary);
      transform: translate3d(0, -12px, 0) scale(.75);
    }

    #editPage .inp input:focus + .label + .focus-bg {
      transform: scaleX(1);
      transition: all .1s ease;
    }

    .button-9 {
      appearance: button;
      backface-visibility: hidden;
      background-color: var(--primary);
      border-radius: 6px;
      border-width: 0;
      box-shadow: rgba(50, 50, 93, .1) 0 0 0 1px inset,rgba(50, 50, 93, .1) 0 2px 5px 0,rgba(0, 0, 0, .07) 0 1px 1px 0;
      box-sizing: border-box;
      color: #fff;
      cursor: pointer;
      font-family: -apple-system,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Ubuntu,sans-serif;
      font-size: 100%;
      height: 44px;
      line-height: 1.15;
      outline: none;
      overflow: hidden;
      padding: 0 25px;
      position: relative;
      text-align: center;
      text-transform: none;
      transform: translateZ(0);
      transition: all .2s,box-shadow .08s ease-in;
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
      margin: 3px 0;
    }

    #editPage .button-9:focus {
      box-shadow: rgba(50, 50, 93, .1) 0 0 0 1px inset, rgba(50, 50, 93, .2) 0 6px 15px 0, rgba(0, 0, 0, .1) 0 2px 2px 0, rgba(50, 151, 211, .3) 0 0 0 4px;
    }

    :root {
      --gray: #34495e;
      --darkgray: #2c3e50;
    }

    #editPage input[type="text"] {
      color: #fff;
      background-color: var(--darkgray);
      background-image: none;
      cursor: pointer;
      padding: 0 1em;
      border: 0;
      box-shadow: none;
      border-radius: .25em;
      margin-bottom: 2px;
    }

    #editPage input[type="text"]:focus {
      outline: none;
    }

    #editPage select {
      appearance: none;
      outline: 10px red;
      border: 0;
      box-shadow: none;
      flex: 1;
      padding: 0 1em;
      color: #fff;
      background-color: var(--darkgray);
      background-image: none;
      cursor: pointer;
    }

    #editPage select::-ms-expand {
      display: none;
    }

    #editPage .select {
      position: relative;
      display: flex;
      width: 20em;
      height: 3em;
      border-radius: .25em;
      overflow: hidden;
    }

    #editPage .select::after {
      content: "↓";
      position: absolute;
      top: 0;
      right: 0;
      padding: 1em;
      background-color: #34495e;
      transition: .25s all ease;
      pointer-events: none;
    }

    #editPage .select:hover::after {
      color: #007BFF;
    }
  </style>
  
  <div id="editButtons" style="display: none; width: 100%; height: 90%; overflow-y: scroll;">
    <div id="inputs-container">
      <button_inputs>
    </div>
    <button class="button-9" id="add-btn" style="color: black; background-color: #39FF14">Add Button</button>
    <button class="button-9" id="add-btn" onclick="saveLayout()" style="color: black; background-color: #39FF14">Save Layout</button>
  </div>
  <script>
    initializeButtonListeners();

    function initializeButtonListeners() {
      document.querySelectorAll("#inputs-container .input-group").forEach(group => {
        const iconInput = group.querySelector("input[type='file']");
        const iconPreview = group.querySelector("#icon-preview");
        const actionTypeSelect = group.querySelector("select");
        const hotkeyInput = group.querySelector("#Hotkey");
        const cmdInput = group.querySelector("#Command");
        const micInput = group.querySelector("#Microphone");

        iconPreview.addEventListener("click", () => {
          iconInput.click();
        });

        iconInput.addEventListener("change", () => {
          const reader = new FileReader();
          reader.onload = (e) => {
            iconPreview.src = e.target.result;
            iconPreview.style.height = "50px";
            iconPreview.style.width = "50px";
            iconPreview.style.padding = "0";
          };
          reader.readAsDataURL(iconInput.files[0]);
        });

        actionTypeSelect.addEventListener("change", () => {
          const selectedAction = actionTypeSelect.value;
          hotkeyInput.style.display = selectedAction === "Hotkey" ? "block" : "none";
          cmdInput.style.display = selectedAction === "Command" ? "block" : "none";
          micInput.style.display = selectedAction === "Microphone" ? "block" : "none";
        });
      });
    }
    async function saveLayout() {
      let buttons = []

      document.querySelectorAll("div.input-group").forEach(e => {
        let icon = e.querySelector("#icon-preview")
        let iconSrc = icon.default ? '' : icon.src
        let type = e.querySelector("select").value
        let value = e.querySelector(`input#${type}`).value

        buttons.push({
          "image": iconSrc,
          "action": `${type}-=:=-${value}`
        })
      })

      await fetch(`/hotkeys/saveLayout?password=${([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{[curr[0]]:curr[1]})),{})["password"]}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: buttons })
      })

      window.location.href = "http://<ip>:<port>/?password=" + "<password>&appId=yPNIETrAqfDMmpFaXZgJcuvOCohewmwQ"
    }
    document.getElementById("add-btn").addEventListener("click", function() {
      const inputGroup = document.createElement("div")
      inputGroup.classList.add("input-group")

      const iconInput = document.createElement("input")
      iconInput.style = "display: none"
      iconInput.type = "file"
      iconInput.accept = "image/*"
      const iconPreview = document.createElement("img")
      iconPreview.id = "icon-preview"
      iconPreview.style.display = "block"
      iconPreview.style.height = "30px"
      iconPreview.style.width = "30px"
      iconPreview.style.padding = "10px"
      iconPreview.default = true
      iconPreview.src = "data:image/png;base64,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"

      iconPreview.addEventListener("click", function() {
        iconInput.click()
      })
      iconInput.addEventListener("change", function() {
        const reader = new FileReader()
        reader.onload = function(e) {
          iconPreview.src = e.target.result
          iconPreview.default = false
          iconPreview.style.height = "50px"
          iconPreview.style.width = "50px"
          iconPreview.style.padding = "0"
        }
        reader.readAsDataURL(iconInput.files[0])
      })

      const parentDiv = document.createElement("div")
      parentDiv.classList.add("select")
      const actionTypeSelect = document.createElement("select")
      const options = ["Hotkey", "Command", "Microphone"]
      options.forEach(option => {
        const optionElement = document.createElement("option")
        optionElement.value = option
        optionElement.textContent = option
        actionTypeSelect.appendChild(optionElement)
      })
      parentDiv.appendChild(actionTypeSelect)

      const hotkeyInput = document.createElement("input")
      hotkeyInput.id = "Hotkey"
      hotkeyInput.type = "text"
      hotkeyInput.placeholder = "Key combination (e.g., 'ctrl+c', or 'play/pause media')"
      hotkeyInput.style.display = "none"

      const cmdInput = document.createElement("input")
      cmdInput.id = "Command"
      cmdInput.type = "text"
      cmdInput.placeholder = "Enter command (e.g., 'start https://www.chatgpt.com/' to open ChatGPT)"
      cmdInput.style.display = "none"

      const micInput = document.createElement("input")
      micInput.id = "Microphone"
      micInput.type = "text"
      micInput.placeholder = "Toggle microphone"
      micInput.style.display = "none"
      micInput.disabled = true

      function updateValueDropdown() {
        const selectedAction = actionTypeSelect.value
        hotkeyInput.style.display = selectedAction === "Hotkey" ? "block" : "none"
        cmdInput.style.display = selectedAction === "Command" ? "block" : "none"
        micInput.style.display = selectedAction === "Microphone" ? "block" : "none"
      }

      actionTypeSelect.addEventListener("change", updateValueDropdown)
      updateValueDropdown()

      const deleteBtn = document.createElement("button")
      deleteBtn.textContent = "Delete"
      deleteBtn.classList.add("button-9")
      deleteBtn.style.backgroundColor = "#ED3419"
      deleteBtn.addEventListener("click", function() {
        inputGroup.remove()
      })

      inputGroup.appendChild(iconInput)
      inputGroup.appendChild(iconPreview)
      inputGroup.appendChild(parentDiv)
      inputGroup.appendChild(micInput)
      inputGroup.appendChild(hotkeyInput)
      inputGroup.appendChild(cmdInput)
      inputGroup.appendChild(deleteBtn)

      document.getElementById("inputs-container").appendChild(inputGroup)
    })
  </script>""".replace("<button_inputs>", button_inputs)

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
      <img onclick="hotkeys_runAction(`{i["action"]}`)" src="{i["image"]}" style="width: 100%; border-radius: 16px;">
    </div>"""
  
  for i in range(len(keys), rows * columns - 1):
    buttons += f"""
    <div class="grid-item">
    </div>"""

  buttons += f"""
    <div class="grid-item">
      <img onclick="editButtons()" src="data:image/png;base64,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" style="width: 100%; border-radius: 16px;">
    </div>"""
  
  return """
    <script>
      function editButtons() {
        document.querySelector("div.grid-container").style.display = "none"
        document.getElementById("editButtons").style.display = "block"
      }

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
    <div class="parent" id="editPage">
      <div class="grid-container">
        <buttonElements>
      </div>
      <editButtons>
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
  """.replace("<buttonElements>", buttons).replace("<x>", str(columns)).replace("<y>", str(rows)).replace("<editButtons>", editButtonsPage()).replace("<ip>", getSetting("ip", "ScreenDeck")).replace("<port>", str(getSetting("port", "ScreenDeck"))).replace("<password>", PASSWORD)
