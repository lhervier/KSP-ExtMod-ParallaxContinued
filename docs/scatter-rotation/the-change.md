# The change

Part of [Scatter rotation](README.md): why Parallax Continued turns its rocks at every load, what the
change on the branch
[`fix/scatter-rotation`](https://github.com/lhervier/KSP-ExtMod-ParallaxContinued/compare/1.0.4...fix/scatter-rotation)
does, in two commits, and what it changes for a player.

## Why the rocks turn

Parallax orients each object of its scatter from the vertical axis of the scene, `Vector3.up`, both the
object it draws and the collider it gives it:

```csharp
// CollisionManager.CreateGameObject
// Ideally I would like this to set localRotation but I spent days trying to get it to work in local space, and couldn't figure it out
Quaternion rotAWorld = Quaternion.FromToRotation(Vector3.up, targetNormal);
Quaternion rotBWorld = Quaternion.AngleAxis(transform.rotation, Vector3.up);
go.transform.rotation = rotAWorld * rotBWorld;
```

```hlsl
// ScatterUtils.cginc, GetTRSMatrix, called by the Evaluate kernels of TerrainScatters.compute
float3 up = float3(0, 1, 0);
float4x4 mat = TransformToPlanetNormal(up, nrm);    // nrm: the normal, in world space
mat = mul(mat, GetRotationMatrix(rotationAngles));  // the random angle of the object, around Y
```

In the scene, `Vector3.up` is the body's axis of rotation, but it does not turn with the body. When the
body is turned by θ in the scene, the normal under an object turns with it and `Vector3.up` does not:

    FromToRotation(up, R(θ)·n) = R(θ) · FromToRotation(up, n) · R(−θ)

so the object comes out turned by −θ around its own normal, on its own pivot. Everything else of an
object, its place, its size, whether it appears at all, is computed in the frame of its terrain quad;
only its orientation depends on how the body is turned in the scene.

**And KSP turns the body in the scene at every load.** Below its rotating-frame altitude (100 km on the
Mun), KSP holds the body still in the scene and turns the rest of the universe instead, and keeps the
time played that way in `Planetarium.InverseRotAngle`. No save holds that angle, and it is 0 when KSP
starts. At every load, the body is turned again in the scene from the date of the save minus that angle
(`CelestialBody.CBUpdate`, KSP 1.12.5):

```csharp
rotationAngle = (initialRotation + 360.0 * rotPeriodRecip * Planetarium.GetUniversalTime()) % 360.0;
if (!inverseRotation)
    directRotAngle = (rotationAngle - Planetarium.InverseRotAngle) % 360.0;
else
    Planetarium.InverseRotAngle = (rotationAngle - directRotAngle) % 360.0;
```

So:

- **nothing turns during a session** as long as the craft stays below that altitude: the body stays still
  in the scene, and the drawn rocks and their colliders keep the orientation they had when they were made;
- **loading an older save turns every object** by the body's rotation over the time played since that
  save was made: the date goes back, `InverseRotAngle` does not;
- **starting KSP again** puts `InverseRotAngle` back to 0: a save loaded then is turned by the time played
  in the whole session it was made in;
- **saving and loading straight away turns nothing.**

The drawn object turns too, far from any collider: its matrix is built at every frame by the `Evaluate`
kernels of the compute shader. The collider is built once, when a craft comes near. Both use the same
formula, and stay together as long as the body is not turned again in the scene.

## What the change does

**It builds the orientation of each object in the frame of its terrain quad, then applies the quad's
rotation**, in the compute shader and in the code of the colliders, the same way on both sides:

```hlsl
// ScatterUtils.cginc, GetTRSMatrix, changed
float3x3 quadToWorld = (float3x3)_ObjectToWorldMatrix;
quadToWorld /= length(quadToWorld._m00_m10_m20);    // Remove the quad's (uniform) scale
float3 localNrm = mul(transpose(quadToWorld), nrm);
float3 up = float3(0, 1, 0);
float4x4 mat = TransformToPlanetNormal(up, localNrm);
mat = mul(mat, GetRotationMatrix(rotationAngles));
mat = mul(quadRotation, mat);                       // quadToWorld, as a 4x4 matrix
```

```csharp
// CollisionManager.CreateGameObject, changed
Vector3 localNormal = scatterSystemQuad.quad.gameObject.transform.InverseTransformDirection(targetNormal);
Quaternion rotALocal = RotationFromUp(localNormal);  // Quaternion.FromToRotation in the first commit
Quaternion rotBLocal = Quaternion.AngleAxis(transform.rotation, Vector3.up);
go.transform.localRotation = rotALocal * rotBLocal;
```

The quad turns with the body, so the object turns with it, whatever the angle of the body in the scene.
`targetNormal` and `nrm` are still computed as before, in world space, from either branch of
`alignToTerrainNormal`: the change only brings them into the quad's frame.

**Why both sides at once.** The collider must have the orientation of the object drawn. Changed on one
side only, the collider would hold still and the drawing would go on turning, or the other way round, and
a craft would hit a rock where none is drawn. This is likely why a collider set in local space alone did
not work.

**What it leaves alone**: the place of each object, its size, which objects appear, the distribution, the
LODs, the colliders' lifetime. Neither the `Distribute` kernels nor the C# that places objects are
touched; of the compiled compute shader, only the four `Evaluate` kernels change.

**What it assumes**: the quad's scale is uniform. That holds for the stock bodies; a mod that rescales a
body with a non-uniform scale would break that assumption
([Work in progress](work-in-progress.md#sigma-dimensions)).

## The second commit: near the south pole

The first commit is the one above, with `Quaternion.FromToRotation` on the side of the colliders, as in
the release. Played near the south pole of Laythe, where the normal of every tree of the four quads that
meet at the pole points 0.0796° from straight down `up`, it showed two things:

- **the collider still turned around the trunk otherwise than the tree drawn**, as on the release:
  `Quaternion.FromToRotation` makes half a turn around X that close to straight down, while the compute
  shader turns around `up × normal`
  ([Near the south pole, the colliders part from the objects drawn](reproducing-the-bug.md#near-the-south-pole-the-colliders-part-from-the-objects-drawn));
  with the first commit, by the same angle at every load, X being that of the quad;
- **the tree drawn was stretched**, taller than its collider, and, from some angles, now and then for
  one frame, an object was drawn stretched across the screen. Neither shows on the release.

![The same tree of Laythe near the south pole and the outline of its collider in yellow, seen from the same place on three builds: on the release, the outline is turned around the trunk from the tree; with the first commit only, it is still turned, and the tree drawn is taller than its outline; with both commits, the outline is on the tree](runs/pole-laythe/three-builds.jpg)

*The same view of the tree of [`pole-laythe.sfs`](saves/pole-laythe.sfs) on the three builds, cropped.*

The stretch comes from `TransformToPlanetNormal`, which builds the rotation as `I + V + V² / (1 + c)`,
`c` being the vertical component of the normal and `V` the matrix of `v = up × normal`. Near straight
down, `c` is close to −1, and `1 + c` the difference of two nearly equal numbers: at 0.0796°, about
10⁻⁶, of the order of the rounding of `c` in `float`. Divided by it, that rounding stretches the matrix
along the normal and across it. The first commit brings the normal into the frame of the quad by a
product of matrices, which rounds `c` once more, by an amount that depends on the angle of the body in
the scene.

**The second commit** computes the same rotation, on both sides, without that difference: for a unit
normal, `1 + c = |v|² / (1 − c)`, where nothing cancels when `c` is negative.

```hlsl
// ScatterUtils.cginc, TransformToPlanetNormal, second commit
float onePlusC = c >= 0 ? 1 + c : dot(v, v) / (1 - c);
if (onePlusC <= 0)
{
    // b is exactly -a: half a turn around an axis perpendicular to a, X for a = (0, 1, 0)
    ...
}
float lastPart = 1 / onePlusC;    // was 1 / (1 + c)
```

```csharp
// CollisionManager.RotationFromUp, second commit: the rotation TransformToPlanetNormal gives the object drawn
Vector3 v = Vector3.Cross(Vector3.up, normal);
float c = normal.y;
float onePlusC = c >= 0 ? 1 + c : v.sqrMagnitude / (1 - c);
if (onePlusC <= 0)
{
    return new Quaternion(1, 0, 0, 0);    // exactly -up: half a turn around X, as the compute shader does
}
return Quaternion.Normalize(new Quaternion(v.x, v.y, v.z, onePlusC));
```

The collider and the object drawn are thus turned around the same axis, by the same angle, everywhere on
the body; at the pole itself, should a normal point exactly straight down, both make the same half
turn. Everything else of the first commit stays. Every protocol of these pages was played again with
both commits; the runs published are those.

## What it changes for a player

- **The rocks keep the same orientation at every load**, whatever the time played since the save, and
  after a restart of KSP.
- **A craft resting on a rock stays on it**, and a craft next to a cluster is no longer reached by it.
- **At the first load with the change**, every object takes a new orientation, tied to its quad. A
  craft saved on a rock, or right next to one, with Parallax as released can then start inside it, once:
  the same as at any load of the release, where every rock already comes back turned by the time played
  since the save ([Non-regression tests](non-regression/a-save-made-with-the-release.md)).
- **Near the south pole, each collider is on its object**, where on the release it is turned around it,
  by another angle at every load
  ([Near the south pole, the colliders part from the objects drawn](reproducing-the-bug.md#near-the-south-pole-the-colliders-part-from-the-objects-drawn)).
