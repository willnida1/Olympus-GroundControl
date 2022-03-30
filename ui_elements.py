
import re

from aiohttp import web

class Element:
    """ base class for a node in the widget tree """
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.parent = None
        self.identifier = None

    def render(self):
        """ returns a str of the html that encodes this element (and child elements).
            Put the elements javascript inline with the html
        """
        pass

    def add_child(self, child):
        """ adds a child element in the element tree """
        self.nodes.append(child)
        child.parent = self

    def get_identifier(self):
        """ generates a unique (but consistent) id that can be used in client - server communication """
        if self.identifier is not None:
            return self.identifier
        if self.parent is None:
            self.identifier = self.name
        else:
            self.identifier = self.parent.get_identifier() + "." + self.name
            # we assume an element's name is unique among siblings

        return self.identifier

    @staticmethod
    def load_template(filename):
        with open(filename, 'r') as file:
            return file.read()

    @staticmethod
    def format(pre_format, **kwargs):
        """ poor mans html template system. {{var}} in the template can be over written with kwargs[var]"""

        # swaps double and single curly braces allowing us to use python str.format() method
        curly = { "{{":"{", "}}":"}", "{":"{{", "}":"}}" }
        substrings = sorted(curly, key=len, reverse=True)
        regex = re.compile('|'.join(map(re.escape, substrings)))
        to_formant = regex.sub(lambda match: curly[match.group(0)], pre_format)

        return to_formant.format(**kwargs) 



class DataLine(Element):
    pass
    def __init__(self, id):
        self.id = id

"""
        <tr>
          <td>{{ID}}</td>
          <td>{{description}}</td>
          <td>12</td>
          <td>{{unit}}</td>
        </tr>
"""

class Table(Element):
    def __init__(self):
        pass

"""
    <table class="dashboard-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Desc</th>
          <th>Value</th>
          <th>Units</th>
        </tr>
      </thead>
      <tbody>
        {{content}}
      </tbody>
    </table>
  </div>
"""


class Dashboard(Element):
    # def __init__(self):
    #     super().__init__(self.name)

    def render(self):
        # identifier = self.get_identifier()
        # content = "\n".join(child.render() for child in self.nodes)
        dashboard = self.load_template("templates/dashboard.template.html")
        template = self.load_template("templates/main.template.html")

        return self.format(template, page = dashboard)

    async def get_dashboard(self, request):
        return web.Response(text=self.dashboard.render(), content_type='text/html')

    def add_routes(self):
        self.app.router.add_get('/', self.get_dashboard)
        self.app.router.add_get('/dashboard', self.get_dashboard)


class Messages(Element):
    # def __init__(self):
    #     super().__init__(self.name)

    def render(self):
        # identifier = self.get_identifier()
        # content = "\n".join(child.render() for child in self.nodes)
        messages = self.load_template("templates/messages.template.html")
        template = self.load_template("templates/main.template.html")

        return self.format(template, page = messages)

class Maps(Element):
    # def __init__(self):
    #     super().__init__(self.name)

    def render(self):
        # identifier = self.get_identifier()
        # content = "\n".join(child.render() for child in self.nodes)
        map = self.load_template("templates/map.template.html")
        template = self.load_template("templates/main.template.html")

        return self.format(template, page = map)

class Graphs(Element):
    # def __init__(self):
    #     super().__init__(self.name)

    def render(self):
        # identifier = self.get_identifier()
        # content = "\n".join(child.render() for child in self.nodes)
        graphs = self.load_template("templates/graphs.template.html")
        template = self.load_template("templates/main.template.html")

        return self.format(template, page = graphs)

class Configure(Element):
    # def __init__(self):
    #     super().__init__(self.name)

    def render(self):
        # identifier = self.get_identifier()
        # content = "\n".join(child.render() for child in self.nodes)
        configure = self.load_template("templates/configure.template.html")
        template = self.load_template("templates/main.template.html")

        return self.format(template, page = configure)