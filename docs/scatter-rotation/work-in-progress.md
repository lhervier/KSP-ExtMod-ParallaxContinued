# Work in progress

Part of [Scatter rotation](README.md): what is still to check before the change can be offered. Each
point says what a player would see if the change broke something, how to play it, what its script needs,
and where it stands. In every test, the colliders of the rocks are shown with KSP Diag - Colliders, and
must follow the rocks drawn. A point moves to [Non-regression tests](non-regression.md) once complete
([What makes a test complete](non-regression.md#what-makes-a-test-complete)).

## Summary

- **When the floating origin moves** — the rocks and their colliders move with it, together.
- **When the frame changes** — the craft goes above the rotating-frame altitude and back: the body turns
  in the scene without any load.
- **The scatters along the radius: the trees of Kerbin** — the other branch of `alignToTerrainNormal`.
- **The south pole** — where `FromToRotation` has no single answer, without the change and with it.
- **Sigma Dimensions** — a body of another size, and quads of another scale.
- **A kerbal on a rock** — the consequence of the rocks that turn: a kerbal saved on a rock, loaded
  again after an hour of time warp, and after a restart of KSP: moved without the change, put back where
  he was with it; on the Mun and on Eve.
- **OpenGL, on Linux** — the GLSL variant of the compute shader.
- **Performance** — the time of a frame in a dense scatter, without the change and with it.
- **Out of reach** — macOS, Linux under Vulkan.

## When the floating origin moves

**If the change broke it**: right after KSP moves the floating origin, the rocks drawn and their
colliders would no longer be at the same place, or would jump.

**Why**: KSP moves the whole world back to the origin when the active craft goes 500 m from it. The
colliders are children of their terrain quads and move with them; the rocks drawn are placed from the
quad's matrix at every frame. The change uses that matrix for the orientation too.

**To play**: a rover driven among rocks, on its own (a second craft landed and loaded holds the origin
still), until Diag Floating Origin counts a shift; stop right after it, and look at the rocks next to the
rover with Diag Colliders. On both builds, on the Mun and on Eve.

**Script**: `drive` or `drive_to`, then `floatingorigin_read` to wait for the shift; a rover save to make.

**Where it stands**: not played.

## When the frame changes

**If the change broke it**: after the craft comes back below the rotating-frame altitude, the rocks
would have turned, or their colliders would part from the rocks drawn.

**Why**: below that altitude (100 km on the Mun), KSP holds the body still in the scene; above it, the
body turns in the scene, and when the craft comes back down, it is held still again at another angle,
without any load. Without the change, the rocks drawn turn with that angle at once. A change of sphere of
influence goes through the same switch.

**To play**: from the save of [The rocks around a craft](non-regression.md#the-rocks-around-a-craft), a screenshot from
above; then the craft put on an orbit above 100 km with *Set Orbit* of the `Alt+F12` menu, some time in
orbit, and put back where it stood with *Set Position*; the same screenshot. Diag Floating Origin shows
the frame go to `Inertial` and back to `Rotating`, and `directRotAngle` move. On both builds.

**Script**: `set_orbit`, `wait` or `warp_to`, `set_position`, then the screenshots of
[The rocks around a craft](non-regression.md#the-rocks-around-a-craft).

**Where it stands**: not played. That the body is held still again at another angle is read in the code
of KSP, not seen.

## The scatters along the radius: the trees of Kerbin

**If the change broke it**: the trees, and the other objects that stand along the radius of the body
rather than on the slope of the ground, would lean, turn at every load, or have their colliders apart
from what is drawn.

**Why**: with `alignToTerrainNormal = False`, the normal is the direction of the body's centre, not the
terrain's: the other branch of the code, which the change also brings into the quad's frame. The stock
configs set it on Kerbin, Laythe and Eve, with colliders on Kerbin and Laythe.

**To play**: [The rocks around a craft](non-regression.md#the-rocks-around-a-craft) on Kerbin, a craft standing among
trees, seen from the side as well as from above: a tree leaning shows from the side.

**Script**: `automation/run-rocks-turning.py`, with another save and another view; `trees-kerbin.sfs`
to make.

**Where it stands**: not played.

## The south pole

**If the change broke it**: near the south pole, the objects would flip, spin from one frame to the next,
or part from their colliders.

**Why**: `FromToRotation(up, n)` has no single answer when the normal `n` points straight down `up`, and
near that point a tiny change of the normal turns the object a lot around it. Without the change, `up` is
the axis of the scene, which is the body's axis of rotation: the case is the south pole of the body. With
it, `up` is the Y axis of the quad, and a quad of KSP is not turned in its sphere (`PQ.SetupQuad` sets
its `localRotation` to identity): the same axis, the same place. The change adds a product of matrices on
the normal, in `float`, which can move it slightly.

**To play**: a craft put down among rocks with *Set Position*, as near the south pole of the Mun as rocks
grow, and the same at the north pole, where nothing degenerates; both builds; screenshots from above and
from the side, with Diag Colliders, and a few seconds of video to see whether anything spins.

**Script**: `set_position`, then the steps of [The rocks around a craft](non-regression.md#the-rocks-around-a-craft).

**Where it stands**: not played.

## Sigma Dimensions

**If the change broke it**: on bodies rescaled by Sigma Dimensions, the rocks would be drawn wrong,
stretched or tilted, or their colliders would part from them.

**Why**: the change takes the rotation of the quad out of its matrix by dividing by the length of one of
its axes: it assumes the scale of a quad is the same along its three axes. Sigma Dimensions changes the
size of the bodies, and Parallax Continued has code of its own for it.

**To play**: [The rocks around a craft](non-regression.md#the-rocks-around-a-craft) and
[A kerbal on a rock](#a-kerbal-on-a-rock) on the Mun rescaled by Sigma Dimensions, on both builds.

**Where it stands**: not played. Sigma Dimensions is still to try.

## A kerbal on a rock

**What it adds**: [The rocks around a craft](non-regression.md#the-rocks-around-a-craft) shows that the rocks turn at a
load, and so that what stands on one is put back elsewhere. This test looks at that consequence: a kerbal
standing on a rock is moved at a load without the change, and put back where he was with it.

**If the change broke it**: a kerbal standing on a rock with **release + change** would still be moved
at a load: put back higher or lower, sliding down the rock, or beside it.

**The install**: [the install](README.md#the-builds-and-the-install), on each build, with
[KSP Diag - Floating Origin](https://github.com/lhervier/KSP-Diag-FloatingOrigin),
[KSP Diag - Landed Vessel](https://github.com/lhervier/KSP-Diag-LandedVessel) and
[KSP Diag - Terrain Height](https://github.com/lhervier/KSP-Diag-TerrainHeight). After a load, Diag
Landed Vessel shows how far the kerbal moved from where the save left him, once settled; Diag Terrain
Height, the height of the surface he stands on above the ground of the terrain, which is the top of the
rock under him.

**Why a kerbal.** At every load, KSP puts a craft of a single part, a kerbal on EVA among others, back
down on the first collider a ray cast from 500 m above it meets (`Vessel.CheckGroundCollision`). A kerbal
on a rock that did not turn is put back where he was; on a rock that turned, he is put back on whatever
the rock now has under him. A craft of several parts is not put back down: it starts where the save left
it, while the rock follows its terrain quad, which stock KSP builds a few centimetres higher or lower at
each load ([Why it is different at every load](https://github.com/lhervier/KSP-TerrainPrecisionFix/blob/main/docs/the-culprit-ground.md#why-it-is-different-at-every-load)).
Such a craft can start slightly inside its rock and jump, with the change as without it: a defect of
stock KSP, not this one.

**The save** is a kerbal on EVA standing on a rock, saved **with the same build** as the one it is loaded
with: the change gives every rock another orientation than the release does. Without the change, it is
made so that the first load of a new session puts the rock where it was when the save was made: the `UT`
of the save is moved back by the time KSP had kept in `InverseRotAngle`. With the change, the orientation
of the rocks no longer depends on `InverseRotAngle`, and the save holds without moving its `UT` back.

1. Start KSP and load [`rocks-mun-jeb.sfs`](saves/rocks-mun-jeb.sfs), Jebediah Kerman already on EVA. Put
   him just above the top of a rock with *Set Position* of the `Alt+F12` menu, and let him settle on a part of the rock
   flat enough that he does not slide.
2. Read `InverseRotAngle` in Diag Floating Origin, and save.
3. In the `.sfs`, in `FLIGHTSTATE`, lower `UT` by `InverseRotAngle / 360 × 138984` seconds (the angle
   taken between 0 and 360).

At the first load of a new session, `InverseRotAngle` is 0, and the Mun is turned as it was when the save
was made. *Not checked yet.*

**By hand**:

1. Start KSP, copy its save into the folder of a sandbox game and load it. Wait for the digits of Diag
   Landed Vessel to stop moving, then press *Record* in the three windows: the kerbal is on his rock, and
   has hardly moved.
2. Let an hour of game time go by: time warp ×100 on rails for about 36 seconds.
3. Load **the same save** again and record: the rock has turned under the kerbal, and KSP has put him
   back on what the rock now has under him: higher, lower, on a slope he slides down, or on the ground
   beside it. Diag Terrain Height shows another surface under him, Diag Landed Vessel how far he moved.
4. Quit KSP, start it again, load the save and record: the kerbal is back on his rock as at step 1.

Played on both builds, on the Mun and on Eve.

**Script**: `automation/run-kerbal-on-a-rock.py`, to write: twelve loads after an hour of time warp
each, then KSP started again and twelve loads more; at each load, Diag Floating Origin, Diag Landed Vessel
and Diag Terrain Height recorded once the digits stop moving, and a view of the kerbal. Tools of
KSP-MCPServer as in [The rocks around a craft](non-regression.md#the-rocks-around-a-craft), and `quit_game`; of the
instruments: `landedvessel_read`, `landedvessel_record`, `terrainheight_record`. Starting KSP again is up
to the script, outside the server.

**Saves**: four, `kerbal-on-a-rock-mun-release.sfs`, `-mun-change.sfs`, `-eve-release.sfs`,
`-eve-change.sfs`, to make by hand: placing a kerbal on a rock takes an eye.

**Where it stands**: played on the Mun, outside the install described here, with a capsule rather
than a kerbal: with the change, the capsule stayed on its rock through twelve loads after an hour of time
warp each, then twelve loads after a restart of KSP; without it, it was thrown off at the first load
after ten minutes of play. To play again on the install, with a kerbal, by the script, with new saves;
the procedure that moves the `UT` back is still to check.

## OpenGL, on Linux

**If the change broke it**: under OpenGL, the rocks would be drawn wrong, or not at all, or still turn.

**Why**: on Linux, KSP renders with OpenGL and Parallax loads its `-linux` bundle, the GLSL variant of the
compute shader. The change is in the HLSL source, translated to GLSL by Unity: another compiler, another
result to see. KSP started with `-force-glcore` on Windows loads the same bundle. Proton presents itself
as Windows and loads the `-windows` bundle, the one of the other tests.

**To play**: [The rocks around a craft](non-regression.md#the-rocks-around-a-craft) and
[A kerbal on a rock](#a-kerbal-on-a-rock), on Linux, on both builds.

**Script**: the same scripts, once KSP-MCPServer and the instruments are checked on Linux.

**Where it stands**: not played.

## Performance

**If the change broke it**: a lower frame rate in a dense scatter (the grass of Kerbin, for instance).

**Why**: the change adds, in each call of `GetTRSMatrix`, a product of matrices and a transpose for
every object drawn, at every frame.

**To play**: the time of a frame, the same view of a dense scatter, on both builds, measured with
KSPProfiler. The protocol is to write: the view, how long to measure, how many runs.

**Where it stands**: not played.

## Out of reach

Not tested, and said as such when the change is offered: **macOS** (the Metal variant of the `-macosx`
bundle) and **Linux under Vulkan** (the SPIR-V variant of the `-linux` bundle), built, never run.
