def mainSettingsWrapper(settings):
  return f"""
    <div style="width: 90%; height: 55vh;">
      {settings}
      <button onclick="saveSettings()" style="color: black;">Save</button>
    </div>
    <script>
      async function saveSettings() {{
        document.getElementById("loading").style.display = "flex"
        data = {{}}
        for (let i of document.querySelector("#subScreen").querySelectorAll("input")) {{
          setting = i.id.split("￾")
          data[setting[0]] = data[setting[0]] ?? {{}}
          data[setting[0]][setting[1]] = i.value
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
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
        
        <meta name="apple-mobile-web-app-capable" content="yes">
        <link rel="icon" href="data:image/x-icon;base64,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" type="image/x-icon">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <script>
          function closeApp() {
            document.getElementById("mainContent").style.display = "block"
            document.getElementById("homeScreen").style.display = "flex"
            document.getElementById("subScreenFull").style.display = "none"
            document.getElementById("subScreen").style.display = "none"
            document.getElementById("cross").style.display = "none"
          }

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
            document.getElementById("loading").style.display = "none"
          }

          function fullscreen() {
            closeApp()
            let element = document.getElementById("widget")
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
        </script>
          
        <style>
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
                display: flex;
                flex-direction: column;
                align-items: center;
                padding-top: 12px;
                overflow-y: scroll;
                width: 80%;
                height: 55vh;
                -ms-overflow-style: none;
                scrollbar-width: none;
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
        <div id="loading" style="z-index: 0; background-color: rgba(255, 255, 255, 0.25); width: 100%; height: 100%; position: absolute; display: none; justify-content: center; align-items: center;">
          <i style="font-size: min(18vh, 60px);" class="fa fa-spinner fa-pulse" aria-hidden="true"></i>
        </div>
        <div class="cross" id="cross" style="display: none; margin: 20px;" onclick="fullscreen()">
          <img src="data:image/png;base64,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">
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
        <div id="subScreenFull" style="position: relative; z-index: 100;"></div>
      </body>
    </html>""".replace("<apps>", apps)
