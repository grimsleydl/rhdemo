
{
  description = "rh-demo flask app";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?rev=c82b46413401efa740a0b994f52e9903a4f6dcd5";
    flake-utils.url = "git://github.com/numtide/flake-utils.git";
    devshell.url = "git://github.com/numtide/devshell.git";
  };

  outputs = { self, nixpkgs, devshell, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system:
  let
    overlays = [ ];
    pkgs = import nixpkgs {
      inherit system overlays;
      config.allowBroken = true;
    };
    p2n = pkgs.poetry2nix;
    python = "python310";

    customOverrides = self: super: { };
    packageName = "rhdemo-py";

    app = p2n.mkPoetryApplication {
      projectDir = ./.;
      python = pkgs.python310;
      overrides =
        [ pkgs.poetry2nix.defaultPoetryOverrides customOverrides ];
    };
    appEnv = p2n.mkPoetryEnv {
      projectDir = ./.;
      python = pkgs.python310;
      overrides = [ p2n.defaultPoetryOverrides customOverrides ];
    };
  in rec
  {
    packages.containerImage = pkgs.dockerTools.buildLayeredImage {
      name = "rhdemo-py";
      contents = [ pkgs.python310 app pkgs.bash pkgs.coreutils ];
      config = {
        Cmd = [ "${app}/bin/main" ];
      };
    };

    # packages.${packageName} = app;
    packages.rhdemo-py = app;
    defaultPackage = app.dependencyEnv;
    devShell =
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ devshell.overlay ];
        };
      in
      pkgs.devshell.mkShell {
        imports = [ (pkgs.devshell.importTOML ./devshell.toml) ];
        devshell.packages = with pkgs; [
          appEnv
          poetry
          black
          python-language-server
          pyright
        ];
      };
  });
}
