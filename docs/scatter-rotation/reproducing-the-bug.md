# Reproducing the bug

Part of [Scatter rotation](README.md): the protocol that shows the bug on Parallax Continued 1.0.4, the
rocks seen from above around a kerbal standing a few metres from them, played by hand and by a script;
the same protocol with the change, where the rocks hold still; what still changes on Eve from one load to
the next, with the change as without it, and does not come from this bug; then what the bug does to a
craft standing on a rock.

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

**On Eve**, with [`rocks-eve-jeb.sfs`](saves/rocks-eve-jeb.sfs): the same kerbal, standing a few metres
from rocks and from vegetation, which has no collider. Eve turns once in 80,500 s, 16.1° for an hour of
game time. At each load the rocks and the plants turn, each on itself.

![Twelve loads of the same save of Eve on the release, an hour of time warp before each: the rocks and the plants turn on themselves, while the ground, the grey edges of the quads and the kerbal at the centre hold still](runs/rocks-eve-jeb/release/rocks-eve-jeb-release.gif)

*The release on Eve: the same screenshots, Eve turned by 194° in the scene in all; it is dusk where the
kerbal stands. Full size: [MP4](runs/rocks-eve-jeb/release/rocks-eve-jeb-release.mp4). Small pebbles
that seem to come and go, and a white plant that shows on some loads only, do not come from this bug:
[On Eve, what changes at every load all the same](#on-eve-what-changes-at-every-load-all-the-same).*

**By script**: [`automation/run-rocks-turning.py`](automation/run-rocks-turning.py). Steps 1 to 5,
twelve times over, with a screenshot before and after each load and the line of Diag Floating Origin at
each of them; it stops if the warp did not move the time on, or if the kerbal moved after a load. On Eve:
`--save rocks-eve-jeb --radius 700000`. The screenshots are the result: the runs are in
[The rocks around a craft](non-regression.md#the-rocks-around-a-craft).

## With the change, the rocks hold still

**The install**: the same, with the **release + change** build
([The builds and the install](README.md#the-builds-and-the-install)). **The saves**: the same,
[`rocks-mun-jeb.sfs`](saves/rocks-mun-jeb.sfs) and [`rocks-eve-jeb.sfs`](saves/rocks-eve-jeb.sfs).

Play the steps of [The rocks turn at every load](#the-rocks-turn-at-every-load) again. At step 4, and at
every load after it, `directRotAngle` moves as before, by the angle the Mun turns in an hour: KSP still
turns the Mun in the scene at each load. The rocks no longer follow it: every cluster is where it was at
step 2, turned the same way, load after load; on Eve, the plants as well. Only the fine shading of the ground and of the rocks changes
by a few levels of grey from one screenshot to the next.

The first screenshot does not show the rocks as the release does: the change gives every rock another
orientation, tied to its terrain quad, once, and keeps it at every load after
([What the change does](the-change.md#what-the-change-does)).

![Twelve loads of the same save with the change, an hour of time warp before each: the rocks, the ground, the grey edges of the quads and the kerbal at the centre hold still](runs/rocks-mun-jeb/change/rocks-mun-jeb-change.gif)

*Release + change: the same screenshots as above, from the same save, the Mun turned by 112° in the scene
in all. Full size: [MP4](runs/rocks-mun-jeb/change/rocks-mun-jeb-change.mp4).*

![Twelve loads of the same save of Eve with the change, an hour of time warp before each: the rocks, the plants, the ground, the grey edges of the quads and the kerbal at the centre hold still](runs/rocks-eve-jeb/change/rocks-eve-jeb-change.gif)

*Release + change on Eve, Eve turned by 194° in the scene in all. Full size:
[MP4](runs/rocks-eve-jeb/change/rocks-eve-jeb-change.mp4). The small pebbles that seem to come and go,
and the white plant that shows on some loads only, are there without the change too:
[On Eve, what changes at every load all the same](#on-eve-what-changes-at-every-load-all-the-same).*

**By script**: the same script, KSP started with the release + change build. The runs are in
[The rocks around a craft](non-regression.md#the-rocks-around-a-craft), next to those on the release.

## On Eve, what changes at every load all the same

With the change, nothing turns any more on Eve. Two things still change from one load to the next, with
the change as with the release, even when the same save is loaded again at once, with no time played.
Neither comes from this bug, and the change does not touch them.

**The small pebbles are drawn in the texture of the ground, and that texture slides.** What looks like
small pebbles coming and going between two screenshots is not objects of the scatter: the terrain shader
of Parallax Continued paints them in the texture of the ground. It places that texture from the position
of each point in the Unity scene, `(worldPos + _TerrainShaderOffset) * _Tiling` (`BiplanarFunctions.cginc`).
KSP turns the body in the scene again at every load ([Why the rocks turn](the-change.md#why-the-rocks-turn)),
so the same point of the ground comes back at another place in the scene, and the texture comes back slid
along the ground. Loading the same save again straight away is enough: Eve turns by a few hundredths of a
degree in the scene, and a point of its ground moves by hundreds of metres in it. The same thing happens on
the Mun, where the texture of the ground has no such pebbles and only its fine shading changes. It is the
same kind of defect as the rocks that turn, a texture tied to the scene rather than to the body, in the
terrain shader, and only seen: the ground the physics uses does not move. It may deserve its own change.

![The same place on Eve at a load, and after the same save is loaded again at once: the rocks have not moved, the light grains painted on the ground are no longer the same](runs/eve-what-still-changes/ground-texture.jpg)

*Release + change on Eve, a view of 10 m from above around the kerbal, enlarged. To be sure the grains are
not objects, every scatter of Eve without a collider was taken out by a ModuleManager patch, and the
scatter of stock KSP switched off in the settings: what is left is the rocks with colliders, which do not
move, and the ground, whose grains change.*

**A plant shows on some loads, and not on others, already with the release.** In the grove at the left of
the view, a white plant under the red ones, at the bottom right, shows at one load and not at the next. It
does so on the release as well; there, it is harder to see, as the whole grove also turns.

![On the release, the grove at loads 3, 4 and 5: every plant has turned, and a white plant shows at load 4 under the red ones, at the bottom right](runs/eve-what-still-changes/plant-release.jpg)

![With the change, the grove at loads 1, 2 and 3: nothing has turned, and the same white plant shows at load 2 only](runs/eve-what-still-changes/plant-change.jpg)

*Crops of the screenshots of [The rocks around a craft](non-regression.md#the-rocks-around-a-craft).*

**This plant follows the ground of stock KSP.** Parallax Continued decides where each object of its
scatter grows from the mesh of the terrain quad (`Distribute`), and stock KSP builds that mesh a little
differently at every load ([Why it is different at every load](https://github.com/lhervier/KSP-TerrainPrecisionFix/blob/main/docs/the-culprit-ground.md#why-it-is-different-at-every-load)):
a plant that sits right on one of the thresholds of `Distribute` grows at one load and not at the next.
With [KSP TerrainPrecisionFix](https://github.com/lhervier/KSP-TerrainPrecisionFix), which builds the
ground of stock KSP the same at every load, the same plants grow every time: shown there,
[With this mod, its scatter grows the same at every load](https://github.com/lhervier/KSP-TerrainPrecisionFix/blob/main/docs/work-in-progress/parallax/its-terrain-and-its-scatter.md#with-this-mod-its-scatter-grows-the-same-at-every-load).

## What it does to a craft

A rock that has turned at a load is no longer where the save left it. A kerbal or a craft standing on
it, or right next to one, starts on another part of the rock, above it, or inside it, and the physics
engine throws a craft that starts inside a rock out: the behaviour reported to Parallax Continued in
[issue #125](https://github.com/Gameslinx/Parallax-Continued/issues/125), *Mun Surface Scatter
Devoured/Torn Apart Small Vessel Upon Game Relaunch*. In a game played normally, the save is loaded after
a restart of KSP, in a session that has not played the same time as the one the save was made in: the
rocks come back turned by any angle. A kerbal on a rock, loaded without the change and with it, is in
[Work in progress](work-in-progress.md#a-kerbal-on-a-rock).
