{
  description = "axON - Blood Red Note Taking TUI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonPackages = pkgs.python3Packages;
        
        # Build the Python package
        axon = pythonPackages.buildPythonPackage rec {
          pname = "axon";
          version = "0.1.0";
          format = "pyproject";
          src = self;
          
          nativeBuildInputs = with pythonPackages; [
            hatchling
          ];
          
          propagatedBuildInputs = with pythonPackages; [
            textual
          ];
          
          doCheck = false;
          
          meta = with pkgs.lib; {
            description = "Blood Red on Pitch Black Note Taking TUI";
            homepage = "https://github.com/yourusername/axon";
            license = licenses.mit;
            maintainers = with maintainers; [ ];
            platforms = platforms.all;
          };
        };
        
      in {
        devShells.default = pkgs.mkShell {
          name = "axon-dev";
          packages = with pkgs; [
            python3
            python3Packages.textual
            python3Packages.pip
            git
            python3Packages.black
            python3Packages.ruff
            python3Packages.mypy
          ];
          
          shellHook = ''
            export PYTHONPATH="${PYTHONPATH:-}:${self.outPath}/lib/python3.12/site-packages"
            echo "axON development environment"
            echo "Run 'python -m axon' to start the app"
            echo "Run 'nix run .#axon' to run from build"
          '';
        };
        
        packages.axon = axon;
        packages.default = axon;
      });
}