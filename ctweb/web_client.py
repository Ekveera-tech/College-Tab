from websocket import create_connection
from io import StringIO
import json
import base64

fp = StringIO()
#image = cam.getImage().flipHorizontal().getPIL()
#image.save(fp, 'JPEG')
ws = create_connection("ws://localhost:8001/websocket")
print("Sending 'Hello, World'...")
ws.send("Hello, World")

#ws.send(fp.getvalue().encode("base64"))
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()

"""
ret, image_np = cap.read()
        IMAGE_SHAPE = image_np.shape
        encoded_image = base64.encodestring(image_np)
        print(type(encoded_image))
        payload = {
            'from': 'rasp',
            'image': encoded_image.decode('utf-8'),
            'shape': IMAGE_SHAPE,
        }

        data = json.dumps(payload)

        try:
            # Send encoded image data.
            await websocket.send(data)

            # receive server message
            received_data = await websocket.recv()
            print('< {}'.format(received_data))

            # image = base64.b64decode(received_data)
            # np_image = np.fromstring(image, dtype=np.uint8)
            # source = np_image.reshape(IMAGE_SHAPE)
            return websocket
        except Exception:
            print('WebSocket send or receive error.')
            exit(1)
            
"""