# coding=utf-8
from .. import app
import logging
from flask import Flask, request, render_template, jsonify, Markup, abort, make_response, Response

#from flask_restful import Resource, Api, reqparse
from .response import koscom_response
#from slackclient import SlackClient


#api = Api(app)
# Your app's Slack bot user token
SLACK_BOT_TOKEN = 'xoxb-85954337637-367075388229-UX1fBNie8uSzTR7F1NzaDAZw'
SLACK_VERIFICATION_TOKEN = 'xxoxp-85954337637-85948092656-366936922818-87e4c4d2ca0bcf6f8664d129e79094f4'
SLACK_API_TOKEN = 'xoxp-85954337637-85948092656-366323959264-5a8636c2ed6dd2a71dbc14d70ea59d18'

user_id = "C2HUDAP5Y"
#parser = reqparse.RequestParser()
#parser.add_argument('text')


# Slack client for Web API requests
# slack_client = SlackClient(SLACK_BOT_TOKEN)
#
# user_id = "0CAV5XME"
#
# order_dm = slack_client.api_call(
# 	"chat.postMessage",
# 	as_user=True,
# 	channel=user_id,
# 	text="I am Coffeebot ::robot_face::, and I\'m here to help bring you fresh coffee :coffee:",
# 	attachments=[{
# 		"text": "",
# 		"callback_id": user_id + "coffee_order_form",
# 		"color": "#3AA3E3",
# 		"attachment_type": "default",
# 		"actions": [{
# 			"name": "coffee_order",
# 			"text": ":coffee: Order Coffee",
# 			"type": "button",
# 			"value": "coffee_order"
# 		}]
#  	}]
# )
#
# # Create a new order for this user in the COFFEE_ORDERS dictionary
# COFFEE_ORDERS[user_id] = {
# 	"order_channel": order_dm["channel"],
# 	"message_ts": "",
# 	"order": {}
# }


#api_response = {}
# # Use by pure Flask
@app.route ('/', methods = ['GET','POST'])
def index():
	return "POST Gensurance RestfulAPI"


@app.route ('/genapi', methods = ['GET','POST'])
def genapi():
	return "Welcome Gensurance API"


@app.route ('/genapi/message_actions', methods = ['POST'])
def message_actions():
	user = 'data'#request.form['name']

	body_response = {'name':user}
	return jsonify(body_response),201
# Parse the request payload
	#message_action = json.loads(request.form["payload"])
	#user_id = message_action["user"]["id"]
	#messages = json.dump(message_action)

	#
	# if message_action["type"] == "interactive_message":
    #     # Add the message_ts to the user's order info
    #     COFFEE_ORDERS[user_id]["message_ts"] = message_action["message_ts"]
	# 	# Show the ordering dialog to the user
	# 	open_dialog = slack_client.api_call(
    #         "dialog.open",
    #         trigger_id=message_action["trigger_id"],
    #         dialog={
    #             "title": "Request a coffee",
    #             "submit_label": "Submit",
    #             "callback_id": user_id + "coffee_order_form",
    #             "elements": [
    #                 {
    #                     "label": "Coffee Type",
    #                     "type": "select",
    #                     "name": "meal_preferences",
    #                     "placeholder": "Select a drink",
    #                     "options": [
    #                         {
    #                             "label": "Cappuccino",
    #                             "value": "cappuccino"
    #                         },
    #                         {
    #                             "label": "Latte",
    #                             "value": "latte"
    #                         },
    #                         {
    #                             "label": "Pour Over",
    #                             "value": "pour_over"
    #                         },
    #                         {
    #                             "label": "Cold Brew",
    #                             "value": "cold_brew"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     )
	#
    #     print(open_dialog)
	#
    #     # Update the message to show that we're in the process of taking their order
    #     slack_client.api_call(
    #         "chat.update",
    #         channel=COFFEE_ORDERS[user_id]["order_channel"],
    #         ts=message_action["message_ts"],
    #         text=":pencil: Taking your order...",
    #         attachments=[]
    #     )
	#
    # elif message_action["type"] == "dialog_submission":
    #     coffee_order = COFFEE_ORDERS[user_id]
	#
    #     # Update the message to show that we're in the process of taking their order
    #     slack_client.api_call(
    #         "chat.update",
    #         channel=COFFEE_ORDERS[user_id]["order_channel"],
    #         ts=coffee_order["message_ts"],
    #         text=":white_check_mark: Order received!",
    #         attachments=[]
    #     )

	#return make_response(message_action, 200)


@app.errorhandler(404)
def page_not_found(error):
	return "Page not found", 404

@app.errorhandler(Exception)
def unhandled_exception(error):
	app.logger.error('Unhandled Exception: %s', (error))
	return "Exception", 500

#Use by Restful
#class Home(Resource):
#    def get(self):
#        return "Gensurance RestfulAPI"

#class Price(Resource):
#    def get(self, issue_code):
#        try:
#            if issue_code is None :
#                result = jsonify({})
#            else:
#                data = {"mode":"price",
#                        "input":{"issue_code":issue_code}
#                        }
#                result = koscom_response(data)
#        except Exception as e:
#            result = jsonify ({'errmsg': e })
#            logging.debug(e)
#        finally:
#            return result

#api.add_resource(Home, '/')
#api.add_resource(Price, '/kospi/price/<string:issue_code>')
