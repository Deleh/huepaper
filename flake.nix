{
  description = "A colorful wallpaper generator";

  nixConfig.bash-prompt = "\[\\e[1m\\e[34mhuepaper-develop\\e[0m\]$ ";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:

    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {

          # Package

          packages.huepaper =

            pkgs.python3Packages.buildPythonPackage rec {

              name = "huepaper";
              src = self;

              nativeBuildInputs = with pkgs; [
                wrapGAppsHook
              ];

              propagatedBuildInputs = with pkgs; [
                python3Packages.colour
                python3Packages.pillow
              ];

            };

          defaultPackage = self.packages.${system}.huepaper;

          # Development shell

          devShell = pkgs.mkShell {

            buildInputs = with pkgs; [
              python3
              python3Packages.colour
              python3Packages.pillow
              python3Packages.pip
              python3Packages.setuptools
              python3Packages.virtualenv
            ];

          };
        }
      );
}
