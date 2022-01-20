#from toolbox import harbor
import harbor
import configparser, os
import getopt, sys

config_name = ".config.ini"


def getProvider(config_file):
    if os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
    else:
        print(f'No config file found, please create {config_file}')
        exit()

    provider = {
        "host": config.get("harbor", "host"),
        "user": config.get("harbor", "user"),
        "pwd": config.get("harbor", "pwd")
    }
    return provider
   

def parseArgs(argv):
    # Parse command line options. 

    help_msg = 'harbor_replication.py -s <source-registry> -i <image>'
    source_registry = None
    image = None

    try:
        opts, args = getopt.getopt(argv[1:], "hs:i:", ["help", "source-registry=", "image="])

    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_msg)
            sys.exit()
        elif opt in ("-s", "--source-registry"):
            source_registry = arg
        elif opt in ("-i", "--image"):
            image = arg

    # Check if all required arguments are present
    if source_registry is None or image is None:
        print(help_msg)
        sys.exit()

    return source_registry, image


def main():
    config_file = os.path.join(os.path.expanduser("~"), config_name)
    provider = getProvider(config_file)
    source_registry, image = parseArgs(sys.argv)

    handler = harbor.harbor(provider)

    # See if the registry exists
    registry = handler.getRegistry(source_registry)
    if registry is None:
        print(f"Registry {source_registry} not found")
        exit()


if __name__ == "__main__":
    main()