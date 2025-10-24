{
  description = "QuickTOC service";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: {
    nixosModules.default = { config, pkgs, ... }: {
      boot.isContainer = true;
      networking.useDHCP = false;
      networking.firewall.enable = false;
      system.stateVersion = "24.05";

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

      environment.etc."quicktoc/app.py".text = ''
        from bottle import route, run
        
        @route('/')
        def hello():
            return "Hello from QuickTOC!"
        
        run(host='0.0.0.0', port=8080)
      '';

      systemd.services.quicktoc = {
        enable = true;
        wantedBy = [ "multi-user.target" ];
        serviceConfig = {
          ExecStart = "${pkgs.python3.withPackages (ps: [ ps.bottle ])}/bin/python /etc/quicktoc/app.py";
          Restart = "always";
        };
      };
    };
  };
}
