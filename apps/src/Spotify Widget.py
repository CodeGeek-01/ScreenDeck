from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from spotipy.oauth2 import SpotifyOAuth
import comtypes
import spotipy

client_id = getSetting("Client ID", "GbqhCFGngQCzUBlVDdIoJIsLyxDatdNf")
client_secret = getSetting("Client Secret", "GbqhCFGngQCzUBlVDdIoJIsLyxDatdNf")
REDIRECT_URI = "http://<ip>:<port>/spotify/callback".replace("<ip>", getSetting("ip", "ScreenDeck")).replace("<port>", str(getSetting("port", "ScreenDeck")))

sp_oauth = SpotifyOAuth(
  client_id=client_id,
  client_secret=client_secret,
  redirect_uri=REDIRECT_URI,
  scope="user-read-playback-state"
)


sp = None
muteAds = "false"


def muteSpotify(state):
  comtypes.CoInitialize()
  sessions = AudioUtilities.GetAllSessions()
  for session in sessions:
    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    if session.Process and session.Process.name() == "Spotify.exe":
      volume.SetMasterVolume(1 if state is False else 0, None)


def close():
  return """
  clearInterval(spotifyIntervalID)
  """


def load():
  global muteAds
  muteAds = getSetting("Mute ADs")
  if sp is not None:
    return """
      <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div id="playback-info"></div>
        
        <div id="songDisplay">
          <style>
            @import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500;700&display=swap");
          </style>
          <div style="display: flex; flex-direction: row; justify-content: center; font-size: 20px; text-align: center;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 45vw;">
              <p id="albumName" style="font-family: 'Roboto Mono';"></p>
              <img id="albumCover" src="" alt="Album Cover" style="width: 35vw; border-radius: 8px;">
              <p style="font-family: 'Roboto Mono';" id="albumDate"></p>
            </div>
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 45vw;">
              <p style="font-family: 'Roboto Mono'; margin: 0; padding-bottom: 12px;" id="songTitle"></p>
              <div style="display: flex; flex-direction: row;">
                <p style="margin: 0; color: #AAAAAA; font-family: 'Roboto Mono'; padding-right: 8px;">By: </p>
                <p style="margin: 0; font-family: 'Roboto Mono';" id="songArtist"></p>
              </div>
              <div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
                <p style="font-family: 'Roboto Mono'; font-size: 12px;" id="currentTime"></p>
                <div style="background-color: #2F2F2F; border-radius: 100px; height: 9px; width: 28vw; padding: 2px; margin: 30px 10px;">
                  <div style="background-color: #2468AA; border-radius: 100px; height: 100%; width: 0%;" id="timeDisplay"></div>
                </div>
                <p style="font-family: 'Roboto Mono'; font-size: 12px;" id="maxTime"></p>
              </div>
            </div>
            <div style="position: absolute; bottom: 10px; right: 10px; padding: 10px;">
              <p style="margin: 0; color: #AAAAAA; font-family: 'Roboto Mono'; font-size: 17px;">Playing On: <span id="device"></span></p>
            </div>
            <div style="position: absolute; right: 10px; padding-right: 20px; transform: translate(0, 50%);">
              <i class="fa fa-volume-up"></i>
              <div style="margin: 10px; padding: 2px; width: 9px; height: 19vw; border-radius: 100px; background-color: #2F2F2F;">
                <div style="position: relative; width: 100%; height: 100%;">
                  <div style="background-color: #2468AA; border-radius: 100px; width: 100%; height: 0%; position: absolute; bottom: 0;" id="volumeDisplay"></div>
                </div>
              </div>
              <i class="fa fa-volume-down"></i>
            </div>
          </div>
        </div>

        <script>
          var playbackInfo = document.getElementById('playback-info');
          var songDisplay = document.getElementById('songDisplay');

          function formatMillisecondsToTime(ms) {
            const totalSeconds = Math.floor(ms / 1000);
            const minutes = Math.floor(totalSeconds / 60);
            const seconds = totalSeconds % 60;
            const formattedSeconds = seconds < 10 ? `0${seconds}` : seconds;
            return `${minutes}:${formattedSeconds}`;
          }

          function fetchPlaybackData() {
            try {
              fetch('/spotify/current_playback')
                .then(response => {
                  if (!response.ok) {
                    throw new Error("User not authenticated or no playback available.");
                  }
                  return response.json();
                })
                .then(data => {
                  playbackInfo.innerHTML = ``
                  songDisplay.style.display = "flex"
                  document.getElementById("albumName").textContent = data.album_name
                  document.getElementById("albumCover").src = data.album_cover
                  document.getElementById("albumDate").textContent = data.release_date
                  document.getElementById("songTitle").textContent = data.song_title
                  document.getElementById("songArtist").textContent = data.song_artist
                  document.getElementById("device").textContent = data.device_name
                  document.getElementById("currentTime").textContent = formatMillisecondsToTime(data.progress)
                  document.getElementById("maxTime").textContent = formatMillisecondsToTime(data.duration)
                  document.getElementById("timeDisplay").style.width = (data.progress / data.duration * 100) + "%"
                  document.getElementById("volumeDisplay").style.height = data.volume + "%"
                })
                .catch(error => {
                  songDisplay.style.display = "none"
                  playbackInfo.innerHTML = `<p style="margin-top: 20px; text-align: center;"><i>Error: ${error.message}</i></p>`;
                });
            } catch {}
          }
          
          var spotifyIntervalID = setInterval(fetchPlaybackData, 1000);
        </script>
      </div>
    """.replace("#2468AA", getSetting("Accent Color"))
  else:
    return """
    <div id="iframe"></div>
    <script>
      async function authenticateSpotify() {
        try {
          const response = await fetch('/spotify/auth_url');
          const data = await response.json();
          
          window.location.href = data.auth_url
        } catch (error) {
          console.error('Error during authentication:', error);
        }
      }

      authenticateSpotify();
    </script>
    """


@app.route('/spotify/auth_url', methods=['GET'])
def get_auth_url():
  auth_url = sp_oauth.get_authorize_url()
  return jsonify({"auth_url": auth_url})


@app.route('/spotify/callback')
def spotify_callback():
  global sp
  code = request.args.get('code')
  if code:
    access_token = sp_oauth.get_access_token(code, as_dict=False)
    sp = spotipy.Spotify(auth=access_token)

    user_profile = sp.me()
    user_name = user_profile.get('display_name', 'Unknown User')
    user_pfp = user_profile.get('images', [{}])[0].get('url', '')
    return f"""
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Signed in</title>
          <style>
            body {{
              background-color: #121212;
              display: flex;
              justify-content: center;
              align-items: center;
              height: 98vh;
              flex-direction: column;
            }}
          </style>
        </head>
        <body>
          <h1 style="font-family: 'Roboto'; color: white;">Logged in as</h1>
          <img src="{user_pfp}" alt="Profile Picture" style="width: 10vh; border-radius:50%;">
          <p style="font-family: 'Roboto'; color: white;">{user_name}</p>
          <p style="font-family: 'Roboto'; color: #AAAAAA; font-style: italic;">You will be redirected soon...</p>
          <script>
            setTimeout(() => {{
              window.location.href = "http://<ip>:<port>/?password=" + "{PASSWORD}&appId=GbqhCFGngQCzUBlVDdIoJIsLyxDatdNf"
            }}, 3500)
          </script>
        </body>
      </html>
      """.replace("<ip>", getSetting("ip", "ScreenDeck")).replace("<port>", str(getSetting("port", "ScreenDeck")))
  else:
    return "Authorization failed."


def format_date(date_str, custom_format):
  try:
    year, month, day = date_str.split("-")

    formatted_date = custom_format.replace("YYYY", year)
    formatted_date = formatted_date.replace("MM", month)
    formatted_date = formatted_date.replace("DD", day)

    return formatted_date
  except:
    try:
      year, month = date_str.split("-")

      formatted_date = custom_format.replace("YYYY", year)
      formatted_date = formatted_date.replace("MM", month)
      formatted_date = formatted_date.replace("DD", "01")

      return formatted_date
    except:
      try:
        formatted_date = custom_format.replace("YYYY", date_str)
        formatted_date = formatted_date.replace("MM", "01")
        formatted_date = formatted_date.replace("DD", "01")

        return formatted_date
      except:
        return "Unkown"

@app.route('/spotify/current_playback', methods=['GET'])
def spotify_current_playback():
  global sp
  if sp is None:
    return jsonify({"error": "User not authenticated"}), 401

  current_track = sp.current_playback()
  if current_track is None:
    return jsonify({"error": "No playback information available."}), 404

  if not current_track['currently_playing_type'] == "ad":
    if muteAds == True:
      muteSpotify(False)

    album_cover = current_track['item']['album']['images'][0]['url']
    album_name = current_track['item']['album']['name']
    song_title = current_track['item']['name']
    song_artist = current_track['item']['artists'][0]['name']
    duration = current_track['item']['duration_ms']
    progress = current_track['progress_ms']
    device_name = current_track['device']['name']
    state = current_track['is_playing']
    volume = current_track['device']['volume_percent']
    date = current_track['item']['album']['release_date']

    return jsonify({
      "album_cover": album_cover,
      "album_name": album_name,
      "song_title": song_title,
      "song_artist": song_artist,
      "duration": duration,
      "progress": progress,
      "device_name": device_name,
      "state": state,
      "volume": volume,
      "release_date": format_date(date, getSetting("Date Format", "GbqhCFGngQCzUBlVDdIoJIsLyxDatdNf"))
    })
  
  else:
    if muteAds == True:
      muteSpotify(True)
    return jsonify({
      "album_cover": "https://dilimangeogging.files.wordpress.com/2018/10/44246252_286677478721382_1989078906161856512_n.jpg?w=1960&h=1960&crop=1",
      "album_name": "",
      "song_title": "Advertisement",
      "song_artist": "Spotify",
      "duration": 0.01,
      "progress": 0.01,
      "device_name": current_track['device']['name'],
      "state": current_track['is_playing'],
      "volume": current_track['device']['volume_percent'],
      "release_date": ""
    })
