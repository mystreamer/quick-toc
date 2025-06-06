{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05") {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (ps: [ 
      ps.openai
      ps.pikepdf
    ]))
    curl
    jq
  ];
}
