{
  description = "QuickTOC service";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: {
    nixosModules.default = { pkgs, config, ... }: {
      environment.systemPackages = with pkgs; [
        (python3.withPackages (ps: [ 
          ps.openai
          ps.pikepdf
          ps.pdf2image
          ps.outlines
          ps.pillow
          ps.bottle
        ]))
        curl
        jq
      ];
      
      systemd.services.quicktoc = {
        enable = true;
        wantedBy = [ "multi-user.target" ];
        serviceConfig = {
          ExecStart = "${pkgs.python3.withPackages (ps: [ ps.bottle ])}/bin/python app.py";
          WorkingDirectory = "/app";
          Restart = "always";
        };
      };
      
      system.activationScripts.copyApp = ''
        mkdir -p /app
        cp -r ${self}/* /app/
      '';
    };

    # Test container configuration
    nixosConfigurations.container = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      modules = [ self.nixosModules.default ];
    };
  };
}
