import aiohttp
import datetime

class bus:
    def __init__(self, origin, destination, arrival, latitude, longitude, visit, congestion, wheelchair, kind):
        self.origin = origin
        self.destination = destination
        self.arrival = arrival
        self.latitude = latitude
        self.longitude = longitude
        self.visit = visit
        self.congestion = congestion
        self.wheelchair = wheelchair
        self.kind = kind

    @property
    def waiting_time(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        return int(max((self.arrival - now).total_seconds(), 0.0) / 60)

class bus_stop:
    def __init__(self, stop):
        self.stop = stop
        self.buses = {}
        self.operators = {}
        
    async def update(self, key):
        buses = {}
        operators = {}
        async with aiohttp.ClientSession(headers={"AccountKey": key, "accept": "application/json"}) as session:
            async with session.get("http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={}".format(self.stop)) as get:
                data = await get.json()
        for service in data["Services"]:
            buses[service["ServiceNo"]] = []
            operators[service["ServiceNo"]] = service["Operator"]
            for next_bus in ["NextBus", "NextBus2", "NextBus3"]:
                # origin, destination, arrival, latitude, longitude, visit, congestion, wheelchair, kind
                valid = True
                for field in service[next_bus]:
                    if service[next_bus][field] == "":
                        valid = False
                if valid:
                    latitude = service[next_bus]["Latitude"]
                    longitude = service[next_bus]["Longitude"]
                    if service[next_bus]["Latitude"] == "0":
                        latitude = None 
                    if service[next_bus]["Longitude"] == "0":
                        longitude = None
                    if service[next_bus]["Load"] == "SEA":
                        congestion = 1
                    elif service[next_bus]["Load"] == "SDA":
                        congestion = 2
                    else:
                        congestion = 3
                    if service[next_bus]["Feature"] == "WAB":
                        wheelchair = True
                    else:
                        wheelchair = False
                    if service[next_bus]["Type"] == "DD":
                        kind = "double"
                    elif service[next_bus]["Type"] == "BD":
                        kind = "bendy"
                    else:
                        kind = "single"
                    buses[service["ServiceNo"]].append(bus(
                        int(service[next_bus]["OriginCode"]),
                        int(service[next_bus]["DestinationCode"]),
                        datetime.datetime.strptime(service[next_bus]["EstimatedArrival"], "%Y-%m-%dT%H:%M:%S%z"),
                        latitude,
                        longitude,
                        int(service[next_bus]["VisitNumber"]),
                        congestion,
                        wheelchair,
                        kind
                    ))
        self.buses = buses
        self.operators = operators