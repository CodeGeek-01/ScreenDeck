def mainSettingsWrapper(settings):
  return f"""
    <style>
      #settings input {{
        background: none;
        color: #d6d6d6; 
        font-size: 18px;
        padding: 2px 0;
        display: block;
        width: 320px;
        border: none;
        border-radius: 0;
        border-bottom: 1px solid #cccccc;
        margin-left: 12px;
        flex: 1;
        height: 80%;
      }}

      #settings input:focus {{
        outline: none;
        border-bottom: 1px solid #0077FF;
      }}

      .checkbox-wrapper-3 input[type="checkbox"] {{
        visibility: hidden;
        display: none;
      }}

      .checkbox-wrapper-3 .toggle {{
        position: relative;
        display: block;
        width: 40px;
        height: 20px;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
        transform: translate3d(0, 0, 0);
      }}

      .checkbox-wrapper-3 .toggle:before {{
        content: "";
        position: relative;
        top: 3px;
        left: 3px;
        width: 34px;
        height: 14px;
        display: block;
        background: #9A9999;
        border-radius: 8px;
        transition: background 0.2s ease;
      }}

      .checkbox-wrapper-3 .toggle span {{
        position: absolute;
        top: 0;
        left: 0;
        width: 20px;
        height: 20px;
        display: block;
        background: white;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgba(154, 153, 153, 0.5);
        transition: all 0.2s ease;
      }}

      .checkbox-wrapper-3 .toggle span:before {{
        content: "";
        position: absolute;
        display: block;
        margin: -18px;
        width: 56px;
        height: 56px;
        background: #0077FF;
        border-radius: 50%;
        transform: scale(0);
        opacity: 1;
        pointer-events: none;
      }}

      .checkbox-wrapper-3 input:checked + .toggle:before {{
        background: #00AAFF;
      }}

      .checkbox-wrapper-3 input:checked + .toggle span {{
        background: #0077FF;
        transform: translateX(20px);
        transition: all 0.2s cubic-bezier(0.8, 0.4, 0.3, 1.25), background 0.15s ease;
        box-shadow: 0 3px 8px rgba(79, 46, 220, 0.2);
      }}

      .checkbox-wrapper-3 input:checked + .toggle span:before {{
        transform: scale(1);
        opacity: 0;
        transition: all 0.4s ease;
      }}

    </style>
    <div style="width: 90%; height: 55vh; overflow-y: scroll;" id="settings">
      <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: center;">
        <h1 style="font-weight: bold;">Settings</h1>
        <button onclick="killServer()" style="appearance: button; backface-visibility: hidden; font-weight: bold; background-color: #ED3419; border-radius: 6px; border-width: 0; box-shadow: rgba(50, 50, 93, 0.1) 0 0 0 1px inset, rgba(50, 50, 93, 0.1) 0 2px 5px 0, rgba(0, 0, 0, 0.07) 0 1px 1px 0; box-sizing: border-box; color: white; cursor: pointer; font-family: -apple-system, system-ui, 'Segoe UI', Roboto, 'Helvetica Neue', Ubuntu, sans-serif; font-size: 75%; height: 30px; line-height: 1.15; margin: 2px 0 0; outline: none; overflow: hidden; padding: 0 16px; position: relative; text-align: center; text-transform: none; transform: translateZ(0); transition: all 0.2s, box-shadow 0.08s ease-in; user-select: none; -webkit-user-select: none; touch-action: manipulation;">Kill Server</button>
      </div>
      {settings}
      <center>
        <button onclick="saveSettings()" style="appearance: button; backface-visibility: hidden; font-weight: bold; background-color: #39FF14; border-radius: 6px; border-width: 0; box-shadow: rgba(50, 50, 93, 0.1) 0 0 0 1px inset, rgba(50, 50, 93, 0.1) 0 2px 5px 0, rgba(0, 0, 0, 0.07) 0 1px 1px 0; box-sizing: border-box; color: black; cursor: pointer; font-family: -apple-system, system-ui, 'Segoe UI', Roboto, 'Helvetica Neue', Ubuntu, sans-serif; font-size: 100%; height: 44px; line-height: 1.15; margin: 2px 0 0; outline: none; overflow: hidden; padding: 0 16px; position: relative; text-align: center; text-transform: none; transform: translateZ(0); transition: all 0.2s, box-shadow 0.08s ease-in; user-select: none; -webkit-user-select: none; touch-action: manipulation;">Save</button>
      </center>
    </div>
    <script>
      function killServer() {{
        let text = "Are you sure you want to shut down the server? This will require you to restart it manually."
        if (confirm(text) == true) {{
          fetch(`/killServer?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{{[curr[0]]:curr[1]}})),{{}})["password"]}}`, {{
            method: 'POST',
            headers: {{
              'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{}})
          }})
        }}
      }}

      async function saveSettings() {{
        document.getElementById("loading").style.display = "flex"
        data = {{}}
        for (let i of document.querySelector("#subScreen").querySelectorAll("input")) {{
          setting = i.id.split("￾")
          data[setting[0]] = data[setting[0]] ?? {{}}
          if (i.type == "checkbox") data[setting[0]][setting[1]] = i.checked
          else data[setting[0]][setting[1]] = i.value
        }}
        
        await fetch(`/saveSettings?password=${{([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{{[curr[0]]:curr[1]}})),{{}})["password"]}}`, {{
          method: 'POST',
          headers: {{
            'Content-Type': 'application/json'
          }},
          body: JSON.stringify(data)
        }})
        document.getElementById("loading").style.display = "none"
        alert("Settings have been saved")
      }}
    </script>
  """


def settingsWrapper(programName, settings):
  return f"""
    <h2 style="color: white; margin: 0;">{programName}</h2>
    <div style="background-color: #313131; height: 3px; border-radius: 2px; margin: 10px 0;"></div>
    {settings}
    <div style="padding-bottom: 18px;"></div>
  """


def appWidget(name, appId, icon):
  return f"""
    <div class="button" id="button1" onclick="load('{appId}')">
      <div class="button-inline">
        <img src="{icon}">
        <p>{name}</p>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">
        <path d="M5,1 L9,5 L5,9" fill="none" stroke="white" stroke-width="1"/>
      </svg>
    </div>
  """


def homePage(apps):
  return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
        
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="viewport" content="user-scalable=no">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="mobile-web-app-status-bar-style" content="black-translucent">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <script>
          async function closeApp() {
            document.getElementById("mainContent").style.display = "block"
            document.getElementById("homeScreen").style.display = "flex"
            document.getElementById("subScreenFull").style.display = "none"
            document.getElementById("subScreen").style.display = "none"
            document.getElementById("cross").style.display = "none"

            let response = await fetch(`/close?password=${([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{[curr[0]]:curr[1]})),{})["password"]}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              }
            })

            response.text().then(text => {
              new Function(text)()
            })
          }

          let timeoutId;

          async function load(id) {
            document.getElementById("loading").style.display = "flex"
            let response = await fetch(`/load?password=${([...(new URLSearchParams(window.location.search))]).reduce((prev,curr)=>(Object.assign(prev,{[curr[0]]:curr[1]})),{})["password"]}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({id: id})
            })
            let result = await response.json()

            let scripts = []
            if (result.fs === "True") {
              document.getElementById("cross").style.display = "block"
              document.getElementById("mainContent").style.display = "none"
              document.getElementById("subScreenFull").style.display = "flex"
              document.getElementById("subScreenFull").innerHTML = result.html
              scripts = document.getElementById('subScreenFull').querySelectorAll("script")
            } else {
              document.getElementById("homeScreen").style.display = "none"
              document.getElementById("subScreen").style.display = "flex"
              document.getElementById("subScreen").innerHTML = result.html
              scripts = document.getElementById('subScreen').querySelectorAll("script")
            }
            for (let i = 0; i < scripts.length; i++) {
              const script = document.createElement('script')
              script.text = scripts[i].text
              document.head.appendChild(script).parentNode.removeChild(script)
            }

            clearTimeout(timeoutId)
            timeoutId = setTimeout(() => {{
              document.getElementById("loading").style.display = "none"
            }}, 250)
          }

          function fullscreen() {
            closeApp()
            fullBody()
          }

          function fullBody() {
            let element = document.querySelector("body")
            if (element.requestFullscreen) {
              element.requestFullscreen()
            } else if (element.webkitRequestFullscreen) {
              element.webkitRequestFullscreen()
            } else if (element.msRequestFullscreen) {
              element.msRequestFullscreen()
            }
          }

          let c = true
          const segmentMap = {
            0: ['a', 'b', 'c', 'e', 'f', 'g'],
            1: ['c', 'f'],
            2: ['a', 'c', 'd', 'e', 'g'],
            3: ['a', 'c', 'd', 'f', 'g'],
            4: ['b', 'c', 'd', 'f'],
            5: ['a', 'b', 'd', 'f', 'g'],
            6: ['a', 'b', 'd', 'e', 'f', 'g'],
            7: ['a', 'c', 'f'],
            8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            9: ['a', 'b', 'c', 'd', 'f', 'g'],
            10: []
          }

          function setDisplay(displayId, number) {
            let display = document.getElementById("display" + displayId)

            display.querySelectorAll('.dot').forEach(dot => {
              dot.style.opacity = "0"
            })

            segmentMap[number].forEach(segment => {
              display.querySelectorAll(".seg-" + segment).forEach(dot => {
                dot.style.opacity = "1"
              })
            })
          }

          setInterval(() => {
            let now = new Date()

            let minutes = now.getMinutes().toString().split("").map(e => parseInt(e))
            if (minutes.length == 1) minutes = [0, minutes[0]]
            let hours = now.getHours().toString().split("").map(e => parseInt(e))
            if (hours.length == 1) hours = [10, hours[0]]

            setDisplay(1, hours[0])
            setDisplay(2, hours[1])
            setDisplay(3, minutes[0])
            setDisplay(4, minutes[1])

            document.getElementById("day").innerHTML = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"][now.getDay()]

            if (c) {
              document.getElementById("display5").querySelectorAll(".dot").forEach(dot => {
                dot.style.opacity = "0"
              })
              c = false
            } else {
              document.getElementById("display5").querySelectorAll(".dot").forEach(dot => {
                dot.style.opacity = "1"
              })
              c = true
            }
          }, 750)

          document.addEventListener("DOMContentLoaded", (event) => {
            let urlParams = new URLSearchParams(window.location.search)
            let appId = urlParams.get('appId')

            if (appId) {
              load(appId)
            }
          })
        </script>
          
        <style>
            * {
              touch-action: pan-y;
              scrollbar-width: none;
            }

            *::-webkit-scrollbar {
              display: none;
            }
            
            html, body {
                touch-action: manipulation;
                background: black;
                height: 100%;
                width: 100%;
                margin: 0;
            }

            #mainContent, #subScreenFull {
                height: 100%;
            }
            
            #subScreenFull {
              display: none;
            }

            * {
                font-family: "Roboto", sans-serif;
                font-weight: 400;
                color: white;
            }

            :root {
                --time-width: 50%;
            }

            .main {
                height: 100%;
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: center;
            }

            .left {
                width: var(--time-width);
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                height: 100%;
                width: 50%;
            }
            
            #subScreen, #subScreenFull {
                overflox-y: scroll;
            }

            .right {
                width: calc(100% - var(--time-width));
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }

            .display, .altDisplay {
                display: grid;
                grid-template-rows: repeat(11, 1fr);
                grid-template-columns: repeat(6, 1fr);
                gap: 2px;
            }

            .altDisplay {
                grid-template-columns: repeat(1, 1fr);
            }

            .dot, .empty {
                width: 0.82vw;
                height: 0.82vw;
                background-color: white;
                color: white;
                background: white;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .empty {
                background-color: transparent;
            }

            .timer {
                display: flex;
                flex-direction: row;
                gap: 2vw;
                justify-content: center;
                width: 100%;
            }

            #button {
                font-size: 200%;
                margin: 25vh 25vw;
                width: 50vw;
                height: 50vh;
            }

            .left p {
                background-color: white;
                color: black;
                padding: 3.5px;
                border-radius: 3px;
                font-size: 130%;
            }

            .devider {
                width: 80%;
                background: #313131;
                height: 3px;
                border-radius: 2px;
            }

            .right p {
                margin-bottom: 3px;
            }

            .button-container {
                overscroll-behavior: contain; 
                -webkit-overflow-scrolling: touch;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding-top: 12px;
                overflow-y: scroll;
                width: 80%;
                height: 55vh;
                -ms-overflow-style: none;
                scrollbar-width: none;
                touch-action: pan-y;
            }

            .button-container::-webkit-scrollbar {
                display: none;
            }

            .button {
                width: 95%;
                margin-bottom: 5px;
                height: 20%;
                border-radius: 10px;
                background: #313131;
                border: 2px solid transparent;
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }

            .button:hover {
                border: 2px solid #555555;
            }

            .button-inline {
                height: 100%;
                width: 100%;
                display: flex;
                flex-direction: row;
                align-items: center;
            }

            .button .button-inline img {
                height: 90%;
                padding-left: 5px;
                border-radius: 50%;
            }

            .button .button-inline p {
                margin: 0;
                padding-left: 7px;
                font-size: 120%;
                font-weight: 600
            }

            svg {
                height: 45%;
                width: 45%;
                margin-right: -8%;
            }

            .cross {
                position: absolute;
                z-index: 101;
                top: 2vh;
                right: 2vh;
            }

            .cross img {
                height: 8vh;
                aspect-ratio: 1;
            }
        </style>
      </head>
      <body>
        <div id="loading" style="z-index: 999999; background-color: rgba(255, 255, 255, 0.25); width: 100%; height: 100%; position: absolute; display: none; justify-content: center; align-items: center;">
          <i style="font-size: min(18vh, 60px);" class="fa fa-spinner fa-pulse" aria-hidden="true"></i>
        </div>
        <div id="mainContent">
          <div id="widget" class="main">
            <div class="left" onclick="fullscreen()">
              <div class="timer">
                <div class="display" id="display1">
                  <div class="empty"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="empty"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="empty"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="empty"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="empty"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                </div>

                <div class="display" id="display2">
                  <div class="empty"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="empty"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="empty"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="empty"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="empty"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                </div>

                <div class="altDisplay" id="display5">
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                </div>

                <div class="display" id="display3">
                  <div class="empty"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="empty"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="empty"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="empty"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="empty"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                </div>

                <div class="display" id="display4">
                  <div class="empty"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="dot seg-a"></div>
                  <div class="empty"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="dot seg-b"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-c"></div>
                  <div class="empty"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="dot seg-d"></div>
                  <div class="empty"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="dot seg-e"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="empty"></div>
                  <div class="dot seg-f"></div>
                  <div class="empty"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                  <div class="dot seg-g"></div>
                </div>
              </div>
              <p id="day"></p>
            </div>
            <div id="homeScreen" class="right">
              <p>HOME</p>
              <div class="devider"></div>
              <div class="button-container">
                <apps>
              </div>
            </div>
            <div style="display: none; position: relative; z-index: 100;" id="subScreen" class="right"></div>
          </div>
        </div>
        <div id="subScreenFull" style="position: relative; z-index: 100; align-items:center; justify-content: center;"></div>
        <div class="cross" id="cross" style="display: none; position: absolute; margin: 20px; z-index: 101;" onclick="fullscreen()">
          <img src="data:image/png;base64,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">
        </div>
      </body>
    </html>""".replace("<apps>", apps)

def enterPassword():
  return """
  <html>
    <head>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
        
      <style>
        body, html, div {
          height: 100%;
          width: 100%;
          margin: 0;
          padding: 0;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .main {
          background: black;
          display: flex;
          flex-direction: column;
        }

        :root {
          --primary: #0077FF;
          --dark: white;
        }

        * {
          font-family: "Roboto", sans-serif;
          font-weight: 300;
          color: white;
          box-sizing: border-box;
        }

        .inp {
          position: relative;
          margin: 0 auto;
          width: 100%;
          max-width: 280px;
          border-radius: 3px;
          overflow: hidden;
          background: rgba(255,255,255,0.1);
          box-shadow: inset 0 -2px 0 rgba(255, 255, 255, 0.2);
        }

        .inp .label {
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

        .inp .focus-bg {
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

        .inp input {
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

        .inp input:hover {
          background: rgba(var(--dark), .04);
          box-shadow: inset 0 -1px 0 rgba(var(--dark), .5);
        }

        .inp input:not(:placeholder-shown) + .label {
          color: rgba(var(--dark), .5);
          transform: translate3d(0, -12px, 0) scale(.75);
        }

        .inp input:focus {
          background: rgba(var(--dark), .05);
          outline: none;
          box-shadow: inset 0 -2px 0 var(--primary);
        }

        .inp input:focus + .label {
          color: var(--primary);
          transform: translate3d(0, -12px, 0) scale(.75);
        }

        .inp input:focus + .label + .focus-bg {
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
          margin: 12px 0 0;
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
        }

        .button-9:focus {
          box-shadow: rgba(50, 50, 93, .1) 0 0 0 1px inset, rgba(50, 50, 93, .2) 0 6px 15px 0, rgba(0, 0, 0, .1) 0 2px 2px 0, rgba(50, 151, 211, .3) 0 0 0 4px;
        }
      </style>
    </head>
    <body>
      <div class="main">
        <label for="inp" class="inp">
          <input type="text" id="inp" placeholder="&nbsp;">
          <span class="label">Password</span>
          <span class="focus-bg"></span>
        </label>

        <button class="button-9" onclick="submitPassword()">Submit</button>
      </div>

      <script>
        function submitPassword() {
          let url = new URL(window.location.href)
          url.searchParams.set("password", document.getElementById("inp").value)
          window.location.href = url.toString()
        }
      </script>
    </body>
  </html>
  """
