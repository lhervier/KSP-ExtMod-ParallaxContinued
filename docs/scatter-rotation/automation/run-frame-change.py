"""Plays "When the frame changes": a craft taken up above the rotating-frame altitude and put back where it stood,
again and again, with the same view from above after each trip, and no load in between.

It drives KSP through KSP-MCPServer, a mod that answers HTTP requests on 127.0.0.1, and needs nothing but
Python 3: no AI, no package to install. Start KSP with Parallax Continued, KSP-MCPServer, KSP Diag - Colliders
and KSP Diag - Floating Origin installed, wait for the main menu, copy the save (rocks-mun-jeb.sfs of the saves
folder, for instance) into the folder of a sandbox game, then run:

    python run-frame-change.py --folder <your sandbox game> --save rocks-mun-jeb --out out

Below the rotating-frame altitude (100 km on the Mun), KSP holds the body still in the scene; above it, the body
turns in the scene. When the craft comes back down, the body is held still again, at the angle it has reached.

1. It loads the save once, lets the craft settle, presses Record in the window of KSP Diag - Floating Origin, and
   takes a screenshot from straight above the craft, the windows and the interface hidden: trip-00.png.
2. It puts the craft on a circular orbit --altitude metres above the body, as Set Orbit of the Alt+F12 menu does,
   and checks that the frame is no longer rotating: KSP Diag - Floating Origin shows Inertial.
3. It warps on rails by --orbit seconds of game time (an hour by default): the body turns in the scene.
4. It puts the craft back where the save left it, as Set Position of the Alt+F12 menu does, and checks that the
   frame is rotating again, at another angle (directRotAngle).
5. It warps on rails, the craft on the ground, up to one solar day (--day) after the time of the previous
   screenshot: the frame stays rotating and nothing turns, and the Sun is back where it was in the sky. It
   records, and takes the same screenshot: trip-01.png. Without the change, every cluster of rocks has turned
   on itself, by the angle the body turned during the time in orbit. After the first trip, it also takes the
   window of KSP Diag - Floating Origin over the same view, its table holding the lines of the trip: table-01.png.
6. Steps 2 to 5 again, --trips times in all.

With --heading and --pitch, the camera looks at the craft from the side rather than from straight above: to
see the colliders KSP Diag - Colliders draws in colour on the rocks next to a craft standing among them.

The camera keeps its heading from north whatever the craft does, so the edges of the terrain quads, which KSP
Diag - Colliders draws, stay at the same place in every screenshot: what moved in the picture is what
turned on the ground. It writes every line of KSP Diag - Floating Origin to readings.json, prints the frame
and the angle the body is turned by in the scene (directRotAngle) at each step, and stops if the frame did not
change, if a warp did not move the time on, or if the craft did not land back where it stood.
"""
import argparse
import json
import math
import os
import urllib.request

URL = None

# Beyond this distance on the ground, in metres, the craft is said not to be back where it stood.
MOVED = 0.5


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
    """Distance on the ground between two get_state vessels, in metres, on a body of the given radius."""
    lat = math.radians((a["latitude"] + b["latitude"]) / 2)
    north = math.radians(b["latitude"] - a["latitude"]) * radius
    east = math.radians(b["longitude"] - a["longitude"]) * radius * math.cos(lat)
    return math.hypot(north, east)


class Stop(Exception):
    """A step did not do what the test needs: the run ends there."""


class Run:
    """The views and the readings of one run."""

    def __init__(self, options):
        self.options = options
        self.out = os.path.abspath(options.out)
        os.makedirs(self.out, exist_ok=True)
        self.readings = []

    def view(self, name):
        """Takes the screenshot of the craft from --distance, --heading and --pitch (straight above by default),
        the windows and the interface hidden."""
        call("colliders_show_window", visible=False)
        # The colliders drawn hidden by what stands in front of them, so that they show on the rocks.
        call("colliders_set_display", mode=0)
        call("floatingorigin_show_window", visible=False)
        call("set_ui", visible=False)
        call("set_camera", distance=self.options.distance, pitch=self.options.pitch, heading=self.options.heading)
        call("wait", seconds=2)
        call("screenshot", path=os.path.join(self.out, name + ".png"), return_image=False)

    def table(self, name):
        """Takes the screenshot of the window of KSP Diag - Floating Origin alone, at the top left of the screen,
        over the same view: its table holds the lines recorded so far."""
        call("floatingorigin_show_window", visible=True)
        call("floatingorigin_move_window", x=20, y=20)
        call("wait", seconds=1)
        call("screenshot", path=os.path.join(self.out, name + ".png"), return_image=False)
        call("floatingorigin_show_window", visible=False)

    def record(self, name, rotating=None):
        """Presses Record in KSP Diag - Floating Origin and keeps the line, with the craft where it is. With
        rotating, stops the run unless the frame is rotating (True) or inertial (False)."""
        line = call("floatingorigin_record")
        vessel = call("get_state")["vessel"]
        self.readings.append({"view": name, "floatingOrigin": line, "vessel": vessel})
        with open(os.path.join(self.out, "readings.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.readings, f, indent=1)
        log("%-11s UT %10.1f  %-8s  directRotAngle %9.4f  InverseRotAngle %9.4f  %s" % (
            name, line["UniversalTime"], "Rotating" if line["RotatingFrame"] else "Inertial",
            line["DirectRotAngle"], line["InverseRotAngle"], vessel["situation"]))
        if rotating is not None and line["RotatingFrame"] != rotating:
            raise Stop("the frame is %s at %s" % ("rotating" if line["RotatingFrame"] else "inertial", name))
        return line, vessel

    def warp(self, ut):
        """Warps on rails up to ut, and stops the run if the time did not move on."""
        before = call("get_state")["ut"]
        call("warp_to", ut=ut)
        # warp_to does not tell when the warp did not happen: look at the time.
        now = call("get_state")["ut"]
        if now < ut - 0.1 * (ut - before):
            raise Stop("the warp did not move the time on (%.1f -> %.1f, to %.1f)" % (before, now, ut))


def main():
    global URL
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", required=True, help="the sandbox game the save is in, under saves/")
    parser.add_argument("--save", default="rocks-mun-jeb", help="the save, without .sfs (default rocks-mun-jeb)")
    parser.add_argument("--trips", type=int, default=12, help="how many times to go up and back (default 12)")
    parser.add_argument("--altitude", type=float, default=150000.0,
                        help="the altitude of the orbit, in metres above the radius of the body (default 150000: "
                             "above the 100 km of the Mun)")
    parser.add_argument("--orbit", type=float, default=3600.0,
                        help="the game time warped in orbit at each trip, in seconds (default 3600)")
    parser.add_argument("--day", type=float, default=141115.4,
                        help="the solar day of the body, in seconds: the game time between two screenshots, so "
                             "that the Sun is at the same place in each (default: the Mun's; get_state of "
                             "KSP-MCPServer gives it for the body of the craft, as solarDay)")
    parser.add_argument("--settle", type=float, default=10.0,
                        help="how long to let the craft settle after the load and after each Set Position, in "
                             "seconds (default 10)")
    parser.add_argument("--distance", type=float, default=40.0,
                        help="the distance of the camera from the craft, in metres (default 40)")
    parser.add_argument("--heading", type=float, default=0.0,
                        help="the direction the camera looks in, in degrees from north towards east (default 0)")
    parser.add_argument("--pitch", type=float, default=89.0,
                        help="how far the camera looks down, in degrees (default 89: straight above the craft)")
    parser.add_argument("--radius", type=float, default=200000.0,
                        help="the radius of the body, in metres, to tell how far the craft moved (default: the Mun)")
    parser.add_argument("--out", default="out", help="where readings.json and the screenshots go")
    parser.add_argument("--port", type=int, default=8770, help="the port of KSP-MCPServer")
    options = parser.parse_args()
    URL = "http://127.0.0.1:%d/mcp/" % options.port
    run = Run(options)

    # KSP-MCPServer loads a save from the space centre or in flight only, as a player does: from the main
    # menu, the game is opened at the space centre first.
    if call("get_state")["scene"] == "MAINMENU":
        call("open_game", folder=options.folder)
    call("load_save", folder=options.folder, save=options.save)
    call("wait", seconds=options.settle)
    try:
        first, start = run.record("trip-00", rotating=True)
        run.view("trip-00")
        for k in range(1, options.trips + 1):
            call("set_orbit", altitude=options.altitude)
            up, _ = run.record("up-%02d" % k, rotating=False)
            run.warp(up["UniversalTime"] + options.orbit)
            run.record("orbit-%02d" % k, rotating=False)
            call("set_position", latitude=start["latitude"], longitude=start["longitude"])
            call("wait", seconds=options.settle)
            run.record("down-%02d" % k, rotating=True)
            # The rest of the solar day on the ground: the frame rotating, the body held still in the scene.
            run.warp(first["UniversalTime"] + k * options.day)
            _, vessel = run.record("trip-%02d" % k, rotating=True)
            run.view("trip-%02d" % k)
            if k == 1:
                run.table("table-01")
            moved = ground_distance(start, vessel, options.radius)
            if moved > MOVED:
                raise Stop("the craft stands %.2f m from where the save left it" % moved)
    except Stop as stop:
        log("STOP: %s" % stop)
    log("done: %d readings, in %s" % (len(run.readings), run.out))


if __name__ == "__main__":
    main()
