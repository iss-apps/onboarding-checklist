#!/bin/bash
set -euo pipefail

# set stdout to append to a file
exec >> "/tmp/url.log"
exec 2>&1

# trap when script exits
trap 'end $? "$LINENO"' EXIT

# pretty logs
info() {
  echo -e "\033[32m[INFO] ${@}\033[0m"
}

warn() {
  echo -e "\033[33m[WARN] ${@}\033[0m"
}

error() {
  echo -e "\033[31m[ERROR] ${@}\033[0m"
  return 1
}

end() {
  if [[ $1 != 0 ]]; then
    error "failed at line $2 with exit code $1"
    exit 1
  else
    info "done"
    exit 0
  fi
}

iss-app() {
  case "$1" in
  "uninstall")
    info running iss-app.uninstall
    pkill -f "ISS App" && info successfully killed ISS App || warn failed to kill ISS App && true
    local rm_status="$(rm -r "/Users/$USER/Applications/Chrome Apps.localized/ISS App.app" 2>&1 || true)"
    if [ -z "$rm_status" ]; then
      info successfully removed ISS App bundle
    else
      warn "$rm_status"
    fi
    ;;
  "fail")
    error "This is a test error"
    ;;
  *)
    error "Unknown action: iss-app.$1"
    ;;
  esac
}

settings() {
  case "$1" in
  "dock")
    open "x-apple.systempreferences:com.apple.preference.dock"
    ;;
  *)
    error "Unknown action: settings.$1"
    ;;
  esac
}

main() {
  method="${1:-}"
  if [[ -z "$method" ]]; then
    exit 0
  fi

  method="${method#*://}"
  method=(${method//./ })

  case "${method[0]}" in
    "iss-app")
      iss-app "${method[@]:1}"
      ;;
    "settings")
      settings "${method[@]:1}"
      ;;
    *)
      error "Unknown method: ${method[0]}"
      ;;
  esac
}

main "$@"