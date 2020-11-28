from flask import Flask, render_template
from flask import jsonify
from flask import request, Response
from flask import abort
from flask_cors import CORS
import json
# import SearchSystem
from SearchSystem import searchService
# import webbrowser
# from SearchSystem import tools
# from SearchSystem import searchService

# from gevent.wsgi import WSGIServer
# from gevent import monkey



app = Flask(__name__,
            static_url_path="",
            static_folder="./dist",
            template_folder="./dist")

# 热更新
app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True

# 解决跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

port = "8080"


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route('/api/authUser', methods=["POST"])
def authUser():
    pkt = request.get_json()
    print(pkt)

    return jsonify({
        "msg": "ok",
        "id": 123
    })

#
#   params={"fetchWays":int}
#   searWord:str
@app.route('/api/getArticles', methods=["GET"])
def getPages():
    print(request.args)
    searchWord = request.args['searchWord']
    searchChoice = int(request.args["searchChoice"])
    resultList = searchService.runservice(searchChoice, searchWord)
    
    return jsonify({
        "resultList": resultList
    })


@app.route('/api/getArticleContent', methods=["GET"])
def getPageArticle():
    pageID = request.args["pageID"]
    title, content = searchService.getArticle(pageID)
    
    return jsonify({
        "title":title,
        "content":content
    })

if __name__ == '__main__':
    # webbrowser.open("http://127.0.0.1:"+port)
    app.run(processes=True,host="0.0.0.0", port=port)
