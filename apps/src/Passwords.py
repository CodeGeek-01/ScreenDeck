from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import keyboard
import base64

PasswordDecryptionKey: str = None

generate_key = lambda seed: base64.urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'\x00' * 16, iterations=100000, backend=default_backend() ).derive(seed.encode()))
encrypt_string = lambda text: Fernet(PasswordDecryptionKey).encrypt(text.encode()).decode()
decrypt_string = lambda text: Fernet(PasswordDecryptionKey).decrypt(text.encode()).decode()


@app.route("/password/setPassword", methods=["POST"])
def password_setPassword():
  if request.args.get('password') == PASSWORD:
    pw = request.get_json()["password"]
    if pw != -2147483647:
      global PasswordDecryptionKey
      PasswordDecryptionKey = generate_key(pw)
  return passwordLoadContent()


@app.route("/password/enterUsername", methods=["POST"])
def password_enterUsername():
  if request.args.get('password') == PASSWORD:
    x = request.get_json()['content']
    with open('passwords.txt', 'r', encoding="utf-8") as file:
      for num, line in enumerate(file, start=1):
        if num == x:
          keyboard.write(decrypt_string(line.split("￢==!￢;")[1]))
  return ""


@app.route("/password/enterPassword", methods=["POST"])
def password_enterPassword():
  if request.args.get('password') == PASSWORD:
    x = request.get_json()['content']
    with open('passwords.txt', 'r', encoding="utf-8") as file:
      for num, line in enumerate(file, start=1):
        if num == x:
          keyboard.write(decrypt_string(line.split("￢==!￢;")[2]))
  return ""

def append_line(file_path, line):
  with open(file_path, 'a', encoding="utf-8") as file:
    file.write(line + """
""")


@app.route("/password/savePasswords", methods=["POST"])
def password_savePasswords():
  if request.args.get('password') == PASSWORD:
    data = request.get_json()
    actionType = data["type"]
    body = data["body"]
    if actionType == 0:
      with open("passwords.txt", 'r') as file:
        lines = file.readlines()

        for index in sorted(body, reverse=True):
          if 0 <= index - 1 < len(lines):
            lines.pop(index - 1)

        with open("passwords.txt", 'w') as file:
          file.writelines(lines)
    elif actionType == 1:
      append_line("passwords.txt", f"{body[2]}￢==!￢;{encrypt_string(body[0])}￢==!￢;{encrypt_string(body[1])}")

  return ""


def load():
  return passwordLoadContent()


def passwordLoadContent():
  if PasswordDecryptionKey != None:
    with open('passwords.txt', 'a'):
      pass
    profiles = ""
    editProfiles = ""
    c = 0
    with open('passwords.txt', 'r', encoding="utf-8") as file:
      for line in file:
        c += 1
        try:
          values = line.split("￢==!￢;")
          image = values[0]
          username = decrypt_string(values[1])
          password = decrypt_string(values[2])

          pos = username.find("@")
          if pos != -1:
            username = username[:2] + len(username[2:pos]) * "*" + username[pos:]
          else:
            username = username[:2] + (len(username) - 2) * "*"
          profiles += f"""
            <div style="margin: 5px 20px; background: #313131; border-radius: 8px; width: calc(100% - 40px); height: 64px; display: flex; flex-direction: row; align-items: center;">
              <img src="{image}" style="max-width: 40px; max-height: 100%; padding: 5px;"> {username} : {password[0:2]}{"*" * (len(password) - 2)}
              <p style="flex-grow: 1; height: 1px;"></p>
              <div onclick="passwordsPasteUsername({c})" style="width: 45px; height: 45px; border-radius: 6px; margin: 5px; font-size: 28px; background-color: #6666EE; display: flex; align-items: center; justify-content: center;">
                <i class="fa fa-user"></i>
              </div>
              <div onclick="passwordsPastePassword({c})" style="width: 45px; height: 45px; border-radius: 6px; margin: 5px; font-size: 28px; background-color: #AA0000; display: flex; align-items: center; justify-content: center;">
                <i class="fa fa-key"></i>
              </div>
            </div>
          """
          editProfiles += f"""
            <div id="del{c}" style="margin: 5px 20px; background: #313131; border-radius: 8px; width: calc(100% - 40px); height: 64px; display: flex; flex-direction: row; align-items: center;">
              <img src="{image}" style="max-width: 40px; max-height: 100%; padding: 5px;"> {username} : {password[0:2]}{"*" * (len(password) - 2)}
              <p style="flex-grow: 1; height: 1px;"></p>
              <div onclick="passwordsDelete({c})" style="width: 45px; height: 45px; border-radius: 6px; margin: 5px; font-size: 28px; background-color: #AA0000; display: flex; align-items: center; justify-content: center;">
                <i class="fa fa-trash"></i>
              </div>
            </div>
          """
        except:
          pass
    return f"""
      <style>
        #passwordList::-webkit-scrollbar, #editPasswordList::-webkit-scrollbar {{
          display: none;
        }}
        
        input[type="file"] {{
          display: none;
        }}
      </style>
      <div id="passwordList" style="width: 100%; max-height: 400px; overflow-y: scroll; overflow-x: hidden;">
        {profiles}
        <center>
          <button onclick="passwordsEdit()" style="background-color: #6666EE; border: 2px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 3px 5px; font-size: 19px; margin-top: 10px;">Edit</button>
        </center>
      </div>
      <div id="editPasswordList" style="display: none; width: 100%; max-height: 400px; overflow-y: scroll; overflow-x: hidden;">
        {editProfiles}
        <center>
          <button onclick="passwordsNew()" style="background-color: #00CC00; border: 2px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 3px 5px; font-size: 19px; margin-top: 10px;">Add</button><br>
          <button onclick="passwordsSave()" style="background-color: #6666EE; border: 2px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 3px 5px; font-size: 19px; margin-top: 10px;">Save</button>
          <button onclick="passwordsCancel()" style="background-color: #AA0000; border: 2px solid rgba(0, 0, 0, 0.1); border-radius: 4px; padding: 3px 5px; font-size: 19px; margin-top: 10px;">Cancel</button>
        </center>
      </div>
      <script>
        function passwordsPasteUsername(x) {{
          fetch(`/password/enterUsername?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{{[curr[0]]:curr[1]}})),{{}})["password"]}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
              content: x
            }})
          }})
        }}
      
        function passwordsPastePassword(x) {{
          fetch(`/password/enterPassword?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{{[curr[0]]:curr[1]}})),{{}})["password"]}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
              content: x
            }})
          }})
        }}
        
        function passwordsEdit() {{
          deletePasswordList = []
          document.getElementById('passwordList').style.display = "none"
          document.getElementById('editPasswordList').style.display = "block"
        }}
        
        function passwordsCancel() {{
          fetch(`/password/setPassword?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{{[curr[0]]:curr[1]}})),{{}})["password"]}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ password: -2147483647 }})
          }}).then(res => {{
            res.text().then(data => {{
              document.getElementById("subScreen").innerHTML = data

              scripts = document.getElementById('subScreen').querySelectorAll("script")
              for (let i = 0; i < scripts.length; i++) {{
                const script = document.createElement('script')
                script.text = scripts[i].text
                document.head.appendChild(script).parentNode.removeChild(script)
              }}
            }})
          }})
        }}
        
        function passwordsNew() {{
          let node = document.createElement("div")
          node.id = "newAccount"
          node.style.margin = "5px 20px"
          node.style.background = "#313131"
          node.style.borderRadius = "8px"
          node.style.width = "calc(100% - 40px)"
          node.style.height = "64px"
          node.style.display = "flex"
          node.style.flexDirection = "row"
          node.style.alignItems = "center"
          node.style.justifyContent = "center"
          let id = `_${{Math.random()}}`
          node.innerHTML = `
          <input type="file" id="${{id}}" name="filename" accept="image/png">
          <label for="${{id}}">
            <i class="fa fa-camera"></i>
          </label>
          <input style="padding: 2px; margin: 4px; background-color: transparent; margin-top: 8px; color: white; font-size: 16px; border: 1px solid white; border-radius: 5px;" type="text" id="user" name="user">
          <input style="padding: 2px; margin: 4px; background-color: transparent; margin-top: 8px; color: white; font-size: 16px; border: 1px solid white; border-radius: 5px;" type="password" id="password" name="password">
          `
          let ePWList = document.getElementById("editPasswordList")
          ePWList.insertBefore(node, ePWList.children[ePWList.children.length - 1])
        }}
        
        let deletePasswordList = []
        function passwordsDelete(x) {{
          document.getElementById("editPasswordList").removeChild(document.getElementById(`del${{x}}`))
          deletePasswordList.push(x)
        }}
        
        function getBase64(file) {{
          return new Promise((resolve, reject) => {{
            let reader = new FileReader()
            reader.onload = function(event) {{
              resolve(event.target.result)
            }};
            reader.onerror = function(error) {{
              reject(error)
            }};
            reader.readAsDataURL(file)
          }})
        }}

        function savePassword(name, pw, img) {{
          return fetch(`/password/savePasswords?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev, curr) => (Object.assign(prev, {{ [curr[0]]: curr[1] }})), {{}}).password}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ type: 1, body: [name, pw, img] }})
          }})
        }}

        async function passwordsSave() {{
          await fetch(`/password/savePasswords?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev, curr) => (Object.assign(prev, {{ [curr[0]]: curr[1] }})), {{}}).password}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ type: 0, body: deletePasswordList }})
          }})
      
          const savePromises = []
      
          document.querySelectorAll("div#newAccount").forEach(element => {{
            let inputs = element.querySelectorAll("input")
            if (inputs[2].value === "" || inputs[1].value === "") return
    
            if (inputs[0].files.length > 0) {{
              const base64Promise = getBase64(inputs[0].files[0])
                .then((base64String) => {{
                  return savePassword(inputs[1].value, inputs[2].value, base64String)
                }})
                .catch(() => {{
                  return savePassword(inputs[1].value, inputs[2].value, "")
                }})
              savePromises.push(base64Promise)
            }} else {{
              savePromises.push(savePassword(inputs[1].value, inputs[2].value, ""))
            }}
          }})
      
          await Promise.all(savePromises)
    
          afterPasswordsSave()
        }}
        
        function afterPasswordsSave() {{
          fetch(`/password/setPassword?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{{[curr[0]]:curr[1]}})),{{}})["password"]}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ password: -2147483647 }})
          }}).then(res => {{
            res.text().then(data => {{
              document.getElementById("subScreen").innerHTML = data
            }})
          }})
        }}
      </script>
    """
  else:
    return """
      <style>
        button:hover {
          cursor: pointer;
        }
      </style>
      <script>
        function submitPassword() {
          fetch(`/password/setPassword?password=${([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{[curr[0]]:curr[1]})),{})["password"]}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: document.getElementById("pwq").value })
          }).then(res => {
            res.text().then(data => {
              document.getElementById("subScreen").innerHTML = data

              scripts = document.getElementById('subScreen').querySelectorAll("script")
              for (let i = 0; i < scripts.length; i++) {
                const script = document.createElement('script')
                script.text = scripts[i].text
                document.head.appendChild(script).parentNode.removeChild(script)
              }
            })
          })
        }
      </script>
      <label for="input_string">Password:</label>
      <input id="pwq" style="padding: 2px; background-color: transparent; margin-top: 8px; color: white; font-size: 16px; border: 1px solid white; border-radius: 5px;" type="password" id="password" name="password">
      <button onclick="submitPassword()" style="background-color: #1457F6; padding: 4px; margin: 6px; font-size: 15px; border: 1.5px solid rgba(0, 0, 255, 0.1); border-radius: 3px;">Login</button>
    """
  
def close():
  global PasswordDecryptionKey
  PasswordDecryptionKey = None
