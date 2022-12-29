{ pkgs ? import <nixpkgs> {} }:

pkgs.python3.buildEnv.withPackages (ps: with ps; [
  requests
  python-telegram-bot
])
