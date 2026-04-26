import argparse
import requests
import sys

def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    forecast_parser = subparsers.add_parser("temperature", help="check the temperature in specific city or zipcode")
    groups = forecast_parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("--zipcode", type=int, help="zipcode of location to check weather")
    groups.add_argument("--city", type=str, help="city of location to check weather")

    sunrise_parser = subparsers.add_parser("sunrise", help="check sunrise in specific location using city or zipcode")
    groups = sunrise_parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("--zipcode", type=int, help="zipcode of location to check weather")
    groups.add_argument("--city", type=str, help="city of location to check weather")

    sunset_parser = subparsers.add_parser("sunset", help="check sunset in specific city or zipcode")
    groups = sunset_parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("--zipcode", type=int, help="zipcode of location to check weather")
    groups.add_argument("--city", type=str, help="city of location to check weather")

    compare_parser = subparsers.add_parser("compare", help="compare temperature in two specific cities")
    compare_parser.add_argument("city1", type=str, help="first city")
    compare_parser.add_argument("city2", type=str, help="second city")

    args = parser.parse_args()

    def get_coordinates(location):
        req = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1")
        if req.status_code != 200:
            print("Geocoding API returned with error")
            sys.exit(1)
        api_parsed = req.json()
        return api_parsed["results"][0]["latitude"], api_parsed["results"][0]["longitude"]

    def get_weather(lat, lon):
        req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m&daily=sunrise,sunset&timezone=auto&forecast_days=1")
        if req.status_code != 200:
            print("Weather API returned with error")
            sys.exit(1)
        return req.json()

    if args.command == "temperature":
        loc = args.zipcode if args.zipcode else args.city
        lat, lon = get_coordinates(loc)
        api_parsed = get_weather(lat, lon)
        temp=api_parsed["current"]["temperature_2m"]
        print(f"Current temperature in {loc} is {temp} Degrees Celcius")
    elif args.command == "sunrise":
        loc = args.zipcode if args.zipcode else args.city
        lat, lon = get_coordinates(loc)
        api_parsed = get_weather(lat, lon)
        print(f"Sunrise in {loc} is {api_parsed['daily']['sunrise'][0]}")
    elif args.command == "sunset":
        loc = args.zipcode if args.zipcode else args.city
        lat, lon = get_coordinates(loc)
        api_parsed = get_weather(lat, lon)
        print(f"Sunset in {loc} is {api_parsed['daily']['sunset'][0]}")
    elif args.command == "compare":
        lat1, lon1 = get_coordinates(args.city1)
        api_parsed1 = get_weather(lat1, lon1)
        temp1=api_parsed1["current"]["temperature_2m"]

        lat2, lon2 = get_coordinates(args.city2)
        api_parsed2 = get_weather(lat2, lon2)
        temp2=api_parsed2["current"]["temperature_2m"]
        print(f"Current temperature in {args.city1} is {temp1} Degrees Celcius")
        print(f"Current temperature in {args.city2} is {temp2} Degrees Celcius")
        
if __name__ == "__main__":
    main()