# make_macos_vm

Windows users <b>MUST</b> enclose anything after "--root" and or "--image" with
double quotes.

To avoid confusion with "--root", this <b>MUST</b> be the same path used in
the preferences window with the selectable list named <b>"Default Machine Folder."</b>

If installing extension pack, you <b>MUST</b> have sudo access.

# Before booting

If Hyper-V is applicable, especially for Windows, it <b>MUST</b> be disabled to use >= 2 CPU's. This panics the kernel and gives the error
"non-monotonic time" when trying to use more than 1 CPU. You can also check if virtualbox is using Hyper-V as it will mention "NEM" in the VM logs.

Side note, if running from a Windows host, memory integrity <b>MUST</b> be disabled. This uses Hyper-V and this will get in the way, I learned that
the hard way.

So, there's no reason to use 1 CPU for MacOS, so abide by this, and especially <b>DO NOT</b> remove the "RealTSCOffset" value, that is required
to enable mutli-core usage.
