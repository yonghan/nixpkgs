{ lib
, stdenv
, fetchFromGitHub
, cmake
, gmp
, libpcap
, boost
, libevent
, libtool
, flex
, bison
, openssl
, thrift
, nanomsg
, autoreconfHook
}:

stdenv.mkDerivation rec {
  pname = "p4-bmv2";
  version = "1.15.0";

  src = fetchFromGitHub {
    owner = "p4lang";
    repo = "behavioral-model";
    rev = version;
    sha256 = "sha256-XXOqRYMQjbfyDJWRg1fKf+Q7n7S8OZX2m/JpuwBi+LI=";
  };

  buildInputs = [
    bison
    flex
  ];

  installFlags = [
    "DESTDIR=."
  ];

  nativeBuildInputs = [
    autoreconfHook

    boost
    gmp
    libpcap
    libevent
    thrift
    nanomsg
  ];

  meta = with lib; {
    homepage = "https://github.com/p4lang/behavioral-model";
    description = "Reference P4 software switch (behavioral model version 2)";
    platforms = platforms.linux;
    maintainers = with maintainers; [ raitobezarius ];
    license = licenses.asl20;
  };
}
