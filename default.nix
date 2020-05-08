with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "myPythonEnv";
  buildInputs = with pkgs; [
    python37Full
    python37Packages.virtualenv
  ];
  src = null;
  shellHook = ''
    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    source .venv/bin/activate
    pip install --upgrade pip
    if [ -s requirements.txt ]; then
      pip install -r requirements.txt
    fi
  '';
}
