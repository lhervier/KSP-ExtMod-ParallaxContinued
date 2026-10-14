"""Plays "The rocks turn at every load": the same save loaded again and again, each time after an hour of time
warp, with the same view from above after each load.

It drives KSP through KSP-MCPServer, a mod that answers HTTP requests on 127.0.0.1, and needs nothing but
Python 3: no AI, no package to install. Start KSP with Parallax Continued, KSP-MCPServer, KSP Diag - Colliders
and KSP Diag - Floating Origin installed, wait for the main menu, copy the save (rocks-mun-jeb.sfs of the saves
folder, for instance) into the folder of a sandbox game, then run:

    python run-rocks-turning.py --folder <your sandbox game> --save rocks-mun-jeb --out out

1. It loads the save, lets the craft settle, presses Record in the window of KSP Diag - Floating Origin, and
   takes a screenshot from straight above the craft, the windows and the interface hidden: load-00.png.
2. It warps on rails by --step seconds of game time (an hour by default), checks that the time did move on,
   and takes the same screenshot: warp-01.png. Nothing has turned: nothing was loaded.
3. It loads the same save again, records, and takes the same screenshot: load-01.png. Without the change, every
   cluster of rocks has turned on itself, by the angle the body turned during the warp.
4. Steps 2 and 3 again, --loads times in all.

With --step 0, it skips step 2: the save is loaded again at once, with no time played in between.

The camera keeps its heading from north whatever the craft does, so the edges of the terrain quads, which KSP
Diag - Colliders draws in grey, stay at the same place in every screenshot: what moved in the picture is what
turned on the ground. It writes every line of KSP Diag - Floating Origin to readings.json, prints the angle the
body is turned by in the scene (directRotAngle) at each load, and stops if the warp did not move the time on, or
if the craft has moved after a load.
"""
import argparse
import json
import math
import os
import urllib.request

URL = None

# Beyond this distance on the ground, in metres, the craft is said to have moved after a load.
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


class Run:
    """The views and the readings of one run."""

    def __init__(self, options):
        self.options = options
        self.out = os.path.abspath(options.out)
        os.makedirs(self.out, exist_ok=True)
        self.readings = []

    def view(self, name):
        """Takes the screenshot from straight above the craft, the windows and the interface hidden."""
        call("colliders_show_window", visible=False)
        call("floatingorigin_show_window", visible=False)
        call("set_ui", visible=False)
        call("set_camera", distance=self.options.distance, pitch=89, heading=0)
        call("wait", seconds=2)
        call("screenshot", path=os.path.join(self.out, name + ".png"), return_image=False)

    def record(self, name):
        """Presses Record in KSP Diag - Floating Origin and keeps the line, with the craft where it is."""
        line = call("floatingorigin_record")
        vessel = call("get_state")["vessel"]
        self.readings.append({"view": name, "floatingOrigin": line, "vessel": vessel})
        with open(os.path.join(self.out, "readings.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.readings, f, indent=1)
        log("%-8s UT %10.1f  directRotAngle %9.4f  InverseRotAngle %9.4f" % (
            name, line["UniversalTime"], line["DirectRotAngle"], line["InverseRotAngle"]))
        return vessel

    def load(self):
        call("load_save", folder=self.options.folder, save=self.options.save)
        call("wait", seconds=self.options.settle)


def main():
    global URL
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--folder", required=True, help="the sandbox game the save is in, under saves/")
    parser.add_argument("--save", default="rocks-mun-jeb", help="the save, without .sfs (default rocks-mun-jeb)")
    parser.add_argument("--loads", type=int, default=12, help="how many times to load the save again (default 12)")
    parser.add_argument("--step", type=float, default=3600.0,
                        help="the game time warped before each load, in seconds (default 3600); 0 loads the "
                             "save again at once, without warp-NN screenshots")
    parser.add_argument("--settle", type=float, default=10.0,
                        help="how long to let the craft settle after each load, in seconds (default 10)")
    parser.add_argument("--distance", type=float, default=40.0, help="the height of the camera, in metres")
    parser.add_argument("--radius", type=float, default=200000.0,
                        help="the radius of the body, in metres, to tell how far the craft moved (default: the Mun)")
    parser.add_argument("--out", default="out", help="where readings.json and the screenshots go")
    parser.add_argument("--port", type=int, default=8770, help="the port of KSP-MCPServer")
    options = parser.parse_args()
    URL = "http://127.0.0.1:%d/mcp/" % options.port
    run = Run(options)

    run.load()
    start = run.record("load-00")
    run.view("load-00")
    for k in range(1, options.loads + 1):
        if options.step > 0:
            ut = call("get_state")["ut"]
            call("warp_to", seconds=options.step)
            # warp_to does not tell when the warp did not happen: look at the time.
            now = call("get_state")["ut"]
            if now < ut + 0.9 * options.step:
                log("STOP: the warp did not move the time on (%.1f -> %.1f)" % (ut, now))
                break
            run.record("warp-%02d" % k)
            run.view("warp-%02d" % k)
        run.load()
        vessel = run.record("load-%02d" % k)
        run.view("load-%02d" % k)
        moved = ground_distance(start, vessel, options.radius)
        if moved > MOVED:
            log("STOP: the craft has moved by %.2f m after the load" % moved)
            break
    log("done: %d readings, in %s" % (len(run.readings), run.out))


if __name__ == "__main__":
    main()
