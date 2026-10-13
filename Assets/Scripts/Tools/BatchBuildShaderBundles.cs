#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;
using System;
using System.IO;
using System.Linq;

// Command line counterpart of CreateAssetBundles.BuildAllAssetBundles (ExportAssetBundle.cs): same legacy
// BuildPipeline.BuildAssetBundle call, same options and platforms, without the save dialog and the selection.
public static class BatchBuildShaderBundles
{
    /// <summary>
    /// Builds one shader bundle per platform (windows, macosx, linux) from a list of assets.
    /// Command line arguments: -bundleOut &lt;path\Name.unity3d&gt; (the platform suffix is added to the name),
    /// -bundleAssets &lt;asset path&gt;[;&lt;asset path&gt;...] (paths relative to the project, e.g.
    /// Assets/Shaders/Scatters/TerrainScatters.compute). Exits with code 1 if an argument or an asset is missing.
    /// </summary>
    public static void Build()
    {
        string[] args = Environment.GetCommandLineArgs();
        string outPath = GetArg(args, "-bundleOut");
        string assetList = GetArg(args, "-bundleAssets");
        if (outPath == null || assetList == null)
        {
            Debug.LogError("BatchBuildShaderBundles: -bundleOut and -bundleAssets are required");
            EditorApplication.Exit(1);
            return;
        }

        UnityEngine.Object[] assets = assetList.Split(';')
            .Select(p => AssetDatabase.LoadMainAssetAtPath(p.Trim()))
            .ToArray();
        if (assets.Any(a => a == null))
        {
            Debug.LogError("BatchBuildShaderBundles: asset not found in " + assetList);
            EditorApplication.Exit(1);
            return;
        }

        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(outPath)));

        var opts = BuildAssetBundleOptions.DeterministicAssetBundle | BuildAssetBundleOptions.ForceRebuildAssetBundle;
        BuildTarget[] platforms = { BuildTarget.StandaloneWindows, BuildTarget.StandaloneOSX, BuildTarget.StandaloneLinux64 };
        string[] platformExts = { "-windows", "-macosx", "-linux" };

        for (int i = 0; i < platforms.Length; ++i)
        {
            string target = outPath.Replace(".unity3d", platformExts[i] + ".unity3d");
            #pragma warning disable CS0618
            bool ok = BuildPipeline.BuildAssetBundle(assets[0], assets, target, opts, platforms[i]);
            #pragma warning restore CS0618
            Debug.Log("BatchBuildShaderBundles: " + target + (ok ? " built" : " FAILED"));
            if (!ok)
            {
                EditorApplication.Exit(1);
                return;
            }
        }
    }

    static string GetArg(string[] args, string name)
    {
        int i = Array.IndexOf(args, name);
        return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
    }
}
#endif
