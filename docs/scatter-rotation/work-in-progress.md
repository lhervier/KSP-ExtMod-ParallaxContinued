# Work in progress

Part of [Scatter rotation](README.md): what is still to check before the change can be offered. Each
point says what a player would see if the change broke something, how to play it, what its script needs,
and where it stands. In every test, the colliders of the rocks are shown with KSP Diag - Colliders, and
must follow the rocks drawn. A point moves to [Non-regression tests](non-regression.md) once complete
([What makes a test complete](non-regression.md#what-makes-a-test-complete)).

## Summary

- **The rocks around a craft** — a craft on the ground near rocks, the same save loaded again after an
  hour of time warp: the rocks turn without the change, and hold still with it; on the Mun and on Eve.
- **A kerbal on a rock** — a kerbal saved on a rock, loaded again after an hour of time warp, and after
  a restart of KSP: moved without the change, put back where he was with it; on the Mun and on Eve.
- **When the floating origin moves** — the rocks and their colliders move with it, together.
- **When the frame changes** — the craft goes above the rotating-frame altitude and back: the body turns
  in the scene without any load.
- **The scatters along the radius: the trees of Kerbin** — the other branch of `alignToTerrainNormal`.
- **The south pole** — where `FromToRotation` has no single answer, without the change and with it.
- **Sigma Dimensions** — a body of another size, and quads of another scale.
- **OpenGL, on Linux** — the GLSL variant of the compute shader.
- **Performance** — the time of a frame in a dense scatter, without the change and with it.
- **Out of reach** — macOS, Linux under Vulkan.

## The rocks around a craft

**If the change broke it**: the rocks of **release + change** would still turn at a load, or would be
drawn wrong.

**To play**: [The rocks turn at every load](reproducing-the-bug.md#the-rocks-turn-at-every-load), on both
builds: a craft on the ground, some ten metres from the nearest rocks, far enough that no rock reaches
it as it turns, near enough to see them. On the Mun, where every scatter with a collider is a rock; on
Eve, where vegetation without colliders grows among them, with both branches of `alignToTerrainNormal`.

**Script**: `automation/run-rocks-turning.py`, to write. Tools of KSP-MCPServer: `load_save`, `warp_to`
(check the time after it: it does not report a warp that did not happen), `set_ui`, `set_camera`,
`screenshot`; of the instruments: `floatingorigin_record`, and the `_show_window` of each.

**Saves**: [`rocks-mun.sfs`](saves/rocks-mun.sfs); `rocks-eve.sfs`, to make.

**Where it stands**: played on the Mun, without the change and with it: the rocks turn at every load by
the angle of the Mun without it, and do not move with it. That run was played outside the install
described here, and some of its readings came from outside the instruments: to play again by the
script. Also seen once on the Mun with the change, outside the install described here, at the date of
a save and an hour and forty minutes later: the outlines of the colliders follow the rocks at both dates,
as on the release; the largest blocks have no outline, with the change and without it: no collider. Not
played on Eve.

## A kerbal on a rock

**If the change broke it**: a kerbal standing on a rock with **release + change** would still be moved
at a load: put back higher or lower, sliding down the rock, or beside it.

**To play**: [A kerbal on a rock is moved](reproducing-the-bug.md#a-kerbal-on-a-rock-is-moved), on both
builds, on the Mun and on Eve, each build with its own save, made by
[Making the save](reproducing-the-bug.md#making-the-save): the change gives every rock another
orientation than the release does. With the change, the orientation of the rocks no longer depends on
`InverseRotAngle`, and the save holds without moving its `UT` back.

**A kerbal, not a craft of several parts.** KSP puts a craft of a single part back down at every load,
not a craft of several parts, which starts where the save left it, while stock KSP builds the ground, and
the rock with it, a few centimetres higher or lower at each load: a capsule on a rock can jump with the
change as with the release, for a reason that is not this bug
([Why a kerbal](reproducing-the-bug.md#a-kerbal-on-a-rock-is-moved)).

**Script**: `automation/run-kerbal-on-a-rock.py`, to write: twelve loads after an hour of time warp
each, then KSP started again and twelve loads more; at each load, Diag Floating Origin, Diag Landed Vessel
and Diag Terrain Height recorded once the digits stop moving, and a view of the kerbal. Tools of
KSP-MCPServer as in [The rocks around a craft](#the-rocks-around-a-craft), and `quit_game`; of the
instruments: `landedvessel_read`, `landedvessel_record`, `terrainheight_record`. Starting KSP again is up
to the script, outside the server.

**Saves**: four, `kerbal-on-a-rock-mun-release.sfs`, `-mun-change.sfs`, `-eve-release.sfs`,
`-eve-change.sfs`, to make by hand: placing a kerbal on a rock takes an eye.

**Where it stands**: played on the Mun, outside the install described here, with a capsule rather
than a kerbal: with the change, the capsule stayed on its rock through twelve loads after an hour of time
warp each, then twelve loads after a restart of KSP; without it, it was thrown off at the first load
after ten minutes of play. To play again on the install, with a kerbal, by the script, with new saves;
the procedure that moves the `UT` back is still to check.

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

**To play**: from the save of [The rocks around a craft](#the-rocks-around-a-craft), a screenshot from
above; then the craft put on an orbit above 100 km with *Set Orbit* of the `Alt+F12` menu, some time in
orbit, and put back where it stood with *Set Position*; the same screenshot. Diag Floating Origin shows
the frame go to `Inertial` and back to `Rotating`, and `directRotAngle` move. On both builds.

**Script**: `set_orbit`, `wait` or `warp_to`, `set_position`, then the screenshots of
[The rocks around a craft](#the-rocks-around-a-craft).

**Where it stands**: not played. That the body is held still again at another angle is read in the code
of KSP, not seen.

## The scatters along the radius: the trees of Kerbin

**If the change broke it**: the trees, and the other objects that stand along the radius of the body
rather than on the slope of the ground, would lean, turn at every load, or have their colliders apart
from what is drawn.

**Why**: with `alignToTerrainNormal = False`, the normal is the direction of the body's centre, not the
terrain's: the other branch of the code, which the change also brings into the quad's frame. The stock
configs set it on Kerbin, Laythe and Eve, with colliders on Kerbin and Laythe.

**To play**: [The rocks around a craft](#the-rocks-around-a-craft) on Kerbin, a craft standing among
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

**Script**: `set_position`, then the steps of [The rocks around a craft](#the-rocks-around-a-craft).

**Where it stands**: not played.

## Sigma Dimensions

**If the change broke it**: on bodies rescaled by Sigma Dimensions, the rocks would be drawn wrong,
stretched or tilted, or their colliders would part from them.

**Why**: the change takes the rotation of the quad out of its matrix by dividing by the length of one of
its axes: it assumes the scale of a quad is the same along its three axes. Sigma Dimensions changes the
size of the bodies, and Parallax Continued has code of its own for it.

**To play**: [The rocks around a craft](#the-rocks-around-a-craft) and
[A kerbal on a rock](#a-kerbal-on-a-rock) on the Mun rescaled by Sigma Dimensions, on both builds.

**Where it stands**: not played. Sigma Dimensions is still to try.

## OpenGL, on Linux

**If the change broke it**: under OpenGL, the rocks would be drawn wrong, or not at all, or still turn.

**Why**: on Linux, KSP renders with OpenGL and Parallax loads its `-linux` bundle, the GLSL variant of the
compute shader. The change is in the HLSL source, translated to GLSL by Unity: another compiler, another
result to see. KSP started with `-force-glcore` on Windows loads the same bundle. Proton presents itself
as Windows and loads the `-windows` bundle, the one of the other tests.

**To play**: [The rocks around a craft](#the-rocks-around-a-craft) and
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
