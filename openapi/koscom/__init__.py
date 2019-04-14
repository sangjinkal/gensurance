# coding=utf-8
from flask import Flask
from flask_restful import Resource, Api, reqparse


def create_app(name = __name__):

    app = Flask(__name__)
    return app
