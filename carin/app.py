from carin.help import show_help
from carin.help import show_bad_argument_help
from enum import Enum, auto
import sys
import getopt
import urllib.request
import json

debug = False
base_url = "https://api.carbonintensity.org.uk"


def log(message):
    if debug:
        print(message)


def run():
    log("Carbon Intensity API")

    class Endpoint(Enum):
        UNKNOWN = auto()
        GENERATION = auto()
        INTENSITY = auto()
        REGIONAL = auto()

    endpoint = Endpoint.UNKNOWN
    postcode = None

    argument_count = len(sys.argv)
    if argument_count == 1:
        show_help()
    else:
        log("Parse Arguments")
        log(sys.argv)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "e:p:", ["endpoint=", "postcode="])
        except getopt.GetoptError:
            show_bad_argument_help()
            sys.exit(2)
        for opt, arg in opts:
            log("option: " + opt + " argument: " + arg)
            if opt == '-e':
                if arg == 'generation':
                    endpoint = Endpoint.GENERATION
                elif arg == "intensity":
                    endpoint = Endpoint.INTENSITY
                elif arg == "regional":
                    endpoint = Endpoint.REGIONAL
            if opt == '-p':
                postcode = arg

        if endpoint == Endpoint.GENERATION:
            generation()
        elif endpoint == Endpoint.INTENSITY:
            intensity()
        elif endpoint == Endpoint.REGIONAL:
            regional(postcode=postcode)
        elif endpoint == Endpoint.UNKNOWN:
            show_bad_argument_help()


def generation():
    log("Endpoint: generation")
    request = urllib.request.urlopen(base_url + "/generation")
    generation_json = json.loads(request.read())
    print(json.dumps(generation_json, indent=2, sort_keys=True))


def intensity():
    log("Endpoint: intensity")
    request = urllib.request.urlopen(base_url + "/intensity")
    intensity_json = json.loads(request.read())
    print(json.dumps(intensity_json, indent=2, sort_keys=True))


def regional(**kwargs):
    log("Endpoint: regional")
    postcode = kwargs.get('postcode', None)
    if postcode is None:
        request = urllib.request.urlopen(base_url + "/regional")
    else:
        request = urllib.request.urlopen(base_url + "/regional/postcode/" + postcode)

    regional_json = json.loads(request.read())
    print(json.dumps(regional_json, indent=2, sort_keys=True))

