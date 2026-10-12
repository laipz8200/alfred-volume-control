"""Package the workflow and its license using only the Python standard library."""
from pathlib import Path
import plistlib
import zipfile

ROOT = Path(__file__).resolve().parent
metadata = plistlib.loads((ROOT / "workflow/info.plist").read_bytes())
assert metadata["name"] == "Volume Control"
files = {
    "info.plist": ROOT / "workflow/info.plist",
    "icon.png": ROOT / "workflow/icon.png",
    "LICENSE": ROOT / "LICENSE",
}
output = ROOT / "build/Volume-Control.alfredworkflow"
output.parent.mkdir(exist_ok=True)
staged = output.with_suffix(".tmp")
with zipfile.ZipFile(staged, "w", zipfile.ZIP_DEFLATED) as archive:
    for name, path in files.items():
        entry = zipfile.ZipInfo(name)
        entry.external_attr = 0o100644 << 16
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, path.read_bytes())
with zipfile.ZipFile(staged) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(files)
staged.replace(output)
print(output)
