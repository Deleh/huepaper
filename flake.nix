{
  description = "A colorful wallpaper generator";

  nixConfig.bash-prompt = "\[\\e[1m\\e[34mhuepaper-dev\\e[0m:\\w\]$ ";

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
              propagatedBuildInputs = with pkgs; [
                python3Packages.colour
                python3Packages.numpy
                python3Packages.pillow
              ];
            };
          defaultPackage = self.packages.${system}.huepaper;

          # App
          apps.huepaper = {
            type = "app";
            program = "${self.packages.${system}.huepaper}/bin/huepaper";
          };
          defaultApp = self.apps.${system}.huepaper;

          # Development shell
          devShell = pkgs.mkShell {
            buildInputs = with pkgs; [
              python3
              python3Packages.colour
              python3Packages.numpy
              python3Packages.pillow
              python3Packages.pip
              python3Packages.setuptools
              python3Packages.virtualenv
            ];

          };
        }
      );
}
