{ pkgs ? import <nixpkgs> {} }:
pkgs.callPackage ./bmv2.nix { }
