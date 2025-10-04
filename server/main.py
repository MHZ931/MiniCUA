from typing import List
from fastapi import FastAPI, Form
import pyautogui
from PIL import Image
from io import BytesIO
import base64
import time

app = FastAPI()

@app.get("/")
def hello_world():
    return {"status": "success", "message": "Hello world!"}

# Screenshots
def read_image_as_base64_stream(image: Image, format: str = 'PNG'):
    # Create an in-memory bytes buffer
    buffer = BytesIO()
    # Save the image to the buffer in the specified format
    image.save(buffer, format=format)
    # Get the byte data from the buffer
    image_data = buffer.getvalue()
    # Encode to base64 and return as string
    return base64.b64encode(image_data).decode()

@app.get("/screen-size/")
def get_screen_size():
    return {"status": "success", "size": pyautogui.size()}

@app.get("/screenshot/")
def take_screenshot():
    try: 
        img = pyautogui.screenshot()
        img_data = read_image_as_base64_stream(img)
        return {"status": "success", "format": "PNG", "data": img_data}
    except Exception as e:
        return {"status": "failure", "error": str(e)}



@app.get("/screenshot/region/{x}/{y}/{w}/{h}/")
def take_screenshot_in_region(x: int, y: int, w: int, h: int):
    try: 
        img = pyautogui.screenshot(region=(x, y, w, h))
        img_data = read_image_as_base64_stream(img)
        return {"status": "success", "format": "PNG", "data": img_data}
    except Exception as e:
        return {"status": "failure", "error": str(e)}
    

@app.get("/wait/")
def wait():
    time.sleep(3)
    return {"status": "success"}

# Mouses
@app.post("/left-click/{x}/{y}")
def left_click(x: int, y: int):
    try: 
        pyautogui.click(x=x, y=y)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}

@app.post("/double-click/{x}/{y}")
def double_click(x: int, y: int):
    try: 
        pyautogui.click(x=x, y=y, clicks=2, interval=0.1)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}

@app.post("/right-click/{x}/{y}")
def right_click(x: int, y: int):
    try: 
        pyautogui.click(x=x, y=y, button="right")
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}


@app.post("/scroll/{where}")
def scroll(where: str):
    try:
        match where:
            case "left":
                pyautogui.hscroll(-5)
            case "right":
                pyautogui.hscroll(5)
            case "up":
                pyautogui.scroll(5)
            case "down":
                pyautogui.scroll(-5)
            case _:
                raise Exception("Nowhere to scroll. Please choose 'left', 'right', 'up', 'down'.")
    except Exception as e:
        return {"status": "failure", "error": str(e)}
	

@app.post("/drag/{x}/{y}")
def drag_to(x: int, y: int):
    try: 
        pyautogui.dragTo(x, y, button='left')
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}

# Typing
@app.post("/type/{text}")
def type_text(text: str):
    try: 
        pyautogui.write(text, interval=0.1)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}


@app.post("/press/")
def press_keys(keys: List[str] = Form(...)):
    try: 
        pyautogui.press(keys)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}

@app.post("/key-combination/")
def press_key_combinations(keys: List[str] = Form(...)):
    try: 
        pyautogui.hotkey(*keys)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3737, reload=True)
