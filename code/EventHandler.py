# Joseph Michael Coffey IV – jmichaelc4@gmail.com – jmcoffey@colostate.edu 
# Hayden Corbin - haydenfcorbin@gmail.com - hayden.corbin@colostate.edu 
# Reilly Bergeron - reillybergeron@gmail.com - reillyjb@colostate.edu 

class EventHandler:
    def __init__(self):
        self.events = {}

    def add_event(self, name, function):
        self.events[name] = function

    def handle_event(self, event_request):
        self.events[event_request[0]](event_request[1])

