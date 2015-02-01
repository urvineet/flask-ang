from flask_restful import abort
from flask_restful.representations import json


__author__ = 'Vineet Shivhare'

from flask import Flask, request, Response, render_template , make_response
from flask.ext.restful import Resource, Api
from model import declare, service

app = Flask(__name__)

api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/')
def index():
    return make_response(open('templates/index.html').read())


@app.route('/<username>')
def contact(username):
    return make_response(open('templates/contact.html').read())


def res_json(data):
    return Response(json.dumps(data, default=str), mimetype='application/json')


def res_data_pass(data):
    return {'status': 'SUCCESS', 'data': data}


def res_data_fail(data):
    return {'status': 'ERROR', 'data': data}


class UserAPI(Resource):
    def get(self):
        try:
            return res_json(res_data_pass(service.GetSession().get_user_list()))
        except Exception as e:
            print e
            abort(400)


    def post(self):
        try:
            request_json_data = request.get_json()
            print(request_json_data)
            if request_json_data:
                if request_json_data.has_key('user_name'):
                    if service.GetSession().add_user(request_json_data.__getitem__('user_name')):
                        return res_json(res_data_pass("ADDED"))
                    else:
                        return res_json(res_data_fail("ISSUE"))
                else:
                    return res_json(res_data_fail("ISSUE"))
            else:
                return res_json(res_data_fail("ISSUE"))
        except Exception as e:
            print(e)
            abort(400)


    def delete(self):
        try:
            request_json_data = request.get_json()
            if request_json_data:
                if request_json_data.has_key('user_name'):
                    if service.GetSession().del_user(request_json_data.__getitem__('user_name')):
                        return res_json(res_data_pass("DELETED"))
                    else:
                        return res_json(res_data_fail("ISSUE"))
                else:
                    return res_json(res_data_fail("ISSUE"))
            else:
                return res_json(res_data_fail("ISSUE"))
        except Exception as e:
            print(e)
            abort(400)


class ContactAPI(Resource):
    def get(self, username):
        try:
            return res_json(res_data_pass(service.GetSession().get_list_of_contact(username)))
        except Exception as e:
            print e
            abort(400)

    def post(self, username):
        try:
            request_json_data = request.get_json()
            if request_json_data:
                if request_json_data.has_key('name') and request_json_data.has_key('number'):
                    if service.GetSession().add_contact(request_json_data.__getitem__('number'),
                                                        username, request_json_data.__getitem__(
                                    'name')):
                        print "dsdsds"
                        if service.GetSession().add_contact_with_user_ref(username, request_json_data.__getitem__(
                                'number')):
                            return res_json(res_data_pass("ADDED"))
                    else:
                        return res_json(res_data_fail("ISSUE"))
                else:
                    return res_json(res_data_fail("ISSUE"))
            else:
                return res_json(res_data_fail("ISSUE"))
        except Exception as e:
            print(e)
            abort(400)


    def delete(self, username):
        try:
            request_json_data = request.get_json()
            if request_json_data:
                if request_json_data.has_key('name') and request_json_data.has_key('number'):
                    if service.GetSession().del_contact(username, request_json_data.__getitem__('name'),
                                                        request_json_data.__getitem__('number')):
                        return res_json(res_data_pass("DELETED"))
                    else:
                        return res_json(res_data_fail("ISSUE"))
                else:
                    return res_json(res_data_fail("ISSUE"))
            else:
                return res_json(res_data_fail("ISSUE"))
        except Exception as e:
            print(e)
            abort(400)


api.add_resource(UserAPI, '/v1/user')
api.add_resource(ContactAPI, '/v1/contact/<username>')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, threaded=True, debug='true')
