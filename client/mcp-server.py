from fastmcp import FastMCP, Image
import requests
import base64
from PIL import Image as PILImage
from typing import List
from io import BytesIO

mcp = FastMCP("VNCControlServer")

HOST = "172.17.0.2" # Default docker address
PORT = 3737 # Default VNC port

IMG = None

url = f"http://{HOST}:{PORT}"

def check_connectivity():
    try:
        res = requests.get(f"{url}/").json()
        if (res["status"] != "success"):
            raise Exception(f"Cannot connect to address: {url}")
    except Exception as e:
        print(str(e))

def read_image_as_base64_stream(image: Image, format: str = 'PNG'):
    # Create an in-memory bytes buffer
    buffer = BytesIO()
    # Save the image to the buffer in the specified format
    image.save(buffer, format=format)
    # Get the byte data from the buffer
    image_data = buffer.getvalue()
    # Encode to base64 and return as string
    return base64.b64encode(image_data)

@mcp.tool()
def get_screen_size():
    """Get the size of the screen."""
    return requests.get(f"{url}/screen-size/").json()

@mcp.tool()
def take_screenshot():
    """Take a screenshot and then store it."""
    global IMG
    try:
        res = requests.get(f"{url}/screenshot/").json()
        if (res["status"] == "success"):
            b64_data = res["data"]
            image_data = base64.b64decode(b64_data.encode())
            buffer = BytesIO(image_data)
            IMG = PILImage.open(buffer)
            return Image(data=b64_data.encode(), format="PNG")
        else:
            raise Exception("Failure from server.")
    except Exception as e:
        return {"status": "failure", "error": str(e)}

@mcp.tool()
def observe_screenshot():
    """Observe the screenshot that was previous taken and stored."""
    if (IMG):
        img_data = read_image_as_base64_stream(IMG)
        return Image(data=img_data, format="PNG")
    else:
        return {"status": "failure", "error": "Image is empty, please take a screenshot first."}

@mcp.tool()
def save_screenshot(filename: str):
    """Save the locally stored screenshot"""
    try: 
        IMG.save(filename)
    except Exception as e:
        return {"status": "failure", "error": str(e)}

@mcp.tool()
def observe_screenshot_region(x: int, y: int, w: int, h: int):
    """Observe the stored screenshot in the selected region"""
    if (IMG):
        cropped = IMG.crop(x, y, x+w, y+h)
        img_data = read_image_as_base64_stream(cropped)
        return Image(data=img_data, format="PNG")
    else:
        return "Image is empty, please take a screenshot first."

@mcp.tool()
def wait():
    """Wait 3 seconds."""
    return requests.get(f"{url}/wait/").json()

@mcp.tool()
def left_click(x: int, y: int):
    """Left click at position (x,y)."""
    return requests.post(f"{url}/left-click/{str(x)}/{str(y)}").json()

@mcp.tool()
def double_click(x: int, y: int):
    """Double click at position (x,y)."""   
    return requests.post(f"{url}/double-click/{str(x)}/{str(y)}").json()

@mcp.tool()
def right_click(x: int, y: int):
    """Right click at position (x,y)."""
    return requests.post(f"{url}/right-click/{str(x)}/{str(y)}").json()

@mcp.tool()
def scroll(where: str):
    """Scroll to direction, can choose from one of 'left', 'right', 'up', 'down'."""
    return requests.post(f"{url}/scroll/{where}").json()

@mcp.tool()
def drag_to(x: int, y: int):
    """Drag from current mouse position to position (x,y)."""
    return requests.post(f"{url}/drag/{str(x)}/{str(y)}").json()

@mcp.tool()
def type_text(text: str):
    """Type a string of text."""
    return requests.post(f"{url}/type/{text}").json()

@mcp.tool()
def press_keys(keys: List[str]):
    """Press a list of keys. For one key input, please also put in a list. """
    data = {"keys": keys}
    return requests.post(f"{url}/press/", data=data).json()

@mcp.tool()
def press_key_combinations(keys: List[str]):
    """Press a key combination. Reserved for key combinations such as ['ctrl', 'c'], ['ctrl', 'shift', 's']. """
    data = {"keys": keys}
    return requests.post(f"{url}/key-combination/", data=data).json()

if __name__ == "__main__":
    # print("Server starting...", file=sys.stderr)
    try:
        check_connectivity()
    except Exception as e:
        exit(1)
    mcp.run()
