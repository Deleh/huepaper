{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  name = "python-environment";
  buildInputs = with pkgs; [
    python3
    python3Packages.virtualenv
  ];
  shellHook = ''
    function log_header {
      echo -ne "==> \e[32m\e[1m$1\e[0m\n\n"
    }
    function log_subheader {
      echo -ne "--> \e[33m\e[1m$1\e[0m\n\n"
    }
    function log {
      echo -ne "    $1\n"
    }

    echo ""
    log_header "python_environment"
    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
    log_subheader "upgrading pip"
    pip install --upgrade pip
    echo ""
    if [ -s requirements.txt ]; then
      log_subheader "found requirements.txt, installing packages"
      pip install -r requirements.txt
      echo ""
    fi
    log_header "package versions"
    log "$(python --version)"
    log "$(pip --version)"
  '';
}
