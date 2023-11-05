
from flask import Flask, request, jsonify
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)

@app.route('/gestureDrive', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    # command Scan is used to fetch radar data
    if data['command'] == 'N':
        import random
        data_list = []
        for i in range(181):
            data_list.append(random.randint(0, 400))
        # print(data_list)
        return jsonify({'data':data_list}) 
    
    # other motion control commands - Front, Back, Left, Right, Stop
    else:
        return jsonify({}) 
    
if __name__ == '__main__':
    app.run()
