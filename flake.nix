{
  description = "QuickTOC service";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: {
    nixosModules.default = { config, pkgs, lib, ... }: {
      boot.isContainer = true;
      networking.useDHCP = false;
      networking.firewall.enable = false;
      system.stateVersion = "25.05";

      # This is crucial - ensures the system can boot
      systemd.services.systemd-udevd.enable = lib.mkForce false;
      systemd.services.systemd-udev-trigger.enable = lib.mkForce false;

      environment.systemPackages = with pkgs; [
        (python3.withPackages (ps: with ps; [ 
          bottle
          openai
          pikepdf
          pdf2image
          pillow
        ]))
        curl
        jq
      ];

      # Copy all repo contents to /opt/quicktoc
      environment.etc."quicktoc-app" = {
        source = self;
        target = "quicktoc-app";
      };

      systemd.services.quicktoc = {
        enable = true;
        wantedBy = [ "multi-user.target" ];
        serviceConfig = {
          WorkingDirectory = "/etc/quicktoc-app";
          ExecStart = "${pkgs.python3.withPackages (ps: with ps; [ 
            bottle
            openai
            pikepdf
            pdf2image
            pillow
          ])}/bin/python app.py";
          Restart = "always";
        };
      };
    };
  };
}
