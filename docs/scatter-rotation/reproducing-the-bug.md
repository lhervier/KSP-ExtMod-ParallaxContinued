# Reproducing the bug

Part of [Scatter rotation](README.md): the protocol that shows the bug on Parallax Continued 1.0.4, the
rocks seen from above around a kerbal standing a few metres from them, played by hand and by a script;
then what it does to a craft standing on a rock.

## The rocks turn at every load

**The install**: [the install](README.md#the-builds-and-the-install) with the **release** build,
[KSP Diag - Colliders](https://github.com/lhervier/KSP-Diag-Colliders) and
[KSP Diag - Floating Origin](https://github.com/lhervier/KSP-Diag-FloatingOrigin). Diag Colliders is only
there to give the screenshots a mark fixed to the ground: it outlines in grey the collider of every
terrain quad within 300 m, so the edges of the quads meet in a cross at each vertex. It would also draw,
in colour, the colliders Parallax gives the rocks near a craft, but a kerbal a few metres from the
nearest rock gets none. Diag Floating Origin shows
`directRotAngle`, the angle the Mun is turned by in the scene. `Alt+F6` hides both windows; the drawing
goes on.

**By hand**, about fifteen minutes:

1. Copy [`rocks-mun-jeb.sfs`](saves/rocks-mun-jeb.sfs) into the folder of a sandbox game and load it:
   Jebediah Kerman on EVA, standing on flat ground of the Mun, a few metres from a vertex of the terrain
   quads and from the nearest rocks. Any craft standing still among rocks will do.
2. Press *Record* in the window of Diag Floating Origin. Look at the kerbal from straight above, from
   some 40 m, and take a screenshot. Near the kerbal, the grey edges meet in a cross: they are fixed to
   the ground, and tell that the view did not move nor turn from one screenshot to the next. The camera
   follows the kerbal, and a kerbal who moved would move the whole picture; its heading is counted from
   north, so the kerbal turning on himself does not turn the picture.
3. Let an hour of game time go by without loading anything: time warp ×100 on rails for about 36
   seconds. Take a screenshot again: nothing has moved, and `directRotAngle` has not changed.
4. Load **the same save** again, not a new one. Press *Record*, take the same screenshot: every cluster
   of rocks has turned on itself, around its own centre, while the ground, the quad edges and the kerbal
   have not. `directRotAngle` has moved by the angle the Mun turns in an hour.
5. Repeat steps 3 and 4: at each load the rocks turn a little further, by the same angle as
   `directRotAngle`.

The Mun turns once in 138,984 s: 9.3° for an hour of game time, 1.6° for ten minutes played in real time.
Saving and loading straight away turns nothing, and neither does time going by while nothing is loaded:
only loading an older save does, or starting KSP again (see [The change](the-change.md#why-the-rocks-turn)).

![Twelve loads of the same save on the release, an hour of time warp before each: the clusters of rocks turn on themselves, while the ground, the grey edges of the quads and the kerbal at the centre hold still](runs/rocks-mun-jeb/release/rocks-mun-jeb-release.gif)

*The release: the screenshot of step 2, then the one of step 4 after each of twelve loads, one a second;
the Mun turned by 112° in the scene in all. The kerbal is the red dot at the centre. Full size:
[MP4](runs/rocks-mun-jeb/release/rocks-mun-jeb-release.mp4).*

**By script**: [`automation/run-rocks-turning.py`](automation/run-rocks-turning.py). Steps 1 to 5,
twelve times over, with a screenshot before and after each load and the line of Diag Floating Origin at
each of them; it stops if the warp did not move the time on, or if the kerbal moved after a load. The
screenshots are the result: a run on each build is in
[Work in progress](work-in-progress.md#the-rocks-around-a-craft).

## What it does to a craft

A rock that has turned at a load is no longer where the save left it. A kerbal or a craft standing on
it, or right next to one, starts on another part of the rock, above it, or inside it, and the physics
engine throws a craft that starts inside a rock out: the behaviour reported to Parallax Continued in
[issue #125](https://github.com/Gameslinx/Parallax-Continued/issues/125), *Mun Surface Scatter
Devoured/Torn Apart Small Vessel Upon Game Relaunch*. In a game played normally, the save is loaded after
a restart of KSP, in a session that has not played the same time as the one the save was made in: the
rocks come back turned by any angle. A kerbal on a rock, loaded without the change and with it, is in
[Work in progress](work-in-progress.md#a-kerbal-on-a-rock).
