#if UNITY_EDITOR
using System.Text;
using UnityEditor;
using UnityEngine;

// What Quaternion.FromToRotation(Vector3.up, n) gives when n points almost straight down, in the Unity of KSP
// (2019.4.18f1). Put this file in the Assets/Editor folder of any project of that version, then run:
//
//     Unity.exe -batchmode -quit -projectPath <project> -executeMethod FromToRotationNearDown.Print -logFile <log>
//
// The log gets one line per normal: how far n is from straight down, the rotation Unity returns, the axis it
// turns around, and how far that rotation sends up from n. The normals lean towards the same side (45° between X
// and Z), at a smaller and smaller angle from straight down.
public static class FromToRotationNearDown
{
    /// <summary>Writes to the log what Quaternion.FromToRotation(Vector3.up, n) returns for normals n closer
    /// and closer to straight down.</summary>
    public static void Print()
    {
        StringBuilder text = new StringBuilder("FromToRotationNearDown\n");
        // 0.0796 degrees: the centre of each of the four finest terrain quads that meet at a pole, on a body whose
        // finest quads are of level 10, is sqrt(2) / 2^10 radians from the pole
        double[] degreesFromDown = { 5, 1, 0.5, 0.2, 0.1, 0.0796, 0.05, 0.01 };
        foreach (double degrees in degreesFromDown)
        {
            double tilt = degrees * Mathf.Deg2Rad;
            float side = (float)(System.Math.Sin(tilt) / System.Math.Sqrt(2));
            Vector3 n = new Vector3(side, -(float)System.Math.Cos(tilt), side).normalized;
            Quaternion q = Quaternion.FromToRotation(Vector3.up, n);
            Vector3 axis = new Vector3(q.x, q.y, q.z).normalized;
            float miss = Vector3.Angle(q * Vector3.up, n);
            text.AppendFormat(System.Globalization.CultureInfo.InvariantCulture,
                "{0,8:0.0000} deg from down  1 + n.y = {1:0.00e+00}  rotation ({2:0.0000}, {3:0.0000}, {4:0.0000}, {5:0.0000})  " +
                "axis ({6:0.0000}, {7:0.0000}, {8:0.0000})  up sent {9:0.0000} deg from n\n",
                degrees, 1.0 + n.y, q.x, q.y, q.z, q.w, axis.x, axis.y, axis.z, miss);
        }
        Debug.Log(text.ToString());
    }
}
#endif
