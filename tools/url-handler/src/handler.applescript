on open location theUrl
	do shell script "/usr/bin/env bash -lc '/usr/bin/dirname \"$0\" >/dev/null 2>&1; /bin/bash \"" & POSIX path of (path to resource "handle-url.sh") & "\" " & quoted form of theUrl & "'"
end open location
