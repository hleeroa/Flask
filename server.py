import flask
from flask import jsonify, request
from flask.views import MethodView
from models import Session, Post
from sqlalchemy.exc import IntegrityError

app = flask.Flask("app")

class HttpError(Exception):
    def __init__(self, status_code: int, error_msg: str | dict | list):
        self.error_msg = error_msg
        self.status_code = status_code

@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    http_response = flask.jsonify({"status": "error", "msg": err.error_msg})
    http_response.status = err.status_code

    return http_response

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(http_response: flask.Response):
    request.session.close()
    return http_response

def add_post(post: Post):
    try:
        request.session.add(post)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "post already exists")  
    return post          


def get_post(post_id):
    post = request.session.get(Post, post_id)
    if post is None:
        raise HttpError(404, "post not found")
    return post

class PostView(MethodView):
    def get(self, post_id: int):
        post = get_post(post_id)
        return jsonify(post.json)

    def post(self):
        json_data = request.json
        post = Post(**json_data)
        post = add_post(post)
        return {"id": post.id}

    def patch(self, post_id: int):
        post = get_post(post_id)
        json_data = request.json
        for field, value in json_data.items():
            setattr(post, field, value)
        post = add_post(post)
        return post.json

    def delete(self, post_id: int):
        post = get_post(post_id)
        request.session.delete(post)
        request.session.commit()
        return jsonify({"status": "deleted"})

post_view = PostView.as_view("post")
app.add_url_rule("/post/", view_func=post_view, methods=["POST"])
app.add_url_rule("/post/<int:post_id>/", view_func=post_view, methods=["GET", "PATCH", "DELETE"])

app.run()
