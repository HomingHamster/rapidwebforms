# RapidWebForms v0.01

import uuid
import time
import http.server

# Name your configuration file
import examplewebsite as config

class RapidServer(http.server.BaseHTTPRequestHandler):
    '''
    Class for running http server, generates html source from config
    '''

    def _renderform(self, form):
        fields = []

        for i in form["fields"]:
            if "name" in i.keys() and "type" in i.keys():

<<<<<<< HEAD
                field = {"name":i["name"], "field_type":i["type"]}
                if "options" in i.keys():
                    field["options"] = i["options"]

                fields+=[Field(**field)]
=======
                field = [i["name"], i["type"]]
                if "options" in i.keys():
                    field+=[i["options"]]

                fields+=[Field(*field)]
>>>>>>> origin/master

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

                self.wfile.write(bytes(('<html><head><title>%s</title><link rel="stylesheet" '
                        'href="http://yui.yahooapis.com/pure/0.6.0/pure-min.css"><meta name="viewport"'
                        ' content="width=device-width, initial-scale=1"><style>body{padding:40px;}'
                        '</style></head><body><div class="content">') % (conf["name"]), "utf-8"))
                self.wfile.write(bytes(self._renderform(conf), "utf-8"))
                self.wfile.write(bytes("</div><center><p>RapidWebForms v0.01</p></center></body></html>", "utf-8"))

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

        html="""
            <form class="pure-form pure-form-stacked">
                <fieldset>
                    <legend><h1>%s</h1><p>%s</p></legend>
                    %s
                    <button type="submit" class="pure-button pure-button-primary">Finished</button>
                </fieldset>
            </form>
        """ % (self.name, self.desc, fields_html)
        return html

class Field():
    """
    This class is responsible for containing each form field and outputting the html representation.
    """
    def __init__(self, name, field_type, initial_value=None, options=None):
        self.name = name
        self.field_type = field_type
        self.initial_value = initial_value
        self.options = options
        self.field_id = uuid.uuid4()

    def as_html(self):

        if self.field_type == "select":

<<<<<<< HEAD
            opts = " ".join(["<option>" + o + "</option>" for o in self.options])
=======
            opts = ["<option>" + o + "</option>" for o in options].join(" ")
>>>>>>> origin/master

            html = """
                <label for="%s">%s</label>
                    <select id="%s">
                        %s 
                    </select>
            """ % (self.field_id, self.name, self.field_id, opts)

        elif self.field_type == "checkbox":

            html = """
                <label for="%s" class="pure-checkbox">
                    <input id="%s" type="checkbox"> %s
                </label>
            """ % (self.field_id, self.field_id, self.name)

        elif self.field_type == "seperator":

            html = "<hr />"

        else:

            html = """
                <label for="%s">%s</label>
                <input id="%s" type="%s" placeholder="%s">
            """ % (self.field_id, self.name, self.field_id, self.field_type, self.initial_value)

        return html

if __name__=="__main__":

    server_class = http.server.HTTPServer
    httpd = server_class((config.server_address, config.server_port), RapidServer)

    print(time.asctime(), "Server Starts - %s:%s" % (config.server_address, config.server_port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print(time.asctime(), "Server Stops - %s:%s" % (config.server_address, config.server_port))