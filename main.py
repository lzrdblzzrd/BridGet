import urllib.request


def main():
    try:
        with urllib.request.urlopen(url="https://torscan-ru.ntc.party/relays.txt") as response:
            bridges = response.read().decode(encoding="UTF-8").strip().split(sep="\n")
            with open(file="bridges.conf", mode="w") as file:
                for bridge in bridges:
                    file.write(f"Bridge {bridge}\n")
    except Exception as exception:
        print(exception)


if __name__ == "__main__":
    main()
