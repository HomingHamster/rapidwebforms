# RapidWebForms v0.01

import uuid
import time
import http.server
from string import Template

# Name your configuration file
import examplewebsite as config

class RapidServer(http.server.BaseHTTPRequestHandler):
    '''
    Class for running http server, generates html source from config
    '''

    def _renderform(self, form):
        fields = []

        for i in form["fields"]:
            field={}
            if "name" in i.keys():
                field["name"] = i["name"]
            if "type" in i.keys():
                field["field_type"] = i["type"]
            if "options" in i.keys():
                field["options"] = i["options"]

            fields+=[Field(**field)]

        html_form = Form(form["name"], form["description"], fields).as_html()

        return html_form

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.do_HEAD()

        for uri_key in config.active_forms.keys():

            if self.path == uri_key:
                conf=config.active_forms[uri_key]

                form_template = open("templates/default/page.html").read()
                form_template = Template(form_template).safe_substitute(title=conf["name"],
                    content=self._renderform(conf))

                self.wfile.write(bytes(form_template, "utf-8"))

    #def do_POST(self, )

class Form():
    def __init__(self, name, description, list_of_fields):
        self.name = name
        self.desc = description
        self.fields = list_of_fields

    def as_html(self):
        fields_html=""
        for i in self.fields:
            fields_html += i.as_html()

        return Template(open("templates/default/form.html").read()).safe_substitute(title=self.name,
            description=self.desc, items=fields_html)


class Field():
    """
    This class is responsible for containing each form field and outputting the html representation.
    """
    def __init__(self, field_type, name=None, initial_value=None, options=None):
        self.name = name
        self.field_type = field_type
        self.initial_value = initial_value
        self.options = options
        self.field_id = uuid.uuid4()

    def as_html(self):

        if self.field_type == "select":

            opts = " ".join([Template(open("templates/default/partials/option.select.form.html").read())
                    .safe_substitute(option=o) for o in self.options])

            html = Template(open("templates/default/partials/select.form.html").read()).safe_substitute(
                    id=self.field_id, name=self.name, optionshtml=opts)

        elif self.field_type == "checkbox":

            html = Template(open("templates/default/partials/checkbox.form.html").read())\
                    .safe_substitute(id=self.field_id, name=self.name)

        elif self.field_type == "seperator":

            html = open("templates/default/partials/seperator.form.html").read()

        else:

            html = Template(open("templates/default/partials/input.form.html").read())\
                    .safe_substitute(id=self.field_id, name=self.name, fieldtype=self.field_type,
                        placeholder=self.initial_value)

        return html

if __name__ == "__main__":

    server_class = http.server.HTTPServer
    httpd = server_class((config.server_address, config.server_port), RapidServer)

    print(time.asctime(), "Server Starts - %s:%s" % (config.server_address, config.server_port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print(time.asctime(), "Server Stops - %s:%s" % (config.server_address, config.server_port))