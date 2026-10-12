"""Compile and validate the workflow on macOS without changing system volume."""

from pathlib import Path
import plistlib
import subprocess
import tempfile

WORKFLOW = Path(__file__).resolve().parents[1] / "workflow" / "info.plist"
ACTION = "set volume output volume level output muted (level is 0)"
INVALID = "Enter a whole number from 0 to 100."
RUN = "\non run argv\n    return alfred_script(item 1 of argv)\nend run\n"


def execute(path, query):
    result = subprocess.run(
        ["/usr/bin/osascript", str(path), query],
        check=True, capture_output=True, text=True,
    )
    return result.stdout.rstrip("\n")


workflow = plistlib.loads(WORKFLOW.read_bytes())
[source] = [
    obj["config"]["applescript"] for obj in workflow["objects"]
    if obj["type"] == "alfred.workflow.action.applescript"
]
assert source.count(ACTION) == 1
assert sum(line.strip().startswith("set volume ") for line in source.splitlines()) == 1
with tempfile.TemporaryDirectory(prefix="volume-tests-") as directory:
    directory = Path(directory)
    genuine = directory / "volume.applescript"
    genuine.write_text(source)
    subprocess.run(
        ["/usr/bin/osacompile", "-o", str(directory / "volume.scpt"), str(genuine)],
        check=True, capture_output=True, text=True,
    )
    mock = directory / "mock.applescript"
    mock.write_text(source.replace(ACTION, "return level as text") + RUN)
    for query in ["0", "1", "50", "99", "100", "003"]:
        assert execute(mock, query) == str(int(query)), repr(query)
    for query in ["", "-1", "101", "1.5", "nan", "999999999999999999999999999999",
                  "text", '50; touch /tmp/volume-test', '50\" & do shell script \"true',
                  " ", " 50", "50 ", "5 0", "\t50", "+50"]:
        assert execute(mock, query) == INVALID, repr(query)
    mock.write_text(source.replace(ACTION, 'error "test failure"') + RUN)
    assert execute(mock, "50") == "Could not set volume: test failure"
print("AppleScript compiled; 22 mocked execution checks passed. No volume writes.")
