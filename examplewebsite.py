# RapidWebForms v0.01 - example config
#

########################################
# Basic Server Config
########################################
server_name 			= "RapidServer"
server_description		= "Instant webforms from static files"
server_address			= "127.0.0.1"
server_port				= 5678

########################################
# Baisic Example Form
########################################
one_form = {
	"name":						"yourformname",
	"description":				"yourformdescription",

	#types: select, checkbox, email, password, text, seperator
	"fields" :[
		{"type": "text", 		"name": "first field"},
		{"type": "email",		"name": "email field"},
		{"type": "seperator"},
		{"type": "password",	"name": "password"},
		{"type": "checkbox", 	"name": "opt out of emails"},
	]
}

########################################
# Contact Example Form
########################################
contact_form = {
	"name": 					"Contact Form",
	"description": 				"Use the form below to contact us.",

	#types: select, checkbox, email, password, text, seperator
	"fields" : [
		{"type":"text", 		"name": "first field"},
		{"type":"text", 		"name": "second field"},
		{"type":"seperator"},
		{"type":"text", 		"name": "age"},
<<<<<<< HEAD
		{"type":"select", 		"name": "selectoption", 	"options":["option1", "secondoption", "333333"]},
=======
		{"type":"select", 		"name": "selectoption", 	"values":["option1", "secondoption", "333333"]},
>>>>>>> origin/master
	]
}

########################################
# Forms to appear on http server
########################################
active_forms = {
	"/"					: one_form,
	"/contact"			: contact_form,
}