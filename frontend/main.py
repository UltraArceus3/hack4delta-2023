from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """<p>Hello, World!</p>
    <style>.embed-container {position: relative; padding-bottom: 80%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 50%; height: 50%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="CA Wildfires" src="//connecticut.maps.arcgis.com/apps/Embed/index.html?webmap=395c014b25084e80846320a0cfa8dfd0&extent=-122.0797,36.4177,-119.0474,37.906&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"></iframe></div>
    
    """