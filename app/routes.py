from flask import Blueprint, request, jsonify
from app.cache import init_cache, get_label_infos
from app.openai_api import call_openAi

main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return 'Hello Flask World!!!'

@main.route('/cache-init')
def cache_init():
    init_cache()
    return "캐싱 완료!"

@main.route('/test-cache')
def cache_test():
    rs = get_label_infos("Speech")
    return rs

@main.route('/api/openai', methods=['POST'])
def openai_test():
    try:
        data = request.get_json()
        image_data = data.get('image_data')
        text = data.get('text')

        if not image_data or not text:
            return jsonify({"error": "image_data과 text를 모두 포함해야 합니다."}), 400

        res = call_openAi(image_data, text)

        return jsonify({"message": res}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
