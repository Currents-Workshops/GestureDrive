'''
dependencies
    pip install 
        - pyserial
        - Flask
        - requests
        - waitress
command to start server-> waitress-serve --listen=127.0.0.1:5000 app:app
'''

import serial
from flask import Flask, request, jsonify
app = Flask(__name__)

# init bluetooth connection with bot
def initialize():
    while True:
        try:
            app.serialPort = serial.Serial(port='COM4', baudrate=9600, timeout=1, parity=serial.PARITY_EVEN, stopbits=1)
            break
        except:
            continue
    print('connection established')

app.before_request_funcs = [(None, initialize())]

@app.route('/gestureDrive', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    # command Scan is used to fetch radar data
    if data['command'] == 'Scan':
        app.serialPort.write(bytes('Scan'.encode('utf-8')))
        while True:
            sensorData = app.serialPort.readline(800)
            if sensorData:
                res = sensorData.decode('utf-8').strip()
                data_list = [int(x) for x in res.split()]
                return jsonify({'data':data_list}) 
    # other motion control commands - Front, Back, Left, Right, Stop
    else:
        app.serialPort.write(bytes(data['command'].encode('utf-8')))
        return jsonify({}) 
    
if __name__ == '__main__':
    app.run(debug=True)
