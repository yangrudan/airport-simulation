import logging

from schedule import Schedule
from aircraft import Aircraft
from route import Route
from itinerary import Itinerary

class Scheduler:

    def __init__(self):

        # Setups the logger
        self.logger = logging.getLogger(__name__)

    def schedule(self, simulation, time):

        # simulation.airport : all airport states
        # simulation.routing_expert : gets routes from node A to node B
        # time : current simulated time of a day
        self.logger.debug("Scheduling starts")
        self.logger.debug("Found %d aircrafts",
                          len(simulation.airport.aircrafts))

        # helper function:
        # conflicts = simulation.predict_state_after(schedule, time_from_now)

        # put break point:
        # from IPython.core.debugger import Tracer; Tracer()()

        requests = []
        for aircraft in simulation.airport.aircrafts:

            # Pulls outs the flight information
            flight = simulation.scenario.get_flight(aircraft)

            if aircraft.is_idle and \
               aircraft.location.is_close_to(flight.from_gate):

                # Gets the route from the routing expert
                # NOTE: We use runway start node as the destination of a
                # departure flight
                route = simulation.routing_expert.get_shortest_route(
                    flight.from_gate, flight.runway.start)
                self.logger.debug("Get route: %s" % route)

                # Generates the itinerary for this aircraft
                target_nodes = []
                for node in route.nodes:
                    target_nodes.append(
                        Itinerary.TargetNode(node, time, time))

                itinerary = Itinerary(target_nodes, time)
                requests.append(Schedule.Request(aircraft, itinerary))
                self.logger.debug("Adds route %s on %s" % (route, aircraft))

        self.logger.debug("Scheduling done")
        return Schedule(requests)

    def __getstate__(self):
        d = dict(self.__dict__)
        del d["logger"]
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)
