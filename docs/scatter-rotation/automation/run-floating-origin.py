"""Plays "When the floating origin moves": a rover driven to scatter objects that have colliders, and the
floating origin moved by KSP while it stands next to them.

It drives KSP through KSP-MCPServer, a mod that answers HTTP requests on 127.0.0.1, and needs nothing but
Python 3: no AI, no package to install. Start KSP with Parallax Continued, KSP-MCPServer, KSP Diag - Colliders
and KSP Diag - Floating Origin installed, wait for the main menu, copy the save (floating-origin-kerbin.sfs of
the saves folder, for instance) into the folder of a sandbox game, then run:

    python run-floating-origin.py --folder <your sandbox game> --save floating-origin-kerbin --out out

The save holds a rover alone, 503 m from a spot in the middle of a cluster of cacti (--latitude and
--longitude), facing it, with nothing in between. Loading the save puts the floating origin on the rover; KSP
moves it back onto the rover once the rover is 500 m from it, that is 3 m before the spot.

1. It loads the save, lets the rover settle, empties the table of KSP Diag - Floating Origin of the lines of
   earlier runs, and records the line in progress of its window.
2. It drives the rover towards the spot and stops it --before metres short of it (8 m by default): close enough
   for the cacti next to it to have colliders, before the floating origin moves. It checks that the origin has
   not moved yet, records, and takes a screenshot: before-shift.png.
3. It drives the rover on to the spot, slowly, through the move of the floating origin. It checks that the
   origin moved once, records, and takes the same screenshot: after-shift.png.

The screenshots show the rover from --distance, --heading and --pitch, the colliders KSP Diag - Colliders draws
in colour on the cacti, and the window of KSP Diag - Floating Origin at the bottom of the screen: the distance to
the origin, the shifts counted and the length of the last one. The interface of the game and the window of KSP
Diag - Colliders are hidden. It writes every line it records of KSP Diag - Floating Origin, with the colliders listed by
KSP Diag - Colliders, to readings.json, and stops if the origin moved too early or not at all.
"""
import argparse
import json
import math
import os
import urllib.request

URL = None


def call(tool, **args):
    """Calls one tool of KSP-MCPServer and returns its answer, decoded from JSON when it is JSON."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args}}).encode()
    request = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=900) as response:
        result = json.loads(response.read())["result"]
    text = result["content"][0].get("text", "") if result["content"] else ""
    if result.get("isError"):
        raise RuntimeError(tool + ": " + text)
    try:
        answer = json.loads(text)
    except ValueError:
        return text
    # The tools another mod adds answer inside "returned".
    if isinstance(answer, dict) and list(answer) == ["returned"]:
        return answer["returned"]
    return answer


def log(text):
    print(text, flush=True)


def ground_distance(a, b, radius):
    """Distance on the ground between two (latitude, longitude) points, in metres, on a body of the given
    radius."""
    lat = math.radians((a[0] + b[0]) / 2)
    north = math.radians(b[0] - a[0]) * radius
    east = math.radians(b[1] - a[1]) * radius * math.cos(lat)
    return math.hypot(north, east)


class Run:
    """The views and the readings of one run."""

    def __init__(self, options):
        self.options = options
        self.out = os.path.abspath(options.out)
        os.makedirs(self.out, exist_ok=True)
        self.readings = []

    def view(self, name):
        """Takes the screenshot of the rover from --distance, --heading and --pitch, with the window of KSP Diag -
        Floating Origin only."""
        call("colliders_show_window", visible=False)
        # The colliders drawn hidden by what stands in front of them, so that they show on the cacti.
        call("colliders_set_display", mode=0)
        call("floatingorigin_show_window", visible=True)
        # The window set on the bottom of the screen, whatever its height.
        window = call("floatingorigin_move_window", x=self.options.window_x, y=self.options.screen_height)
        call("floatingorigin_move_window", x=self.options.window_x,
             y=self.options.screen_height - window["height"] - 2)
        call("set_ui", visible=False)
        call("set_camera", distance=self.options.distance, pitch=self.options.pitch, heading=self.options.heading)
        call("wait", seconds=2)
        call("screenshot", path=os.path.join(self.out, name + ".png"), return_image=False)
        call("set_ui", visible=True)

    def record(self, name):
        """Keeps the line in progress of KSP Diag - Floating Origin, the rover where it is and the colliders KSP
        Diag - Colliders lists."""
        # The line in progress rather than Record: the table of the window stays empty, and the window small.
        line = call("floatingorigin_read")["live"]
        vessel = call("get_state")["vessel"]
        colliders = call("colliders_read")
        self.readings.append({"view": name, "floatingOrigin": line, "vessel": vessel, "colliders": colliders})
        with open(os.path.join(self.out, "readings.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.readings, f, indent=1)
        log("%-13s origin %7.1f m  shifts %d  last shift %12.3f m  colliders %d" % (
            name, line["OriginDistance"], line["Shifts"], line["LastShift"] or 0, colliders["collidersOn"]))
        return line, vessel


def main():
    global URL
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", required=True, help="the sandbox game the save is in, under saves/")
    parser.add_argument("--save", default="floating-origin-kerbin",
                        help="the save, without .sfs (default floating-origin-kerbin)")
    parser.add_argument("--latitude", type=float, default=-5.4171528896692855,
                        help="the spot among the cacti the rover drives to, in degrees (default: that of "
                             "floating-origin-kerbin)")
    parser.add_argument("--longitude", type=float, default=-144.01398092667205,
                        help="the spot among the cacti the rover drives to, in degrees (default: that of "
                             "floating-origin-kerbin)")
    parser.add_argument("--before", type=float, default=8.0,
                        help="where the rover stops before the floating origin moves, in metres short of the "
                             "spot (default 8)")
    parser.add_argument("--speed", type=float, default=4.0,
                        help="the speed up to the first stop, in metres per second (default 4)")
    parser.add_argument("--slow", type=float, default=1.0,
                        help="the speed through the move of the floating origin, in metres per second (default 1)")
    parser.add_argument("--settle", type=float, default=10.0,
                        help="how long to let the rover settle after the load, in seconds (default 10)")
    parser.add_argument("--distance", type=float, default=15.0,
                        help="the distance of the camera from the rover, in metres (default 15)")
    parser.add_argument("--heading", type=float, default=284.0,
                        help="the direction the camera looks in, in degrees from north towards east (default 284: "
                             "the way the rover drives in floating-origin-kerbin)")
    parser.add_argument("--pitch", type=float, default=15.0,
                        help="how far the camera looks down, in degrees (default 15)")
    parser.add_argument("--window-x", type=float, default=60.0,
                        help="where the window of KSP Diag - Floating Origin goes, in pixels from the left "
                             "(default 60)")
    parser.add_argument("--screen-height", type=float, default=720.0,
                        help="the height of the screen of KSP, in pixels, to set the window of KSP Diag - "
                             "Floating Origin on its bottom (default 720)")
    parser.add_argument("--radius", type=float, default=600000.0,
                        help="the radius of the body, in metres (default: Kerbin)")
    parser.add_argument("--out", default="out", help="where readings.json and the screenshots go")
    parser.add_argument("--port", type=int, default=8770, help="the port of KSP-MCPServer")
    options = parser.parse_args()
    URL = "http://127.0.0.1:%d/mcp/" % options.port
    run = Run(options)
    spot = (options.latitude, options.longitude)

    # KSP-MCPServer loads a save from the space centre or in flight only, as a player does: from the main
    # menu, the game is opened at the space centre first.
    if call("get_state")["scene"] == "MAINMENU":
        call("open_game", folder=options.folder)
    call("load_save", folder=options.folder, save=options.save)
    call("wait", seconds=options.settle)
    # The table of the window emptied of the lines of earlier runs.
    call("floatingorigin_clear")
    _, vessel = run.record("load")
    start = (vessel["latitude"], vessel["longitude"])
    length = ground_distance(start, spot, options.radius)
    log("the rover is %.1f m from the spot" % length)

    # The first stop, on the line from the rover to the spot: so short a line is straight in degrees.
    k = options.before / length
    stop = (spot[0] + (start[0] - spot[0]) * k, spot[1] + (start[1] - spot[1]) * k)
    # The shifts are counted by KSP (get_floating_origin), not by KSP Diag - Floating Origin: the count of its
    # window can go back to 0 after the load.
    shifts = call("get_floating_origin")["shiftsThisScene"]
    call("drive_to", latitude=stop[0], longitude=stop[1], speed=options.speed, tolerance=0.5)
    run.record("before-shift")
    if call("get_floating_origin")["shiftsThisScene"] != shifts:
        log("STOP: the floating origin moved before the first stop; give --before more metres")
        return
    run.view("before-shift")

    call("drive_to", latitude=spot[0], longitude=spot[1], speed=options.slow)
    run.record("after-shift")
    moves = call("get_floating_origin")["shiftsThisScene"] - shifts
    if moves != 1:
        log("STOP: the floating origin moved %d times on the way to the spot, not once" % moves)
        return
    run.view("after-shift")
    log("done: %d readings, in %s" % (len(run.readings), run.out))


if __name__ == "__main__":
    main()
