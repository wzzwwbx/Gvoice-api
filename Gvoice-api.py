from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

import crawler

app = Flask(__name__)

results = [
    {
        'title': u'title1',
        'content': u'This is content1',
        'pictureUrl': 'https://www.baidu.com/img/bd_logo1.png',
        'url': 'https://www.baidu.com'
    }
]


@app.route('/gvoice/api/v1.0/results', methods=['GET'])
def get_results():
    return jsonify({'results': results})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/gvoice/api/v1.0/query', methods=['POST'])
def create_query():
    if not request.json or not 'query' in request.json:
        abort(400)
    result = query(request.json['query'])
    print(result)
    return jsonify({'result': result}), 200


def query(query_string):

    '''TODO: implement a crawler for query string
    '''
    return crawler.search(query_string)




if __name__ == '__main__':
    app.run(host='192.168.69.45')
