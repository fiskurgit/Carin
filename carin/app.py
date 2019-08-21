from carin.help import show_help
from carin.help import show_bad_argument_help
from enum import Enum, auto
import sys
import getopt
import urllib.request
import json

debug = False


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

    argument_count = len(sys.argv)
    if argument_count == 1:
        show_help()
    else:
        log("Parse Arguments")
        log(sys.argv)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "e:", ["endpoint="])
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

        if endpoint == Endpoint.GENERATION:
            generation()
        elif endpoint == Endpoint.INTENSITY:
            intensity()
        elif endpoint == Endpoint.REGIONAL:
            regional()
        elif endpoint == Endpoint.UNKNOWN:
            show_bad_argument_help()


def generation():
    log("Endpoint: generation")
    request = urllib.request.urlopen("https://api.carbonintensity.org.uk/generation")
    generation_json = json.loads(request.read())
    print(json.dumps(generation_json, indent=2, sort_keys=True))


def intensity():
    log("Endpoint: intensity")
    request = urllib.request.urlopen("https://api.carbonintensity.org.uk/intensity")
    intensity_json = json.loads(request.read())
    print(json.dumps(intensity_json, indent=2, sort_keys=True))


def regional():
    log("Endpoint: regional")
    request = urllib.request.urlopen("https://api.carbonintensity.org.uk/regional")
    regional_json = json.loads(request.read())
    print(json.dumps(regional_json, indent=2, sort_keys=True))

