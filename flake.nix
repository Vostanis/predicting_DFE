{
  description = "Python dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            (pkgs.python313.withPackages
              (ps: with ps; [
                pandas
                numpy
                seaborn
                matplotlib
                scikit-learn
                torch
                timm
                tqdm

                jupyterlab
                ipykernel
              ]))
          ];

          shellHook = ''
            export JUPYTER_PATH=$PWD/.jupyter
          '';
        };
      });
}
