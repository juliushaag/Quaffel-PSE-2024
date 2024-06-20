"""
This module is responsible to handle runs and manage the input and output of the API.
"""

# Maybe more methods?

from quafelweb.simulation_data.simulation import SimulationEnv, SimulationGroup
import paramiko


class Simulators:
    def __init__(self, simulation_env: SimulationEnv):
        self._env = simulation_env

    def setup_quafel(self, ssh):
        """
        Setup the quafel on the node.
        """
        # https://www.baeldung.com/linux/sudo-non-interactive-mode
        self._command(ssh, f'echo "{self._password}" | sudo -S apt-get update && sudo apt-get upgrade', True)
        self._command(ssh, f'echo "{self._password}" | sudo -S apt install python3.10', True)
        self._command(ssh, f'echo "{self._password}" | sudo -S apt install pipx', True)
        self._command(ssh,"pipx install poetry")
        self._command(ssh,"pipx ensurepath")
        self._command(ssh,"exec bash")
        self._command(ssh,"cd ~")
        self._command(ssh,"mkdir git")
        self._command(ssh,"cd git/")
        self._command(ssh,"git clone https://github.com/cirKITers/Quafel.git")
        self._command(ssh,"cd Quafel/")
        self._command(ssh,"poetry lock --no-update")
        self._command(ssh,"poetry install --without dev")

        self._close_ssh(ssh)


    def submit_simulation(self, ssh, simulation_group: SimulationGroup):
        # ssh = self._connect_ssh()
        # self.command(ssh,"cd ~/git/Quafel/")

        list_frameworks: str = '["' + '","'.join(quantum_framework) + '"]'

        output, error = self._command(ssh, "cd ~/git/Quafel/ && grep -n 'frameworks' conf/base/parameters/data_generation.yml | cut -d ':' -f1")
        line: int = output.split("\n")[0]
        self._command(ssh, f"cd ~/git/Quafel/ && sed -i '{line}s/.*/  frameworks: {list_frameworks}/' conf/base/parameters/data_generation.yml")

        prepare_command: str = (
            f"cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline prepare --params=data_generation.min_qubits={min_qubits},data_generation.max_qubits={max_qubits},data_generation.qubits_increment={qubits_increment},data_generation.qubits_type={qubits_type},"
            f"data_generation.min_depth={min_depth},data_generation.max_depth={max_depth},data_generation.depth_increment={depth_increment},data_generation.depth_type={depth_type},"
            f"data_generation.min_shots={min_shots},data_generation.max_shots={max_shots},data_generation.shots_increment={shots_increment},data_generation.shots_type={shots_type},"
            f"data_science.evaluations={evaluations}"
        )

        self._command(ssh, prepare_command)
        self._command(ssh, "cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline measure --runner quafel.runner.MyParallelRunner")
        self._command(ssh, "cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline combine")
        self._command(ssh, "cd ~/git/Quafel/ && /home/ubuntu/.local/bin/poetry run kedro run --pipeline visualize")

        self._close_ssh(ssh)

    def submit_simulation_point(self, qubits: int, depth: int, shots: int, quantum_framework: list[str], evaluations: int):
        self.submit_simulation(qubits, qubits, 1, "linear", depth, depth, 1, "exp2", shots, shots+1, 1, "exp2", quantum_framework, evaluations)

    def check_status(self):
        ssh = self._connect_ssh()
        #unkonwn squeue stuff here
        self._close_ssh(ssh)

    def get_results(self):
        ssh = self._connect_ssh()
        scp = SCPClient(ssh.get_transport())

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"results/{now}/"
        os.makedirs(path, exist_ok=True)
        scp.get("~/git/Quafel/data/", path, recursive=True, preserve_times=True)
        scp.close()
        self._close_ssh(ssh)

    def connect_ssh(self) -> paramiko.SSHClient:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        # Automatically add the server's SSH key to known hosts
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the server
            ssh.connect(
                hostname=self._host,
                port=self._port,
                username=self._username,
                #password=self._password,
                key_filename="./myKey"
            )
            print(f"Connected to {self._host}")
            return ssh

        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except paramiko.SSHException as sshException:
            print(f"Unable to establish SSH connection: {sshException}")
        except Exception as e:
            print(f"Exception in connecting to SSH server: {e}")

    def close_ssh(self, ssh: paramiko.SSHClient):
        ssh.close()

    def _command(self, ssh: paramiko.SSHClient, command:str, show_prompts:bool = False):
        # Execute the command
        print(f">> {command}")
        stdin, stdout, stderr = ssh.exec_command(command)

        # Read the command's output
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        # if output:
        print("<<\n", output)
        if error:
            print("Error<<\n", error)
            if not show_prompts:
                raise Exception(f"Error in command: {command}")

        return output, error