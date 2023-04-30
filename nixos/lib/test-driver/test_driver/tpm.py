import subprocess
from tempfile import TemporaryDirectory


class Tpm:
    """
    This is a TPM driver for QEMU tests.
    It gives you access to a TPM socket path on the host
    you can access at `tpm_socket_path`.
    """

    state_dir: TemporaryDirectory
    swtpm_binary_path: str
    tpm_socket_path: str

    def __init__(self, swtpm_binary_path: str, tpm_socket_path: str):
        self.state_dir = TemporaryDirectory()
        self.swtpm_binary_path = swtpm_binary_path
        self.tpm_socket_path = tpm_socket_path
        self.start()

    def start(self) -> None:
        """
        Start swtpm binary and wait for its proper startup.
        In case of failure, this will raise a runtime error.
        """
        self.proc = subprocess.Popen(
            [
                self.swtpm_binary_path,
                "socket",
                "--tpmstate",
                f"dir={self.state_dir.name}",
                "--ctrl",
                f"type=unixio,path={self.tpm_socket_path}",
                "--tpm2",
            ]
        )

        # Check whether starting swtpm failed
        try:
            exit_code = self.proc.wait(timeout=0.2)
            if exit_code is not None and exit_code != 0:
                raise RuntimeError(f"failed to start swtpm, exit code: {exit_code}")
        except subprocess.TimeoutExpired:
            pass

    def check(self) -> None:
        """
        Check whether the swtpm process exited due to an error
        Useful as a @polling_condition.
        """
        exit_code = self.proc.poll()
        if exit_code is not None and exit_code != 0:
            raise RuntimeError("swtpm process died")
