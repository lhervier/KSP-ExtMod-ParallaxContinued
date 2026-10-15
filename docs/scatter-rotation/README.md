# Scatter rotation: the rocks that turn at every load

Parallax Continued orients each object of its scatter, the rock it draws and the collider it gives it,
from the vertical axis of the Unity scene. KSP turns the body in the scene again at every load, by the
time played since the save was made: every rock comes back turned on itself, and a craft standing on
one, or right next to one, can start inside it and be thrown off. These pages show how to see it, what
the change on the branch
[`fix/scatter-rotation`](https://github.com/lhervier/KSP-ExtMod-ParallaxContinued/compare/1.0.4...fix/scatter-rotation)
does about it, and how we check that the change breaks nothing.

**How this was made.** This change and these pages were written with Claude, Anthropic's AI, then read
and checked by a human. I say it from the start because a contribution made with an AI deserves a closer
look, and because some will prefer to stop here. What is worth checking here: the two files of the
change, and that every protocol below gives what it says on your own install.

## Reproducing the bug

**A kerbal standing on the Mun a few metres from the rocks, the same save loaded again after an hour of
time warp: every cluster of rocks has turned on its own centre, by the angle the Mun has turned in that
hour, while the ground and the kerbal have not.** A craft standing on a rock, or right next to one, then
starts elsewhere on it, or inside it, and can be thrown off. On Kerbin, a cluster of cacti, which
stand along the radius of the body rather than on the slope of the ground, turns the same way. With the
change, the same protocol shows the rocks and the cacti holding still, load after load. Near the south
pole of a body, a second defect: the collider of each object is turned around it otherwise than the
object drawn, already in the release; with the change, it is on its object. The texture of the ground,
on every body, and a plant here and there on Eve still change at every load, with the change as without
it: they do not come from this bug.

**→ Full page: [Reproducing the bug](reproducing-the-bug.md)**

## The change

**The orientation of each object is built in the frame of its terrain quad, then turned by the quad's
rotation, in the compute shader that draws the scatter and in the code that gives it its colliders.**
A second commit gives both sides the same rotation near the south pole, where the code of the colliders
and the compute shader disagree. Nothing else moves: the place, the size and the choice of each object
are computed as before.

**→ Full page: [The change](the-change.md)**

## Non-regression tests

**Whether the change breaks anything else in the game, each test with its save, its script and its
result, on Parallax Continued 1.0.4 as players have it.** Complete: the colliders on the scatter, on the
Mun, on Eve and on Kerbin: with the change, they stay on the objects drawn, load after load; and when the
floating origin moves, on Kerbin: the cacti and their colliders stay together; and when the frame
changes, on the Mun: a kerbal taken to orbit and back finds the rocks as he left them, their colliders
on them.

**→ Full page: [Non-regression tests](non-regression.md)**

## Work in progress

**What is still to check before the change can be offered: Sigma Dimensions, a kerbal on a rock,
OpenGL on Linux, and performance.** Each point says what a player would see if the change broke it, and
how to play it.

**→ Full page: [Work in progress](work-in-progress.md)**

## The builds and the install

**The change is offered on top of the `1.0.4` tag**, on the branch
[`fix/scatter-rotation`](https://github.com/lhervier/KSP-ExtMod-ParallaxContinued/tree/fix/scatter-rotation):
two commits, two files.

**It is tested on Parallax Continued 1.0.4 as players have it**: the archive of the 1.0.4 release on
GitHub, which is also the one CKAN installs. That release is not built from the `1.0.4` tag in every
part. Its C# is: its DLL decompiles to the same code as one built from the tag. Its compute shader is
not: it lacks the check of each triangle's biome that `Distribute` has in the source. So the branch
[`claude/scatter-rotation-tests`](https://github.com/lhervier/KSP-ExtMod-ParallaxContinued/tree/claude/scatter-rotation-tests)
adds, on top of the change, one commit that takes that check out, with which the source gives back the
compute shader of the release byte for byte; then the tool that builds it, and these pages. The change
touches the `Evaluate` kernels only, that commit the `Distribute` kernels only.

Every protocol is played on two builds, each in its own install:

| build | what it is | how to get it |
|---|---|---|
| **release** | Parallax Continued 1.0.4, as players have it | CKAN, or the 1.0.4 release on GitHub |
| **release + change** | the same, with the change | the release, with the DLL and the compute shader built from `claude/scatter-rotation-tests` as below |

When a new version of Parallax Continued is released, the change is brought onto it and the tests are
played again.

**The install.** KSP 1.12.5, with:

- Parallax Continued 1.0.4, its three packs of stock textures (planet, terrain and scatter, 1.0.3) and
  what it requires: Kopernicus (release 250), ModularFlightIntegrator 1.2.10, KSPTextureLoader 1.0.36,
  Harmony 2.2.1, KSPBurst 1.7.4.11, ModuleManager 4.2.3; with its default settings: the rocks of the Mun
  have colliders;
- Deferred 1.3.5 and Shabby 0.4.2, the renderer most players run Parallax Continued with;
- KSP Community Fixes 1.41.1;
- the instruments each protocol names, among
  [KSP Diag - Colliders](https://github.com/lhervier/KSP-Diag-Colliders) (draws the edges of the
  terrain quads, and the colliders of the scatter),
  [KSP Diag - Floating Origin](https://github.com/lhervier/KSP-Diag-FloatingOrigin) (shows the angle the
  body is turned by in the scene, `directRotAngle`),
  [KSP Diag - Landed Vessel](https://github.com/lhervier/KSP-Diag-LandedVessel) (where a craft is put
  down at a load, and where it settles) and
  [KSP Diag - Terrain Height](https://github.com/lhervier/KSP-Diag-TerrainHeight) (the height of the
  surface the craft touches, a rock or the ground);
- [KSP-MCPServer](https://github.com/lhervier/KSP-MCPServer), only to play a protocol by script.

No other mod.

**Building release + change.** The build replaces two things in the `GameData/ParallaxContinued` of the
release: the DLL and the three `ParallaxCompute` bundles. The rest comes from the release: the shader
bundles committed in the repository are older than the release, and `Config/ParallaxGlobalSettings.cfg`,
which gives the rocks their colliders (`collisionLevel = 2`), is not in it.

The DLL, from `Mod Source/Parallax/Parallax.csproj`:

    dotnet build -c Release -p:Platform=x64 -p:GameDataPath=<GameData>\ -p:OutDir=<output>\

with `GameDataPath` pointing at a `GameData` that holds `000_Harmony`, `000_KSPBurst`, `Kopernicus` and
`KSPTextureLoader`, next to `KSP_x64_Data\Managed`. Without both properties, the project writes into
its default KSP install. The compute shader, with Unity 2019.4.18f1 (the version of KSP 1.12.5) and
`Assets/Scripts/Tools/BatchBuildShaderBundles.cs` of this branch:

    Unity.exe -batchmode -quit -projectPath <project> -executeMethod BatchBuildShaderBundles.Build
        -bundleOut <folder>\ParallaxCompute.unity3d
        -bundleAssets Assets/Shaders/Scatters/TerrainScatters.compute -logFile <log>

It writes `ParallaxCompute-windows.unity3d`, `-macosx` and `-linux`. Without `-nographics`: it would add
a variant for the null graphics device.
